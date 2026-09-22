#!/usr/bin/env python3
"""Validate reference-first PPTX design plans before HTML generation."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


CONTENT_ROLES = {"content", "proof", "process", "closing"}
UTILITY_ROLES = {"cover", "agenda", "speaker", "section-divider"}
LAYOUT_MODES = {"template-node", "reference-derived", "custom-synthesis"}


def validate(plan: dict) -> list[str]:
    errors: list[str] = []
    slides = plan.get("slides")
    if not isinstance(slides, list) or not slides:
        return ["slides must be a non-empty list"]

    exception = str(plan.get("design_exception", "")).strip()
    content_slides = []
    previous_content_recipe = None

    for index, slide in enumerate(slides, start=1):
        label = f"slide {slide.get('slide', index)}"
        role = slide.get("role")
        mode = slide.get("layout_mode")
        if role not in CONTENT_ROLES | UTILITY_ROLES:
            errors.append(f"{label}: invalid or missing role")
        if mode not in LAYOUT_MODES:
            errors.append(f"{label}: invalid or missing layout_mode")
            continue
        if mode == "template-node" and not (slide.get("node") or slide.get("template_node")):
            errors.append(f"{label}: template-node requires node")
        if role in CONTENT_ROLES:
            content_slides.append(slide)
            if mode in {"reference-derived", "custom-synthesis"} and not exception:
                if not slide.get("reference_ids"):
                    errors.append(f"{label}: reference-derived content requires reference_ids")
                if not slide.get("composition_recipe"):
                    errors.append(f"{label}: missing composition_recipe")
                if len(slide.get("borrowed_moves", [])) < 2:
                    errors.append(f"{label}: record at least two borrowed_moves")
            recipe = slide.get("composition_recipe")
            if recipe and recipe == previous_content_recipe and not exception:
                errors.append(f"{label}: adjacent content slides repeat composition_recipe {recipe!r}")
            previous_content_recipe = recipe

        asset = slide.get("asset_decision")
        if not isinstance(asset, dict):
            errors.append(f"{label}: missing asset_decision")
            continue
        decision = asset.get("decision")
        if decision not in {"selected", "none"}:
            errors.append(f"{label}: asset_decision.decision must be selected or none")
        if not asset.get("role"):
            errors.append(f"{label}: asset_decision.role is required")
        if decision == "selected":
            selected = asset.get("selected_url", "")
            candidates = asset.get("candidate_urls", [])
            if selected not in candidates:
                errors.append(f"{label}: selected_url must be listed in candidate_urls")
            if not str(selected).startswith("https://assets.westmonroe-cloud.com/"):
                errors.append(f"{label}: selected asset must use the approved West Monroe host")
            if not asset.get("placement") or not asset.get("rationale"):
                errors.append(f"{label}: selected asset requires placement and rationale")
            role_name = str(asset.get("role", "")).lower()
            if role_name not in {"logo", "known-logo"} and asset.get("visually_inspected") is not True:
                errors.append(f"{label}: selected non-logo asset must be visually inspected")

        surface = str(slide.get("surface", "")).lower()
        logo = str(slide.get("logo_variant", "")).lower()
        if surface == "dark" and logo and not any(token in logo for token in ("white", "reversed", "rev_wht")):
            errors.append(f"{label}: dark surface requires a white/reversed logo")
        if surface == "light" and logo and any(token in logo for token in ("white", "reversed", "rev_wht")):
            errors.append(f"{label}: light surface requires the positive Grounded Blue logo")

    if content_slides and not exception:
        template_count = sum(s.get("layout_mode") == "template-node" for s in content_slides)
        maximum = math.floor(len(content_slides) * 0.4)
        if template_count > maximum:
            errors.append(
                f"deck: {template_count} of {len(content_slides)} content slides use template-node; maximum is {maximum}"
            )
        recipes = {s.get("composition_recipe") for s in content_slides if s.get("composition_recipe")}
        required = min(3, len(content_slides)) if len(content_slides) >= 4 else min(2, len(content_slides))
        if len(recipes) < required:
            errors.append(f"deck: requires at least {required} distinct composition recipes; found {len(recipes)}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    errors = validate(plan)
    result = {"status": "pass" if not errors else "fail", "errors": errors}
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
