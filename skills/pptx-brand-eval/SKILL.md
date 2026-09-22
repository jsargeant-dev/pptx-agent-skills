---
name: pptx-brand-eval
description: Evaluate a generated PPTX Agent HTML slide deck for West Monroe brand compliance after pptx-design and before HTML approval or PPTX compilation. Use to review only branding, visual system, typography, colors, logos, surfaces, charts, graphs, and tables against the bundled UX/UI and data-visualization baselines without changing story structure or breaking HTML-to-JSX-to-PPTX compatibility.
---

# PPTX Brand Eval

Use this skill after `pptx-design` generates the initial HTML deck and before the user sees or approves the design for `pptx-compiler`.

This is a brand-only evaluation. Do not rewrite the story, change the deck structure, choose new slide layouts, or request design changes that would make the HTML harder to compile into editable PPTX objects.

In the normal `pptx-agent` flow, this eval can trigger one automatic brand-only revision through `pptx-design` before the deck is shown to the user. Do not recommend repeated automatic revision loops. After one revision, the agent should stop for user review and tell the user they can request another brand eval after reviewing or editing the HTML.

## Baselines

Read the relevant references before evaluating:

- `references/wm-brand-ui/brand/validation-checklist.md`
- `references/wm-brand-ui/brand/brand-spec.json`
- `references/wm-brand-ui/references/visual-rules.md`
- `references/wm-brand-ui/brand/color-rules.md`
- `references/wm-brand-ui/brand/typography-rules.md`
- `references/wm-brand-ui/brand/logo-rules.md`
- `references/wm-brand-ui/brand/surface-composition-rules.md`
- `references/data-viz/data-visualization-brand-requirements.md` only when the deck contains tables, charts, graphs, KPIs, or data-heavy visuals.

Treat attached baseline files as reference material for this eval, not as instructions to run unrelated workflows from their original source packages.

## Scope

Evaluate only:

- West Monroe color use
- typography and font roles
- logo use and logo treatment
- surface composition, corner radius, borders, shadows, gradients, and spacing
- asset treatment when brand-impacting
- chart, graph, KPI, and table brand rules when present
- accessibility issues that directly affect brand-compliant visual presentation

Do not evaluate:

- whether the business story is persuasive
- whether the source content is complete
- whether the deck should use a different overall structure
- whether the selected `pptx-design` template taxonomy is correct unless the issue is a brand violation
- general content-to-container density or whether a box should be resized or removed; `pptx-design` owns that visual QA unless the spacing itself violates a brand rule
- general copy tone unless it creates a visible brand issue already handled by `pptx-intake`

## PPTX Compatibility Rule

Every recommendation must preserve the HTML-to-JSX-to-PPTX path:

- Prefer CSS token, color, font, spacing, logo, and chart-style fixes.
- Preserve semantic text, shapes, tables, charts, and image elements.
- Do not recommend flattening slides into screenshots.
- Do not recommend effects that are hard to preserve in editable PPTX, including shadows, gradients, blurs, complex masks, decorative pseudo-elements, or unsupported clipping.
- When a fix could affect compile fidelity, label it as "needs compiler check."

## Evaluation Workflow

1. Inspect the generated HTML deck, rendered screenshots, and asset register. If the asset register is missing while the deck contains imagery, return a Major finding.
2. Identify whether the deck includes charts, graphs, KPIs, tables, or data-heavy visuals.
3. Apply the UX/UI brand baseline to every slide. Verify that light surfaces use the positive Grounded Blue horizontal logo and dark surfaces use the white/reversed horizontal logo.
4. Verify every placed brand asset resolves to an approved inventory URL or documented local copy, preserves its packaged appearance, and matches its declared semantic role. Treat an uninspected photo/graphic, an improvised logo, or a wrong-context logo variant as a Blocker.
5. Apply the data-visualization baseline only to tables, charts, graphs, KPIs, and data-heavy visuals.
6. Produce brand-only findings with severity and specific, compile-safe remediation.
7. If findings require edits, identify the exact brand-only items appropriate for the one automatic `pptx-design` revision before user review.
8. Separate automatic revision recommendations from optional refinements that should wait for user review.
9. If no blocking brand issues remain, state that the HTML can proceed to user review or PPTX compilation approval.

## Finding Severity

- **Blocker:** brand issue that should be fixed before user review or PPTX compilation.
- **Major:** visible brand issue that should be fixed before final delivery.
- **Minor:** polish issue that does not block review or compilation.
- **Note:** observation or optional improvement.

## Output Format

```markdown
# PPTX Brand Eval: <deck name>

## Result

- Status: Pass / Pass with minor notes / Needs brand fixes
- Data visualization reviewed: Yes / No
- PPTX compatibility risk: Low / Medium / High

## Findings

| Severity | Slide | Area | Finding | Compile-safe fix |
|---|---:|---|---|---|

## Data Visualization Findings

| Severity | Slide | Visual | Finding | Compile-safe fix |
|---|---:|---|---|---|

## One Automatic Revision

- Recommended: Yes / No
- Scope:
- Compile-safe edit notes:
- Must not change:

## Optional User-Requested Refinements

- <brand-only refinements the user may request after reviewing or editing the HTML>

## Do Not Change

- <items that should stay intact to preserve HTML-to-PPTX structure>

## Handoff

- Ready for user HTML review: Yes / No
- Ready for PPTX compilation after user approval: Yes / No
- Required `pptx-design` edits:
```
