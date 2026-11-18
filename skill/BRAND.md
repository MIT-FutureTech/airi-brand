# AIRI brand specification

Version 2.0. The visual identity of the MIT AI Risk Initiative (AIRI), for every medium: slides, documents, the website, interactive tools, charts, papers, video and anything Claude generates.

Values in this file match `tokens.json` exactly. `brand.css` and the files in `templates/` are generated from `tokens.json`. If you are applying the brand in a tool, start from the template for that tool (section 10) instead of typing values.

## 1. What AIRI looks like

Five things make a piece of work look like AIRI.

1. **Red is structure.** One red, used for the things that frame the work: titles, covers, section dividers, header bars, buttons, links.
2. **Figtree everywhere.** One typeface, left-aligned, sentence case.
3. **Restraint in data.** Red marks the one thing a chart is about. Grey is everything else.
4. **Light grounds.** White or near-white pages, near-black text, few rules.
5. **Titles state the point.** Every data slide and figure names its source.

The best AIRI work uses the fewest colours. A deck that uses red, grey and near-black looks better than one that uses twenty.

## 2. How to read the rules

The kit is a starting point. It has three tiers.

### Hard rules

Claude always follows these, and people should too. They protect the identity, accessibility and meaning.

| | Hard rule | Why it is hard |
|---|---|---|
| 1 | Use the logo files as they are: never redrawn, recoloured, stretched or merged with another mark. There is one AIRI logo for all products. | It must look the same everywhere |
| 2 | AIRI red is `#A32035`, taken from the theme, the template or the token. Never approximate it, and never add a red from outside the kit. | Near-reds are the most common drift |
| 3 | Figtree for all text, with the fallback stack Figtree, Arial, sans-serif. Code may use the monospace stack. | One typeface ties the products together |
| 4 | Text meets WCAG AA contrast: 4.5 to 1, or 3 to 1 for large text. | People must be able to read it |
| 5 | Colour never carries meaning alone. A status colour comes with a word or an icon. | Some readers cannot tell colours apart |
| 6 | In data, red never means good, and a red scale never shows a neutral amount. | Everywhere else in AIRI work red means risk |
| 7 | Nothing flashes more than three times a second, and every video has captions. | Flashing can trigger seizures, and many people watch without sound |

These cover AIRI-led work. In partner-led work the partner's template sets colour and type, and the logo rule still holds (section 8).

### Defaults

**Everything else in this file is a default.** That covers data palettes, type sizes, spacing, layouts, chart conventions, motion values and video furniture. Words like "never" and "always" outside the table above describe the default; they do not make a hard rule.

- Claude follows a default unless a person asks for something different.
- When a person asks, Claude does it. It does not argue, ask for a reason, or quietly put the default back later.
- Claude speaks up only if the request breaks a hard rule. It says which one in a line and offers the closest option that keeps it.
- Claude does not decide by itself to stray from a default. A person does. People sometimes stray on purpose to make a point, and a little drift is fine.

### When the kit says nothing

1. Reuse the closest pattern the kit already has. Look in the templates (`templates/`), the components and by-medium sections (9 and 10), and the visual guide.
2. If nothing is close, choose the most neutral option: ink and greys, Figtree regular, the default spacing, no new colour.
3. Never invent a new creative treatment. Invented treatments are how products end up looking different from each other.
4. When handing the work back, say which gap you hit and what you reused, so the gap can be added to the kit.

Sections below carry a "Hard rule" note where one of the seven applies. Nothing else is marked, because everything else is a default.

## 3. Colour

### Core

**Hard rule 2:** AIRI red is `#A32035`, taken from the theme, the template or the token. How the red and its ramp are used is a default.

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
| `blue` | `#2171B5` | One job: shading neutral amounts. A step of the blue scale, the cool end of two-sided scales, the info status. Not a comparison series, not a category, not for links |
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

**Hard rule 4:** text meets WCAG AA contrast. The pairs below are the default way to get there.

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

