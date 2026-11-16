---
name: airi-brand
description: |
  Apply AIRI (MIT AI Risk Initiative) visual branding to generated output.
  Use when creating HTML, React, SVG, CSS, charts, presentations, or any
  visual artifact for AIRI projects. Triggers on mentions of AIRI, AI Risk
  Repository, AI Risk Index, AI Risk Initiative, airisk.mit.edu, or requests
  to style or brand outputs for these projects.
allowed-tools: Read, Glob
---

# AIRI brand skill

Apply this to anything visual made for AIRI: pages, apps, charts, slides, documents, figures. It applies to internal tools and quick prototypes too, not only public work.

## Five rules

1. **One red: `#A32035`.** Take it from the theme, the template or the token. Never retype or approximate it.
2. **Two text colours:** ink `#1A1A1A` and muted `#666666`. White on red or dark.
3. **In data, red is the subject, the finding or more risk.** Grey `#898A8D` is context. Blue `#2171B5` is a neutral amount.
4. **A figure uses a red scale or a red highlight, never both.**
5. **Figtree for all text**, weights 400 and 700 (600 allowed on the web). Sentence case, left-aligned.

## The swatches

| Token | Hex | Use |
|---|---|---|
| `primary` | `#A32035` | Red fills: covers, header bars, buttons, the highlighted series. Red text uses `link` |
| `primary-hover` | `#8A1B2D` | Hover on red buttons and links |
| `primary-dark` | `#5E0E20` | Dark end of red scales, visited links. Never headings |
| `primary-light` | `#D07886` | Red text and links on dark grounds. Never text on light |
| `red-tint` | `#F8E1E5` | Chips, selected rows, highlights |
| `red-wash` | `#FBF3F4` | Faint red surfaces, screen only |
| `text` | `#1A1A1A` | All text by default |
| `text-muted` | `#666666` | The only other text grey |
| `gray` | `#898A8D` | Chart context, icons, control borders. Not text |
| `rule` | `#CCCCCC` | Visible borders, table rules, axis lines |
| `border` | `#D9D9D9` | Hairlines, gridlines |
| `fill` | `#F3F3F3` | Zebra rows, callouts, empty cells |
| `background` | `#FAFAFA` | Page and slide background |
| `blue` | `#2171B5` | The one second colour |

Data palettes:

- Highlight: `#A32035` on `#898A8D`. Two conditions: `#A32035` and `#E29CA8`.
- Severity, 1 to 5, higher is worse: `#E29CA8` `#D07886` `#B8455A` `#A32035` `#5E0E20`. None: `#F3F3F3`. Labels: ink on steps 1 and 2, white on steps 3 to 5.
- Counts (more is only more): `#EFF6FF` `#C6DBEF` `#9ECAE1` `#6BAED6` `#4292C6` `#2171B5` `#084594`. Labels: ink on steps 1 to 5, white on steps 6 and 7.
- Two-sided: `#084594` `#4292C6` `#9ECAE1` `#F3F3F3` `#E29CA8` `#B8455A` `#5E0E20`. Red is the worse side.
- Categories, in fixed order, never red: `#2171B5` `#6BAED6` `#55399E` `#CC6699` `#D4762C` `#D9A531` `#117A66`, then Other `#898A8D`. The seven AI Risk Repository domains take these slots in order. Labels on the fills: white on blue, violet and teal; ink on sky, pink, orange and gold.
- Status, always with a word or icon: good `#3A8F5C`, partial `#E8A317`, poor `#A32035`.

## What to read

1. This file is enough for a simple page or chart.
2. [BRAND.md](BRAND.md) for the full spec: text pairs and contrast, category text and tint pairs, dark mode, type scales, logo rules, a section for each medium (slides, documents, website, interactive tools, papers, Claude artifacts), and motion and video.
3. [tokens.json](tokens.json) for every value in machine-readable form.
4. [templates/](templates/README.md) for a starting file per tool. Use the template instead of typing values:

| Making | Start from |
|---|---|
| A web page or app | `brand.css` |
| A Claude artifact or single-file page | `templates/claude-artifact.html` (light and dark) |
| Tailwind | `templates/tailwind-theme.css` |
| matplotlib | `templates/airi.mplstyle` and `templates/airi_mpl.py` |
| Plotly | `templates/airi-plotly-template.json` |
| R / ggplot2 | `templates/airi_palette.R` |
| LaTeX | `templates/airi-colors.sty` |
| PowerPoint or Word | `templates/office-theme-colors.xml`, `office-theme-fonts.xml`, `office-theme.md` |
| Google Slides or Sheets | `templates/google-slides-theme.md` |
| Google Docs | `templates/google-docs-styles.md` |
| An explainer video or animation | `templates/video/` |

## Rules

1. Every colour in the output is a token. If you need a colour that is not in `tokens.json`, stop and ask; do not invent one, and do not borrow from a chart library or CSS framework.
2. In CSS, use the variables, not hex values. Artifacts must work in light and dark; the artifact template handles both.
3. Text is `text` or `text-muted`. Never use `gray` or anything lighter for text.
4. **Red text is `link`, red fills are `primary`.** Use `link` for red headings, chip text, secondary-button text and borders, numerals and the current navigation item. `link` lightens in dark mode; `primary` as text is unreadable there.
5. Red goes on the top-level title (`h1`, slide title, document Title and Heading 1), links, buttons and bars. Headings below that are ink.
6. Links are red and underlined. Focus ring is 2 px red; never remove outlines.
7. Charts: decide what the chart is about and make that red; make the rest grey. Use the red scale only when more means more risk, blue when it is only more. Named groups use the category colours, never red. No red-to-green, traffic lights or rainbows. Title states the finding; add a source line.
8. A label on a coloured fill uses the colour the spec gives for that fill (in CSS, `--color-cat-N-label`). Do not guess white.
9. Charts made in Google Sheets, Slides, PowerPoint or Excel start red, blue, gold, teal by default. Keep that only for one or two series. Set context grey and category colours by hex (BRAND.md section 5).
10. Status colours always carry a word or an icon.
11. Slides: red titles that state the point, full-red section dividers, five sizes (72, 56, 36, 28, 22 px on a 1920 canvas), gaps of 8, 16, 24 or 48 px, a source line on data slides, no logo on body slides.
12. Radius is 8 px for cards and images and 4 px otherwise. No pill-shaped buttons or chips. Prefer borders to shadows.
13. Logos: use the files in `logos/initiative/` as they are (`on-light`, `on-dark`, `on-red`). One logo for all AIRI work. No product lockups, no recolouring. `logos/futuretech/` is the parent logo, for co-branded work only.
14. AIRI red is not MIT red (`#750014`) and not FutureTech's logo red (`#9A2030`). Do not use either as a colour.
15. Fewer colours is better. Red, grey, ink and white are enough for most work.

## Motion and video

- Interface motion: the `--motion-` durations (70 to 700 ms) and `--ease-` curves in `brand.css`; `transform` and `opacity` only; honour `prefers-reduced-motion`.
- Video motion: 400, 700 or 1000 ms with the video curves; frame, then text, then data; stagger 80 to 150 ms; about three brand moments a video.
- Never: bounce, elastic, overshoot, rotation, glitch, software presets, diagonal moves, or a logo that fades, slides or scales in.
- Start videos from `templates/video/` (it sits on the `generate-video` template). Every video has captions, an SRT file and an end card.
- Run `python3 templates/video/check_video.py comp.html captions.srt` before rendering. Detail: BRAND.md section 11.
