# AIRI brand specification

Version 2.0. The visual identity of the MIT AI Risk Initiative (AIRI), for every medium: slides, documents, the website, interactive tools, charts, papers and anything Claude generates.

Values in this file match `tokens.json` exactly. `brand.css` and the files in `templates/` are generated from `tokens.json`. If you are applying the brand in a tool, start from the template for that tool (section 10) instead of typing values.

## 1. What AIRI looks like

Five things make a piece of work look like AIRI.

1. **Red is structure.** One red, used for the things that frame the work: titles, covers, section dividers, header bars, buttons, links.
2. **Figtree everywhere.** One typeface, left-aligned, sentence case.
3. **Restraint in data.** Red marks the one thing a chart is about. Grey is everything else.
4. **Light grounds.** White or near-white pages, near-black text, few rules.
5. **Titles state the point.** Every data slide and figure names its source.

The best AIRI work uses the fewest colours. A deck that uses red, grey and near-black looks better than one that uses twenty.

## 2. Five rules to remember

1. **One red: `#A32035`.** Take it from the theme, the template or the token. Never retype or approximate it.
2. **Two text colours:** ink `#1A1A1A` and muted `#666666`. White on red or dark.
3. **In data, red is the subject, the finding or more risk.** Grey `#898A8D` is context. Blue `#2171B5` is a neutral amount.
4. **A figure uses a red scale or a red highlight, never both.**
5. **Figtree for all text**, weights 400 and 700 (600 allowed on the web). Sentence case, left-aligned.

## 3. Colour

### Core

| Token | Hex | Use |
|---|---|---|
| `primary` | `#A32035` | AIRI red. Logo, slide titles, document Title and Heading 1, covers, dividers, header bars, buttons, links, list markers, the one highlighted series in a chart |
| `primary-hover` | `#8A1B2D` | Hover and pressed states on red buttons and links. Not a data colour |
| `primary-dark` | `#5E0E20` | Dark end of red scales, visited links. Never headings (it reads brown at size) |
| `primary-light` | `#D07886` | Red text, links and focus ring on dark grounds. Never text on light grounds |
| `red-500` | `#B8455A` | Middle step of red scales; gradient stop on covers and heroes |
| `red-300` | `#E29CA8` | Lightest step of red scales; the pale partner bar beside red. Fill only |
| `red-tint` | `#F8E1E5` | Chips, selected rows, lead-sentence highlight. The palest red that survives printing |
| `red-wash` | `#FBF3F4` | Faint red surface for callouts and cards. Screen only |
| `blue` | `#2171B5` | The one second colour: a comparison series, neutral amounts, the cool end of two-sided scales. Not for links |
| `blue-dark` | `#084594` | Text on blue tints; dark end of the blue scale |
| `blue-tint` | `#DCE9F4` | Group-header bands in tables, info backgrounds |
| `highlight` | `#FFF0B3` | Marked passages, search hits, draft or AI-written text |

### Neutrals

| Token | Hex | Use |
|---|---|---|
| `text` | `#1A1A1A` | Ink. All text by default, and every heading below the top level. Also the dark band on the website |
| `text-muted` | `#666666` | The only other text grey: captions, metadata, source lines, axis labels, footers |
| `gray` | `#898A8D` | Graphics only: the context series in charts, icons, control borders. Fails contrast as text |
| `rule` | `#CCCCCC` | Visible borders: card outlines on slides, table rules, axis lines |
| `border` | `#D9D9D9` | Hairlines: gridlines, card borders on the web, uncertainty bands |
| `fill` | `#F3F3F3` | Zebra rows, callout boxes, empty cells, the midpoint of two-sided scales |
| `background` | `#FAFAFA` | Page and slide background |
| `surface` | `#FFFFFF` | Cards, panels, chart backgrounds, document pages |
| `white` | `#FFFFFF` | Text and logo on red or dark |

Pure black text in an office document is tolerated; nobody can see the difference. Templates set `#1A1A1A`.

There is no third text grey. If text matters, it is ink. If it is secondary, it is muted.

Four neutrals are Google presets, so they can be clicked in Docs, Slides and Sheets: `text-muted` is "dark gray 3", `rule` is "gray", `border` is "light gray 1" and `fill` is "light gray 3". Ink, `gray` and `background` are custom colours; take them from the theme or the template. Google's preset named "gray" is `#CCCCCC`, the kit's `rule`. It is not the kit's `gray`, the chart grey.

