---
name: pptx-design
description: Turn a PPTX intake package and required reference map into a West Monroe branded 16:9 editable HTML slide deck. Use to plan slide compositions, write slide-ready copy, select inspected brand assets, build HTML, and run reference-influence, asset, density, and fit validation before brand evaluation.
---

# PPTX Design

Create an editable 1280x720 HTML deck for review. Do not create the final PowerPoint file.

## Inputs And Design Authority

Prefer a `pptx-intake` package. If the pipeline has user-supplied or bundled examples, a `pptx-design-reference` brief and `reference-map.json` are required, not optional.

Use this hierarchy:

1. Source content controls meaning and evidence.
2. Selected references control composition, hierarchy, pacing, density, and layout silhouettes.
3. `$west-monroe-brand-for-ui-ux` controls typography, colors, logo rules, surfaces, accessibility, and approved brand behavior.
4. The packaged template supplies the 16:9 shell, brand components, and useful primitives. It must not become the default layout answer for content slides.

## Resources

- `references/composition-patterns.json`: compact first-pass pattern library. Read this before opening many previews.
- `references/design-plan-contract.md`: required slide-plan and asset-selection contract.
- `references/visual-example-index.json` and `references/example-slide-previews/`: evidence behind selected patterns.
- `references/source-deck-corpus.json`: slide-family and density metadata.
- `references/slide-template-index.json`: available template nodes for appropriate utility slides or scaffolds.
- `references/story-mapping-rules.md` and `references/copy-fit-rules.md`: narrative and fit rules.
- `assets/template/index.html`: brand shell and reusable components.
- `references/hosted-asset-catalog.json`: cached hosted asset aliases.

Use `$wm-brand-assets` for approved logos, icons, accents, or photography. The asset skill discovers and verifies files; it does not decide the deck's composition.

## Workflow

### 1. Plan The Story And Composition

- Convert intake into a concise slide sequence by story function, not source order.
- Assign each slide a `layout_mode`: `template-node`, `reference-derived`, or `custom-synthesis`.
- For every content slide, select references and record borrowed composition moves before choosing components.
- Use direct template nodes mainly for covers, agendas, speakers, and section dividers.
- For decks with four or more content slides, use at least three distinct composition recipes unless a documented content-driven exception explains why fewer are better.
- Do not use the same base silhouette on adjacent content slides.

### 2. Write Slide-Ready Copy

- Preserve mandatory claims, evidence, names, metrics, and dates.
- Write concise headlines, labels, callouts, and proof points sized for the selected composition.
- Split dense content instead of shrinking text below the hierarchy.
- Never add filler to occupy a large template surface.

### 3. Run A Deliberate Asset Pass

- Define the semantic role before searching: logo, explanatory icon, evidence image, editorial photo, or optional accent.
- Use `$wm-brand-assets` to return a small candidate set and visually inspect final photo/graphic candidates.
- Record the query, candidate URLs, selected URL, inspection status, placement, crop intent, and rationale in the slide plan.
- `none` is a valid and preferred decision when an asset would be decorative filler.
- Use the positive Grounded Blue horizontal logo on light surfaces and the white/reversed horizontal logo on dark surfaces. Never improvise or recolor a logo.
- Avoid repeating one stock image, using abstract art unrelated to the message, or substituting photography for an information structure.

### 4. Validate The Plan Before HTML

Run:

```bash
python3 scripts/validate_design_plan.py /path/to/slide-plan.json
```

Do not build HTML until the plan passes. Correct missing references, template overuse, adjacent repetition, weak asset decisions, and logo-context errors first.

### 5. Build Editable HTML

- Rebuild selected patterns as native HTML text, shapes, borders, images, and diagrams.
- When all slides intentionally use template nodes, `scripts/build_deck.py` may populate them.
- When any slide is `reference-derived` or `custom-synthesis`, use the template as the document shell and author the slide section directly; a template node may be used only as a starting scaffold and must be materially recomposed.
- Never embed reference-slide JPEGs, full-slide screenshots, rasterized text, or `data:` URIs.
- Keep the DOM compatible with editable HTML-to-PPTX compilation.

### 6. Run Design QA

- Render every slide and a full contact sheet.
- Compare each content slide to its reference-map entry. Confirm the listed composition moves are observable.
- Confirm at least three distinct silhouettes when required, no adjacent repeated base layout, and no template-dominated content sequence.
- Flag large underfilled panels, card-grid defaults, decorative images, incorrect logo contrast, and assets that were not visually inspected.
- Run `scripts/evaluate_fit.py` and fix avoidable overflow or density problems.
- If reference influence is weak, perform one targeted design correction before brand evaluation.

### 7. Brand Evaluation And Review

- Send the initial HTML and asset register to `pptx-brand-eval`.
- Apply at most the one automatic brand-only revision allowed by `pptx-agent`.
- Do not change story, approved copy, or successful reference-derived composition during that brand-only pass unless the issue is itself a brand violation.
- Stop at HTML and ask for user review before `pptx-compiler`.

## Commands

For an all-template utility deck only:

```bash
python3 scripts/build_deck.py \
  --template assets/template/index.html \
  --plan /path/to/slide-plan.json \
  --outdir /path/to/output-folder \
  --asset-catalog references/hosted-asset-catalog.json \
  --linked-assets
```

For every deck:

```bash
python3 scripts/evaluate_fit.py /path/to/output-folder/index.html \
  --out /path/to/output-folder/eval.json
```

## Handoff

Report the HTML path, slide count, reference map, composition recipes used, design-plan validation result, selected asset register, fit result, reference-influence QA, brand-eval result, automatic revision status, and remaining review notes.
