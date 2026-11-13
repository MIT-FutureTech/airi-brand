# AIRI styles for Google Docs

Google Docs has no theme colours. The look lives in the named styles, so set
them once in a template document and start new documents from a copy of it.

## Set the named styles

For each row: format one paragraph as shown, then Format > Paragraph styles >
(style name) > "Update to match". When all are done, Format > Paragraph styles >
Options > "Save as my default styles" if you want them in your own new documents.

| Style | Font | Size | Colour |
|---|---|---|---|
| Title | Figtree Bold | 24 pt | `#A32035` |
| Subtitle | Figtree Regular | 14 pt | `#666666` |
| Heading 1 | Figtree Bold | 18 pt | `#A32035` |
| Heading 2 | Figtree Bold | 14 pt | `#1A1A1A` |
| Heading 3 | Figtree Bold | 12 pt | `#1A1A1A` |
| Normal text | Figtree Regular | 11 pt, line spacing 1.15 | `#1A1A1A` |
| Notes and captions (use Normal text) | Figtree Regular | 9 pt | `#666666` |

Only the Title and Heading 1 are red. Heading 2 and below are near-black, so
there is never a reason to pick a second red.

## Links

Docs colours links one by one. Set each link to `#A32035` and keep the underline.
Pasting text with "Paste without formatting" keeps the template's styles.

## Page furniture

- Header: a full-width bar in `#A32035`, 7 pt tall, at the top edge. The AIRI logo
  (`logos/initiative/horizontal-on-light.png`) top right, about 2.5 cm wide.
- Footer: site address and contact address in `#666666` at 9 pt, page number on the right,
  and a matching `#A32035` bar at the bottom edge.
- Lead-sentence highlight: `#F8E1E5`. Marked or draft text: `#FFF0B3`.

## Tables and callouts

- Header row: bold on `#F3F3F3`. For a short table, white bold on `#A32035`.
- Body rows alternate white and `#F3F3F3`. Borders `#CCCCCC`, 0.5 pt.
- Callout: a one-cell table filled `#F3F3F3` (or `#FBF3F4` on screen-only documents), no border.

## Colours to paste

Add these under "Custom" in the colour picker:

`#A32035` `#1A1A1A` `#F8E1E5` `#FBF3F4` `#2171B5` `#FFF0B3`

The greys are Google presets, so they can be clicked:
`#666666` (dark gray 3), `#CCCCCC` (gray), `#D9D9D9` (light gray 1), `#F3F3F3` (light gray 3).

## Do not click

- "Dark red berry 1" (`#980000`) or any other red in the toolbar grid.
- The default link blue (`#1155CC`).
- Pure red (`#FF0000`) for emphasis. Emphasis is bold, or bold in `#A32035`.
