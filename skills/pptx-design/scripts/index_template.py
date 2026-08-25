#!/usr/bin/env python3
"""Index the editable HTML slide template into a compact JSON reference."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ARCHETYPES = {
    "1:2": "hero",
    "1:3": "section-divider",
    "1:5": "problem-statement",
    "1:9": "transformation-positioning",
    "1:11": "approach-card-grid",
    "61:2": "statement-photo",
    "61:192": "bullet-list",
    "61:423": "keyword-card-grid",
    "61:436": "timeline",
    "62:524": "differentiator-grid",
    "ref:agenda": "agenda",
    "ref:executive-summary": "executive-summary",
    "ref:metric-proof": "metric-proof",
    "ref:two-column-detail": "two-column-detail",
    "ref:case-study": "case-study",
    "ref:credentials": "credentials",
}

USAGE = {
    "hero": "Open the deck with a bold thesis and one strong visual.",
    "section-divider": "Create a visual pause between major story chapters.",
    "problem-statement": "Frame the primary challenge and supporting tensions.",
    "transformation-positioning": "Reframe the challenge as a business transformation.",
    "approach-card-grid": "Present a four-part approach or operating model.",
    "statement-photo": "Make one memorable point with a supporting image.",
    "bullet-list": "Hold supporting details, proof points, or recommendations.",
    "keyword-card-grid": "Compare three themes, pillars, or capabilities.",
    "timeline": "Show four phases, steps, or waves in sequence.",
    "differentiator-grid": "Show two rows of three differentiators, findings, or proof points.",
    "agenda": "Set up a meeting, proposal, or walking-deck flow with numbered sections.",
    "executive-summary": "Summarize situation, implication, recommendation, and decision needed.",
    "metric-proof": "Make a small set of metrics or proof points visually dominant.",
    "two-column-detail": "Compare current and future state, options, or two workstreams.",
    "case-study": "Show a client proof story with image, bullets, and result.",
    "credentials": "Present West Monroe experience, capabilities, proof, or team strengths.",
}

FIT = {
    "hero": {"headline_chars": 80, "body_chars": 180},
    "section-divider": {"headline_chars": 70},
    "problem-statement": {"headline_chars": 120, "callouts": 4},
    "transformation-positioning": {"headline_chars": 165, "callouts": 4},
    "approach-card-grid": {"headline_chars": 150, "cards": 4, "card_title_chars": 34, "card_body_chars": 190},
    "statement-photo": {"headline_chars": 135, "body_chars": 220},
    "bullet-list": {"headline_chars": 120, "bullets": 6, "bullet_chars": 120},
    "keyword-card-grid": {"headline_chars": 150, "cards": 3, "card_title_chars": 34, "bullet_chars": 80},
    "timeline": {"headline_chars": 150, "cards": 4, "card_title_chars": 24, "bullet_chars": 115},
    "differentiator-grid": {"headline_chars": 150, "cards": 6, "card_title_chars": 42},
    "agenda": {"headline_chars": 70, "agenda_items": 4, "agenda_item_chars": 42},
    "executive-summary": {"headline_chars": 115, "cards": 3, "card_title_chars": 24, "card_body_chars": 95, "decision_chars": 115},
    "metric-proof": {"headline_chars": 110, "metrics": 4, "metric_value_chars": 8, "metric_label_chars": 70},
    "two-column-detail": {"headline_chars": 120, "columns": 2, "column_title_chars": 28, "bullet_chars": 55},
    "case-study": {"headline_chars": 105, "bullets": 4, "bullet_chars": 55, "result_chars": 115},
    "credentials": {"headline_chars": 120, "cards": 4, "card_title_chars": 24, "card_body_chars": 90},
}


def textify(value: str) -> str:
    value = re.sub(r"<br\s*/?>", " / ", value)
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", value).strip()


def first_text(body: str, pattern: str) -> str | None:
    match = re.search(pattern, body, re.S)
    return textify(match.group(1)) if match else None


def classify_slots(body: str) -> dict:
    slots = {}
    headline = first_text(body, r"<h1[^>]*>(.*?)</h1>")
    if not headline:
        headline = first_text(body, r'<p class="abs bold"[^>]*>(.*?)</p>')
    if headline:
        slots["headline"] = headline

    bullets = [textify(x) for x in re.findall(r"<li>(.*?)</li>", body, re.S)]
    if bullets:
        slots["bullets"] = bullets

    card_titles = [textify(x) for x in re.findall(r"<h3[^>]*>(.*?)</h3>", body, re.S)]
    card_titles += [textify(x) for x in re.findall(r'<div class="diff-card[^"]*"[^>]*>.*?<strong>(.*?)</strong>', body, re.S)]
    if card_titles:
        slots["card_titles"] = card_titles

    images = re.findall(r'<img[^>]+src="([^"]+)"', body)
    slots["images"] = [src for src in images if "logos/" not in src]
    slots["icons"] = sorted(set(re.findall(r'class="[^"]*\b([a-z-]*(?:strategy|success|tech|experience|magenta|blue-success)[a-z-]*)\b[^"]*"', body)))
    return slots


def index_template(template: Path) -> dict:
    html = template.read_text(encoding="utf-8")
    slides = []
    for idx, match in enumerate(re.finditer(r'<section class="slide"([^>]*)>(.*?)</section>', html, re.S), start=1):
        attrs, body = match.groups()
        node = (re.search(r'data-node="([^"]+)"', attrs) or [None, None])[1]
        archetype = ARCHETYPES.get(node, "custom")
        classes = sorted(set(re.findall(r'class="([^"]+)"', body)))
        slides.append(
            {
                "slide": idx,
                "node": node,
                "archetype": archetype,
                "best_for": USAGE.get(archetype, "Use only when a known indexed slide does not fit."),
                "fit": FIT.get(archetype, {}),
                "slots": classify_slots(body),
                "class_signals": classes[:20],
                "duplicate_allowed": archetype not in {"hero"},
            }
        )
    return {
        "template": str(template),
        "canvas": {"width": 1280, "height": 720, "ratio": "16:9"},
        "slides": slides,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("template", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(index_template(args.template), indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
