#!/usr/bin/env python3
"""Check an AIRI video composition and its captions against the brand kit.

    python3 check_video.py comp.html captions.srt
    python3 check_video.py captions.srt --narrow      vertical or square video
    python3 check_video.py captions.srt --fps 60

The kit has a few hard rules; everything else is a default that a person may change.
This check follows that split. Exit code 1 only when something FAILs.

FAIL  a hard rule is broken, or the file is broken and will not render properly:
      the logo is given a fade, slide or zoom entrance (hard rule 1);
      text is set in a font other than Figtree (hard rule 3);
      there is no .srt file, or it has no usable captions (hard rule 7);
      a remote file, a frame size or rate the kit's styles do not cover, a missing
      "airi" class or style sheet, a malformed .srt file.

warn  a default was changed. Fine if a person asked for it; otherwise put it back:
      caption line length, line count, reading speed and time on screen;
      motion the kit avoids (bounce, elastic, overshoot, rotation, glitch, presets);
      more brand moments than usual, no end card, or an end card shorter than usual;
      a dropped square-step transition.

Limits come from tokens.json two folders up. If this file has been copied somewhere
else, it uses the copy of the limits below. Standard library only.
"""
import json
import re
import sys
from pathlib import Path

# Kept equal to tokens.json by dev/build-kit/build.py --check.
DEFAULTS = {"max-chars-per-line": 42, "max-chars-per-line-narrow": 30, "max-lines": 2, "max-chars-per-second": 20, "min-frames": 20, "fps": [30, 60], "formats": [[1920, 1080], [1080, 1920], [1080, 1080]], "brand-moments-max": 3, "end-card-hold-s": 3}


def limits():
    path = Path(__file__).resolve().parents[2] / "tokens.json"
    if not path.exists():
        return dict(DEFAULTS)
    t = json.loads(path.read_text())
    cap = t["video"]["captions"]
    out = {k: cap[k] for k in ("max-chars-per-line", "max-chars-per-line-narrow", "max-lines", "max-chars-per-second", "min-frames")}
    out["fps"] = sorted(t["video"]["fps"].values())
    out["formats"] = [[f["width"], f["height"]] for f in t["video"]["formats"].values()]
    out["brand-moments-max"] = t["motion"]["video"]["brand-moments-max"]
    out["end-card-hold-s"] = t["video"]["end-card"]["hold-s"]
    return out


STAMP = re.compile(r"(\d+):(\d\d):(\d\d)[,.](\d{1,3})\s*-->\s*(\d+):(\d\d):(\d\d)[,.](\d{1,3})")


def seconds(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms.ljust(3, "0")) / 1000


BROKEN = "[broken file] "
DEFAULT = "[default] "


def hard(n):
    return f"[hard rule {n}] "


def check_srt(path, lim, fps, narrow):
    fails, warns = [], []
    width = lim["max-chars-per-line-narrow"] if narrow else lim["max-chars-per-line"]
    cues = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        rows = [r.rstrip() for r in block.splitlines() if r.strip()]
        at = next((i for i, r in enumerate(rows) if STAMP.search(r)), None)
        if at is None:
            if rows:
                fails.append(BROKEN + f"{path.name}: a block has no time line: {rows[0][:40]!r}")
            continue
        g = STAMP.search(rows[at]).groups()
        cues.append((seconds(*g[:4]), seconds(*g[4:]), [re.sub(r"<[^>]+>", "", r) for r in rows[at + 1:]], rows[0] if at else "?"))
    if not cues:
        fails.append(hard(7) + f"{path.name}: no captions found")
    last_end = 0
    for start, end, lines, n in cues:
        where = f"{path.name} cue {n} ({start:g} s)"
        chars = sum(len(x) for x in lines)
        if not lines:
            fails.append(BROKEN + f"{where}: no text")
        if len(lines) > lim["max-lines"]:
            warns.append(DEFAULT + f"{where}: {len(lines)} lines; the usual limit is {lim['max-lines']}")
        for x in lines:
            if len(x) > width:
                warns.append(DEFAULT + f"{where}: a line of {len(x)} characters; the usual limit is {width}: {x!r}")
        length = end - start
        if length <= 0:
            fails.append(BROKEN + f"{where}: ends before it starts")
            continue
        if round(length * fps) < lim["min-frames"]:
            warns.append(DEFAULT + f"{where}: on screen for {round(length * fps)} frames; the usual minimum is {lim['min-frames']}")
        if chars / length > lim["max-chars-per-second"] + 1e-9:
            need = chars / lim["max-chars-per-second"]
            warns.append(DEFAULT + f"{where}: {chars / length:.1f} characters a second; the usual limit is {lim['max-chars-per-second']}. Give it {need:.1f} s or cut words")
        if start < last_end - 1e-9:
            fails.append(BROKEN + f"{where}: starts before the cue before it ends")
        last_end = end
    return fails, warns


