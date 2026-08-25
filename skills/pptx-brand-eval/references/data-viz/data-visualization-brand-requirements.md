# Data Visualization Brand Requirements for Existing HTML Sites

This guide translates the attached data-visualization references into implementation rules for existing HTML sites.

The rules below are normative. The HTML and CSS examples show one way to apply them; they do not introduce additional brand requirements.

## 1. Apply the rules in this order

1. Identify whether the visual is a categorical chart, a KPI/status visual, or a deemphasis treatment.
2. Use only the palette assigned to that purpose.
3. Apply the required Grounded Blue strokes and text.
4. Add direct descriptive labels and leader lines where the visual requires them.
5. For tables, select the theme based on the table's context and preserve the reference hierarchy, spacing, proportions, and color application.
6. Check the misuse and accessibility rules before delivery.

## 2. Approved data-visualization colors

Use these values as CSS custom properties so the existing site can apply the same rules consistently.

```css
:root {
  /* Categorical palette: use in the order listed below. */
  --dv-highlight-magenta: #f900d3;
  --dv-light-blue: #00e8fa;
  --dv-green: #1dd566;
  --dv-gold: #ffc700;
  --dv-purple: #b641ff;
  --dv-light-green: #00fcb0;
  --dv-orange: #ff8a00;
  --dv-blue: #00a3ff;
  --dv-red: #f52c00;

  /* Deemphasis palette. */
  --dv-light-gray: #e8eef8;
  --dv-medium-gray: #ced7e6;
  --dv-gray: #8da3ba;

  /* Use the site's approved Grounded Blue token. Do not invent a replacement. */
  --dv-grounded-blue: var(--wm-grounded-blue);

  /* Map these aliases to the site's existing table-theme tokens. */
  --dv-table-divider: var(--wm-table-divider);
  --dv-table-primary-accent: var(--wm-table-primary-accent);
  --dv-table-secondary-accent: var(--wm-table-secondary-accent);
  --dv-table-secondary-surface: var(--wm-table-secondary-surface);
}
```

| Palette | Approved colors | Use |
| --- | --- | --- |
| Categorical | Highlight Magenta, Light Blue, Green, Gold, Purple, Light Green, Orange, Blue, Red | Categories, series, charts, graphs, and color-coded visuals |
| KPI | Green, Gold, Red | Positive, median, and negative data metaphors, such as a stoplight |
| Deemphasis | Light Gray, Medium Gray, Gray | Data that should recede in emphasis |

### Categorical palette values

Use the colors in this order. A series may start at any color, but once started it must continue in the defined order.

| Order | Name | HEX | RGB |
| ---: | --- | --- | --- |
| 1 | Highlight Magenta | `#f900d3` | `249, 0, 211` |
| 2 | Light Blue | `#00e8fa` | `0, 232, 250` |
| 3 | Green | `#1dd566` | `29, 213, 102` |
| 4 | Gold | `#ffc700` | `255, 199, 0` |
| 5 | Purple | `#b641ff` | `182, 65, 255` |
| 6 | Light Green | `#00fcb0` | `0, 252, 176` |
| 7 | Orange | `#ff8a00` | `255, 138, 0` |
| 8 | Blue | `#00a3ff` | `0, 163, 255` |
| 9 | Red | `#f52c00` | `245, 44, 0` |

Highlight Magenta is the only brand color included in the categorical palette. Do not add other brand colors to categorical charts or graphs.

### KPI palette values

Use only for KPI/status metaphors:

| Name | HEX | RGB |
| --- | --- | --- |
| Green | `#1dd566` | `29, 213, 102` |
| Gold | `#ffc700` | `255, 199, 0` |
| Red | `#f52c00` | `245, 44, 0` |

### Deemphasis palette values

Use these colors to deemphasize data. Colored parts must come from the categorical palette and follow its defined order. The order may start at any color. Tinting the deemphasis colors is allowed when more variation is required.

| Name | CMYK | RGB | HEX |
| --- | --- | --- | --- |
| Light Gray | `11, 3, 0, 0` | `232, 238, 248` | `#e8eef8` |
| Medium Gray | `24, 11, 0, 0` | `206, 215, 230` | `#ced7e6` |
| Gray | `40, 30, 25, 6` | `141, 163, 186` | `#8da3ba` |

## 3. Chart and graph construction

### Required

- Use data colors only inside charts and graphs.
- Use Grounded Blue for chart strokes and chart text.
- Keep chart bars and pie segments together; do not create separating gaps.
- When labels are needed for comprehension, label the data points directly with descriptive text and leader lines instead of relying on a legend.
- Make each leader line point directly to the bar or pie segment whose information it describes.

### Leader-line treatment

The references require a centered two-stroke construction:

- a 1px foreground stroke over
- a 4px white stroke behind it for readability.

Leader lines must use Grounded Blue. Preserve the two-stroke construction and map the visible foreground stroke to the site's approved Grounded Blue token; do not introduce another brand color.

For SVG, the construction can be represented as two coincident lines:

