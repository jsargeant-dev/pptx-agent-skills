---
name: pptx-design-reference
description: Analyze user-provided PPTX or HTML slide examples as design references for the PPTX Agent. Use when the user supplies branded slides, example decks, HTML slides, or specific slides to emulate, reuse conceptually, or replicate in new PPTX Agent outputs while keeping pptx-design templates as the primary design rules.
---

# PPTX Design Reference

Use this skill when the user provides existing PPTX or HTML slides as examples for the new deck.

This skill produces a design-reference brief for `pptx-design`. It does not build the final HTML deck, compile PPTX, or override the core `pptx-design` template rules.

## Reference Modes

Classify each supplied reference into one of these modes:

- **Inspiration:** capture visual patterns, pacing, tone, density, and storytelling moves.
- **Reference:** capture specific layout structures or content treatments that should inform new slides.
- **Replicate:** identify slides or sections the user wants recreated closely in the new HTML deck.
- **Content reuse:** extract copy, claims, tables, proof points, or narrative structure from the reference.

If the user's intent is unclear, infer conservatively and state the assumption in the brief.

## Rules

- Treat uploaded PPTX/HTML as design input, not as the primary template system.
- `pptx-design` templates, copy-fit rules, and West Monroe HTML slide system remain the primary design rules.
- Do not embed reference slides as screenshots.
- Do not copy off-brand colors, fonts, logos, or visual systems into final design unless the user explicitly requests a non-West Monroe output.
- When a reference is not West Monroe branded, preserve useful structure or content while translating the final design into West Monroe standards through `pptx-design`.
- When the user asks to reuse specific reference slides, describe what should be replicated as HTML objects: layout, hierarchy, text treatment, diagrams, tables, image placement, and interaction between elements.

## What To Extract

For each relevant reference slide or section, capture:

- source file and slide/page number
- mode: inspiration, reference, replicate, or content reuse
- slide purpose
- visual structure
- hierarchy and reading order
- density and copy length
- notable components: title treatment, cards, diagram, table, timeline, quote, proof point, image, icon, or callout
- reusable content
- brand risks or off-brand elements
- handoff guidance for `pptx-design`

## Handoff Format

Produce a concise Markdown brief:

```markdown
# PPTX Design Reference Brief: <working title>

## Reference Inventory

| ID | Source | Slide/Page | Mode | Notes |
|---|---|---:|---|---|

## Patterns To Use

- <pattern and where it came from>

## Slides Or Elements To Replicate

| Ref ID | What To Replicate | How pptx-design Should Interpret It |
|---|---|---|

## Content To Reuse

- <copy, proof, data, or structure with source reference>

## Off-Brand Or Avoid

- <colors, typography, logos, layouts, claims, or density issues that should not carry forward>

## Handoff To pptx-design

- Recommended design direction:
- Applicable slide moments:
- Reference constraints:
- User confirmations needed:
```

