#!/usr/bin/env python3
"""Extract lightweight structural metadata from reference PPTX decks."""

from __future__ import annotations

import argparse
import json
import re
import statistics
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def slide_number(path: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", path)
    return int(match.group(1)) if match else 10**9


def textify(root: ET.Element) -> str:
    parts = []
    for node in root.findall(".//a:t", NS):
        if node.text:
            parts.append(node.text)
    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def rel_types(zf: ZipFile, slide_path: str) -> list[str]:
    rel_path = slide_path.replace("ppt/slides/", "ppt/slides/_rels/") + ".rels"
    if rel_path not in zf.namelist():
        return []
    root = ET.fromstring(zf.read(rel_path))
    return [rel.attrib.get("Type", "").split("/")[-1] for rel in root]


def shape_summary(root: ET.Element) -> dict:
    sp_count = len(root.findall(".//p:sp", NS))
    pic_count = len(root.findall(".//p:pic", NS))
    graphic_count = len(root.findall(".//a:graphic", NS))
    table_count = len(root.findall(".//a:tbl", NS))
    return {
        "shapes": sp_count,
        "pictures": pic_count,
        "graphics": graphic_count,
        "tables": table_count,
    }


def infer_family(text: str, summary: dict, rels: list[str], index: int) -> str:
    t = text.lower()
    words = len(text.split())
    if index == 1:
        return "cover"
    if "agenda" in t or re.search(r"\b0?1\b.*\b0?2\b.*\b0?3\b", t):
        return "agenda"
    if "executive summary" in t or "our understanding" in t:
        return "executive-summary"
    if "case stud" in t or "client testimonial" in t or "proof" in t:
        return "proof"
    if "approach" in t or "workflow" in t or "roadmap" in t:
        return "approach-process"
    if summary["tables"] or words > 260:
        return "dense-detail"
    if any(token in t for token in ["at-a-glance", "about west monroe", "credentials", "bios"]):
        return "credentials"
    if summary["pictures"] >= 2:
        return "photo-story"
    if words <= 45 and summary["pictures"] >= 1:
        return "statement-photo"
    return "content"


def inspect_deck(path: Path) -> dict:
    with ZipFile(path) as zf:
        slides = sorted(
            [name for name in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)],
            key=slide_number,
        )
        media = [name for name in zf.namelist() if name.startswith("ppt/media/")]
        slide_items = []
        for i, slide in enumerate(slides, start=1):
            root = ET.fromstring(zf.read(slide))
            text = textify(root)
            summary = shape_summary(root)
            rels = rel_types(zf, slide)
            slide_items.append(
                {
                    "slide": i,
                    "wordCount": len(text.split()),
                    "charCount": len(text),
                    "family": infer_family(text, summary, rels, i),
                    "relationshipTypes": sorted(set(rels)),
                    "shapeSummary": summary,
                    "textPreview": text[:240],
                }
            )
    word_counts = [item["wordCount"] for item in slide_items]
    return {
        "path": str(path),
        "fileName": path.name,
        "slideCount": len(slide_items),
        "mediaFileCount": len(media),
        "wordCount": {
            "min": min(word_counts) if word_counts else 0,
            "avg": round(statistics.mean(word_counts), 1) if word_counts else 0,
            "max": max(word_counts) if word_counts else 0,
        },
        "familyCounts": dict(sorted({k: sum(1 for s in slide_items if s["family"] == k) for k in {s["family"] for s in slide_items}}.items())),
        "slides": slide_items,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    decks = [inspect_deck(path) for path in args.pptx]
    family_counts = {}
    for deck in decks:
        for family, count in deck["familyCounts"].items():
            family_counts[family] = family_counts.get(family, 0) + count
    payload = {
        "sourceDeckCount": len(decks),
        "totalSlides": sum(deck["slideCount"] for deck in decks),
        "familyCounts": dict(sorted(family_counts.items())),
        "decks": decks,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
