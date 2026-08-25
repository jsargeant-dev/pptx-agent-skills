---
name: pptx-design
description: Turn a PPTX intake package into a West Monroe branded 16:9 HTML slide deck for review. Use after pptx-intake, or with clear source content, to plan the deck, write slide-ready copy, select linked brand assets, map content to HTML slide layouts, build the editable HTML deck, and run fit checks before PPTX compilation.
---

# PPTX Design

Use this skill for the design stage of the PPTX Agent pipeline. The output is an editable 1280x720 HTML deck, not the final PowerPoint file.

This skill combines the prior mapping, writer, brand pass, asset selection, and HTML builder responsibilities because they all affect the reviewed HTML deck.

## Inputs

Prefer a `pptx-intake` package. If only raw source is provided, first identify the audience, purpose, core story, evidence, constraints, and gaps before building slides.

When the user provides example PPTX or HTML slides as branded references, direct slide examples, or inspiration, use a `pptx-design-reference` brief as an optional input. Treat that brief as guidance for patterns, visual intent, and specific replication asks, not as a replacement for this skill's templates or design rules.

## Required Resources

Use bundled resources in this skill:

- `assets/template/index.html` for the HTML slide system.
- `references/slide-template-index.json` for available slide archetypes and copy limits.
- `references/source-deck-corpus.json` when the user wants the 9 good-example PPTX decks reflected in layout decisions.
- `references/visual-example-usage.md` and `references/visual-example-index.json` when the deck needs stronger design variety or the user provides good-example decks to copy as visual inspiration.
- `references/story-mapping-rules.md` and `references/copy-fit-rules.md` for story and fit decisions.
- `references/hosted-asset-catalog.json` for cached hosted asset aliases.

Use `wm-brand-assets` as an external skill when searching for content-matched West Monroe logos, icons, accents, or photos. Do not bundle `wm-brand-assets` with this skill.

## Workflow

1. Plan the deck.
   - Convert the intake into a concise slide sequence.
   - Choose slide structures by story function, not by source order.
   - Use the source-deck corpus as taxonomy guidance, not as screenshots to embed.
   - Use the visual example previews to vary composition, pacing, and visual hierarchy when the deck would otherwise feel repetitive.
   - If a `pptx-design-reference` brief exists, decide which patterns or replication notes should influence each slide.

2. Write slide-ready copy.
   - Create concise headlines, bullets, cards, callouts, metrics, and labels.
   - Preserve mandatory claims, evidence, names, metrics, and dates.
   - Split dense content across slides rather than shrinking text until it fits.
   - Size containers to the approved copy. Do not place a short amount of text in a large fixed-height box merely to fill a template slot.
   - Follow `references/copy-fit-rules.md` for both overflow and content-to-container density decisions.

3. Run a brand and asset pass.
   - Keep voice clear, practical, outcome-focused, and West Monroe aligned.
   - Use linked hosted assets. Do not use `data:` URIs.
   - Prefer `wm-brand-assets` for content-matched asset search, then place selected hosted URLs in the slide plan.
   - Translate off-brand references into West Monroe standards rather than copying their colors, fonts, logos, or visual system.

4. Build the HTML deck.
   - Draft a slide plan JSON with selected template nodes and slot values.
   - Rebuild any copied reference pattern as editable HTML/CSS. Do not embed example slide JPEGs or full-slide screenshots.
   - Run `scripts/build_deck.py` with `--linked-assets`.
   - Run `scripts/evaluate_fit.py` on the generated `index.html`.
   - Render every slide and run a visual density review. Flag cards, panels, and boxes whose meaningful content occupies less than roughly half of the interior height without a functional reason.
   - Resolve underfilled surfaces by shrinking or removing the container, choosing a more suitable layout, increasing type within the established hierarchy, or adding only message-strengthening content. Never add filler copy.
   - Preserve each template's relational geometry during density fixes. If resizing breaks an overlap, connector, shared edge, or other intended relationship, select another template or create a compatible content-shaped variant.

5. Prepare for review.
   - Fix avoidable overflow and underfilled-surface errors before handoff.
   - Hand the initial generated HTML to `pptx-brand-eval` before user review.
   - When invoked with brand-eval findings, perform only the one automatic brand revision allowed by `pptx-agent` unless the user explicitly asks for additional revisions.
   - Apply only brand-eval fixes in HTML/CSS: colors, font roles, logo treatment, surface styling, spacing, asset treatment, and table/chart/graph styling.
   - Do not change story, slide order, approved copy, template choice, or page structure during the automatic brand-revision pass unless the issue is itself a brand violation.
   - Do not flatten slides, replace editable text with images, or break the HTML-to-JSX-to-PPTX structure.
   - Give the user the HTML path and ask for review before `pptx-compiler`.

## Slide Plan Contract

Use this JSON shape with `scripts/build_deck.py`:

```json
{
  "title": "Client or Deck Title",
  "slides": [
    {
      "node": "1:2",
      "slots": {
        "headline": "Short rewritten headline",
        "body": "Optional supporting copy",
        "image_src": "https://assets.westmonroe-cloud.com/example/path.svg"
      }
    }
  ]
}
```

Supported slot keys include `headline`, `kicker`, `body`, `bullets`, `card_titles`, `card_bodies`, `image_src`, `images`, `logo_src`, `icon_urls`, `asset_overrides`, `agenda_items`, `summary_titles`, `summary_bodies`, `decision_text`, `metric_values`, `metric_labels`, `column_titles`, `column_bullets`, `case_result`, `credential_titles`, and `credential_bodies`.

## Commands

Run from the skill folder or pass absolute paths:

```bash
python3 scripts/build_deck.py \
  --template assets/template/index.html \
  --plan /path/to/slide-plan.json \
  --outdir /path/to/output-folder \
  --asset-catalog references/hosted-asset-catalog.json \
  --linked-assets

python3 scripts/evaluate_fit.py /path/to/output-folder/index.html \
  --out /path/to/output-folder/eval.json
```

## Validation

Before handing off to `pptx-compiler`, report:

- HTML path
- slide count
- selected asset sources
- reference brief used, if any
- visual example previews used, if any
- brand eval status, if completed
- whether the one automatic brand revision was applied
- fit evaluation result
- visual density review result and any intentional low-density exceptions
- remaining warnings or review notes
