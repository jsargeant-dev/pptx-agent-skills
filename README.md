# PPTX Agent Skills

An HTML-first, West Monroe presentation workflow for Codex. The agent creates and reviews an editable HTML deck before any PowerPoint compilation.

## Included skills

- `pptx-agent` — coordinates the complete workflow and HTML approval gate.
- `pptx-intake` — extracts and rewrites source content into a presentation narrative.
- `pptx-design-reference` — analyzes supplied decks or HTML as design references.
- `pptx-design` — builds and visually validates the editable HTML deck.
- `pptx-brand-eval` — performs the scoped West Monroe brand review.
- `pptx-compiler` — converts approved HTML into an editable object-level PPTX.

`wm-brand-assets` is intentionally not included. The design skill treats it as an optional external asset source and can continue with available hosted URLs when it is unavailable.

## Workflow

```text
pptx-intake
  -> optional pptx-design-reference
  -> pptx-design
  -> pptx-brand-eval
  -> one automatic brand-only revision
  -> user HTML review and explicit approval
  -> optional pptx-compiler
```

The workflow must stop at HTML until the user explicitly approves PPTX compilation. Slides remain semantic HTML, and compiled decks preserve text boxes, shapes, and individual images rather than using full-slide screenshots.

## Installation

Copy all six folders under `skills/` into the Codex skills directory, normally `~/.codex/skills/`. Keep the folder names unchanged because the coordinator references the companion skills by name.

The design and compiler scripts require a local Python and Node.js runtime. HTML rendering and object extraction also require Chrome or Chromium plus Playwright; PPTX compilation requires `@oai/artifact-tool`.

## Repository contents

The `pptx-design` package includes its editable HTML template, scripts, slide archetype indexes, visual-reference previews, and linked-asset catalog. No brand assets are embedded as data URIs.
