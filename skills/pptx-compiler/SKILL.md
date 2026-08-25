---
name: pptx-compiler
description: Compile an approved 16:9 HTML slide deck into an editable object-level PPTX. Use after pptx-design and user HTML approval to extract the HTML DOM, optionally map semantic regions toward JSX-style presentation objects, rebuild text, shapes, and images as editable PowerPoint objects, and validate that slides were not flattened to screenshots.
---

# PPTX Compiler

Use this skill after the HTML deck has been visually reviewed and approved. The HTML is the source of truth.

## Output Contract

- Input is a 16:9 HTML deck, usually one `section.slide` per slide.
- Extract or map HTML into a scene graph of separate objects:
  - text boxes
  - shapes
  - individual images
  - CSS background images when they resolve to URLs
- Build an editable PowerPoint deck with `@oai/artifact-tool`.
- Do not embed each slide as a full-slide PNG unless the user explicitly asks for image-only fidelity.
- Keep the HTML deck, scene JSON, generated source, QA renders, and final PPTX as reproducible artifacts.

## JSX Positioning

This compiler stage is the home for the `HTML -> JSX -> PPTX` concept. Use semantic presentation JSX mapping when the HTML structure is clean enough to map to rows, columns, grids, paragraphs, images, tables, or charts.

Use the bundled object extraction scripts as the reliable baseline for exact-position conversion. Do not force every visual element into JSX semantics when exact-position objects better preserve the reviewed HTML.

## Runtime Setup

This skill relies on the bundled presentation artifact tool. Prefer discovering the current runtime rather than using version-pinned local paths:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SETUP_ARTIFACT_TOOL="$(find "$CODEX_HOME/plugins/cache/openai-primary-runtime/presentations" \
  -path "*/skills/presentations/container_tools/setup_artifact_tool_workspace.mjs" \
  | sort -V \
  | tail -1)"

node "$SETUP_ARTIFACT_TOOL" --workspace "$WORKSPACE/tmp"
```

Run Node commands from `"$WORKSPACE/tmp"` so `@oai/artifact-tool` resolves.

## Workflow

1. Confirm the HTML is approved.
2. Render the HTML and fix visible HTML issues before conversion.
3. Extract the HTML scene graph:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILL_DIR="$CODEX_HOME/skills/pptx-compiler"

node "$SKILL_DIR/scripts/extract-html-objects.mjs" \
  --html "$HTML_DECK" \
  --out "$WORKSPACE/tmp/html-object-scene.json"
```

4. Audit the scene JSON against the browser render.
5. Build the editable object-level PPTX:

```bash
cd "$WORKSPACE/tmp"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILL_DIR="$CODEX_HOME/skills/pptx-compiler"

node "$SKILL_DIR/scripts/create-object-html-pptx.mjs" \
  --scene "$WORKSPACE/tmp/html-object-scene.json" \
  --out "$WORKSPACE/output/deck.pptx" \
  --qa-dir "$WORKSPACE/tmp/qa-objects" \
  --asset-base "$(dirname "$HTML_DECK")"
```

6. Validate structure and visual output.

## Validation

Run:

- `unzip -t "$WORKSPACE/output/deck.pptx"`
- inspect the generated `.inspect.ndjson`
- confirm slide count
- confirm editable textbox count is nonzero where text exists
- confirm shape and individual image counts are plausible
- confirm unintended full-slide image count is `0`
- review QA PNGs/contact sheet when available

## Handoff

Report:

- PPTX path
- HTML source path
- scene JSON path
- slide count
- editable textbox count
- shape count
- individual image count
- full-slide image count
- visual QA status
- any known fidelity differences