### Text and background pairs

Use only these pairs for text. Ratios are WCAG contrast; 4.5 is the minimum for body text.

| Text | On | Ratio |
|---|---|---|
| ink `#1A1A1A` | white, background, fill, red-tint | 17.4, 16.7, 15.7, 14.0 |
| muted `#666666` | white, background, fill, red-tint, blue-tint, highlight | 5.7, 5.5, 5.2, 4.6, 4.7, 5.0 |
| red `#A32035` | white, background, fill, red-tint | 7.5, 7.2, 6.7, 6.0 |
| white | primary, primary-hover, primary-dark, red-500, blue | 7.5, 9.2, 13.5, 5.2, 5.1 |
| ink | red-300, primary-light | 7.9, 5.6 |
| blue-dark `#084594` | white, blue-tint | 9.2, 7.4 |

Pairs that fail, and what to do instead:

- Gray `#898A8D` as text (3.5 on white). Use muted.
- Red `#A32035` as text on dark `#1A1A1A` (2.3). Use `#D07886` (5.6); the `link` token makes this switch by itself. A red button with white text on dark is fine.
- White text on `#D07886` or `#E29CA8`. Label those fills in ink.

### Links and emphasis

- **Red text is the `link` token. Red fills are `primary`.** The two are the same red on light grounds. In dark mode `link` lightens to `#D07886` and `primary` stays put, so red text set in `primary` becomes unreadable (2.1 on a dark card). Use `link` for every piece of red text: links, red headings, chip text, secondary-button text, numerals.
- Links are `#A32035` and underlined, in every medium. Hover `#8A1B2D`. Visited `#5E0E20`.
- One exception, for PDFs set in LaTeX: links are coloured and not underlined. Web addresses are `#A32035`; cross-references and citations stay ink. `airi-colors.sty` sets this.
- Emphasis is bold. Stronger emphasis, and "the ask" in a document, is bold in `#A32035`. Never pure red.
- Focus ring: 2 px solid `#A32035` (`#D07886` on dark). Never remove the outline.

### Status

Status always carries a word or an icon, never colour alone.

| Meaning | Mark | Text | Tint |
|---|---|---|---|
| Good, yes, pass | `#3A8F5C` | `#17653C` | `#E3F1EA` |
| Partial, gap, warning | `#E8A317` | `#8A5A18` | `#FCF3E3` |
| Poor, no, error | `#A32035` | `#A32035` | `#F8E1E5` |
| Info | `#2171B5` | `#084594` | `#DCE9F4` |
| None, not applicable, no data | `#D9D9D9` | `#666666` | `#F3F3F3` |

There is no separate error red. Amber is a mark, not a text colour: put ink on it, or use `#8A5A18` for amber text. Uncertain or to-be-confirmed keeps its status colour and adds a dashed ink outline.

**Grade variant.** A dense Yes / Partial / No matrix that sits under a red header may use no red and no green:

| Grade | Fill | Border | Text |
|---|---|---|---|
| Yes | `#FFFFFF` | `#CCCCCC` | ink |
| Partial | `#FCF3E3` | `#E8A317` | ink, bold |
| No | `#8A5A18` | `#8A5A18` | white, bold |

Amber then means a gap and nothing else. Use one variant per product, with the same words everywhere.

### Dark mode

For Claude artifacts and dark tools. These values are computed and contrast-checked but new; treat them as provisional.

| Token | Dark value | Note |
|---|---|---|
| `background` | `#1A1A1A` | Page |
| `surface`, `fill` | `#242424` | Cards and panels |
| `border`, `rule` | `#3A3A3A` | Hairlines |
| `gray` | `#6E6E6E` | Context series, control borders |
| `text-muted` | `#A6A6A6` | 7.2 on the page |
| `text` | `#F2F2F2` | 15.6 on the page |
| `link`, `focus` | `#D07886` | Red text and links; hover `#E29CA8` |
| `red-tint`, `red-wash` | `#431C22`, `#2A1B1D` | |
| `blue-tint`, `info-ink` | `#1C3245`, `#6BAED6` | |
| `good-tint`, `good-ink` | `#22362A`, `#89BC9D` | |
| `partial-tint`, `partial-ink` | `#433519`, `#E8A317` | |

