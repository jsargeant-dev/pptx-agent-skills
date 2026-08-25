#!/usr/bin/env python3
"""Run low-cost structural and copy-fit checks on a generated HTML slide deck."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SECTION_RE = re.compile(r'<section class="slide"[^>]*data-node="([^"]+)"[^>]*>(.*?)</section>', re.S)
PAGE_RE = re.compile(r'<span class="page-number(?: light)?">(\d+)</span>')


def textify(value: str) -> str:
    value = re.sub(r"<br\s*/?>", " ", value)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def evaluate(deck: Path) -> dict:
    html = deck.read_text(encoding="utf-8")
    sections = SECTION_RE.findall(html)
    page_numbers = [int(x) for x in PAGE_RE.findall(html)]
    issues = []

    expected = list(range(1, len(sections) + 1))
    if page_numbers != expected:
        issues.append({"level": "error", "message": f"Page numbers are {page_numbers}, expected {expected}."})
    if "figma.com/api/mcp/asset" in html:
        issues.append({"level": "error", "message": "Deck contains short-lived Figma MCP asset URLs."})
    if re.search(r'(?:src|href)="data:', html) or "url(data:" in html:
        issues.append({"level": "error", "message": "Deck contains embedded data URI assets."})
    if re.search(r'<section class="slide"[^>]*>\s*<img[^>]+class="[^"]*(?:slide|screenshot|render)[^"]*"', html, re.S):
        issues.append({"level": "error", "message": "Slide appears to be embedded as a rendered image instead of editable HTML."})

    for slide_num, (node, body) in enumerate(sections, start=1):
        if "<main" in body or "</main>" in body:
            issues.append({"level": "error", "slide": slide_num, "message": "Slide section contains a nested or malformed main element."})
        headline_match = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S) or re.search(r'<p class="abs bold[^"]*"[^>]*>(.*?)</p>', body, re.S)
        if headline_match and len(textify(headline_match.group(1))) > 170:
            issues.append({"level": "warn", "slide": slide_num, "message": "Headline is likely too long for the template."})
        for bullet in re.findall(r"<li>(.*?)</li>", body, re.S):
            if len(textify(bullet)) > 130:
                issues.append({"level": "warn", "slide": slide_num, "message": "Bullet may wrap too deeply.", "text": textify(bullet)[:90]})
        for src in re.findall(r'<img[^>]+src="([^"]+)"', body):
            if src.startswith(("http://", "https://", "data:")):
                continue
            if not (deck.parent / src).exists():
                issues.append({"level": "error", "slide": slide_num, "message": f"Missing local image asset: {src}"})

    return {
        "deck": str(deck),
        "slide_count": len(sections),
        "page_numbers": page_numbers,
        "passed": not any(issue["level"] == "error" for issue in issues),
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("deck", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = evaluate(args.deck)
    payload = json.dumps(result, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(payload)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
