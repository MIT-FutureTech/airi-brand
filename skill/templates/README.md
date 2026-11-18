# Templates

Ready-made files that already hold the AIRI colours and fonts, one per tool.
Start from these instead of typing hex values. All are generated from
`../tokens.json`, so they always match the spec in `../BRAND.md`.

| For | File | How to use |
|---|---|---|
| PowerPoint, Word, Excel | `office-theme-colors.xml`, `office-theme-fonts.xml`, `office-theme.md` | Copy the two XML files into Office's theme folders; "AIRI" then appears under Colors and Fonts. Steps and Word styles are in the .md |
| Google Slides, Sheets | `google-slides-theme.md` | Hex per theme slot, by hand or as one API request |
| Google Docs | `google-docs-styles.md` | Named styles, page furniture, colours to paste |
| Websites and apps | `../brand.css` | Import it, or copy the variables |
| Tailwind | `tailwind-theme.css` | Paste after `@import "tailwindcss"` |
| Apps using short names | `short-aliases.css` | Maps `--ink`, `--muted`, `--rule` and friends onto the kit tokens |
| Claude artifacts, single-file pages | `claude-artifact.html` | Paste the `<link>` and `<style>`; light and dark |
| matplotlib | `airi.mplstyle`, `airi_mpl.py` | `import airi_mpl; plt.style.use(airi_mpl.STYLE)` |
| Plotly | `airi-plotly-template.json` | See below |
| R, ggplot2 | `airi_palette.R` | `source("airi_palette.R")`, then `airi$...`, `airi_ramp()`, `theme_airi()` |
| LaTeX | `airi-colors.sty` | `\usepackage{airi-colors}` |
| Explainer videos, animation | `video/` | Sits on the `generate-video` template; see `video/README.md` |

## Chart defaults

The default colour order in the chart templates is red, grey, ink, then the
category colours. That makes a one- or two-series chart read as "the
subject, and everything else" without any work. Bars that compare groups
stay one colour. For named categories, switch
to the category colours (`airi_mpl.use_categorical()`, `airi$categorical`, or
the `cat` values in `tokens.json`). Categories never use red.

Office, Google Slides and Google Sheets are different: their charts take the
theme accents in order (red, grey, ink, blue, sky, violet). That suits a chart
of one to three series. `office-theme.md` and `google-slides-theme.md`
list what to set by hand.

The default colour scale for heatmaps is blue, because blue means "more" and
nothing else. Use the red scale only when more means more risk.

## Plotly

```python
import json, plotly.io as pio, plotly.graph_objects as go
pio.templates["airi"] = go.layout.Template(json.load(open("airi-plotly-template.json")))
pio.templates.default = "airi"

AIRI_RED_SCALE = ["#FBF3F4", "#E29CA8", "#D07886", "#B8455A", "#A32035", "#5E0E20"]       # more means more risk
AIRI_SEVERITY = ["#E29CA8", "#D07886", "#B8455A", "#A32035", "#5E0E20"]              # ordered levels 1 to 5
AIRI_CATEGORIES = ["#2C6395", "#7DC1E3", "#443471", "#B973AB", "#ECBA7B", "#8F8D44", "#2A9484", "#ACC6B1", "#898A8D"]
fig.update_traces(colorscale=AIRI_RED_SCALE)       # on a heatmap
fig.update_layout(colorway=AIRI_CATEGORIES)        # named categories
```

## Regenerating

Edit `skill/tokens.json`, then run `python3 dev/build-kit/build.py` from the
repository root. `--check` verifies that nothing is out of date.