- Red fills stay `#A32035` with white text. Red text is `link`, never `primary`.
- Category violet becomes `#9875DA`, and its label switches from white to ink (4.9; white would be 3.6).
- Label colours on fills are fixed: "ink" on a fill means `#1A1A1A` in both themes. Only violet changes, as above.
- Give any dark mark that fades into the page a 1 px `#6E6E6E` outline: the darkest scale steps, and category teal on a dark card (3.0).

## 4. Colour in data

One rule decides most charts: **red is the subject, grey is context, blue is a neutral amount.**

### Which palette

| The data shows | Use | Values |
|---|---|---|
| One thing that matters, against everything else | Highlight | `#A32035` on `#898A8D` |
| Two conditions that are both the subject | Pair | `#A32035` and `#E29CA8`, values labelled on the bars |
| Ordered levels where higher is worse (severity, vulnerability, likelihood) | Severity | 5 red steps |
| A continuous amount of risk | Red scale | 6 stops |
| Counts, coverage, anything where more is only more | Blue scale | 7 steps |
| Two directions from a real midpoint (agree and disagree, above and below) | Two-sided | Blue, grey, red |
| Named groups with no order | Categories | 7 slots and Other |

### Highlight and pair

- The default chart is one series in `#A32035` and everything else in `#898A8D`.
- Uncertainty bands and reference ranges are `#D9D9D9`.
- For a second subject of equal weight, add `#2171B5`.

### Categories

For named groups: risk domains, sectors, roles, laws. The slot order is fixed. Take slots in order from 1; three groups are blue, violet and teal when they need to be far apart.

| Slot | Name | Fill | Text | Tint | Label on fill | AI Risk Repository domain |
|---|---|---|---|---|---|---|
| 1 | Blue | `#2171B5` | `#084594` | `#E0EBF5` | white | Discrimination & toxicity |
| 2 | Sky | `#6BAED6` | `#084594` | `#EAF4F9` | ink | Privacy & security |
| 3 | Violet | `#55399E` | `#55399E` | `#E7E3F1` | white | Misinformation |
| 4 | Pink | `#CC6699` | `#A3446F` | `#F8EAF1` | ink | Malicious actors & misuse |
| 5 | Orange | `#D4762C` | `#A54A0C` | `#F9ECE1` | ink | Human-computer interaction |
| 6 | Gold | `#D9A531` | `#7F5D00` | `#FAF2E2` | ink | Socioeconomic & environmental |
| 7 | Teal | `#117A66` | `#0B6655` | `#DEEFEB` | white | AI system safety, failures & limitations |
| | Other | `#898A8D` | `#666666` | `#F3F3F3` | ink | Other, folded groups, context |

- **Red is never a category.** That keeps red free to pick out one category: grey the others when you do.
- A chip or tag uses the tint as background and the text colour on it. Every pair passes contrast.
- An eighth category folds into Other. Never cycle the slots.
- New work uses the slot shown for each of the seven risk domains. Existing pages, tools and decks keep their current colours until a decision is made.
- The label on each fill is the colour in the table, at any size. Every one is at least 4.9:1. Never put white on sky, pink, orange or gold.
- Sky and gold are faint as thin marks on white. Label them directly or give them an outline.
- More than three lines or scatter series need direct labels or small multiples.
- In print the seven hues are close in lightness. Domain figures in papers need direct labels.

### Severity (5 ordered levels, higher is worse)

| 1 | 2 | 3 | 4 | 5 | None or not rated |
|---|---|---|---|---|---|
| `#E29CA8` | `#D07886` | `#B8455A` | `#A32035` | `#5E0E20` | `#F3F3F3` |

Labels: ink on steps 1 and 2, white on steps 3 to 5. The scale stays ordered in greyscale. A 1 to 5 rating is ordered, so it takes this scale, not the two-sided one.

### Red scale (continuous risk)

Stops: `#FBF3F4` `#E29CA8` `#D07886` `#B8455A` `#A32035` `#5E0E20`. Interpolate between the stops. Never switch to a library's own red ramp. Labels are ink on anything lighter than `#B8455A` and white from there on.

### Blue scale (counts and coverage)

Stops: `#EFF6FF` `#C6DBEF` `#9ECAE1` `#6BAED6` `#4292C6` `#2171B5` `#084594`. Labels: ink on steps 1 to 5, white on steps 6 and 7. White on step 5 `#4292C6` fails (3.4); ink on it passes (5.1). Five ordered steps: the last five, with ink on the first three.

