# Typography Rules

## Core Font Rule

Use `IBM Plex Sans` for headings, headlines, display type, subheads, large statistics, and eyebrows.

Use `Arial` for paragraphs, navigation, buttons, form labels, captions, and other body or UI copy. Use `Helvetica, sans-serif` only as the body-copy fallback when Arial is unavailable.

## Weights

- Regular: `400`
- Medium: `500`
- Semibold: `600`
- Bold: `700`

## Case and Kerning

- All Caps means text should use uppercase styling.
- Sentence case means natural capitalization; do not force uppercase.
- Kerning percentages are represented as CSS `letter-spacing` values:
  - `0%` = `0em`
  - `5%` = `0.05em`
  - `10%` = `0.10em`

## Website Type Styles

| Style | Font | Weight | Case | Size | Line Height | Kerning |
| --- | --- | --- | --- | ---: | ---: | ---: |
| Display | IBM Plex Sans | Bold | All Caps | `42px` | `120%` | `5%` |
| H1 | IBM Plex Sans | Bold | All Caps | `28px` | `120%` | `5%` |
| H2 | IBM Plex Sans | Bold | All Caps | `24px` | `120%` | `5%` |
| H3 | IBM Plex Sans | Bold | Sentence case | `20px` | `130%` | `0%` |
| Subhead | IBM Plex Sans | Bold | Sentence case | `30px` | `130%` | `0%` |
| P1 | Arial | Regular | Sentence case | `36px` | `130%` | `0%` |
| P2 | Arial | Regular | Sentence case | `18px` | `130%` | `0%` |
| P3 | Arial | Regular | Sentence case | `16px` | `130%` | `0%` |
| P4 | Arial | Regular | Sentence case | `14px` | `130%` | `0%` |
| P5 | Arial | Regular | Sentence case | `11px` | `130%` | `0%` |
| Large Stats | IBM Plex Sans | Medium | Sentence case | `120px` | `130%` | `0%` |
| Global Nav | Arial | Semibold | Sentence case | `16px` | `130%` | `0%` |
| Sub Nav | Arial | Regular | Sentence case | `25px` | `130%` | `0%` |
| Eyebrow | IBM Plex Sans | Bold | All Caps | `15px` | `130%` | `10%` |
| Large Link | IBM Plex Sans | Bold | All Caps | `56px` | `120%` | `0%` |
| Title Link | IBM Plex Sans | Bold | All Caps | `20px` | `120%` | `0%` |
| Title Link 2 | Arial | Bold | Sentence case | `12px` | `130%` | `0%` |

## Extension Guidance

Additional type variants may be created when needed, but they must follow this system:

- Use IBM Plex Sans for heading and display roles.
- Use Arial for body-copy and UI-copy roles.
- Use the approved weights only: Regular, Medium, Semibold, Bold.
- Keep sizes within the documented website range unless a special display use requires review.
- Use `120%` line height for compact display, headline, and link styles.
- Use `130%` line height for sentence-case, body, navigation, stats, and utility styles.
- Use all caps sparingly for display hierarchy, not for long body copy.
- Use `0.05em` or `0.10em` letter spacing only when the corresponding style calls for it.

## LLM Instruction

When generating West Monroe digital assets, use IBM Plex Sans for headings and display roles and Arial for body and UI copy. Match the named style closest to the content's role. Do not invent unrelated typography styles when one of the documented styles can be used.
