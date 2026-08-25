# Copy Fit Rules

Write to the design instead of shrinking the design.

## General Limits

- Hero headline: 8-14 words when possible.
- Standard headline: 1-2 lines, usually under 150 characters.
- Card title: 2-5 words.
- Bullet: 10-18 words.
- Timeline step: one short title plus 2-3 short bullets.
- Differentiator card: one phrase, usually under 42 characters.

## Rewrite Patterns

- Replace long setup clauses with a direct claim.
- Turn paragraphs into parallel bullets.
- Turn lists of mixed ideas into grouped slides.
- Move proof details to a follow-up bullet slide when a card layout gets crowded.
- Use active verbs for approach slides: Assess, Prioritize, Modernize, Sustain.

## Content-To-Container Density

Size cards, panels, and boxes to the content they contain. A surface should clarify grouping or comparison, not create a large empty interior. Aim for meaningful content to occupy a majority of the usable interior.

- Treat a container as underfilled when its meaningful content occupies less than roughly half of the available interior height and the remaining space has no functional purpose.
- For short copy, prefer an auto-height or shorter container, or remove the container and use open typography.
- If a surface remains useful, improve fit by increasing type size or spacing within the established hierarchy, not by stretching a few lines across a large fixed-height box.
- Add content only when it strengthens the message with a useful explanation, distinction, example, or implication. Never add filler to occupy space.
- In repeated card rows, equal heights are optional. Use equal heights only when they aid comparison and every card remains meaningfully occupied; otherwise use content-shaped cards aligned to a common top or baseline.
- Do not count decorative icons, accents, or a separate footer/callout as evidence that the main content area is filled.
- Preserve relational geometry. If a template uses overlap, touching surfaces, connectors, arrows, or shared edges to express a relationship, a density fix must retain that visual connection.
- If shortening a container would detach related elements or break the template's intended image, choose another archetype or create a content-shaped variant that preserves the relationship. Do not leave a partial or disconnected version of the original composition.

During visual QA, inspect every filled surface at slide scale. Flag oversized low-density boxes even when no text overflows.

## Eval Response

If `evaluate_fit.py` reports overflow warnings, revise copy first and duplicate a slide second. Do not shrink typography below the established hierarchy. For underfilled surfaces, increasing type size is an allowed remedy when it preserves hierarchy and readability.

The fit script detects overflow, not visual underfill. Pair it with the content-to-container density review above before handoff.