**Hard rule 5:** colour never carries meaning alone. Which colours mean what is a default.

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
- Category blue becomes `#4576A2` and category violet becomes `#786D99`, so they show on a dark card. Both keep white labels (4.8 and 4.7).
- Label colours on fills are fixed: "ink" on a fill means `#1A1A1A` in both themes.
- Give any dark mark that fades into the page a 1 px `#6E6E6E` outline: the darkest scale steps.

## 4. Colour in data

**Hard rule 6:** red never means good, and a red scale never shows a neutral amount. The palettes and chart conventions are defaults.

One rule decides most charts: **red is the subject, grey is context, ink is a comparison, blue shades a neutral amount.** Each colour has one job.

### Which palette

| The data shows | Use | Values |
|---|---|---|
| One thing that matters, against everything else | Highlight | `#A32035` on `#898A8D` |
| Two conditions that are both the subject | Pair | `#A32035` and `#E29CA8`, values labelled on the bars |
| Ordered levels where higher is worse (severity, vulnerability, likelihood) | Severity | 5 red steps |
| A continuous amount of risk | Red scale | 6 stops |
| Counts, coverage, anything where more is only more | Blue scale | 7 steps |
| Two directions from a real midpoint (agree and disagree, above and below) | Two-sided | Blue, grey, red |
| Named groups that each need their own mark | Categories | 8 slots and Other |

### Highlight and pair

- The default chart is one series in `#A32035` and everything else in `#898A8D`.
- Uncertainty bands and reference ranges are `#D9D9D9`.
- For a comparison series (last year, a benchmark, a second subject), use ink `#1A1A1A`. Never a flat blue: a flat blue is always a category colour.

### Categories

One palette of eight colours for any grouping: risk domains, actors, sectors, roles, mitigations, laws. The team chose it in November 2026 (palette B, "quiet but distinct": Paul Tol's muted scheme in the Repository's hue order). It gives AIRI work one look, and n colours ready for any figure with n groups.

| Slot | Name | Fill | Text | Tint | Label on fill | AI Risk Repository domain |
|---|---|---|---|---|---|---|
| 1 | Blue | `#2C6395` | `#2C6395` | `#E1E9F0` | white | Discrimination & toxicity |
| 2 | Sky | `#7DC1E3` | `#4B7488` | `#EDF6FB` | ink | Privacy & security |
| 3 | Violet | `#443471` | `#443471` | `#E5E3EB` | white | Misinformation |
| 4 | Mauve | `#B973AB` | `#8D5782` | `#F5EBF3` | ink | Malicious actors & misuse |
| 5 | Sand | `#ECBA7B` | `#846845` | `#FCF5ED` | ink | Human-computer interaction |
| 6 | Olive | `#8F8D44` | `#6D6B34` | `#EFEFE5` | ink | Socioeconomic & environmental |
| 7 | Teal | `#2A9484` | `#22766A` | `#E1F0EE` | ink | AI system safety, failures & limitations |
| 8 | Sage | `#ACC6B1` | `#647367` | `#F3F7F4` | ink | — |
| | Other | `#898A8D` | `#666666` | `#F3F3F3` | ink | Other, folded groups, context |

How to colour a grouping:

- **Colour a grouping only when the colour says something.** Bars that compare values across groups are one colour (grey, or red for the subject); the names and the lengths do the work, and extra colours make lengths harder to compare. Two exceptions: pick one group out in red, or give related groups the same colour to show they belong together.
- **Use the slots where each group needs its own mark:** a diagram or schematic with a few named parts, the parts of a stacked bar, one line per group across the same items (for example, the share of organisations disclosing each risk, one line per actor type).
- **Take the slots in order from 1.** Never cycle them. Red is never a category, which keeps it free to pick one group out.
- **More than eight groups** (sectors, mitigation domains, subdomains): don't give each its own colour. Draw them grey with names on the chart, and colour only the one or two the chart is about.
- **Subgroups** take lighter and darker steps of their parent's colour.
- **Two groupings at once** (domain by sector): colour one of them; put the other on the axis, or in small separate charts.
- **Keep a group's colour the same** within one paper or product.
- **Risk domains** take slots 1 to 7 in new work. Existing pages, tools and decks keep their colours; nothing is retrofitted. A person can set the domain colours aside for one figure, with a reason.