### Two-sided scale

Seven steps: `#084594` `#4292C6` `#9ECAE1` `#F3F3F3` `#E29CA8` `#B8455A` `#5E0E20`. Five steps for small tables: `#2171B5` `#9ECAE1` `#F3F3F3` `#E29CA8` `#A32035`.

Red is the riskier or worse side. The midpoint is grey, never yellow. Labels on the seven steps: white on step 1, ink on steps 2 to 5, white on steps 6 and 7. On the five steps: white on step 1, ink on steps 2 to 4, white on step 5. Label the two palest steps directly; they are hard to tell apart for some colour-blind readers.

### Chart furniture

| Part | Value |
|---|---|
| Titles and data labels | `#1A1A1A` |
| Axis labels, tick labels, legend, source line | `#666666` |
| Axis lines | `#CCCCCC` |
| Gridlines, uncertainty bands | `#D9D9D9` |
| Background | `#FFFFFF` |
| No data | `#F3F3F3` |

### Rules for charts

- If more means more risk, use red. If it is only more, use blue.
- A figure with a red scale cannot also highlight in red. Highlight with an ink outline or an ink annotation.
- The title states the finding. A source line sits under every chart.
- Label directly where you can. Use a legend only when you cannot.
- No traffic-light scales, no rainbow scales, no red-to-green.

## 5. Theme slots

PowerPoint, Word and Google Slides share the same 12 theme slots. Filling them is what keeps a file on brand: default charts start with AIRI red and links come out red.

| Slot | Hex | Slot | Hex |
|---|---|---|---|
| Dark 1 (text) | `#1A1A1A` | Accent 1 | `#A32035` |
| Light 1 (background) | `#FFFFFF` | Accent 2 | `#2171B5` |
| Dark 2 | `#666666` | Accent 3 | `#D9A531` |
| Light 2 | `#F3F3F3` | Accent 4 | `#117A66` |
| Hyperlink | `#A32035` | Accent 5 | `#CC6699` |
| Followed hyperlink | `#5E0E20` | Accent 6 | `#6BAED6` |

Office builds lighter and darker rows from each accent. Those are not AIRI tints; use the values in section 3. The colours worth keeping as custom swatches are listed in `tokens.json` under `theme.custom-swatches`: the red steps, the neutrals, the remaining category colours, the status marks and the blue-scale steps, so a heat map built from table cells needs no typing.

### Charts in Slides, Sheets and Office

A chart made in Google Sheets, Google Slides, PowerPoint, Word or Excel takes its series colours from Accent 1 to 6 in order: red, blue, gold, teal, pink, sky. That order is right for one kind of chart only: one series (red), or two series (red and blue). For every other chart, set the colours by hand.

- **Context series:** `#898A8D`. It is not a theme colour, so it is never the default.
- **Named groups:** set each series to its category colour, in slot order. The first group is blue. Left alone, the tool makes the first group red, which the kit forbids, and puts every risk domain on the wrong colour.

| Slot | Colour | Hex | AI Risk Repository domain |
|---|---|---|---|
| 1 | Blue | `#2171B5` | Discrimination & toxicity |
| 2 | Sky | `#6BAED6` | Privacy & security |
| 3 | Violet | `#55399E` | Misinformation |
| 4 | Pink | `#CC6699` | Malicious actors & misuse |
| 5 | Orange | `#D4762C` | Human-computer interaction |
| 6 | Gold | `#D9A531` | Socioeconomic & environmental |
| 7 | Teal | `#117A66` | AI system safety, failures & limitations |

- **Scales:** the severity, blue and two-sided values in section 4, set per series or per cell.

The code templates (matplotlib, Plotly, R) default to red, grey, blue. A chart made in an office tool matches them only after the grey and the category colours are set as above. A chart pasted in as an image from a code template needs none of this.

## 6. Typography

Figtree, from Google Fonts, for everything. Fallback: Arial, then the system sans-serif. Monospace is the system stack (`ui-monospace, SFMono-Regular, Menlo, monospace`); there is no brand mono face.

- Left-aligned. Centre only short labels and hero lines.
- Sentence case. No all-caps and no letter-spacing in slides and documents.
- Weights: 400 and 700 in slides, documents and figures. The web and apps may also use 600. No 500.
- Line height 1.5 for body and 1.25 for headings.