```html
<line class="dv-leader-line-under" x1="180" y1="120" x2="250" y2="120" />
<line class="dv-leader-line" x1="180" y1="120" x2="250" y2="120" />
```

```css
.dv-leader-line-under {
  stroke: #fff;
  stroke-width: 4px;
  stroke-linecap: butt;
}

.dv-leader-line {
  stroke: var(--dv-grounded-blue);
  stroke-width: 1px;
  stroke-linecap: butt;
}
```

Place the solid white stroke directly behind the leader line so labels remain readable over the chart. Keep the leader line attached to the exact data point it describes.

## 4. Palette selection

### Categorical visuals

Use the categorical palette for charts, graphs, and color-coded visuals that distinguish categories or series. Start at any color, then continue through the approved sequence. Do not mix in other brand colors.

### KPI visuals

Use the KPI palette when color communicates a positive, median, or negative condition. Keep the meaning of Green, Gold, and Red tied to the KPI/status metaphor rather than using them as a general-purpose series palette.

### Deemphasis visuals

Use the deemphasis palette when data should recede. If colored data remains in the visual, use categorical colors in the defined order and use tints only when additional variation is required.

## 5. Misuses to prevent

- Do not use Highlight Yellow for anything other than the Highlight Yellow graphic.
- Do not use data colors outside charts and graphs.
- Do not use a color other than Highlight Yellow in the Highlight Yellow graphic.
- Do not use general brand colors for data visualizations when shape or size is necessary for comprehension; use the approved data-visualization palette instead.
- Do not create data-visualization graphics without Grounded Blue strokes and text.
- Do not separate chart bars or pie segments with gaps.
- Do not replace direct descriptive labels and leader lines with a legend when the labels are needed to explain the data points.

## 6. Tables

Use tables when people need to scan and compare aligned information.

### Table anatomy

- **Header row:** column labels and hierarchy.
- **Body rows:** comparable values aligned by column.
- **Dividers:** separate rows without heavy boxes.
- **Theme accent:** communicates context and emphasis.

### Theme selection

| Theme | Apply when | Construction direction |
| --- | --- | --- |
| Light | The table sits on a neutral surface | Use a light, neutral treatment with clear row dividers |
| Dark | The table belongs to a Grounded Blue experience | Use the dark Grounded Blue treatment with sufficient contrast for text and dividers |
| Primary | The header needs strong emphasis | Use the strong primary accent for the header treatment |
| Secondary | The table is a quieter supporting element | Use the secondary accent with the lighter supporting surface |

Keep column labels concise and align similar data consistently. The desktop reference is a construction example, not a mandatory display width. Adapt the table to its container while preserving its hierarchy, spacing, proportions, and approved color application.

Sorting, pagination, mobile layouts, selected states, and error states require separate patterns; do not invent those states from the static table reference.

### HTML/CSS application pattern

Keep the table content semantic and apply the theme through a class on the table or its wrapper:

```html
<table class="dv-table dv-table--light">
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Category</th>
      <th scope="col">Status</th>
      <th scope="col">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Item name</td>
      <td>Category</td>
      <td>Active</td>
      <td>$0</td>
    </tr>
  </tbody>
</table>
```

```css
.dv-table {
  width: 100%;
  border-collapse: collapse;
}

.dv-table th,
.dv-table td {
  text-align: left;
  border-bottom: 1px solid var(--dv-table-divider);
}

.dv-table th {
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.dv-table--light {
  color: var(--dv-grounded-blue);
  background: #fff;
}

.dv-table--dark {
  color: #fff;
  background: var(--dv-grounded-blue);
}

.dv-table--primary {
  color: var(--dv-grounded-blue);
  background: #fff;
  border-top: 4px solid var(--dv-table-primary-accent);
}

.dv-table--primary th {
  color: #fff;
  background: var(--dv-table-primary-accent);
}

.dv-table--secondary {
  color: var(--dv-grounded-blue);
  background: var(--dv-table-secondary-surface);
  border-top: 4px solid var(--dv-table-secondary-accent);
}
```

The example uses existing approved tokens and demonstrates the reference's hierarchy. Match the site's established spacing and proportions rather than copying the desktop image's pixel dimensions.

## 7. Final implementation check

- [ ] The visual has been assigned to categorical, KPI, or deemphasis use.
- [ ] Only the assigned palette is used.
- [ ] Categorical colors follow the approved sequence, starting at any color if needed.
- [ ] Grounded Blue is used for strokes and text where required.
- [ ] Bars and pie segments are not separated.
- [ ] Descriptive labels point directly to their data points.
- [ ] Leader lines use the 1px-over-4px white two-stroke treatment.
- [ ] Data colors appear only in charts and graphs.
- [ ] Highlight Yellow is restricted to the Highlight Yellow graphic.
- [ ] Table structure has a clear header row, aligned body rows, light dividers, and an intentional theme accent.
- [ ] Table theme matches the context: Light, Dark, Primary, or Secondary.
- [ ] No unsupported sorting, pagination, mobile, selected, or error pattern has been inferred from the static references.
