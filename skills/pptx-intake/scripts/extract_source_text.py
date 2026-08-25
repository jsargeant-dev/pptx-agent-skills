#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


XML_NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}


def clean_chunks(chunks: list[str]) -> str:
    lines = []
    for chunk in chunks:
        text = " ".join(part.strip() for part in chunk.splitlines() if part.strip())
        if text:
            lines.append(text)
    return "\n".join(lines).strip() + "\n"


def extract_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        chunks = [(page.extract_text() or "") for page in reader.pages]
        return clean_chunks(chunks)
    except ModuleNotFoundError:
        try:
            import fitz
        except ModuleNotFoundError:
            from PyPDF2 import PdfReader  # type: ignore

            reader = PdfReader(str(path))
            chunks = [(page.extract_text() or "") for page in reader.pages]
            return clean_chunks(chunks)

        doc = fitz.open(path)
        chunks = [page.get_text("text") for page in doc]
        return clean_chunks(chunks)


def extract_docx(path: Path) -> str:
    chunks: list[str] = []
    with zipfile.ZipFile(path) as zf:
        with zf.open("word/document.xml") as fh:
            root = ET.parse(fh).getroot()
    for para in root.findall(".//w:p", XML_NS):
        texts = [node.text or "" for node in para.findall(".//w:t", XML_NS)]
        joined = "".join(texts).strip()
        if joined:
            chunks.append(joined)
    return clean_chunks(chunks)


def extract_pptx(path: Path) -> str:
    chunks: list[str] = []
    with zipfile.ZipFile(path) as zf:
        slide_names = sorted(
            name
            for name in zf.namelist()
            if name.startswith("ppt/slides/slide") and name.endswith(".xml")
        )
        for slide_name in slide_names:
            with zf.open(slide_name) as fh:
                root = ET.parse(fh).getroot()
            texts = [node.text or "" for node in root.findall(".//a:t", XML_NS)]
            joined = " ".join(text.strip() for text in texts if text and text.strip())
            if joined:
                chunks.append(joined)
    return clean_chunks(chunks)


def extract_xlsx(path: Path) -> str:
    chunks: list[str] = []
    shared_strings: list[str] = []
    with zipfile.ZipFile(path) as zf:
        if "xl/sharedStrings.xml" in zf.namelist():
            with zf.open("xl/sharedStrings.xml") as fh:
                root = ET.parse(fh).getroot()
            for si in root.findall(".//main:si", XML_NS):
                text = "".join(node.text or "" for node in si.findall(".//main:t", XML_NS))
                shared_strings.append(text)

        sheet_names = sorted(
            name
            for name in zf.namelist()
            if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")
        )

        for sheet_name in sheet_names:
            with zf.open(sheet_name) as fh:
                root = ET.parse(fh).getroot()
            rows: list[str] = []
            for row in root.findall(".//main:row", XML_NS):
                values: list[str] = []
                for cell in row.findall("main:c", XML_NS):
                    cell_type = cell.attrib.get("t")
                    value_node = cell.find("main:v", XML_NS)
                    if value_node is None or value_node.text is None:
                        continue
                    value = value_node.text
                    if cell_type == "s":
                        try:
                            value = shared_strings[int(value)]
                        except (ValueError, IndexError):
                            pass
                    values.append(value.strip())
                row_text = " | ".join(v for v in values if v)
                if row_text:
                    rows.append(row_text)
            if rows:
                chunks.append(f"[{Path(sheet_name).stem}]")
                chunks.extend(rows)
    return clean_chunks(chunks)


def extract_csv_text(path: Path) -> str:
    rows: list[str] = []
    with path.open(newline="", encoding="utf-8", errors="replace") as fh:
        reader = csv.reader(fh)
        for row in reader:
            cleaned = [cell.strip() for cell in row if cell.strip()]
            if cleaned:
                rows.append(" | ".join(cleaned))
    return clean_chunks(rows)


def extract_plain_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return extract_plain_text(path)
    if suffix == ".csv":
        return extract_csv_text(path)
    if suffix == ".pdf":
        return extract_pdf(path)
    if suffix == ".docx":
        return extract_docx(path)
    if suffix == ".pptx":
        return extract_pptx(path)
    if suffix in {".xlsx", ".xlsm"}:
        return extract_xlsx(path)
    raise ValueError(f"Unsupported file type: {path.suffix}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract PPTX Agent intake source files into plain text."
    )
    parser.add_argument("files", nargs="+", help="Files to extract")
    parser.add_argument(
        "--output-dir",
        default="extracted",
        help="Directory for extracted txt files (default: extracted)",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    had_error = False
    for raw_file in args.files:
        path = Path(raw_file).expanduser().resolve()
        try:
            text = extract_text(path)
            out_path = output_dir / f"{path.stem}.txt"
            out_path.write_text(text, encoding="utf-8")
            print(out_path)
        except Exception as exc:  # noqa: BLE001
            had_error = True
            print(f"ERROR {path}: {exc}", file=sys.stderr)

    return 1 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
