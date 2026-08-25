#!/usr/bin/env python3
"""Build a hosted West Monroe asset catalog for HTML slide generation."""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
from pathlib import Path


TAG_RULES = {
    "ai": ["ai", "artificial", "intelligence", "brain", "automated", "automation"],
    "data": ["data", "analytics", "database", "science", "quality"],
    "cloud": ["cloud", "backup", "storage"],
    "risk": ["risk", "alert", "caution", "security", "firewall", "compliance"],
    "finance": ["bank", "financial", "financing", "currency", "mortgage"],
    "healthcare": ["health", "healthcare", "care", "life sciences"],
    "industry": ["factory", "manufacturing", "industrial", "construction", "energy"],
    "people": ["collaboration", "people", "hands", "stakeholder", "customer", "employee"],
    "strategy": ["strategy", "advisory", "direction", "guidance", "alignment"],
    "success": ["success", "award", "approved", "completion", "achievement", "goals"],
    "technology": ["technology", "digital", "coding", "system", "network"],
    "accent": ["handdrawn", "arrow", "highlight", "spark", "grid", "circle"],
    "logo": ["logo", "wm_h", "compass"],
    "photo": ["getty", "adobestock", "photo", "photos"],
}


def asset_url(host: str, path: str) -> str:
    return host.rstrip("/") + "/" + urllib.parse.quote(path, safe="/")


def tags_for(asset: dict) -> list[str]:
    haystack = re.sub(
        r"[^a-z0-9]+",
        " ",
        " ".join(str(asset.get(k, "")).lower() for k in ("path", "directory", "fileName", "extension")),
    )
    tags = []
    for tag, needles in TAG_RULES.items():
        if any(needle in haystack for needle in needles):
            tags.append(tag)
    return sorted(set(tags))


def usage_note(asset: dict) -> str:
    directory = asset.get("directory", "")
    filename = asset.get("fileName", "")
    stem = Path(filename).stem.lower()
    if directory == "logos":
        if "rev_wht" in stem or "wht" in stem:
            return "Reversed white West Monroe logo for dark, colored, or image backgrounds."
        if "compass" in stem:
            return "West Monroe compass mark for compact brand moments."
        return "Primary positive-color West Monroe logo for light backgrounds."
    if directory.startswith("icons/"):
        color = "magenta" if "magenta" in directory else "grounded blue"
        concept = Path(filename).stem.replace("_", " ").replace("-", " ")
        return f"{color.title()} icon for {concept}."
    if directory.startswith("handdrawn-animations/"):
        return "Hand-drawn accent for highlights, arrows, circles, grids, and visual emphasis."
    if directory == "photos/abstract":
        return "Abstract photography for conceptual backgrounds, section dividers, or atmosphere."
    if directory == "photos/industry":
        return "Industry photography; inspect image before choosing for a specific sector."
    if directory == "photos/provocative":
        return "Bold editorial photography for high-impact or thought-leadership moments."
    return "Approved West Monroe image asset."


def make_aliases(assets: list[dict]) -> dict[str, str]:
    by_path = {asset["path"]: asset["url"] for asset in assets}
    aliases = {
        "logo.primary.svg": by_path.get("logos/wm_h_pos_clr_rgb_august2024.svg"),
        "logo.primary.png": by_path.get("logos/wm_h_pos_clr_rgb_august2024.png"),
        "logo.reversed-white.svg": by_path.get("logos/wm_h_rev_wht_rgb_august2024.svg"),
        "logo.reversed-white.png": by_path.get("logos/wm_h_rev_wht_rgb_august2024.png"),
        "logo.compass.svg": by_path.get("logos/wm_compass_pos_clr_rgb_august2024.svg"),
        "logo.compass.png": by_path.get("logos/wm_compass_pos_clr_rgb_august2024.png"),
        "handdrawn.whiteboard-grid.svg": by_path.get("handdrawn-animations/svg/handdrawn-whiteboard-grid.svg"),
        "handdrawn.right-angle-arrow.svg": by_path.get("handdrawn-animations/svg/handdrawn-right-angle-arrow.svg"),
        "handdrawn.underscore-highlight.svg": by_path.get("handdrawn-animations/svg/handdrawn-underscore-highlight.svg"),
        "handdrawn.circle-outline.svg": by_path.get("handdrawn-animations/svg/handdrawn-circle-outline.svg"),
        "handdrawn.single-arrow.svg": by_path.get("handdrawn-animations/svg/handdrawn-single-arrow.svg"),
        "handdrawn.spark-accent.svg": by_path.get("handdrawn-animations/svg/handdrawn-spark-accent.svg"),
        "icon.magenta.strategy.svg": by_path.get("icons/svgs/magenta/strategy.svg"),
        "icon.magenta.success.svg": by_path.get("icons/svgs/magenta/success.svg"),
        "icon.magenta.technology.svg": by_path.get("icons/svgs/magenta/technology.svg"),
        "icon.magenta.digital-technology.svg": by_path.get("icons/svgs/magenta/digital-technology.svg"),
        "icon.blue.strategy.svg": by_path.get("icons/svgs/grounded-blue/strategy.svg"),
        "icon.blue.success.svg": by_path.get("icons/svgs/grounded-blue/success.svg"),
        "icon.blue.technology.svg": by_path.get("icons/svgs/grounded-blue/technology.svg"),
        "icon.blue.digital-technology.svg": by_path.get("icons/svgs/grounded-blue/digital-technology.svg"),
    }
    return {key: value for key, value in aliases.items() if value}


def build_catalog(inventory_path: Path) -> dict:
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    host = inventory["assetHostDefault"]
    assets = []
    for asset in inventory.get("assets", []):
        enriched = {
            "path": asset.get("path", ""),
            "directory": asset.get("directory", ""),
            "fileName": asset.get("fileName", ""),
            "extension": asset.get("extension", ""),
            "assetType": asset.get("assetType", ""),
            "sizeBytes": asset.get("sizeBytes"),
            "modifiedAt": asset.get("modifiedAt", ""),
            "tags": tags_for(asset),
            "usage": usage_note(asset),
            "url": asset_url(host, asset.get("path", "")),
        }
        assets.append(enriched)
    return {
        "source": str(inventory_path),
        "generatedFrom": inventory.get("generatedAt", ""),
        "assetHost": host,
        "assetCount": len(assets),
        "aliases": make_aliases(assets),
        "assets": assets,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(build_catalog(args.inventory), indent=2), encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