| Medium | Sizes |
|---|---|
| Web and apps (px) | 12, 14, 16, 20, 26, 34; one hero size of 44 |
| Slides on a 1920 x 1080 canvas (px) | Cover 72, title 56, outcome 36, body 28, small 22 |
| Slides on a 960 x 540 pt page (pt) | Cover 36, title 28, outcome 18, body 14, small 11 |
| Documents (pt) | Title 24, Heading 1 18, Heading 2 14, Heading 3 12, body 11, notes and captions 9 |
| Print figures at final size (pt) | Panel title 9.5, labels 8, smallest values 7 |

Slides never go below the small size, except one verbatim legal or source passage per slide, which may be 20 px (10 pt). On Google's default 720 x 405 pt page, multiply the 960 pt sizes by 0.75.

Where red goes in type: slide titles, the document Title and Heading 1, and the page `h1` on the web. Every heading below that is ink.

## 7. Spacing, radius and layout

- Spacing steps: 4, 8, 16, 24, 32, 48, 64 px (`--space-1` to `--space-7`). Slides use only 8, 16, 24 and 48.
- Radius: 8 px for cards, panels and images; 4 px for everything else. No pill-shaped buttons, chips or tags. A status dot or an avatar may be a circle.
- Borders are 1 px on the web and 2 px on a 1920 px slide canvas.
- On a 960 x 540 pt slide page, halve every 1920 px value and read it as points: gaps of 4, 8, 12 and 24 pt, borders 1 pt, radius 4 pt for cards and images and 2 pt otherwise.
- Shadows are rare. Prefer a border.
- A rule sits above the block it introduces, never under a heading.

## 8. Logo

There is one AIRI logo: the icon beside the two-line wordmark "MIT AI Risk / Initiative". Use it for all AIRI work, including the AI Risk Repository and the AI Risk Index. Those products have no lockups of their own.

```
logos/
  initiative/
    icon.*  icon-on-light.*      red, transparent background
    icon-on-dark.*               white, transparent background
    icon-on-red.*                white on #A32035
    horizontal.*  horizontal-on-light.*  horizontal-on-dark.*  horizontal-on-red.*
  futuretech/                    MIT FutureTech parent logo, SVG only, same four variants
```

AIRI logos are SVG and PNG. PNG icons are 1024 x 1024; PNG horizontals are 512 px tall. Text is outlined, so the files need no font.

- **Which variant.** Default or `on-light` on white and light grounds. `on-dark` on dark grounds and on photographs. `on-red` where the logo needs its own red block.
- **Clear space.** Keep one large square of the icon free on every side.
- **Smallest size.** Horizontal logo 120 px or 2.5 cm wide. Below that, use the icon alone.
- **Do not** recolour, stretch, rotate, outline or rebuild the logo, add a product name to it, or set the wordmark in type yourself. Use the files.
- **Do not** use the retired Index or Repository lockups, or any older version with a vertical divider.
- The lockup proportions are fixed and generated by `dev/logo-builder/build.py` in the repository.

### Where the logo goes

| Medium | Placement |
|---|---|
| Slides | On the cover: FutureTech bottom left, AIRI bottom right. A closing slide may use the `on-red` logo as a banner. Body slides carry no logo |
| Documents | Horizontal logo top right in the header, about 2.5 cm wide |
| Report covers | White AIRI logo, then white FutureTech logo, top left on `#A32035` |
| Website | Horizontal logo in the navigation, 200 to 250 px wide. Icon only on phones and as the favicon |
| Standalone app | White horizontal logo in a `#A32035` header bar, with the product name in white bold |
| App framed inside the AIRI website | No logo; the site navigation already has one |

### Parent organisation and partners

AIRI sits within MIT FutureTech. The FutureTech logo is included for co-branded work; it is not an AIRI brand element.

- Set the FutureTech logo apart from the AIRI logo at a balanced size. Do not merge them into one mark.
- Report covers carry two logos: AIRI and FutureTech. Do not add a third.
- There are three different reds. AIRI `#A32035`. FutureTech's logo red `#9A2030`. MIT's institutional red `#750014`. The last two stay inside their own logos. AIRI red is not "MIT red".
- In AIRI-led work with a partner, AIRI colours and type win, and the partner's logo sits apart at equal height.
- In partner-led work, the partner's template wins. The AIRI logo appears in its white or on-light version at the same weight as the other marks. Never recolour it to a partner's colour.

