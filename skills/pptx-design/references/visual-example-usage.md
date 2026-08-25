# Visual Example Usage

Use `visual-example-index.json` and `example-slide-previews/` when the deck needs stronger visual variety, richer pacing, or a closer match to the good-example West Monroe slide corpus.

## How To Use The Previews

- Start with each deck's contact sheets to understand rhythm, slide density, section pacing, and repeated visual motifs.
- Open individual slide JPEGs only for the few examples most relevant to the current slide type.
- Translate useful patterns into editable HTML/CSS using the slide template system.
- Favor varied silhouettes across adjacent slides: mix statement/photo, executive summary, proof, process, agenda, dense-detail, and credentials patterns when the story supports it.
- Use `source-deck-corpus.json` for slide family, word count, media density, and text-preview metadata before opening image previews.

## Good Uses

- Choosing a more interesting composition for a slide that otherwise maps to a repetitive template.
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
