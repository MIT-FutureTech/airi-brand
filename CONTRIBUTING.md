# Contributing to the AIRI Brand Kit

## Questions and proposed changes

Open a [GitHub issue](https://github.com/MIT-FutureTech/airi-brand/issues) for anything about the brand. That covers questions, mistakes in the kit (a broken file, a wrong colour, an old logo) and changes you'd like to see.

For a proposed change, the issue should say:

1. **What problem it solves.** Name the use case that prompted it.
2. **What would change.** One idea per issue. A new colour and a new component are two issues.
3. **Who it affects.** Would existing pages, slides or charts need updating?
4. **An example.** A screenshot, a before-and-after, or a link to the work that prompted it.

If you've already drafted the change, attach the diff or link your branch.

## How the kit fits together

`skill/tokens.json` is the source for every value. Three files state the brand and must always agree:

| File | Format | How it is kept in step |
|------|--------|------------------------|
| `skill/tokens.json` | JSON | Edited by hand. The source |
| `skill/brand.css` | CSS custom properties | Generated from `tokens.json` |
| `skill/BRAND.md` | Markdown | Written by hand; a check compares its values with `tokens.json` |

To change a colour, size, spacing step, radius, or a motion or video value:

1. Edit `skill/tokens.json`.
2. Run `python3 dev/build-kit/build.py`. It rewrites `brand.css`, everything in `skill/templates/` and `guide/index.html`.
3. Update the prose and tables in `skill/BRAND.md` and `skill/SKILL.md`.
4. Run `python3 dev/build-kit/build.py --check`. It fails if:
   - a generated file is stale;
   - any label-on-fill or text-on-ground pair in `tokens.json` is below 4.5:1, in light or dark;
   - a hand-written file names a colour that is not a token, gives a token the wrong hex, lists a palette in the wrong order, or gets a category, status, grade or theme-slot row wrong;
   - the five rules differ between `BRAND.md` and `SKILL.md`;
   - a motion or video token is out of range, the video styles use a time or curve that is not a token, or `BRAND.md` and `SKILL.md` do not state the motion values.

   It cannot check prose that carries no hex, such as where the logo goes. Read your change to `BRAND.md` against `tokens.json` as well.
5. Rebuild the Claude.ai upload: `rm airi-brand-skill.zip && zip -rq airi-brand-skill.zip skill/`

Never edit a generated file by hand; change `tokens.json` or `dev/build-kit/` instead. Two things in `skill/templates/video/` are kept by hand: `check_video.py` and the font in `fonts/`. The logo files are generated too, by `dev/logo-builder/build.py`.

## Working with an AI assistant

These prompts work in Claude Code, Codex or Cursor with this repo open.

### Check an existing file against the brand

```
Audit [path/to/file] against the current AIRI brand. Read skill/SKILL.md,
skill/BRAND.md and skill/tokens.json first. Report:
(a) what already matches
(b) what has drifted, with the current value and the correct token side by side
(c) anything ambiguous I need to decide (e.g. a colour outside the palette
    that might be intentional)
(d) brand elements the file should use but doesn't (Figtree, the right logo
    variant, the template for this tool)
Don't change anything yet.
```

Then, once you've read the report:

```
Fix the items in (b) and (d). Keep all content and structure; change only
presentation. Leave (c) alone. Show me the diff before writing.
```

### Build something new

```
I'm building [thing]. Read skill/SKILL.md first and start from the matching
file in skill/templates/. Use only the brand's tokens. If you need a colour
that isn't in tokens.json, stop and ask me.
```

With the skill installed (see the README), you only need to mention AIRI.

### Reconcile an old copy of this repo

```
Compare my local copy of skill/ against origin/main. For each difference,
say whether main has simply moved on (take main's version), whether mine
is an addition worth proposing, or whether both changed the same thing.
Then run python3 dev/build-kit/build.py --check on my copy.
Don't resolve anything yet.
```

Anything worth proposing goes into a GitHub issue, as above.

## Common mistakes

- **Editing `brand.css`, a template or the guide by hand.** They are generated; the next build overwrites the edit.
- **Changing `tokens.json` and not `BRAND.md`.** Run the check before you commit.
- **Adding colours.** The palette has a named answer for tints, greys, status, categories and scales. If something is missing, open an issue instead of inventing a value.
- **Using gray `#898A8D` for text.** It fails contrast. Muted text is `#666666`.
- **Using the FutureTech red as an AIRI colour.** `#9A2030` belongs to the FutureTech logo. AIRI's red is `#A32035`; MIT's institutional red is `#750014`.
- **Using the retired Index or Repository logos.** Everything uses the AIRI logo in `skill/logos/initiative/` now.
- **Replacing `guide/logos` or `guide/brand.css` with copies.** They are links into `skill/`, which is what keeps the guide current.
