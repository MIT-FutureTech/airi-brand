# AIRI theme for Google Slides and Sheets

Set these once in a deck and every new slide, link and chart starts on brand.
Do it in a template deck, then start new decks with File > Make a copy.

## Slides: by hand

1. Slide > Edit theme. Click **Colors** in the toolbar.
2. Open the "Choose a theme color" list. Set each entry to the hex below.
3. Still in the theme editor, select the master slide. Set its background to `#FAFAFA`.
   Select all text placeholders and set the font to Figtree.
4. Set the title placeholder to Figtree Bold, Accent 1.

| Entry in the list | API name | Hex |
|---|---|---|
| Text and background 1 | `DARK1` | `#1A1A1A` |
| Text and background 2 | `LIGHT1` | `#FFFFFF` |
| Text and background 3 | `DARK2` | `#666666` |
| Text and background 4 | `LIGHT2` | `#F3F3F3` |
| Accent 1 | `ACCENT1` | `#A32035` |
| Accent 2 | `ACCENT2` | `#2171B5` |
| Accent 3 | `ACCENT3` | `#D9A531` |
| Accent 4 | `ACCENT4` | `#117A66` |
| Accent 5 | `ACCENT5` | `#CC6699` |
| Accent 6 | `ACCENT6` | `#6BAED6` |
| Link | `HYPERLINK` | `#A32035` |
| (API only) | `FOLLOWED_HYPERLINK` | `#5E0E20` |

Sizes for a 960 x 540 pt page (File > Page setup > Custom > 13.333 x 7.5 in): cover 36 pt,
slide title 28 pt, outcome 18 pt, body 14 pt, small 11 pt.
Nothing smaller than 11 pt. On Google's default 720 x 405 pt page, multiply by 0.75.

Spacing on the 960 x 540 pt page: margins 48 pt top, 64 pt sides, 72 pt bottom.
Gaps of 4, 8, 12 or 24 pt. Borders 1 pt. Corner radius 4 pt for cards and images, 2 pt otherwise.

## Slides: by API

The same change as one `presentations.batchUpdate` request. Replace `MASTER_OBJECT_ID`
with the id of the deck's master page (`masters[0].objectId` from `presentations.get`).
The API needs all 12 colours in one request.

```json
{
 "requests": [
  {
   "updatePageProperties": {
    "objectId": "MASTER_OBJECT_ID",
    "pageProperties": {
     "colorScheme": {
      "colors": [
       {
        "type": "DARK1",
        "color": {
         "red": 0.102,
         "green": 0.102,
         "blue": 0.102
        }
       },
       {
        "type": "LIGHT1",
        "color": {
         "red": 1.0,
         "green": 1.0,
         "blue": 1.0
        }
       },
       {
        "type": "DARK2",
        "color": {
         "red": 0.4,
         "green": 0.4,
         "blue": 0.4
        }
       },
       {
        "type": "LIGHT2",
        "color": {
         "red": 0.9529,
         "green": 0.9529,
         "blue": 0.9529
        }
       },
       {
        "type": "ACCENT1",
        "color": {
         "red": 0.6392,
         "green": 0.1255,
         "blue": 0.2078
        }
       },
       {
        "type": "ACCENT2",
        "color": {
         "red": 0.1294,
         "green": 0.4431,
         "blue": 0.7098
        }
       },
       {
        "type": "ACCENT3",
        "color": {
         "red": 0.851,
         "green": 0.6471,
         "blue": 0.1922
        }
       },
       {
        "type": "ACCENT4",
        "color": {
         "red": 0.0667,
         "green": 0.4784,
         "blue": 0.4
        }
       },
       {
        "type": "ACCENT5",
        "color": {
         "red": 0.8,
         "green": 0.4,
         "blue": 0.6
        }
       },
       {
        "type": "ACCENT6",
        "color": {
         "red": 0.4196,
         "green": 0.6824,
         "blue": 0.8392
        }
       },
       {
        "type": "HYPERLINK",
        "color": {
         "red": 0.6392,
         "green": 0.1255,
         "blue": 0.2078
        }
       },
       {
        "type": "FOLLOWED_HYPERLINK",
        "color": {
         "red": 0.3686,
         "green": 0.0549,
         "blue": 0.1255
        }
       }
      ]
     }
    },
    "fields": "colorScheme.colors"
   }
  }
 ]
}
```

## Colours outside the theme

Google lists custom colours under "Custom" in the colour picker. Add these there,
and keep a small strip of them on the template's last slide so they travel with copies:

`#8A1B2D` `#5E0E20` `#B8455A` `#D07886` `#E29CA8` `#F8E1E5` `#898A8D` `#CCCCCC` `#D9D9D9` `#55399E` `#D4762C` `#E8A317` `#3A8F5C` `#FFF0B3` `#EFF6FF` `#C6DBEF` `#9ECAE1` `#4292C6` `#084594`

## Sheets

Format > Theme > Customize. Font: Figtree.

| Entry | Hex |
|---|---|
| Text | `#1A1A1A` |
| Background | `#FFFFFF` |
| Accent 1 | `#A32035` |
| Accent 2 | `#2171B5` |
| Accent 3 | `#D9A531` |
| Accent 4 | `#117A66` |
| Accent 5 | `#CC6699` |
| Accent 6 | `#6BAED6` |
| Hyperlink | `#A32035` |

## Charts in Slides and Sheets

A chart made here takes its series colours from Accent 1 to 6 in order:
`#A32035`, `#2171B5`, `#D9A531`, `#117A66`, `#CC6699`, `#6BAED6`. That order is right for one kind of chart only: one series (red), or
two series (red and blue). For every other chart, set the colours by hand. A chart in Slides is made in Sheets: double-click the chart, then Customize > Series > Fill colour > Custom, and type the hex.

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

## Do not click

- The dark red in the toolbar grid ("dark red berry 1", `#980000`) or any other toolbar red. AIRI red is the Accent 1 theme colour.
- The default link colours: teal `#0097A7` in Slides, blue `#1155CC` in Docs. Links are `#A32035` and underlined.
- Four greys are safe to click, because they are Google presets: `#666666` (dark gray 3), `#CCCCCC` (gray), `#D9D9D9` (light gray 1), `#F3F3F3` (light gray 3).
  Ink `#1A1A1A`, chart grey `#898A8D` and background `#FAFAFA` are not presets; take them from the theme or the custom colours.
  Google's preset named "gray" is `#CCCCCC`, the kit's `rule`. It is not the kit's chart grey.