# Motion the kit avoids. These are defaults, so they warn.
AVOIDED = [
    (re.compile(r"\b(rotate[XYZ3d]*|skew[XY]?)\s*\(", re.I), "rotation or skew"),
    (re.compile(r"bounce|elastic|glitch|wobble|jello|shake", re.I), "a bounce, elastic or glitch effect"),
    (re.compile(r"\banimate\.css|animista|\bwow\.js", re.I), "a software preset library"),
]
# Remote files break a render, which uses local files only. These fail.
REMOTE = [
    (re.compile(r"""(?:src|href)\s*=\s*["']https?://""", re.I), "a remote file (renders use local files only)"),
    (re.compile(r"@import\s+url\(\s*['\"]?https?://", re.I), "a remote stylesheet (renders use local files only)"),
]
# Hard rule 3: Figtree for all text. Code may use the monospace stack.
FONT = re.compile(r"font-family\s*:\s*([^;}\n]+)", re.I)
FONT_OK = ("figtree", "inherit", "initial", "unset", "var(", "ui-monospace", "sfmono-regular", "menlo", "monospace")
BEZIER = re.compile(r"cubic-bezier\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)")


def check_comp(path, lim, have_srt):
    fails, warns = [], []
    text = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
    tag = re.search(r"<html\b[^>]*>", text, re.I)
    head = tag.group(0) if tag else ""
    name = path.name

    def attr(key):
        m = re.search(rf'{key}\s*=\s*"([^"]*)"', head)
        return m.group(1) if m else None

    classes = (attr("class") or "").split()
    if "airi" not in classes:
        fails.append(BROKEN + f'{name}: <html> needs class "airi"')
    try:
        size = [int(attr("data-width")), int(attr("data-height"))]
    except (TypeError, ValueError):
        size = None
    if size not in lim["formats"]:
        fails.append(BROKEN + f"{name}: frame is {size}; the kit's styles cover " + ", ".join(f"{w} x {h}" for w, h in lim["formats"]))
    elif size[0] < size[1] and "format-vertical" not in classes:
        fails.append(BROKEN + f'{name}: a vertical frame needs class "format-vertical" on <html>')
    elif size[0] == size[1] and "format-square" not in classes:
        fails.append(BROKEN + f'{name}: a square frame needs class "format-square" on <html>')
    fps = attr("data-fps")
    if fps is None or int(float(fps)) not in lim["fps"]:
        fails.append(BROKEN + f"{name}: data-fps is {fps}; use " + " or ".join(str(x) for x in lim["fps"]))
    if "airi-video.css" not in text:
        fails.append(BROKEN + f"{name}: airi-video.css is not linked")
    for pattern, what in REMOTE:
        m = pattern.search(text)
        if m:
            fails.append(BROKEN + f"{name}: uses {what}: {m.group(0)!r}")

    # Hard rules.
    if re.search(r'class="[^"]*airi-logo\b[^"]*"[^>]*data-enter', text):
        fails.append(hard(1) + f"{name}: the logo has a data-enter entrance; the logo cuts in or builds from its squares, and never fades, slides or zooms")
    # Rules on code apply to code, not to words on screen: a slide may say "No bounce".
    code = "\n".join(body for _, body in re.findall(r"<(style|script)\b[^>]*>(.*?)</\1>", text, re.S | re.I))
    code += "\n" + "\n".join(re.findall(r'\b(?:class|style)\s*=\s*"([^"]*)"', text))  # not data-at: it names spoken words
    for m in FONT.finditer(code):
        first = m.group(1).split(",")[0].strip(" '\"").lower()
        if not first.startswith(FONT_OK):
            fails.append(hard(3) + f"{name}: text is set in {m.group(1).strip()!r}; use Figtree (var(--airi-font))")
    if not have_srt and not list(path.parent.glob("*.srt")):
        fails.append(hard(7) + f"{name}: no .srt file beside it; every video has captions")

    # Defaults.
    if "style-square" in classes or re.search(r'class="[^"]*\bairi-reveal\b', text):
        warns.append(DEFAULT + f"{name}: uses a square-step transition (style-square or airi-reveal); these were dropped and now do nothing")
    for pattern, what in AVOIDED:
        m = pattern.search(code)
        if m:
            warns.append(DEFAULT + f"{name}: uses {what}, which the kit avoids: {m.group(0)!r}")
    for m in BEZIER.finditer(text):
        if not all(0 <= float(x) <= 1 for x in m.groups()):
            warns.append(DEFAULT + f"{name}: {m.group(0)} overshoots; the kit's curves are --airi-ease, --airi-ease-in and --airi-ease-out")
    moments = len(re.findall(r'class="[^"]*\bairi-(?:card|endcard|logocard)\b(?!-)', text))
    if moments > lim["brand-moments-max"]:
        warns.append(DEFAULT + f"{name}: {moments} brand moments (cards, end card); the usual number is {lim['brand-moments-max']}")
    end = re.search(r'<[^>]*class="[^"]*\bairi-endcard\b[^>]*>', text)
    if not end:
        warns.append(DEFAULT + f"{name}: no end card; external videos usually end on one")
    else:
        start, stop = re.search(r'data-from="([\d.]+)"', end.group(0)), re.search(r'data-to="([\d.]+)"', end.group(0))
        total = attr("data-duration")
        try:
            length = float(stop.group(1) if stop else total) - float(start.group(1))
        except (AttributeError, TypeError, ValueError):
            length = None
        if length is not None and length < lim["end-card-hold-s"]:
            warns.append(DEFAULT + f"{name}: the end card lasts {length:g} s; the usual hold is {lim['end-card-hold-s']} s after the logo is complete")
    return fails, warns


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args or "--help" in argv or "-h" in argv:
        print(__doc__.strip())
        return 0 if args or "--help" in argv or "-h" in argv else 2
    fps = 30
    if "--fps" in argv:
        fps = int(argv[argv.index("--fps") + 1])
        args = [a for a in args if a != str(fps)]
    lim = limits()
    fails, warns = [], []
    srts = [Path(a) for a in args if a.lower().endswith(".srt")]
    for a in args:
        p = Path(a)
        if not p.exists():
            fails.append(BROKEN + f"{a}: no such file")
        elif p.suffix.lower() == ".srt":
            f, w = check_srt(p, lim, fps, "--narrow" in argv)
            fails += f
            warns += w
        elif p.suffix.lower() in (".html", ".htm"):
            f, w = check_comp(p, lim, bool(srts))
            fails += f
            warns += w
        else:
            fails.append(BROKEN + f"{a}: expected an .html composition or an .srt file")
    for w in warns:
        print("warn", w)
    for f in fails:
        print("FAIL", f)
    if warns:
        print(f"{len(warns)} default(s) changed: fine if a person asked for it, otherwise put it back")
    print("ok" if not fails else f"{len(fails)} problem(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
