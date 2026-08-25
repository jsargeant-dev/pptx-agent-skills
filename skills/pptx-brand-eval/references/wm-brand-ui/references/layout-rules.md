# Asset Layout Rules

Use approved rules where the package provides them. Treat values labeled **operational default** as temporary implementation guidance, not approved brand policy.

## Scaling

- Preserve each asset's intrinsic aspect ratio.
- Set one dimension and allow the other to scale automatically.
- Prefer SVG for logos, favicons, icons, and graphics.
- Use `max-width: 100%` and `height: auto` for responsive raster images.
- Do not stretch, squeeze, crop, or redraw a logo.
- Do not scale a non-square social icon into square artwork; center it within a consistent container instead.

## Asset geometry

| Asset | Intrinsic geometry | Size guidance | Clear space |
| --- | --- | --- | --- |
| Horizontal logo | `344.6:72`, approximately `4.79:1` | Minimum rendered symbol height: `24px` | `0.5 ×` rendered logo height on every side |
| Compass favicon | `72:72`, `1:1` | Export or reference at the size required by the platform | No package-specific rule |
| UI icons | `24:24`, `1:1` | **Operational default:** render at `24px`; use `16`, `20`, or `32px` only when the control scale requires it | **Operational default:** keep at least `8px` from adjacent text |
| Industry icons | `100:100`, `1:1` | **Operational default:** use `48px` or larger so packaged detail remains legible | **Operational default:** keep at least `16px` from unrelated elements |
| Social icons | Varies by service | **Operational default:** fit proportionally within a `24 × 24px` container | **Operational default:** use `12px` between social links |
| Whiteboard grid | `255:255`, `1:1` | Scale proportionally as a secondary composition element | Keep separate from critical text and controls |
| Hero photograph | `6000:4000`, `3:2` | Preserve `3:2` until an approved crop and focal point are supplied | No package-specific rule |

For a horizontal logo rendered at height `H`:

```text
rendered width = H × (344.6 / 72)
minimum clear space on each side = H × 0.5
```

At the minimum `24px` height, the rendered width is approximately `115px` and the minimum clear space is `12px` on every side.

## Position

### Logo

- Use the full horizontal logo in navigation and other brand placements.
- Place it on a quiet solid background with the approved color variant.
- Keep the complete clear-space area free of text, icons, borders, and container edges.
- Do not place it over busy photography.
- The package does not mandate top-left, centered, or footer placement; choose the position that fits the approved component while preserving visibility and clear space.

### Favicon

- Use the compass only in favicon, browser-icon, or app-icon metadata.
- Do not use it as a standalone brand mark in page content.

### Icons

- Center UI icons optically inside their controls.
- Place an icon before or after a label according to the action's established interaction pattern; keep the position consistent within a component family.
- Place industry icons adjacent to the industry heading or content they identify.
- Group social icons together in a dedicated social-link area.

### Graphics and photography

- Keep the whiteboard grid secondary to content and outside critical reading or interaction areas.
- Do not use the grid as a full-page texture or required hero background.
- Do not position text over an approved hero photograph unless contrast, readability, and a suitable image area have been verified.
- Do not crop an approved photograph around an assumed focal point.

## Provisional spacing system

The supplied package does not define a formal spacing scale or responsive page gutters. Until approved spacing tokens are provided, use this **operational default**:

| Purpose | Mobile | Tablet | Desktop |
| --- | ---: | ---: | ---: |
| Page gutter | `24px` | `40px` | `64px` |
| Section separation | `48px` | `64px` | `96px` |
| Image or graphic to related text | `24px` | `24px` | `32px` |

- Use an `8px` base increment for other gaps and padding.
- Prefer `8`, `16`, `24`, `32`, `48`, `64`, and `96px`.
- Do not reduce the logo's `0.5H` clear space to fit the provisional grid.
- Replace these provisional values when official spacing, breakpoint, icon, and photography specifications become available.
