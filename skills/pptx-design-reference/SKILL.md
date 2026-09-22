---
name: pptx-design-reference
description: Analyze user-provided or bundled PPTX, PDF, and HTML examples as composition references for the PPTX Agent. Use before slide design to select relevant examples and produce a per-slide reference map that drives hierarchy, pacing, density, and layout silhouettes without copying full-slide images.
---

# PPTX Design Reference

Use this skill before `pptx-design` whenever the user supplies examples, asks for example-informed design, or the PPTX pipeline includes bundled reference decks.

The output is a reference brief plus `reference-map.json`. It does not build the final deck.

## Design Hierarchy

Apply these roles without ambiguity:

- Source content controls the story, claims, and required meaning.
- Reference examples control composition, hierarchy, pacing, density, visual rhythm, and layout silhouettes.
- West Monroe standards control typography, color, logo treatment, accessibility, surfaces, and editability.
- The packaged template is a brand shell and component source. It is not the default composition system when relevant references exist.

Do not let a template archetype override a selected reference pattern. Translate references into new editable HTML/CSS; never embed a full-slide screenshot.

## Efficient Reference Selection

Do not ask a lower-cost model to inspect the full reference corpus indiscriminately.

1. Classify each planned slide by purpose and approximate density.
2. Read `pptx-design/references/composition-patterns.json` and shortlist two or three compatible patterns per slide.
3. Inspect the shortlisted individual previews and only the contact sheets needed to understand deck rhythm.
4. Choose one primary pattern and, when helpful, one secondary influence per slide.
5. Record the observable composition moves to borrow and what must not be copied.

When the user supplies a new reference, add it to the brief even if it is not in the bundled pattern library.

## Reference Modes

- **Inspiration:** borrow pacing, tone, density, or visual tension.
- **Reference:** borrow a specific layout structure or information treatment.
- **Replicate:** recreate the requested structure closely with new editable objects and approved branding.
- **Content reuse:** extract approved copy, claims, tables, evidence, or narrative structure.

## Required Extraction

For each selected source, capture:

- stable reference ID, source file, and slide/page number
- preview path when bundled
- slide purpose and density
- silhouette, hierarchy, and reading order
- specific composition moves to borrow
- copy-to-region mapping
- image role, if any
- off-brand or client-specific elements to exclude

## Required Per-Slide Map

Every output slide must include:

```json
{
  "slide": 4,
  "role": "content",
  "purpose": "Show the operating-model shift",
  "layout_mode": "reference-derived",
  "reference_ids": ["ai-strategy-roadmap:s04"],
  "composition_recipe": "asymmetric-operating-model",
  "borrowed_moves": ["40/60 hierarchy", "numbered progression", "single focal proof block"],
  "content_mapping": ["thesis -> left lead", "three changes -> right progression"],
  "brand_shell": ["West Monroe palette", "IBM Plex headings", "approved logo variant"],
  "avoid": ["equal-card grid", "decorative stock image", "copied client content"]
}
```

Allowed `layout_mode` values are `template-node`, `reference-derived`, and `custom-synthesis`. Use `template-node` mainly for covers, agendas, speakers, and section dividers. Content slides should normally be `reference-derived` or `custom-synthesis`.

## Handoff

Provide:

- a concise Markdown inventory and design direction
- `reference-map.json` using the contract above
- the shortlisted previews actually inspected
- any content-driven exception to pattern diversity
- explicit instructions for `pptx-design` to preserve reference influence while translating brand details

