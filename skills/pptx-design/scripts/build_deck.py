#!/usr/bin/env python3
"""Build an editable HTML deck from a template and a slide-plan JSON file."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from pathlib import Path


SECTION_RE = re.compile(r'(<section class="slide"[^>]*data-node="([^"]+)"[^>]*>.*?</section>)', re.S)
URL_RE = re.compile(r"^https?://", re.I)


def html_lines(value: str) -> str:
    return html.escape(value).replace("\n", "<br>")


def replace_first(pattern: str, repl: str, source: str) -> str:
    return re.sub(pattern, repl, source, count=1, flags=re.S)


def replace_wrapped_first(pattern: str, source: str, value: str) -> str:
    return re.sub(pattern, lambda m: f"{m.group(1)}{value}{m.group(2)}", source, count=1, flags=re.S)


def replace_all_tag_text(tag: str, source: str, values: list[str]) -> str:
    values_iter = iter(values)

    def repl(match: re.Match) -> str:
        try:
            value = next(values_iter)
        except StopIteration:
            return match.group(0)
        return f"{match.group(1)}{html_lines(value)}{match.group(3)}"

    return re.sub(fr"(<{tag}[^>]*>)(.*?)(</{tag}>)", repl, source, flags=re.S)


def load_asset_catalog(path: Path | None) -> dict:
    if not path:
        return {"aliases": {}, "by_path": {}}
    catalog = json.loads(path.read_text(encoding="utf-8"))
    return {
        "aliases": catalog.get("aliases", {}),
        "by_path": {asset.get("path"): asset for asset in catalog.get("assets", [])},
    }


def resolve_asset_ref(value: str, asset_catalog: dict) -> str:
    if not value:
        return value
    if URL_RE.match(value):
        return value
    aliases = asset_catalog.get("aliases", {})
    if value in aliases:
        return aliases[value]
    asset = asset_catalog.get("by_path", {}).get(value)
    if asset:
        return asset.get("url", value)
    return value


def css_url(value: str) -> str:
    return f"url('{html.escape(value, quote=True)}')"


def add_inline_style_property(tag_start: str, prop: str, value: str) -> str:
    if " style=" in tag_start:
        return re.sub(r'style="([^"]*)"', lambda m: f'style="{m.group(1).rstrip(";")};{prop}:{value}"', tag_start, count=1)
    return tag_start[:-1] + f' style="{prop}:{value}">'


def replace_list_items(source: str, values: list[str]) -> str:
    items = "".join(f"<li>{html_lines(v)}</li>" for v in values)
    return replace_first(r"<ul>.*?</ul>", f"<ul>{items}</ul>", source)


def replace_list_groups(source: str, groups: list[list[str]]) -> str:
    groups_iter = iter(groups)

    def repl(match: re.Match) -> str:
        try:
            values = next(groups_iter)
        except StopIteration:
            return match.group(0)
        items = "".join(f"<li>{html_lines(v)}</li>" for v in values)
        return f"<ul>{items}</ul>"

    return re.sub(r"<ul>.*?</ul>", repl, source, flags=re.S)


def replace_why_bodies(source: str, values: list[str]) -> str:
    values_iter = iter(values)

    def repl(match: re.Match) -> str:
        try:
            value = next(values_iter)
        except StopIteration:
            return match.group(0)
        return f"{match.group(1)}{html_lines(value)}{match.group(3)}"

    return re.sub(r'(<div class="why"[^>]*>.*?<p>)(.*?)(</p>)', repl, source, flags=re.S)


def replace_scoped_text(source: str, scope_class: str, tag: str, values: list[str]) -> str:
    values_iter = iter(values)

    def repl(match: re.Match) -> str:
        try:
            value = next(values_iter)
        except StopIteration:
            return match.group(0)
        return f"{match.group(1)}{html_lines(value)}{match.group(3)}"

    return re.sub(
        fr'(<[^>]+class="[^"]*{re.escape(scope_class)}[^"]*"[^>]*>.*?<{tag}[^>]*>)(.*?)(</{tag}>)',
        repl,
        source,
        flags=re.S,
    )


def replace_scoped_lists(source: str, scope_class: str, groups: list[list[str]]) -> str:
    groups_iter = iter(groups)

    def repl(match: re.Match) -> str:
        try:
            values = next(groups_iter)
        except StopIteration:
            return match.group(0)
        items = "".join(f"<li>{html_lines(v)}</li>" for v in values)
        return f"{match.group(1)}<ul>{items}</ul>"

    return re.sub(
        fr'(<[^>]+class="[^"]*{re.escape(scope_class)}[^"]*"[^>]*>.*?)<ul>.*?</ul>',
        repl,
        source,
        flags=re.S,
    )


def replace_agenda_items(source: str, values: list[str]) -> str:
    values_iter = iter(values)

    def repl(match: re.Match) -> str:
        try:
            value = next(values_iter)
        except StopIteration:
            return match.group(0)
        return f"{match.group(1)}{html_lines(value)}{match.group(3)}"

    return re.sub(r'(<div><strong>\d+</strong><span>)(.*?)(</span></div>)', repl, source, flags=re.S)


def replace_metric_values(source: str, values: list[str]) -> str:
    values_iter = iter(values)
    return re.sub(
        r'(<div class="metric-card"[^>]*><strong>)(.*?)(</strong>)',
        lambda m: f"{m.group(1)}{html_lines(next(values_iter, text_from_html(m.group(2))))}{m.group(3)}",
        source,
        flags=re.S,
    )


def replace_image_sources(section: str, selector_class: str, values: list[str], asset_catalog: dict) -> str:
    values_iter = iter(values)

    def repl(match: re.Match) -> str:
        try:
            value = resolve_asset_ref(next(values_iter), asset_catalog)
        except StopIteration:
            return match.group(0)
        return f'{match.group(1)}{html.escape(value)}{match.group(2)}'

    return re.sub(fr'(<img[^>]+class="[^"]*{re.escape(selector_class)}[^"]*"[^>]+src=")[^"]+(")', repl, section)


def apply_icon_urls(section: str, icon_urls: dict[str, str], asset_catalog: dict) -> str:
    for icon_class, icon_ref in icon_urls.items():
        url = resolve_asset_ref(icon_ref, asset_catalog)
        section = re.sub(
            fr'(<(?:div|span)\b[^>]*class="[^"]*\bicon\b[^"]*\b{re.escape(icon_class)}\b[^"]*"[^>]*>)',
            lambda m, u=url: add_inline_style_property(m.group(1), "background-image", css_url(u)),
            section,
            flags=re.S,
        )
    return section


def apply_slots(section: str, slots: dict, asset_catalog: dict) -> str:
    if "headline" in slots:
        if re.search(r"<h1[^>]*>.*?</h1>", section, re.S):
            section = replace_wrapped_first(r"(<h1[^>]*>).*?(</h1>)", section, html_lines(slots["headline"]))
        else:
            section = replace_wrapped_first(r'(<p class="abs bold[^"]*"[^>]*>).*?(</p>)', section, html_lines(slots["headline"]))

    if "kicker" in slots:
        section = replace_wrapped_first(r'(<p class="small-kicker[^"]*"[^>]*>).*?(</p>)', section, html_lines(slots["kicker"]))

    if "body" in slots:
        section = replace_wrapped_first(r'(<p class="abs(?![^"]*bold)[^"]*"[^>]*>).*?(</p>)', section, html_lines(slots["body"]))

    if "bullets" in slots:
        section = replace_list_items(section, slots["bullets"])

    if "card_bullets" in slots:
        section = replace_list_groups(section, slots["card_bullets"])

    if "card_titles" in slots:
        section = replace_all_tag_text("h3", section, slots["card_titles"])
        section = re.sub(
            r"(<div class=\"diff-card[^\"]*\"[^>]*>.*?<strong>).*?(</strong>)",
            lambda m, vals=iter(slots["card_titles"]): f"{m.group(1)}{html_lines(next(vals, text_from_html(m.group(0))))}{m.group(2)}",
            section,
            flags=re.S,
        )

    if "card_bodies" in slots:
        section = replace_all_tag_text("p", section, slots["card_bodies"])

    if "why_bodies" in slots:
        section = replace_why_bodies(section, slots["why_bodies"])

    if "agenda_items" in slots:
        section = replace_agenda_items(section, slots["agenda_items"])

    if "summary_titles" in slots:
        section = replace_scoped_text(section, "summary-card", "h3", slots["summary_titles"])

    if "summary_bodies" in slots:
        section = replace_scoped_text(section, "summary-card", "p", slots["summary_bodies"])

    if "decision_text" in slots:
        section = replace_wrapped_first(r"(<div class=\"summary-band\"[^>]*>.*?<span>).*?(</span>)", section, html_lines(slots["decision_text"]))

    if "metric_values" in slots:
        section = replace_metric_values(section, slots["metric_values"])

    if "metric_labels" in slots:
        section = replace_scoped_text(section, "metric-card", "span", slots["metric_labels"])

    if "column_titles" in slots:
        section = replace_scoped_text(section, "detail-column", "h3", slots["column_titles"])

    if "column_bullets" in slots:
        section = replace_scoped_lists(section, "detail-column", slots["column_bullets"])

    if "case_result" in slots:
        section = replace_wrapped_first(r"(<div class=\"case-result\"[^>]*>.*?<span>).*?(</span>)", section, html_lines(slots["case_result"]))

    if "credential_titles" in slots:
        section = replace_scoped_text(section, "credential-card", "h3", slots["credential_titles"])

    if "credential_bodies" in slots:
        section = replace_scoped_text(section, "credential-card", "p", slots["credential_bodies"])

    if "image_src" in slots:
        image_src = resolve_asset_ref(slots["image_src"], asset_catalog)
        section = replace_wrapped_first(r'(<img class="photo"[^>]+src=")[^"]+(")', section, html.escape(image_src, quote=True))

    if "images" in slots:
        section = replace_image_sources(section, "photo", slots["images"], asset_catalog)

    if "logo_src" in slots:
        logo_src = resolve_asset_ref(slots["logo_src"], asset_catalog)
        section = re.sub(
            r'(<img[^>]+class="[^"]*logo-img[^"]*"[^>]+src=")[^"]+(")',
            lambda m: f'{m.group(1)}{html.escape(logo_src, quote=True)}{m.group(2)}',
            section,
        )

    if "asset_overrides" in slots:
        for old, new in slots["asset_overrides"].items():
            section = section.replace(old, resolve_asset_ref(new, asset_catalog))

    if "icon_urls" in slots:
        section = apply_icon_urls(section, slots["icon_urls"], asset_catalog)

    return section


def text_from_html(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", value)).strip()


def set_page_number(section: str, number: int) -> str:
    return re.sub(r'(<span class="page-number(?: light)?">)\d+(</span>)', rf"\g<1>{number}\2", section)


def replace_known_assets(html_text: str, asset_catalog: dict) -> str:
    replacements = {
        "assets/brand/logos/wm-blue.svg": "logo.primary.svg",
        "assets/brand/logos/wm-white.svg": "logo.reversed-white.svg",
        "assets/brand/handdrawn/whiteboard-grid.svg": "handdrawn.whiteboard-grid.svg",
        "assets/brand/handdrawn/right-angle-arrow.svg": "handdrawn.right-angle-arrow.svg",
        "assets/brand/handdrawn/underscore-highlight.svg": "handdrawn.underscore-highlight.svg",
        "assets/brand/handdrawn/spark-accent.svg": "handdrawn.spark-accent.svg",
        "assets/brand/icons/magenta/strategy.svg": "icon.magenta.strategy.svg",
        "assets/brand/icons/magenta/success.svg": "icon.magenta.success.svg",
        "assets/brand/icons/magenta/technology.svg": "icon.magenta.technology.svg",
        "assets/brand/icons/magenta/tech-and-experience.svg": "icon.magenta.digital-technology.svg",
        "assets/brand/icons/blue/success.svg": "icon.blue.success.svg",
    }
    for local_path, alias in replacements.items():
        resolved = resolve_asset_ref(alias, asset_catalog)
        if resolved != alias:
            html_text = html_text.replace(local_path, resolved)
    return html_text


def build(template: Path, plan: Path, outdir: Path, asset_catalog_path: Path | None = None, linked_assets: bool = False) -> Path:
    plan_data = json.loads(plan.read_text(encoding="utf-8"))
    asset_catalog = load_asset_catalog(asset_catalog_path)
    template_root = template.parent
    html_text = template.read_text(encoding="utf-8")
    if linked_assets:
        html_text = replace_known_assets(html_text, asset_catalog)
    sections = {node: block for block, node in SECTION_RE.findall(html_text)}
    ordered = []
    for index, slide in enumerate(plan_data["slides"], start=1):
        node = slide.get("node") or slide.get("template_node")
        if node not in sections:
            raise ValueError(f"Unknown template node: {node}")
        section = apply_slots(sections[node], slide.get("slots", {}), asset_catalog)
        ordered.append(set_page_number(section, index))

    rebuilt = re.sub(r"(<main\b[^>]*>).*?(</main>)", "\\1\n" + "\n\n".join(ordered) + "\n\\2", html_text, flags=re.S)
    title = html.escape(plan_data.get("title", "West Monroe HTML Slide Deck"))
    rebuilt = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", rebuilt, count=1, flags=re.S)

    outdir.mkdir(parents=True, exist_ok=True)
    output = outdir / "index.html"
    output.write_text(rebuilt, encoding="utf-8")
    if not linked_assets and (template_root / "assets").exists():
        shutil.copytree(template_root / "assets", outdir / "assets", dirs_exist_ok=True)
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--asset-catalog", type=Path, help="Hosted asset catalog generated from wm-brand-assets inventory.")
    parser.add_argument("--linked-assets", action="store_true", help="Reference hosted asset URLs instead of copying local template assets.")
    args = parser.parse_args()
    print(build(args.template, args.plan, args.outdir, args.asset_catalog, args.linked_assets))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
