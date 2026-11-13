# AIRI theme for PowerPoint, Word and Excel

Two small files set the theme colours and fonts for every Office app:
`office-theme-colors.xml` and `office-theme-fonts.xml`. Once installed, "AIRI"
appears in the Colors and Fonts menus. A default chart then starts with AIRI red;
see "Charts" below for what to set by hand.

## Install

Copy `office-theme-colors.xml` into the Theme Colors folder and
`office-theme-fonts.xml` into the Theme Fonts folder, then restart the app.
Rename them `AIRI.xml` if you like; the menu shows the name inside the file.

| System | Folder |
|---|---|
| Windows | `%AppData%\Microsoft\Templates\Document Themes\Theme Colors` and `...\Theme Fonts` |
| macOS | `~/Library/Group Containers/UBF8T346G9.Office/User Content/Themes/Theme Colors` and `.../Theme Fonts` |

Then choose the theme:

- PowerPoint: Design > Variants > Colors > AIRI, and Fonts > AIRI.
- Word: Design > Colors > AIRI, and Fonts > AIRI.
- Excel: Page Layout > Colors > AIRI, and Fonts > AIRI.

To make a template, apply both, set the styles below, and save as `.potx` or `.dotx`.
Figtree must be installed on the computer (it is free from Google Fonts).

## The 12 slots

If you would rather type them: Colors > Customize Colors.

| Slot | Name in the dialog | Hex |
|---|---|---|
| dk1 | Text/Background: Dark 1 | `#1A1A1A` |
| lt1 | Text/Background: Light 1 | `#FFFFFF` |
| dk2 | Text/Background: Dark 2 | `#666666` |
| lt2 | Text/Background: Light 2 | `#F3F3F3` |
| accent1 | Accent 1 | `#A32035` |
| accent2 | Accent 2 | `#2171B5` |
| accent3 | Accent 3 | `#D9A531` |
| accent4 | Accent 4 | `#117A66` |
| accent5 | Accent 5 | `#CC6699` |
| accent6 | Accent 6 | `#6BAED6` |
| hlink | Hyperlink | `#A32035` |
| folHlink | Followed Hyperlink | `#5E0E20` |

## PowerPoint

- Slide size 13.333 x 7.5 in (960 x 540 pt, the widescreen default).
- Master background `#FAFAFA`. Section divider background `#A32035` with white text.
- Sizes in pt: cover 36, slide title 28, outcome 18, body 14, small 11. Nothing smaller than 11.
- Slide titles are Figtree Bold in Accent 1. Everything else is Dark 1, or Dark 2 for small text.
- Margins 48 pt top, 64 pt sides, 72 pt bottom. Gaps of 4, 8, 12 or 24 pt. Borders 1 pt.

## Word styles

| Style | Font | Size | Colour |
|---|---|---|---|
| Title | Figtree Bold | 24 pt | `#A32035` (Accent 1) |
| Subtitle | Figtree Regular | 14 pt | `#666666` (Dark 2) |
| Heading 1 | Figtree Bold | 18 pt | `#A32035` (Accent 1) |
| Heading 2 | Figtree Bold | 14 pt | `#1A1A1A` (Dark 1) |
| Heading 3 | Figtree Bold | 12 pt | `#1A1A1A` (Dark 1) |
| Normal | Figtree Regular | 11 pt | `#1A1A1A` (Dark 1) |
| Caption, table and figure notes | Figtree Regular | 9 pt | `#666666` (Dark 2) |
| Hyperlink | underlined | | `#A32035` |

Tables: header row bold on `#F3F3F3` (Light 2), or white on `#A32035` for short tables.
Body rows alternate white and `#F3F3F3`. Rules `#CCCCCC`.

## Colours outside the theme

Office builds its own lighter and darker rows from each accent. Those are not AIRI
tints. When you need a tint or a chart colour that is not one of the 12 slots,
type one of these under More Colors (they then stay in Recent Colors):

`#8A1B2D` `#5E0E20` `#B8455A` `#D07886` `#E29CA8` `#F8E1E5` `#898A8D` `#CCCCCC` `#D9D9D9` `#55399E` `#D4762C` `#E8A317` `#3A8F5C` `#FFF0B3` `#EFF6FF` `#C6DBEF` `#9ECAE1` `#4292C6` `#084594`

## Charts in PowerPoint, Word and Excel

A chart made here takes its series colours from Accent 1 to 6 in order:
`#A32035`, `#2171B5`, `#D9A531`, `#117A66`, `#CC6699`, `#6BAED6`. That order is right for one kind of chart only: one series (red), or
two series (red and blue). For every other chart, set the colours by hand. Click a series, then Format Data Series > Fill > More Colors, and type the hex.

- **Context series** (everything that is not the subject): `#898A8D`. It is not a theme colour.
- **Named groups** (risk domains, sectors, roles): set each series to its category colour,
  in slot order. The first group is blue, never red.

| Slot | Colour | Hex | Label on it | AI Risk Repository domain |
|---|---|---|---|---|
| 1 | Blue | `#2171B5` | white | Discrimination & toxicity |
| 2 | Sky | `#6BAED6` | ink | Privacy & security |
| 3 | Violet | `#55399E` | white | Misinformation |
| 4 | Pink | `#CC6699` | ink | Malicious actors & misuse |
| 5 | Orange | `#D4762C` | ink | Human-computer interaction |
| 6 | Gold | `#D9A531` | ink | Socioeconomic & environmental |
| 7 | Teal | `#117A66` | white | AI system safety, failures & limitations |
| | Other | `#898A8D` | ink | Other, folded groups |

- **Ordered levels where higher is worse:** `#E29CA8` `#D07886` `#B8455A` `#A32035` `#5E0E20`.
- **Counts:** `#9ECAE1` `#6BAED6` `#4292C6` `#2171B5` `#084594`.

The code templates (matplotlib, Plotly, R) default to red, grey, blue. A chart made
here matches them only after the grey and the category colours are set as above.
