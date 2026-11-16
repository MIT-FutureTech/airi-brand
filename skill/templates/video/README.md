# Video templates

A starting point for AIRI explainer videos and explanatory animations. It sits on
top of the composed-video template from the `generate-video` skill: that template
supplies the timing (`stage.js`, `stage.css`) and the renderer; these files supply
the AIRI look, motion and furniture. Everything here except `check_video.py` and
the font is generated from `../../tokens.json`.

| File | What it is |
|---|---|
| `airi-video.css` | Tokens as CSS variables, the scene components, and both motion styles |
| `comp.html` | A sample that uses every component. Copy it and replace the content |
| `script.txt` | Narration for the sample, one line per line |
| `captions.srt` | Captions for the sample |
| `check_video.py` | Checks a composition and its captions against the rules |
| `fonts/` | Figtree, so a render never falls back to another font |

## Start a video

```bash
cp -r ~/.claude/skills/generate-video/assets/template my-video
cp -r airi-video.css comp.html script.txt captions.srt fonts my-video/
cp -r ../../logos my-video/logos
cd my-video
python3 /path/to/skill/templates/video/check_video.py comp.html captions.srt
node ~/.claude/skills/generate-video/scripts/render.js comp.html --check
node ~/.claude/skills/generate-video/scripts/render.js comp.html --sheet every=1 --out out/sheet.jpg
node ~/.claude/skills/generate-video/scripts/render.js comp.html --out out/video.mp4
```

Write the storyboard and the script first, as the `generate-video` skill says.
Renders use local files only: no web fonts, no remote images.

## The two styles

Set one class on `<html>` beside `airi`:

- `style-conventional`: the red card slides on and off smoothly, titles rise in, the logo cuts in.
- `style-square`: the red card arrives as a wipe of squares on the icon's grid, titles are
  revealed a column at a time, and the logo assembles square by square. Steps, no easing.

Only the brand moments differ: the title card, section cards and the end card. Use at most
3 in a video. Charts, labels, captions and lower thirds move the same calm way in both.

## Components

| Class | Use |
|---|---|
| `airi-card airi-title` | Title card: red, white logo top left, `h1`, one line under it. `--hold` is how long it stays |
| `airi-card` | Section card: wipes on, holds for `--hold`, wipes off. Change the scene underneath during the hold. `--n` is the heading's width in large squares |
| `scene airi-statement` | One large sentence at a time. `<em>` is the red emphasis |
| `scene airi-chart` | `h2` states the finding; `airi-bars` rows grow last; `airi-source` under it |
| `airi-lower-third` | Name and role, bottom left. `data-out` is `data-at` plus 1 s plus a 4 to 5 s hold; the scene must last 1 s longer |
| `airi-caption` | A burned-in caption cue, `<br>` between its two lines. `#captions` gets the same look |
| `scene airi-endcard` | The logo and `airisk.mit.edu`, held 3 s after the logo is complete |
| `scene airi-logocard` | The logo alone, 2 to 3 s, to open a video shorter than 15 s |
| `airi-reveal` | A title outside a card that should arrive as a brand moment |

Formats: 1920 x 1080 | 1080 x 1920 | 1080 x 1080. For the second and third add `format-vertical` or `format-square`
to `<html>` and set `data-width` and `data-height` to match.

## Values

| | Value |
|---|---|
| Durations | short 400 ms (small moves, exits, a crossfade), long 700 ms (entrances, bars growing, lines drawing), scene 1000 ms (a scene change) |
| Easing | standard `cubic-bezier(0.4, 0.14, 0.3, 1)`, entrance `cubic-bezier(0, 0, 0.3, 1)`, exit `cubic-bezier(0.4, 0.14, 1, 1)` |
| Stagger | 80 to 150 ms between items that arrive together |
| Order | frame, then text, then dynamic content, then data visualisation |
| Square grid | module 40 px; squares of 40, 80 and 120 px; 15 steps a second |
| Frame rate | 30 fps; 60 for data-heavy animation |
| Safe areas | title-safe 10% inset, action-safe 5% |
| Captions | 54 px or larger, 42 characters a line (30 in vertical and square), 2 lines, 20 characters a second, at least 20 frames |

Never: bounce, elastic, overshoot, rotation, glitch, software presets, diagonal moves, fading, sliding or scaling the logo in, more than 3 flashes a second.

## Captions and the alternative

Every video ships with an SRT file, a transcript and one static key frame
(`render.js comp.html --frame 12 --out key-frame.png`). Keep each narration line
to 84 characters or fewer so it fits one two-line caption. Run `check_video.py`
on the SRT before rendering.

## Sound

Music is optional: a quiet bed under the voice. Place it with `data-role="music"`
and the renderer sets the level. Say when music or a voice was generated.

## On a web page

These files are for rendered video. Motion in a web page or tool uses the
interface values in `../../brand.css` (70 to 700 ms) and must honour
`prefers-reduced-motion`.
