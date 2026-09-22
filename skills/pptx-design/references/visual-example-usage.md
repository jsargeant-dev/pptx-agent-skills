# Visual Example Usage

Use `composition-patterns.json` first, then `visual-example-index.json` and `example-slide-previews/` to inspect the few examples shortlisted for each slide. When bundled examples are part of the pipeline, reference selection is required rather than an optional remedy for a repetitive deck.

## How To Use The Previews

- Start with `composition-patterns.json` to match slide purpose and density to two or three candidate patterns.
- Open the cited individual slide JPEGs and only the contact sheets needed to understand surrounding rhythm.
- Translate useful patterns into editable HTML/CSS using the slide template system.
- Favor varied silhouettes across adjacent slides: mix statement/photo, executive summary, proof, process, agenda, dense-detail, and credentials patterns when the story supports it.
- Use `source-deck-corpus.json` for slide family, word count, media density, and text-preview metadata before opening image previews.

## Good Uses

- Choosing the composition before selecting template components, so the template cannot become the default layout answer.
- Matching the density, hierarchy, and visual pacing of a relevant reference slide.
- Borrowing layout logic such as split emphasis, quote/photo tension, proof blocks, process lanes, or executive-summary grids.
- Checking whether a deck overuses the same structure across several consecutive slides.

## Do Not Do

- Do not embed preview JPEGs, full-slide screenshots, or exported slide images in generated HTML or PPTX output.
- Do not copy client-specific copy, names, data, or screenshots from the examples unless the user supplied the same content as source material for the current request.
- Do not let visual examples override West Monroe brand rules, `pptx-brand-eval`, or HTML-to-JSX-to-PPTX compatibility.
- Do not create effects that are hard to compile as editable PPTX objects, including complex masks, blur effects, rasterized text, or full-slide background screenshots.

## Expected Output

The final deck should look informed by the examples while remaining a new, editable 16:9 HTML artifact. Text, shapes, tables, charts, and image placements must remain separate DOM elements so `pptx-compiler` can create editable PowerPoint objects after user approval.
