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

Apply this to anything visual made for AIRI, internal or public. The kit is a starting point: a few hard rules, then defaults a person can change.

## Hard rules

Always follow these. People should too.

1. Use the logo files as they are: never redrawn, recoloured, stretched or merged with another mark. There is one AIRI logo for all products. (It must look the same everywhere.)
2. AIRI red is `#A32035`, taken from the theme, the template or the token. Never approximate it, and never add a red from outside the kit. (Near-reds are the most common drift.)
3. Figtree for all text, with the fallback stack Figtree, Arial, sans-serif. Code may use the monospace stack. (One typeface ties the products together.)
4. Text meets WCAG AA contrast: 4.5 to 1, or 3 to 1 for large text. (People must be able to read it.)
5. Colour never carries meaning alone. A status colour comes with a word or an icon. (Some readers cannot tell colours apart.)
6. In data, red never means good, and a red scale never shows a neutral amount. (Everywhere else in AIRI work red means risk.)
7. Nothing flashes more than three times a second, and every video has captions. (Flashing can trigger seizures, and many people watch without sound.)

In partner-led work the partner's template sets colour and type; rule 1 still holds.

## Defaults

Everything else in the kit is a default. Follow it unless a person asks for something different. You do not decide when to stray; a person does.

When a person asks, do it. Do not argue, ask for a reason, or quietly put the default back later. If the request breaks a hard rule, say which one in a line and offer the closest option that keeps it.

## When the kit says nothing

1. Reuse the closest pattern the kit already has. Look in `templates/`, BRAND.md sections 9 and 10, and the visual guide.
2. If nothing is close, choose the most neutral option: ink and greys, Figtree regular, the default spacing, no new colour. Never invent a new creative treatment.
3. In your handback, say which gap you hit and what you reused, so it can be added to the kit.

## The swatches

| Token | Hex | Use |
|---|---|---|
| `primary` | `#A32035` | Red fills: covers, header bars, buttons, the highlighted series. Red text uses `link`, which lightens in dark mode |
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
- Categories, in fixed order, never red: `#2171B5` `#6BAED6` `#55399E` `#CC6699` `#D4762C` `#D9A531` `#117A66`, then Other `#898A8D`. The seven AI Risk Repository domains take these slots in order, in new work only; leave existing work as it is. Labels on the fills (`--color-cat-N-label`): white on blue, violet and teal; ink on sky, pink, orange and gold.
- Status: good `#3A8F5C`, partial `#E8A317`, poor `#A32035`.

## What to read

This file is enough for a simple page or chart. [BRAND.md](BRAND.md) is the full spec, with a section per medium and a list of what is still open. [tokens.json](tokens.json) has every value. [templates/](templates/README.md) has a starting file per tool; use it instead of typing values:

| Making | Start from |
|---|---|
| Web page or app | `brand.css` |
| Claude artifact or single-file page | `templates/claude-artifact.html` |
| Tailwind | `templates/tailwind-theme.css` |
| matplotlib | `templates/airi.mplstyle`, `templates/airi_mpl.py` |
| Plotly | `templates/airi-plotly-template.json` |
| R / ggplot2 | `templates/airi_palette.R` |
| LaTeX | `templates/airi-colors.sty` |
| PowerPoint or Word | `templates/office-theme.md` and the two XML files beside it |
| Google Slides, Sheets, Docs | `templates/google-slides-theme.md`, `templates/google-docs-styles.md` |
| Video | `templates/video/` |

## Defaults to know

- Every colour is a token; in CSS use the variables. Artifacts work in light and dark.
- Red goes on the top-level title (`h1`, slide title, document Title and Heading 1), links, buttons and bars. Lower headings are ink.
- Links are red and underlined. Focus ring 2 px red.
- Weights 400 and 700 (600 on the web). Sentence case, left-aligned.
- Radius 8 px for cards and images, 4 px otherwise. No pill shapes. Borders before shadows.
- Charts: red is the subject, the finding or more risk; grey is context; blue is a neutral amount. A red scale or a red highlight, not both. No red-to-green, traffic lights or rainbows. The title states the finding; add a source line.
- Charts in Google or Office tools: set series colours by hex (BRAND.md section 5).
- Slides: red titles that state the point, full-red section slides, sizes 72, 56, 36, 28, 22 px on a 1920 canvas, gaps of 8, 16, 24 or 48 px, no logo on body slides.
- Logos: `logos/initiative/`. `logos/futuretech/` is the parent logo, for co-branded work only.

## Motion and video

- Interface: the `--motion-` durations (70 to 700 ms) and `--ease-` curves in `brand.css`; `transform` and `opacity` only; honour `prefers-reduced-motion`.
- Video: 400, 700 or 1000 ms; frame, then text, then data.
- Transitions are conventional: no bounce, elastic, overshoot, rotation, glitch, presets or diagonal moves.
- The logo cuts in or builds from its squares (timing being finalised; use the template's). Fading, sliding or zooming it breaks rule 1.
- Start from `templates/video/`. Under a minute, an SRT file, an end card, no music unless asked.
- Before rendering, run `python3 templates/video/check_video.py comp.html captions.srt`. It fails on hard rules and broken files, and warns on defaults. Detail: BRAND.md section 11.
