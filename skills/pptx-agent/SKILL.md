---
name: pptx-agent
description: Orchestrate the mandatory HTML-first PowerPoint workflow from source content through PPTX intake, optional design-reference analysis, PPTX design, brand evaluation, HTML review, and separate editable PPTX compilation only after explicit HTML approval. Use when the user wants a guided PPTX Agent that always stops at HTML before any PPTX export.
---

# PPTX Agent

Use this as the top-level coordinator for building a presentation through an HTML-first workflow.

## Start By Orienting The User

If the user has not already answered these, ask before starting expensive work:

- What is the goal of the presentation?
- Who is the audience?
- What should the audience do, decide, or understand after reading it?
- Are any provided PPTX/HTML slides source content, design inspiration, slides to replicate, or all of the above?

Do not ask whether the user wants to go directly to PPTX or whether the workflow should continue through PPTX during intake. The workflow always produces an HTML review deck first. If the user already asks for PPTX, acknowledge that PPTX can be created only after they review and explicitly approve the HTML deck.

Keep the questions concise. If the user provides enough context, proceed and state the assumptions.

## Pipeline

1. **PPTX Intake**
   - Use `pptx-intake` to extract source content, understand the ask, identify the goal/audience/focus/message, rewrite into West Monroe voice, and create a concise presentation narrative handoff.
   - Output a deck intake package before design work begins.

2. **Optional Design Reference**
   - Use `pptx-design-reference` when the user provides PPTX or HTML slides as examples, branded references, or specific slides they want replicated.
   - The reference brief may influence slide patterns, but `pptx-design` templates and West Monroe standards remain the primary design rules.

3. **PPTX Design**
   - Use `pptx-design` to turn the intake package and optional reference brief into a slide plan, slide-ready copy, brand-aware linked asset choices, and an editable 16:9 HTML deck.
   - When the user wants less repetition, stronger design, or good-example deck influence, tell `pptx-design` to use its bundled visual example previews and contact sheets as reference-only composition guidance.
   - Use `wm-brand-assets` as an external image source when hosted West Monroe logos, icons, accents, or photos are needed. Do not package `wm-brand-assets` into this agent.
   - Require `pptx-design` to run both overflow fit checks and visual content-density QA before brand evaluation. Large boxes with only a few lines of copy must be resized, removed, replaced with a better layout, or strengthened with useful content rather than filler.

4. **PPTX Brand Eval And One Revision**
   - Use `pptx-brand-eval` after `pptx-design` and before user HTML review.
   - Evaluate only branding: visual system, typography, colors, logo treatment, surfaces, and data visualization rules for tables/charts/graphs.
   - Do not allow this eval to rewrite story, alter page structure, flatten slides, or introduce effects that would weaken HTML-to-JSX-to-PPTX compatibility.
   - If brand issues are found, route fixes back through `pptx-design` for exactly one automatic brand-only revision before user review.
   - Do not continue automatic eval/revision loops. After the one revision, show the user the revised HTML, summarize the eval result, and call out any remaining brand notes.
   - Tell the user they can ask for another `pptx-brand-eval` pass after they review or edit the HTML.

5. **HTML Review And Edit Gate**
   - Stop after the HTML deck.
   - Give the user the HTML path, brand-eval result, whether the one automatic brand revision was applied, and a concise review checklist.
   - Require the user to review and make or request necessary HTML design edits before PPTX compilation.
   - Offer the user clear next actions: request more HTML edits, run another brand eval, or approve the reviewed HTML for PPTX compilation.
   - Do not push to PPTX until the user explicitly approves the HTML deck for compilation.

6. **Optional PPTX Compiler**
   - By default, stop at the HTML deck for review and editing.
   - If the user approves PPTX generation, use `pptx-compiler` to convert the approved HTML into an editable PPTX.
   - Preserve text boxes, shapes, and individual images as editable PowerPoint objects.
   - Validate that slides were not flattened into full-slide screenshots.

## HTML Review Checklist

Before compiling to PPTX, ask the user to confirm:

- slide order and story are right
- headline and body copy are approved
- important claims, dates, metrics, and names are correct
- visual hierarchy and density feel right
- cards, panels, and boxes are sized to their content without large accidental empty interiors
- linked assets/images are acceptable
- any reference-slide replication is close enough
- no known edits remain

If edits are requested, return to `pptx-design` and regenerate or patch the HTML before compiling.

## Operating Rules

- Keep all work in the current project or thread folder.
- Keep intake, optional reference brief, slide plan, HTML, scene JSON, QA renders, and final PPTX as separate artifacts.
- Treat HTML as the visual source of truth.
- Never offer a straight-to-PPTX path at intake. PPTX generation is a separate post-HTML-approval action.
- Do not embed brand assets in HTML as data URIs; use linked hosted assets unless the user asks for an offline package.
- Do not flatten slides to images unless the user explicitly chooses image-only fidelity.
- If `wm-brand-assets` is unavailable, continue with available hosted URLs or ask for asset direction.

## Handoff

After HTML design, report:

- HTML path
- slide count
- selected asset sources
- brand eval result
- whether the one automatic brand revision was applied
- option to request another brand eval after review or edits
- fit or visual QA result
- review checklist
- that the workflow is paused at HTML until the user approves PPTX compilation

After PPTX compilation, report:

- PPTX path
- HTML source path
- scene JSON path
- slide count
- editable textbox count
- shape count
- individual image count
- full-slide image count
- QA status