## 9. Components

Defaults for the web, apps and artifacts. Token names are the CSS variables in `brand.css` without the `--color-` prefix. Red text is always `link`; `primary` is for fills (section 3).

- **Primary button.** `primary` fill, white text, weight 600, radius 8 px. Hover `primary-hover`.
- **Secondary button.** `surface` fill, 1 px `link` border, `link` text. Hover fill `red-wash`. On a dark band: transparent with a white border and white text.
- **Card.** `surface` on `background`, 1 px `border`, radius 8 px, padding 24 px.
- **Chip or tag.** `red-tint` with `link` text, or a category tint with its text colour. Radius 4 px.
- **Callout.** `fill` or `red-wash`, no border, radius 8 px.
- **Table.** Header row bold ink on `fill`, or white on `primary` for a short table. Rows alternate `surface` and `fill`. Rules `rule`. Group-header band `blue-tint`.
- **Navigation.** `surface` bar, logo left, ink links right. The current page is `link`.
- **Header bar (apps).** `primary` bar, white logo, product name in white bold.
- **Numbered findings.** Every numeral is `link`. Order is carried by the number, not by a colour ramp.
- **Marked text.** `highlight` behind ink.

## 10. By medium

Each medium has a starting file in `templates/` that already holds the values.

### Slides (Google Slides, PowerPoint, Claude slide artifacts)

Templates: `templates/google-slides-theme.md`, `templates/office-theme-colors.xml`, `templates/office-theme-fonts.xml`, `templates/office-theme.md`.

- Page 960 x 540 pt (PowerPoint widescreen), or a 1920 x 1080 px canvas for HTML decks. Background `#FAFAFA`. Fill the theme slots in section 5.
- Margins on the 1920 canvas: 96 px top, 128 px sides, 144 px bottom. Up to four equal columns with a 48 px gap. On the 960 pt page: 48 pt top, 64 pt sides, 72 pt bottom, and a 24 pt column gap.
- **Slide titles are red** (`#A32035`, bold), state the slide's point and make sense read alone. No eyebrow line and no subtitle.
- **Section dividers are full-bleed red** with a white title.
- Body text is ink. Small text, sources and footers are muted.
- The outcome, the one result or decision on the slide, is set at the outcome size, the largest running text below the title. The only thing larger is the number on a stat card, which is itself the outcome of that slide.
- A footer line names the data source on every data slide.
- Only the five sizes in section 6. Only 8, 16, 24 and 48 px gaps. Radius 8 px for cards and screenshots, 4 px otherwise. In points, halve them (section 7).
- Logos on the cover: FutureTech bottom left, AIRI bottom right. Body slides carry no logo.

Layouts to build from:

- **Cover.** Title, one sentence on what the work is, date. Logos as above.
- **Section divider.** `#A32035` full bleed, white title.
- **Title and body.**
- **Main point.** One statement in muted text at the outcome size, with the key words in bold red.
- **Stat cards.** Up to four white cards with a `#CCCCCC` outline. Each has three levels of text: the number, bold red at the cover size; the statement, one line in ink at the body size saying what the number counts; and an optional note in muted small text for the source or the base.
- **Chart.** Highlight on context (section 4), title states the finding, source in the footer. For a chart made in Slides or PowerPoint itself, set the colours as in section 5.
- **Process.** Equal cards left to right, muted arrows between.
- **Closing.** Next steps, and the `on-red` logo as a banner.

Slide components:

- **Card.** White, 2 px `#CCCCCC` border, radius 8 px, padding 24 px, title in bold at body size. One outcome card per slide may take a 3 px ink border.
- **Callout.** A `#F3F3F3` box, no border, radius 8 px, padding 24 px, text in ink at the body size. Slides do not use the red wash: it disappears on projectors and in print. For a stronger callout use the outcome card's ink border.
- **Label.** Small, bold, muted, on its own line above its value.
- **Tag.** Solid ink with white text, or an ink outline; marks a card and sits before its title. For three or more groups use category dots with a legend.
- **Grade chip.** The grade variant in section 3, at body size.
- **List.** Numbers only when order matters; otherwise a small red square marker.
- **Heatmap table.** Cells from the severity, blue or two-sided scale with the label rule for that scale.
- **Screenshot.** The real product, cropped to the part discussed, in a 2 px `#CCCCCC` frame.