Notes on the values:

- A chip or tag uses the tint as background and the text colour on it. Every pair passes contrast.
- The label on each fill is the colour in the table, at any size. Every one is at least 4.7:1. Never put white on a fill whose label is ink.
- Sky, sand and sage are faint as thin marks on white. Label them directly or give them an outline.
- More than three lines or scatter series need direct labels or small multiples.
- In print the palette falls to four greys. Category figures in papers need direct labels.

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

PowerPoint, Word and Google Slides share the same 12 theme slots. Filling them is what keeps a file on brand: default charts start with AIRI red, then grey and ink, and links come out red.

| Slot | Hex | Slot | Hex |
|---|---|---|---|
| Dark 1 (text) | `#1A1A1A` | Accent 1 | `#A32035` |
| Light 1 (background) | `#FFFFFF` | Accent 2 | `#898A8D` |
| Dark 2 | `#666666` | Accent 3 | `#1A1A1A` |
| Light 2 | `#F3F3F3` | Accent 4 | `#2C6395` |
| Hyperlink | `#A32035` | Accent 5 | `#7DC1E3` |
| Followed hyperlink | `#5E0E20` | Accent 6 | `#443471` |

Office builds lighter and darker rows from each accent. Those are not AIRI tints; use the values in section 3. The colours worth keeping as custom swatches are listed in `tokens.json` under `theme.custom-swatches`: the red steps, the neutrals, the category colours not in the accents, the status marks and the blue-scale steps, so a heat map built from table cells needs no typing.

### Charts in Slides, Sheets and Office

A chart made in Google Sheets, Google Slides, PowerPoint, Word or Excel takes its series colours from Accent 1 to 6 in order: red (the subject), grey (context), ink (a comparison), then category blue, sky and violet. That order suits a chart of one to three series. For anything else, set the colours by hand.

- **Bars that compare groups:** one colour. Leave every bar grey `#898A8D`, and set the subject's bar to red.
- **Named groups that each need their own mark:** set each series to its category colour, in slot order. The first group is blue. Left alone, the tool makes the first group red, which the kit forbids.

| Slot | Colour | Hex | AI Risk Repository domain |
|---|---|---|---|
| 1 | Blue | `#2C6395` | Discrimination & toxicity |
| 2 | Sky | `#7DC1E3` | Privacy & security |
| 3 | Violet | `#443471` | Misinformation |
| 4 | Mauve | `#B973AB` | Malicious actors & misuse |
| 5 | Sand | `#ECBA7B` | Human-computer interaction |
| 6 | Olive | `#8F8D44` | Socioeconomic & environmental |
| 7 | Teal | `#2A9484` | AI system safety, failures & limitations |
| 8 | Sage | `#ACC6B1` | — |

- **Scales:** the severity, blue and two-sided values in section 4, set per series or per cell.

The code templates (matplotlib, Plotly, R) use the same order: red, grey, ink, then the category colours. A chart pasted in as an image from a code template needs none of this.

## 6. Typography

**Hard rule 3:** Figtree for all text. Sizes, weights and alignment are defaults.

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

**Hard rule 1:** use the logo files as they are. Placement and size are defaults.

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

Templates: `templates/files/airi-slides.pptx` (a ready deck with these layouts), `templates/google-slides-theme.md`, `templates/office-theme-colors.xml`, `templates/office-theme-fonts.xml`, `templates/office-theme.md`.

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

Templates: `templates/files/airi-document.docx` (a ready document with these styles), `templates/google-docs-styles.md`, `templates/office-theme.md` (Word styles).

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

## 11. Motion and video

Templates: `templates/video/` for video; the `--motion-` and `--ease-` variables in `brand.css` for interfaces.

AIRI moves in two registers. Interface motion is quick and quiet. Video motion is slower, so a viewer seeing it once can follow it. Both are restrained: things move in straight lines, settle without overshoot, and most of the frame is still most of the time. Pick a value from the tables before inventing a duration or a curve.

### Interface motion

For web pages, interactive tools and Claude artifacts. These are IBM Carbon's "productive" values, unchanged.

