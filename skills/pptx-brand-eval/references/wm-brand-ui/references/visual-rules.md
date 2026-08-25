# Visual Rules

Apply these West Monroe rules after selecting an asset. Use the packaged files under `brand/` as the detailed authority.

## Rule priority

1. Follow `brand/brand-spec.json`.
2. Use `brand/tokens.json` or `brand/tokens.css` for implementation values.
3. Follow the relevant detailed specification: logo, color, typography, component, or surface composition.
4. Use `brand/validation-checklist.md` before delivery.
5. Do not infer brand voice or copy guidance; it is outside this package.

## Typography

- Use IBM Plex Sans for headings, headlines, display type, subheads, large statistics, and eyebrows.
- Use Arial for paragraphs, navigation, buttons, form labels, captions, and other UI copy.
- Load weights `400`, `500`, `600`, and `700`.
- Use the named style closest to the content role in `brand/typography-rules.md`.
- Use `120%` line height for compact display, headline, and link styles.
- Use `130%` line height for sentence-case, body, navigation, stats, and utility styles.
- Use uppercase sparingly for documented display hierarchy, not long body copy.
- Use Helvetica followed by `sans-serif` only as the body-copy fallback when Arial is unavailable.
- Do not apply negative tracking.

Canonical implementation sources:

- `brand/typography-spec.json`
- `brand/typography-rules.md`
- `brand/tokens.json`
- `brand/tokens.css`

## Color

| Role | Color |
| --- | --- |
| Default page background | Canvas Gray `#F8F8F8` |
| Content surfaces, controls, inverse text | White `#FFFFFF` |
| Primary text/structure/secondary background | Grounded Blue `#070154` |
| Sparse large emphasis | Highlight Magenta `#F900D3` |
| Interactive and small-text emphasis | Highlight Blue `#0047FF` |
| Supporting dark neutral | Dark Gray `#50658E` |
| Supporting medium neutral | Medium Gray `#CED7E6` |
| Supporting light neutral | Light Gray `#E8EEF8` |

- Keep Canvas Gray, White, and Grounded Blue dominant.
- Use accent colors sparingly.
- Use only text/background combinations approved in `brand/color-rules.md`.
- Reserve Highlight Magenta on White, or White on Highlight Magenta, for large text: at least `18pt` regular or `14pt` bold.
- Target WCAG 2.0 AA.

## Surfaces and components

- Use square corners for boxes, cards, panels, containers, images, tables, charts, and layout surfaces.
- Use `80px` rounding only for approved buttons and search fields.
- Use `20px` rounding for the approved search dropdown treatment.
- Do not use gradients, shadows, glow, or elevation effects.
- Build hierarchy with solid color blocks, borders, spacing, scale, and typographic weight.
- Use `1px` borders by default and `2px` for strong emphasis.
- Use Grounded Blue or Highlight Magenta for emphasis borders and approved neutrals for quiet structure.

Canonical implementation sources:

- `brand/component-spec.json`
- `brand/surface-composition-spec.json`
- `brand/surface-composition-rules.md`

## Asset treatment

- Keep logos, favicons, icons, and graphics at their intrinsic proportions.
- Retain packaged logo and graphic colors; do not add effects.
- Use the whiteboard grid as a subtle supporting layer only.
- Do not infer a required hero treatment from the packaged photograph.
- Do not apply an undocumented crop, filter, duotone, overlay, or color treatment to photography.

## Data visualization

- Use only the categorical, KPI, and deemphasis palettes in `brand/color-spec.json`.
- Preserve the documented categorical sequence, although the sequence may begin at any listed color.
- Do not rely on color alone; use direct labels and leader lines where applicable.
- Follow the chart stroke and accessibility rules in `brand/color-rules.md`.