Slide copy:

- Outcome first. Reasoning goes in small text or the speaker notes.
- Define each term on first use, and keep one word for each thing.
- Show an excerpt, not a summary of it.
- Name the source of every grouping and number.

Checklist before sharing a deck:

1. Only the five sizes, nothing below small except one legal block.
2. Weights 400 or 700. No all-caps, no letter-spacing.
3. Every colour is a token in this file.
4. Titles are red, stand alone and state the point.
5. Charts follow section 4: one highlight, or one scale, never both.
6. Every data slide names its source.
7. No logo on body slides. No retired lockups.

### Documents (Google Docs, Word)

Templates: `templates/google-docs-styles.md`, `templates/office-theme.md` (Word styles).

| Style | Type | Colour |
|---|---|---|
| Title | Figtree Bold 24 pt | `#A32035` |
| Subtitle | Figtree Regular 14 pt | `#666666` |
| Heading 1 | Figtree Bold 18 pt | `#A32035` |
| Heading 2 | Figtree Bold 14 pt | `#1A1A1A` |
| Heading 3 | Figtree Bold 12 pt | `#1A1A1A` |
| Normal text | Figtree Regular 11 pt, line spacing 1.15 | `#1A1A1A` |
| Notes and captions | Figtree Regular 9 pt | `#666666` |

- Put the look in the named styles, not in hand formatting, so new headings come out right.
- **Page furniture.** A full-width `#A32035` bar, 7 pt tall, at the top and bottom edges. Logo top right, about 2.5 cm wide. Footer in muted 9 pt: site address, contact address, page number.
- **Metadata table** under the title where needed: last update, contact, sharing. 9 pt, bold labels.
- **Lead-sentence highlight** is `#F8E1E5`. Marked or draft text is `#FFF0B3`.
- **Tables and callouts** as in section 9.
- **Flagship covers** follow the report cover in the papers section.
- In Google Docs, never click the toolbar's dark red (`#980000`) or leave the default link blue (`#1155CC`). In Slides, replace the default teal link (`#0097A7`). Never use pure red (`#FF0000`).

### Website

Template: `brand.css`. For Tailwind, `templates/tailwind-theme.css`.

- Use the variables. Do not hard-code hex values in page styles.
- **Hero.** A dark band (`#1A1A1A`) with a line texture, white heading, a red primary button and a white-outline secondary button. Red text on the dark band is `#D07886`.
- **Closing band.** The same dark band with a call to action.
- **Page body.** `background` with white cards, 1 px `border`.
- **Findings cards.** Numbered, every numeral in `link`.
- **Share images.** `#A32035` ground, white logo top left, bold white Figtree title, one motif at low opacity.
- One neutral temperature: the greys in section 3. No warm or beige neutrals.
- Type scale: the six web sizes and the hero size.

### Interactive tools and charts

Templates: `brand.css`, `templates/short-aliases.css`, `templates/airi.mplstyle` and `templates/airi_mpl.py`, `templates/airi-plotly-template.json`, `templates/airi_palette.R`.

- Import `brand.css`. Apps that already use short names (`--ink`, `--muted`, `--rule`) add `short-aliases.css` instead of renaming their code.
- **Header.** A standalone app has the red header bar with the white logo. An app framed inside the AIRI website drops its own logo.
- **Embeds.** The embed's background matches the section it sits in. Furniture is ink, muted, rule and border. Override framework greys (Tailwind, Bootstrap) with the kit neutrals.
- Every chart that can take a colour setting offers a brand mode: one red on grey.
- Third-party embeds that cannot be styled (hosted tables, hosted chart tools) are acceptable for working data. Do not use them for a headline figure.
- Focus ring on every control.
- Chart colours follow section 4. The chart templates default to red, grey, blue; switch to the category colours for named groups.

### Papers and reports

Templates: `templates/airi_palette.R`, `templates/airi.mplstyle`, `templates/airi-colors.sty`, `templates/office-theme.md` (Word manuscripts).

