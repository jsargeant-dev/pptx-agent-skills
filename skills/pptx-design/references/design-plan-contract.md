# Design Plan Contract

Use this contract before building HTML. The purpose is to make design intent explicit enough that a lower-cost model cannot silently fall back to filling template slots.

## Deck Shape

```json
{
  "title": "Deck title",
  "design_exception": "Optional content-driven reason for fewer patterns or more template use",
  "slides": []
}
```

## Slide Shape

```json
{
  "slide": 4,
  "role": "content",
  "purpose": "Show the operating-model shift",
  "layout_mode": "reference-derived",
  "reference_ids": ["ai-strategy-roadmap:s04"],
  "composition_recipe": "asymmetric-operating-model",
  "borrowed_moves": ["40/60 hierarchy", "numbered progression"],
  "content_mapping": ["thesis -> left lead", "changes -> right progression"],
  "brand_shell": ["West Monroe palette", "IBM Plex headings"],
  "avoid": ["equal-card grid", "decorative stock image"],
  "base_node": "1:9",
  "asset_decision": {
    "role": "explanatory-icon",
    "decision": "selected",
    "query": "operating model workflow icon",
    "candidate_urls": ["https://assets.westmonroe-cloud.com/example.svg"],
    "selected_url": "https://assets.westmonroe-cloud.com/example.svg",
    "visually_inspected": true,
    "placement": "right progression labels",
    "crop_intent": "none",
    "rationale": "Clarifies the stages without replacing the information structure"
  },
  "slots": {}
}
```

## Rules

- `role`: `cover`, `agenda`, `speaker`, `section-divider`, `content`, `proof`, `process`, or `closing`.
- `layout_mode`: `template-node`, `reference-derived`, or `custom-synthesis`.
- `node` is required only for `template-node`. `base_node` is optional scaffolding for other modes and does not authorize leaving the template composition unchanged.
- Content, proof, process, and closing slides require `reference_ids`, `composition_recipe`, and at least two observable `borrowed_moves` unless a deck-level exception is documented.
- A deck with four or more content slides normally needs at least three recipes.
- Direct template-node slides may not exceed 40% of content slides without a documented exception.
- Adjacent content slides may not repeat one recipe.
- `asset_decision.decision` is `selected` or `none`. Use `none` when an asset does not add meaning.
- Selected photos, graphics, and unfamiliar icons must be visually inspected. A known approved logo may be selected by exact inventory path and context rule.
- A selected asset must appear among `candidate_urls`, use the approved West Monroe host, and include placement plus rationale.
- Light surfaces use the positive Grounded Blue horizontal logo; dark surfaces use the white/reversed horizontal logo.
