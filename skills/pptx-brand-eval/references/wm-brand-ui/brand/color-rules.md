# Color Rules

## Core Principles

The West Monroe color palette consists of:

- Primary palette
- Accent palette
- Supporting neutrals palette
- Data visualization palettes

Colors are listed in hierarchy order. For primary, accent, and support-neutral palettes, the order describes intended share of use. For data visualization palettes, the order describes the display sequence when a chart needs multiple colors.

WCAG 2.0 accessibility is a priority. Use approved text/background combinations whenever text is placed on color.

## Primary Palette

Canvas Gray is the default page background. White is used for cards, controls, inverse text, and clearly separated content surfaces. Grounded Blue is used for primary text, structure, controls, and dark sections.

1. Canvas Gray
   - RGB: `248, 248, 248`
   - HEX: `#F8F8F8`
   - Role: default page background

2. White
   - RGB: `255, 255, 255`
   - HEX: `#FFFFFF`
   - Role: content surfaces, controls, inverse text

3. Grounded Blue
   - RGB: `7, 1, 84`
   - HEX: `#070154`
   - Role: headlines, body copy, secondary background, primary structure

## Accent Palette

Accent colors are used sparingly to accent key points.

1. Highlight Magenta
   - RGB: `249, 0, 211`
   - HEX: `#F900D3`
   - Role: large sub-headlines, large callouts, UI hover states, illustrations
   - Rule: may be used as text only in approved accessible combinations

2. Highlight Blue
   - RGB: `0, 71, 255`
   - HEX: `#0047FF`
   - Role: small emphasis text, body copy headers, illustration, interactive emphasis
   - Rule: may be used as text in approved accessible combinations

## Supporting Neutrals

Supporting neutrals can be used as background colors to help organize heavy content. Light Gray is also used for the square matrix grid in the graphic elements library.

1. Dark Gray
   - RGB: `80, 101, 142`
   - HEX: `#50658E`
   - Role: dark support background, secondary content

2. Medium Gray
   - RGB: `206, 215, 230`
   - HEX: `#CED7E6`
   - Role: support background

3. Light Gray
   - RGB: `232, 238, 248`
   - HEX: `#E8EEF8`
   - Role: support background, matrix grid background

## Approved Text and Background Combinations

These combinations may be used at any text size because they meet WCAG 2.0 AA contrast for normal text.

| Foreground | Background | Contrast |
| --- | --- | --- |
| Grounded Blue `#070154` | Canvas Gray `#F8F8F8` | 17.32 |
| Highlight Blue `#0047FF` | Canvas Gray `#F8F8F8` | 5.91 |
| Dark Gray `#50658E` | Canvas Gray `#F8F8F8` | 5.50 |
| Grounded Blue `#070154` | White `#FFFFFF` | 18.40 |
| White `#FFFFFF` | Grounded Blue `#070154` | 18.40 |
| White `#FFFFFF` | Dark Gray `#50658E` | 5.84 |
| Grounded Blue `#070154` | Medium Gray `#CED7E6` | 12.69 |
| Grounded Blue `#070154` | Light Gray `#E8EEF8` | 15.78 |
| Highlight Blue `#0047FF` | White `#FFFFFF` | 6.28 |
| White `#FFFFFF` | Highlight Blue `#0047FF` | 6.28 |
| Grounded Blue `#070154` | Highlight Magenta `#F900D3` | 5.23 |
| Highlight Magenta `#F900D3` | Grounded Blue `#070154` | 5.23 |
| Highlight Blue `#0047FF` | Light Gray `#E8EEF8` | 5.39 |

These combinations are reserved for large text only. Large text means at least 18pt regular or 14pt bold.

| Foreground | Background | Contrast |
| --- | --- | --- |
| Highlight Magenta `#F900D3` | White `#FFFFFF` | 3.52 |
| White `#FFFFFF` | Highlight Magenta `#F900D3` | 3.52 |

## Highlight Magenta Accessibility Preference

WCAG 2.0 standards apply to digital applications and are the accessibility standard used by the Americans with Disabilities Act.

Highlight Magenta and Grounded Blue pass WCAG 2.0 AA standards for type of any size with a contrast ratio of approximately `5.2:1`. This applies in both directions:

- Grounded Blue `#070154` on Highlight Magenta `#F900D3`
- Highlight Magenta `#F900D3` on Grounded Blue `#070154`

Highlight Magenta and White pass WCAG 2.0 AA standards only for large text, with a contrast ratio of approximately `3.5:1`. This applies in both directions:

- Highlight Magenta `#F900D3` on White `#FFFFFF`
- White `#FFFFFF` on Highlight Magenta `#F900D3`

Although Grounded Blue and Highlight Magenta are mathematically more accessible together, West Monroe templates generally prefer the visual interaction between Highlight Magenta and White. Use Highlight Magenta for large, bold text such as subheads and callouts when it appears on White. Highlight Magenta may also be used on Grounded Blue backgrounds for strong visual emphasis.

## Categorical Data Visualization Palette

Use this palette in charts, graphs, and color-coded visuals. No other brand colors may be used in data visuals that use the categorical palette. Colors must be used in the order listed, but the series may start at any color in the sequence.

1. Highlight Magenta `#F900D3`
2. Light Blue `#00E8FA`
3. Green `#1DD566`
4. Gold `#FFC700`
5. Purple `#B641FF`
6. Light Green `#00FCB0`
7. Orange `#FF8A00`
8. Blue `#00A3FF`
9. Red `#F52C00`

## Data Visualization KPIs Palette

Use this palette for positive, median, and negative data metaphors, such as stoplight-style indicators.

1. Green `#1DD566` for positive
2. Gold `#FFC700` for median or neutral
3. Red `#F52C00` for negative

## Deemphasis Data Visualization Palette

Use this palette to deemphasize data. Any colored parts used with the deemphasis palette must come from the categorical palette and follow the categorical sequence, though the sequence may start at any color. Tinting of deemphasis colors is allowed if more variation is required.

1. Light Gray `#E8EEF8`
2. Medium Gray `#CED7E6`
3. Gray `#8DA3BA`

## Accessibility With Data Visualization

Charts and graphs may need modification for accessibility. Apply these specifications where applicable:

- Center-align a `1px` black stroke on top of a `4px` white stroke.
- Do not separate chart bars or pie chart segments.
- Use data points with descriptive labels and leader lines instead of relying only on legends.
- Leader lines must point directly to the chart bar or pie segment they describe.
- Leader lines must be Grounded Blue.
- Place a solid white background behind leader lines to improve readability.
- Use a `4px` white stroke center-aligned below the `1px` black or Grounded Blue leader line.

## LLM Instruction

Use Canvas Gray `#F8F8F8` as the default page background, White for content surfaces and controls, and Grounded Blue for primary text, structure, controls, and dark sections. Use accent colors sparingly. Highlight Magenta and Highlight Blue may be used for text only in approved accessible combinations. Use Highlight Magenta on White only for large, bold display text such as subheads and callouts. For charts, use only the documented data visualization palettes and preserve the listed order.
