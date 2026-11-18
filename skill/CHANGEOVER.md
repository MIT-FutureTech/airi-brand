# Updating existing work to the kit

Use this when someone asks to bring a deck, site, repo or document up to the current brand, or to check one against the kit. For new work, use SKILL.md instead.

The scanner reads and reports. It never changes a file. You propose changes, and a person approves them before anything is edited.

## What holds throughout

- **Hard rules always apply.** A breach of one of the seven hard rules is a must-fix. Say which rule.
- **Everything else is a default.** Propose the kit value; do not insist. People stray on purpose, so ask before you change.
- **Category colours are never retrofitted.** The agreed domain colours are for new work only. Report the palettes you find and leave them alone, unless the person asks for them to change.
- **Where the kit says nothing,** reuse its closest pattern, else use ink and greys. Never invent a colour or treatment.
- **Partner-led work** keeps the partner's colour and type. Only the logo rule applies; do not run a changeover on it.

## Steps

1. **Agree the scope.** Ask which files or folders, and whether it is AIRI-led. Leave out archives, saved copies of other people's pages, data and generated output.
2. **Run the scan.**

   ```
   python3 tools/brand_scan.py PATH [PATH ...]
   python3 tools/brand_scan.py PATH --exclude archive --exclude data
   ```

   The first lines of the report show which folders hold the differences. If most sit in folders that are out of scope, exclude them and run it again. Add `--json` when you want every finding with its line of context.
3. **Read the report.** It has four groups:

   | Group | What it holds | What you do |
   |---|---|---|
   | Must fix | Reds that are not the kit's, fonts other than Figtree, text that fails contrast | Propose the fix. Name the rule |
   | Probably drift | Near-misses of kit colours, kit 1.x values, tool defaults | Propose the token shown, after step 4 |
   | Needs a decision | Colours with no close kit colour | Ask. Offer the closest kit colour or a neutral; do not pick for them |
   | For information | Category palettes, logo files to check, icon fonts | Mention. Change nothing |

   Open a few of the places listed before you trust a line. A colour named in a comment or in documentation is not a use.
4. **Ask which differences are deliberate.** Show the drift and decision lists in a few lines and ask one question: which of these are on purpose? A colour defined once as a named variable and used in many places is often a choice. Leave everything the person names as deliberate, and do not ask for a reason.
5. **Check what the scan cannot see.** Look at the logo files and how they are placed (rule 1), status shown by colour alone (rule 5), what red means in each chart (rule 6), and video (rule 7, with `templates/video/check_video.py`).
6. **Propose the changes, grouped by file.** For text files, show a diff. Change a value where it is defined, not at every use. Prefer the token (`var(--color-primary)`) to a typed hex where the work already loads `brand.css`. Apply only what the person approves.
7. **Hand back a short summary:** what changed, what was left because it is deliberate, what was left because it is a category palette, and which gaps should go to the kit as issues.

## Office and Google files

Do not edit `.pptx`, `.docx` or `.xlsx` files directly. The scan reads the theme, the colours set by hand and the fonts inside them. Give the person steps to follow instead:

1. Apply the kit theme: `templates/office-theme.md` for PowerPoint, Word and Excel. This fixes every element that takes its colour and font from the theme.
2. List what the theme will not reach: colours set by hand, with the slide or part the report names and the kit colour to pick, and fonts set by hand (Replace Fonts in PowerPoint; the styles in Word).
3. Treat chart series colours as a category palette. Leave them unless asked.

For Google Slides, Docs and Sheets, ask for a downloaded copy (`.pptx`, `.docx`, `.xlsx`), scan that, and give the steps from `templates/google-slides-theme.md` or `templates/google-docs-styles.md`. The copy is only for reading; the changes are made by hand in the Google file.

If the kit gains finished template files, moving the content into the template is the better route. Until then, the theme files are what exists.

## Flags

| Flag | Use |
|---|---|
| `--exclude GLOB` | Leave out a folder or pattern. May be repeated |
| `--json` | Every finding, with counts per file and lines of context |
| `--top N` | List more or fewer findings per group (default 20) |
| `--include-categories` | Judge category palettes too. Only when the person asks for them to change |
| `--near N` | How close counts as a near-miss (default 5). Lower it if too many greys are matched |
| `--fail-on-hard` | Exit with code 1 on a hard-rule breach, for use in a check |

## Worked example

Someone asks: "Bring the project site up to the new brand." They confirm it is AIRI-led and that `archive/` is out of scope.

```
python3 tools/brand_scan.py project-site --exclude archive
```

The report, shortened:

```
## Must fix (hard rules)
- `#A52238` → `primary` `#A32035` (a near-miss of a kit red, difference 0.8). 12 places in 4 files. Defined as `--brand`.
- `Inter`: not Figtree. Kit stack: `Figtree, Arial, sans-serif`. 3 places in 1 file.

## Probably drift
- `#E0E0E0` → `border` `#D9D9D9` (a kit 1.x value). 20 places in 5 files. Defined as `--line`.
- `#898A8D` → `text-muted` `#666666` (kit grey used as a text colour ...). 6 places in 2 files.

## Needs a decision
- `#0D9488`: closest kit colour is `cat-7` `#117A66`, difference 10.3. 9 places in 3 files. Defined as `--accent`.

## For information
- `#4E79A7 #F28E2B #76B7B2 #59A14F #EDC948`
  - A category palette of 5 colours, 5 not in the kit. Left as it is ...
```

You ask: "Two things look like drift: the border grey is the old kit value, and the kit's chart grey is used for text, where it is too faint. One colour has no kit match: the teal accent. Are any of these on purpose?" The person says the teal is deliberate.

You propose, and apply once approved:

```diff
 /* styles.css */
-  --brand: #A52238;
-  --line: #E0E0E0;
-  font-family: Inter, system-ui, sans-serif;
+  --brand: #A32035;
+  --line: #D9D9D9;
+  font-family: Figtree, Arial, sans-serif;
-.caption { color: #898A8D; }
+.caption { color: #666666; }
```

You hand back:

> Changed: the red (hard rule 2), the font (hard rule 3), the border grey and the caption text colour, all in `styles.css`. Left on purpose: the teal accent. Left as it is: the five-colour chart palette, because category colours are not retrofitted. For the kit: the site wants a second accent beside blue and the kit has none; worth an issue.
