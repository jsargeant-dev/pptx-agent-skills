# Surface and Composition Rules

## Confirmed Brand Decisions

- Use IBM Plex Sans for headings and display type.
- Use Arial for body copy and UI copy.
- Use Canvas Gray `#F8F8F8` as the default page background and White `#FFFFFF` for content surfaces.
- Do not use gradients anywhere.
- Do not use shadows.
- Build depth and emphasis with borders, solid blocks, scale, spacing, and approved graphic elements.
- Voice and copy guidance are intentionally excluded from this package.

## Corner Radius Rule

West Monroe is primarily a square-corner brand.

Default rule:

- Use `border-radius: 0` for boxes, cards, panels, containers, images, chart containers, tables, and layout surfaces.

Rounded-corner exception:

- Approved buttons may use the rounded `80px` radius treatment from the component source.
- Search fields may use the same rounded `80px` radius as buttons.
- Dropdown lists paired with search may use a smaller rounded radius, such as `20px`, when matching the approved source component.
- Rounded corners should be the exception, not the default.
- Do not use rounded corners on large layout containers, image frames, hero panels, cards, or dashboard panels.
- Do not use pill shapes unless an approved component specifically requires one.
- If a new non-button, non-search rounded exception is needed, use a small radius such as `4px`; do not exceed `8px` without brand review.

LLM rule:

- Assume square corners for layout. Use rounded corners for approved buttons and search fields that match the source component states.

## Gradients

Gradients are not allowed.

Do not use:

- Linear gradients
- Radial gradients
- Mesh gradients
- Gradient text
- Gradient borders
- Gradient chart backgrounds
- Gradient hero backgrounds
- Gradient overlays

Use solid approved brand colors instead.

## Shadows

Shadows are not allowed.

Do not use:

- Box shadows
- Drop shadows
- Text shadows
- Glow effects
- Ambient elevation effects

Use borders, solid blocks, spacing, and scale to create hierarchy.

## Borders

Use borders for structure and emphasis.

Approved emphasis border colors:

- Grounded Blue `#070154`
- Highlight Magenta `#F900D3`

Neutral borders may use approved support neutrals when the border should organize content quietly.

Recommended border defaults:

- Standard border width: `1px`
- Strong emphasis border width: `2px`
- Border radius: `0`

## Whiteboard Grid Graphic

Approved grid asset:

- `assets/graphic/wm_whiteboard_grid_100_rgb_240912.svg`

Usage:

- Use as a supporting graphic element when content benefits from the matrix grid motif.
- Keep it subtle and secondary to content.
- Do not recolor unless a future approved variant is provided.
- Do not use it as a full-page decorative texture.
- Do not treat it as a required hero pattern.

## LLM Instruction

Build West Monroe layouts with solid colors, square rectangles, borders, spacing, and scale. Do not use gradients or shadows. Treat rounded corners as a rare small-component exception, not as a general style. Do not infer a required hero layout from example imagery.