| Token | Duration | Use |
|---|---|---|
| `fast-01` | 70 ms | Small state changes: a button press, a toggle |
| `fast-02` | 110 ms | Fades, hover |
| `moderate-01` | 150 ms | Small expansions, short moves |
| `moderate-02` | 240 ms | A panel or a menu opening |
| `slow-01` | 400 ms | A large expansion |
| `slow-02` | 700 ms | A background change. Rare |

| Curve | Value | Use |
|---|---|---|
| standard | `cubic-bezier(0.2, 0, 0.38, 0.9)` | Something that stays on screen and moves or resizes |
| entrance | `cubic-bezier(0, 0, 0.38, 0.9)` | Something arriving |
| exit | `cubic-bezier(0.2, 0, 1, 0.9)` | Something leaving |

- Animate `transform` and `opacity` only.
- Items that arrive together are staggered by 20 ms each, and the whole group finishes inside 500 ms.
- Honour `prefers-reduced-motion`: replace movement with a short opacity change, or nothing. `brand.css` and the artifact template switch motion off for people who ask for that.
- Motion that runs for more than 5 seconds needs a way to stop it.

### Video motion

For explainer videos and explanatory animation. The curves are Carbon's "expressive" set.

| Token | Duration | Use |
|---|---|---|
| `short` | 400 ms | Small moves, exits, a crossfade |
| `long` | 700 ms | Entrances, bars growing, lines drawing |
| `scene` | 1000 ms | A scene change |

| Curve | Value |
|---|---|
| standard | `cubic-bezier(0.4, 0.14, 0.3, 1)` |
| entrance | `cubic-bezier(0, 0, 0.3, 1)` |
| exit | `cubic-bezier(0.4, 0.14, 1, 1)` |

- **Order of arrival:** the frame, then text, then anything that changes, then the data. A chart's title and labels are in place before its bars grow.
- **Stagger** items that arrive together by 80 to 150 ms. The interface value of 20 ms is too fast to read in a video.
- **Paths follow the grid:** horizontal or vertical, never diagonal.
- **Same meaning, same motion.** If bars grow from the left in one chart, they grow from the left in all of them.
- **Brand moments are few.** A video has about three: the title, a section change, the end. Everything between them is calm.

### Transitions

Transitions are conventional. A red card slides on and off with the standard curve. Text rises in. Scenes cut, or crossfade over 400 ms. The team confirmed this in November 2026.

Avoid bounce, elastic and overshoot, rotation, glitch effects, software presets and diagonal moves. Like the rest of this section these are defaults, so a person can ask for one.

**Hard rules 1 and 7:** the logo is never faded in, slid in or scaled up, and nothing flashes more than 3 times a second.

### Video furniture

**Hard rule 7:** every video has captions, and nothing flashes more than three times a second. The other values in the table are defaults.

