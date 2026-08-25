---
name: pptx-intake
description: Intake and rewrite source content for the PPTX Agent before design. Use when source files, notes, outlines, decks, docs, transcripts, HTML, existing PPTX slides, or pasted content need to be extracted, understood, cleaned, and shaped into a concise West Monroe presentation narrative for pptx-design.
---

# PPTX Intake

Use this as the first stage of the PPTX Agent pipeline. Its job is to understand the ask, extract the needed content, and rewrite it into a concise West Monroe presentation narrative that `pptx-design` can turn into an HTML deck.

This is not the design stage. Do not choose final slide templates, build HTML, create PPTX files, or override `pptx-design` design rules.

## Core Rules

- Extract source text from every provided file.
- Identify the goal, audience, focus, core message, and useful story structure before rewriting.
- Write in West Monroe voice: direct, practical, collaborative, outcome-led.
- Do not use em dashes.
- Do not sound like generic consulting marketing.
- Start with the point in every major section.
- If the source lacks proof, quantify only what is explicitly supported.
- Rewrite source content to fit a storytelling presentation, not a long-form document.
- Keep final intake output concise enough for `pptx-design` to use without rereading every source.
- Keep all output inside the current project or thread folder when creating files.

## Supported Inputs

- `.txt`, `.md`, `.csv`
- `.pdf`
- `.docx`
- `.pptx`
- `.xlsx`, `.xlsm`
- HTML files or pasted HTML
- folders containing a mix of supported files
- pasted notes, outlines, transcripts, prompts, or rough draft copy

Use `scripts/extract_source_text.py` first when files need text extraction:

```bash
python3 <pptx-intake-skill-dir>/scripts/extract_source_text.py <file1> <file2> ... --output-dir ./extracted
```

Legacy binary Office files such as `.doc`, `.xls`, and `.ppt` are not reliably supported by the script. Ask for converted `.docx`, `.xlsx`, or `.pptx` versions only if needed.

## Required References

Before rewriting, read:

- `references/brand-voice.md`
- `references/presentation-rubric.md`
- `references/intake-output.md`

## Required Workflow

1. Extract source text from every provided file.
   - Preserve source labels, page or slide references when available, and important order.
   - For PPTX inputs, capture slide titles, body text, notes when available, key claims, metrics, and repeated themes.
   - For HTML inputs, extract visible page/section text and note the section structure.

2. Understand the ask before rewriting.
   - Identify the likely audience, business goal, desired action, central message, stakes, proof points, constraints, and missing information.
   - Identify what content is essential, what is supporting detail, and what should be left for appendix or backup.

3. Treat provided HTML or PPTX as content and design inspiration only.
   - Note useful content patterns, visual intent, section structure, or layout ideas.
   - Do not treat provided HTML or PPTX as binding design rules.
   - Final design decisions belong to `pptx-design`, whose templates and HTML slide system are primary.
   - If the source is off-brand or from another brand, rewrite the content into West Monroe voice and flag design elements that should not carry forward.

4. Rewrite into West Monroe presentation narrative.
   - Use `references/brand-voice.md`.
   - Create concise slide-ready narrative copy, not a final slide layout.
   - Lead with the point, keep sentences short, and connect business outcomes to the work.
   - Preserve supported claims, names, dates, metrics, evidence, and client-specific language that matters.
   - Mark inferred messages and unsupported claims clearly.

5. Self-review against the rubric.
   - Use all seven categories in `references/presentation-rubric.md`.
   - Revise weak areas before finalizing the intake package.
   - Do not hand off a first pass when the story is unclear, generic, unsupported, or off-brand.

6. Save the intake package.
   - Use the structure in `references/intake-output.md`.
   - Save as Markdown in the current project or thread folder when creating an artifact.

## Guardrails

- Do not invent claims, metrics, customer stories, or recommendations.
- Do not keep off-brand source phrasing just because it appeared in source material.
- Do not overfit to a source deck's design if it conflicts with West Monroe standards or `pptx-design`.
- Do not create a rigid proposal-style field scaffold.
- Do not perform asset selection, HTML generation, or PPTX compilation in this stage.

## Handoff To PPTX Design

End with a compact handoff that tells `pptx-design`:

- the recommended presentation narrative
- the audience and desired action
- the highest-priority messages
- proof points and evidence to preserve
- sections or slide moments likely needed
- design inspiration notes from provided HTML/PPTX, if any
- what is off-brand or should not carry forward
- open questions or user confirmations still needed
