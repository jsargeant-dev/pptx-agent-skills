#!/usr/bin/env python3
"""Create a lightweight searchable asset index from approved West Monroe assets."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TAG_RULES = {
    "ai": ["ai", "artificial", "intelligence", "brain", "automated", "automation"],
    "data": ["data", "analytics", "database", "science", "quality"],
    "cloud": ["cloud", "backup", "storage"],
    "risk": ["risk", "alert", "caution", "security", "firewall", "compliance"],
    "finance": ["bank", "financial", "financing", "currency", "mortgage"],
    "healthcare": ["health", "healthcare", "care"],
    "industry": ["factory", "manufacturing", "industrial", "construction", "energy"],
    "people": ["collaboration", "people", "hands", "stakeholder", "customer", "employee"],
    "strategy": ["strategy", "advisory", "direction", "guidance", "alignment"],
    "success": ["success", "award", "approved", "completion", "achievement", "goals"],
    "technology": ["technology", "digital", "coding", "system", "network"],
    "accent": ["handdrawn", "arrow", "highlight", "spark", "grid", "circle"],
    "logo": ["logo", "wm_h"],
    "photo": ["getty", "adobestock", "photo"],
}

EXT_TYPES = {
    ".svg": "icon-or-vector",
    ".png": "raster",
    ".jpg": "photo",
    ".jpeg": "photo",
    ".webp": "photo",
}


def tags_for(path: Path) -> list[str]:
    haystack = re.sub(r"[^a-z0-9]+", " ", str(path).lower())
    tags = []
    for tag, needles in TAG_RULES.items():
        if any(needle in haystack for needle in needles):
            tags.append(tag)
    return sorted(set(tags))


def index_assets(root: Path) -> dict:
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == ".DS_Store":
            continue
        ext = path.suffix.lower()
        if ext not in EXT_TYPES:
            continue
        rel = path.relative_to(root)
        parts = [p.lower() for p in rel.parts]
        files.append(
            {
                "path": str(path),
                "relative_path": str(rel),
                "kind": EXT_TYPES[ext],
                "family": parts[0] if parts else "",
                "tags": tags_for(rel),
            }
        )
    return {"asset_root": str(root), "assets": files}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("asset_root", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(index_assets(args.asset_root), indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