| Item | Rule |
|---|---|
| Frame | 1920 x 1080 by default. 1080 x 1920 for phones and 1080 x 1080 for square feeds, each designed again for its shape |
| Length | Under a minute; shorter is better. Most explainers land between 30 and 60 s. Cut scenes before speeding up the voice |
| Narration | A brisk, conversational pace of 150 to 170 words a minute (voice style "clear, warm, brisk"). About 140 words for a 55 s video |
| Music | Off by default (see below) |
| Frame rate | 30 fps; 60 for data-heavy animation |
| Safe areas | Text and logos inside the title-safe area, a 10% inset. Anything that matters inside the action-safe area, a 5% inset |
| Type | Title 120 px, section 96, statement 72, chart title 56, body 44, labels 32. Nothing under 28 px |
| Captions | White on an ink plate, bottom centre. 54 px or larger (1/20 of the frame's short side). At most 42 characters a line (30 in vertical and square), 2 lines, 20 characters a second. At least 20 frames on screen. An SRT file ships with every video |
| Lower third | Bottom left, inside title-safe. 1 s in, 4 to 5 s hold, 1 s out. Never over a face or a caption |
| Title card | Red ground, white logo top left, white bold title |
| Section card | Full red, white heading, as in slides |
| End card | On every external video: the AIRI logo and `airisk.mit.edu`, held 3 s |
| Logo card | A video shorter than 15 s opens on the logo alone for 2 to 3 s |
| Charts | Colours follow section 4. The title states the finding; a source line sits under the chart |

`templates/video/check_video.py` checks a composition and its SRT file. It fails on a hard-rule breach or a file that will not render. It warns on a default, so a deliberate change still passes.

### The logo in video

The logo is not animated. It cuts in and holds still, on the end card, the logo card and the title card alike. The team chose this in November 2026 over four 600 ms builds, to keep things simple. Don't add a logo animation without a new decision.

The video layout sits on a grid built from the same squares: a module of 40 px (the icon's small square at 1/27 of the frame's short side), with squares of 40, 80 and 120 px. The large square tiles every format exactly.

### Dropped after team review

Square-step transitions are gone: the red-square section wipe and the stepped title reveal. Do not rebuild them. The classes `style-square` and `airi-reveal` no longer do anything.

### Music

Off by default. People often watch explainers at 1.5x or 2x, and music sounds wrong sped up. When a video does want music (a title sequence, a trailer, a loop at an event), use one style:

- A sparse ambient bed: soft piano or warm pads, 70 to 90 bpm.
- No vocals, no drums or percussion, no build-ups or drops.
- At least 15 LU under the voice; the renderer sets the level. Fade out over 2.5 s.
- Say that it was generated.

### Alternatives

Every video comes with a transcript and one static key frame that makes sense alone. On a web page, a video does not autoplay with sound, and motion respects `prefers-reduced-motion`.

## 12. Do and don't

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

## 13. Changes from kit 1.x

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

## 14. Files

- `tokens.json`: every value, machine-readable. The source for the generated files.
- `brand.css`: CSS custom properties, light and opt-in dark.
- `templates/`: starting files for Office, Google Workspace, Tailwind, Claude artifacts, matplotlib, Plotly, R and LaTeX. See `templates/README.md`.
- `templates/files/`: ready starter files: `airi-slides.pptx`, `airi-document.docx`, `airi-sheet.xlsx` and a 1200 x 630 social card (`airi-og-image.html`, `.png`). Generated by `dev/build-kit/build_files.py`. Upload one to Drive to get the Google Slides, Docs or Sheets version.
- `templates/video/`: video styles, a sample composition and `check_video.py`. See `templates/video/README.md`.
- `logos/initiative/`, `logos/futuretech/`: logo files.
- `SKILL.md`: the short version Claude loads first.
- `CHANGEOVER.md`, `tools/brand_scan.py`: how to bring existing work up to the kit, and the read-only scanner that reports what differs.

Retired logo lockups live in `legacy/logos/` at the repository root. Do not use them.

## 15. Decided and still open

The team reviewed the kit in November 2026. `tokens.json` holds the same list under `decisions`.

Decided:

| Topic | Decision |
|---|---|
| Slide titles | Red. Section slides are full red |
| Music in video | Off by default |
| Transitions in video | Conventional. The square-step wipe and the stepped title reveal are dropped |
| Logo animation | None. The logo cuts in. Chosen over four 600 ms builds to keep things simple |
| Category palette | Palette B, "quiet but distinct": eight colours in a fixed order for any grouping. The seven risk domains take slots 1 to 7 |
| Colour for groups | Colour a grouping only when the colour says something. Bars that compare groups are one colour. Up to eight groups take the slots in order; more than eight are grey with direct labels |
| Blue | One colour, one job. A comparison series is ink, not blue. Blue shades counts; a flat blue is a category colour |
| End card | Held 3 s, as a default |
| Risk-domain colours | One set, as a default for new work only. Existing work is never retrofitted. A person can set it aside for one figure, with a reason |

Still open. Each has a default to use until it closes:

| Topic | Default until then |
|---|---|
| Dark mode | The values in section 3, as provisional |
| Print colour | None. AIRI red has not been matched to a print ink |
| Image and illustration style | No rules yet. Reuse what the report covers do: one white line texture on red |
| Template files for Slides, Docs, PowerPoint and Word | The starter files in `templates/files/`, new and not yet used in real work |
