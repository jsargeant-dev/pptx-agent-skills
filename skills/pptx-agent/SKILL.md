---
name: pptx-agent
description: Orchestrate the mandatory HTML-first PowerPoint workflow from source content through PPTX intake, reference-first design when examples are supplied, PPTX design, brand evaluation, HTML review, and separate editable PPTX compilation only after explicit HTML approval. Use when the user wants a guided PPTX Agent that always stops at HTML before any PPTX export.
---

# PPTX Agent

Use this as the top-level coordinator for building a presentation through an HTML-first workflow.

## Canonical Pipeline Boundary

This six-skill suite is the active PPTX pipeline. Its only supported export route is:

`pptx-agent -> pptx-intake -> optional pptx-design-reference -> pptx-design -> pptx-brand-eval -> user HTML approval -> pptx-compiler`

Do not route new work through legacy template-placement or alternate HTML-to-PPTX skills. The compiler owns the approved HTML-to-editable-PPTX conversion; template-specific placement is outside this suite unless a separate template workflow is explicitly restored.

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

2. **Reference-First Design**
   - When the user supplies PPTX, HTML, or PDF references, or asks for reference-inspired slides, this stage is mandatory before design. Treat references as composition sources, not optional decoration.
   - Use `pptx-design-reference` for user-provided examples, branded references, or specific slides they want replicated. For bundled examples, inspect the contact sheets first, then only the relevant individual previews.
   - Select two to four source slides or archetypes and create a reference map before slide planning. For every output slide, record the reference slide/archetype, composition moves to borrow, copy/content mapping, and elements to avoid copying.
   - The template and West Monroe standards govern brand, editability, canvas, typography, color, and surface constraints. Reference slides govern composition, pacing, density, layout silhouettes, and visual rhythm.
   - Never embed a reference slide or use a full-slide screenshot. Rebuild the selected composition as new editable HTML with the new copy and linked assets.

3. **PPTX Design**
   - Use `pptx-design` to turn the intake package and reference map into a slide plan, slide-ready copy, brand-aware linked asset choices, and an editable 16:9 HTML deck. Require it to build new slides from the selected reference archetypes, not just reuse the template shell.
   - For decks of four or more slides, use at least three distinct reference-derived composition patterns when the content supports it. Document any content-driven exception in the reference map.
   - When the user wants less repetition, stronger design, or good-example deck influence, tell `pptx-design` to inspect the bundled visual example previews and contact sheets and use them as a layout taxonomy and composition reference, not merely as style hints.
   - Use `wm-brand-assets` as an external image source when hosted West Monroe logos, icons, accents, or photos are needed. Do not package `wm-brand-assets` into this agent.
   - Require `pptx-design` to run both overflow fit checks and visual content-density QA before brand evaluation. Large boxes with only a few lines of copy must be resized, removed, replaced with a better layout, or strengthened with useful content rather than filler.

4. **Reference Influence QA**
   - Before brand evaluation, compare the HTML renders or contact sheet to the selected references and the reference map.
   - Confirm every slide has observable reference-derived composition moves, the deck is not a repeated template shell, and the layouts are shaped by the content. Confirm the reference pattern was rebuilt as editable HTML rather than copied as a screenshot.
   - If reference influence is weak or missing, route one targeted reference-first design correction back through `pptx-design` before brand evaluation. This is separate from the single automatic brand-only revision.
   - Record the reference-influence result and any documented exception in the handoff.

5. **PPTX Brand Eval And One Revision**
   - Use `pptx-brand-eval` after `pptx-design` and before user HTML review.
   - Evaluate only branding: visual system, typography, colors, logo treatment, surfaces, and data visualization rules for tables/charts/graphs.
   - Do not allow this eval to rewrite story, alter page structure, flatten slides, or introduce effects that would weaken HTML-to-JSX-to-PPTX compatibility.
   - If brand issues are found, route fixes back through `pptx-design` for exactly one automatic brand-only revision before user review.
   - Do not continue automatic eval/revision loops. After the one revision, show the user the revised HTML, summarize the eval result, and call out any remaining brand notes.
   - Tell the user they can ask for another `pptx-brand-eval` pass after they review or edit the HTML.

6. **HTML Review And Edit Gate**
   - Stop after the HTML deck.
   - Give the user the HTML path, brand-eval result, whether the one automatic brand revision was applied, and a concise review checklist.
   - Require the user to review and make or request necessary HTML design edits before PPTX compilation.
   - Offer the user clear next actions: request more HTML edits, run another brand eval, or approve the reviewed HTML for PPTX compilation.
   - Do not push to PPTX until the user explicitly approves the HTML deck for compilation.
   - Keep the review package together in the project folder, including the intake package, reference map when references exist, slide plan, generated HTML, fit report, brand-eval result, and requested HTML revisions.

7. **Optional PPTX Compiler**
   - By default, stop at the HTML deck for review and editing.
   - If the user approves PPTX generation, use `pptx-compiler` to convert the approved HTML into an editable PPTX.
   - Preserve text boxes, shapes, and individual images as editable PowerPoint objects.
   - Validate that slides were not flattened into full-slide screenshots.
   - Keep the scene JSON, compiler QA renders, structural inspection output, and conversion report beside the final PPTX.

## HTML Review Checklist

Before compiling to PPTX, ask the user to confirm:

- slide order and story are right
- headline and body copy are approved
- important claims, dates, metrics, and names are correct
- visual hierarchy and density feel right
- cards, panels, and boxes are sized to their content without large accidental empty interiors
- linked assets/images are acceptable
- each selected reference archetype is visibly reflected in the corresponding slide
- the reference map is faithful to composition without copying a slide image
- requested layout variety is present, or any content-driven exception is documented
- no known edits remain

If edits are requested, return to `pptx-design` and regenerate or patch the HTML before compiling.

## Operating Rules

- Keep all work in the current project or thread folder.
- Keep intake, optional reference brief, slide plan, HTML, scene JSON, QA renders, and final PPTX as separate artifacts.
- When references are present, keep the reference map with the intake and slide plan; reference-first design is required and template shells must not override selected archetypes.
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
- reference map and reference-influence QA result
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