- **Report cover.** `#A32035` full bleed. White AIRI and FutureTech logos top left. White Figtree bold title, subtitle in regular. One white line texture per report, low contrast. Date bottom left.
- **Divider page** before supplements: full red, white title. **Back cover:** full red, logos and the site address.
- **Interior.** The document styles above. Tables in print: ink or black rules are fine, zebra `#F3F3F3`, header bold.
- **Figures.** Same meaning, same mark, across every figure in a paper. Sizes from section 6. Direct labels on category figures. One shared palette file per project, taken from `templates/`.
- **LaTeX and preprint servers.** Links in a LaTeX PDF are coloured, not underlined (section 3). Use `airi-colors.sty` for link and figure colours and `\airimark` for a small identity line in the title block.
- Before a print run, get one proof of `#A32035`; it has not been matched to a print ink.

### Claude artifacts and Claude Code

Template: `templates/claude-artifact.html`.

- Start from the template. It defines every token for light and dark, loads Figtree and styles the basic elements.
- Artifacts must work in both themes. Use variables only; a hex in the page body will be wrong in one theme.
- Red text is `link`, red fills are `primary`. `primary` as a text colour is unreadable in dark mode.
- A label on a category fill uses `--color-cat-N-label`, which holds the right colour for each theme.
- Charts follow section 4 whatever library draws them.
- Slide artifacts follow the slides section on the 1920 x 1080 canvas.
- This applies to internal tools too. A quick internal page still uses Figtree and the tokens.

## 11. Do and don't

| Do | Don't |
|---|---|
| Take red from the theme, template or token | Type a red from memory or sample one from a screenshot |
| Use ink and muted for all text | Use `#898A8D` or any lighter grey for text |
| Make Heading 2 and below ink | Reach for a second, darker red for sub-headings |
| Use `#F8E1E5` or `#FBF3F4` for pale red | Mix a new pale pink or use an opacity of red |
| Use `#8A1B2D` for hover | Invent a hover red |
| Pick status and category colours from this file | Borrow a palette from a chart library or CSS framework |
| Mark one thing in red per chart | Use a red scale and a red highlight together |
| Use the red scale for risk and blue for amounts | Use red-to-green, traffic lights or a rainbow |
| Underline red links | Leave a tool's default blue or teal links |
| Use the one AIRI logo from `logos/` | Use retired lockups or recolour the logo |

## 12. Changes from kit 1.x

| 1.x | 2.0 |
|---|---|
| `gray` `#898A8D` for muted text | `text-muted` `#666666`; `gray` is for graphics only |
| Border `#E0E0E0` | `border` `#D9D9D9`, plus `rule` `#CCCCCC` for visible borders |
| "Use opacity variants of red for light fills" | `red-tint` `#F8E1E5` and `red-wash` `#FBF3F4` |
| Link hover `primary-dark` | Link hover `primary-hover` `#8A1B2D`; `primary-dark` is for scales and visited links |
| `--color-primary-light-hover` `#C4606F` | `red-500` `#B8455A` |
| Charts: red, light red, grey, dark | Section 4: fixed meanings, category, severity, blue and two-sided palettes |
| No status colours, no dark mode | Both defined |
| `dark` token | `text` (old name still works in `brand.css`) |
| Sizes 12 to 32 px, "flexible" | Fixed scales per medium |
| Radius 4, 8, 12 px and pill | 4 and 8 px. `--radius-lg` now gives 8 px; `--radius-full` still gives a full round, for dots and avatars |
| `--font-size-lg`, `-xl`, `-2xl` at 18, 20, 24 px | 20, 26, 34 px. Pages that use these names get larger headings; check them |
| `--color-text-muted` `#898A8D` | `#666666` |

`brand.css` keeps the 1.x variable names as aliases, so pages do not break, but the three size names above change value. `tokens.json` is not backward compatible: the keys `color.dark`, `typography.size.3xl`, `typography.line-height.relaxed`, `radius.lg` and `radius.full` are gone. A script that reads them must move to `color.text`, `typography.size.2xl`, `typography.line-height.normal` and `radius.md`.

## 13. Files

- `tokens.json`: every value, machine-readable. The source for the generated files.
- `brand.css`: CSS custom properties, light and opt-in dark.
- `templates/`: starting files for Office, Google Workspace, Tailwind, Claude artifacts, matplotlib, Plotly, R and LaTeX. See `templates/README.md`.
- `logos/initiative/`, `logos/futuretech/`: logo files.
- `SKILL.md`: the short version Claude loads first.

Retired logo lockups live in `legacy/logos/` at the repository root. Do not use them.
