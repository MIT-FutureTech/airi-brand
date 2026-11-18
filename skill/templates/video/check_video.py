#!/usr/bin/env python3
"""Check an AIRI video composition and its captions against the brand rules.

    python3 check_video.py comp.html captions.srt
    python3 check_video.py captions.srt --narrow      vertical or square video
    python3 check_video.py captions.srt --fps 60

For an .srt file it fails on a line that is too long, a cue with too many lines, a cue
read faster than the limit, a cue on screen for too few frames, and cues that overlap.
For a composition (.html) it fails on a frame size or rate the kit does not define, a
missing "airi" class, prohibited motion, remote files, and a missing .srt file.
It warns about more brand moments than the limit, a missing end card, and a dropped
square-step transition.

Limits come from tokens.json two folders up. If this file has been copied somewhere
else, it uses the copy of the limits below. Standard library only. Exit code 1 on failure.
"""
import json
import re
import sys
from pathlib import Path

# Kept equal to tokens.json by dev/build-kit/build.py --check.
DEFAULTS = {"max-chars-per-line": 42, "max-chars-per-line-narrow": 30, "max-lines": 2, "max-chars-per-second": 20, "min-frames": 20, "fps": [30, 60], "formats": [[1920, 1080], [1080, 1920], [1080, 1080]], "brand-moments-max": 3}


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
    return out


STAMP = re.compile(r"(\d+):(\d\d):(\d\d)[,.](\d{1,3})\s*-->\s*(\d+):(\d\d):(\d\d)[,.](\d{1,3})")


def seconds(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms.ljust(3, "0")) / 1000


def check_srt(path, lim, fps, narrow):
    fails = []
    width = lim["max-chars-per-line-narrow"] if narrow else lim["max-chars-per-line"]
    cues = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        rows = [r.rstrip() for r in block.splitlines() if r.strip()]
        at = next((i for i, r in enumerate(rows) if STAMP.search(r)), None)
        if at is None:
            if rows:
                fails.append(f"{path.name}: a block has no time line: {rows[0][:40]!r}")
            continue
        g = STAMP.search(rows[at]).groups()
        cues.append((seconds(*g[:4]), seconds(*g[4:]), [re.sub(r"<[^>]+>", "", r) for r in rows[at + 1:]], rows[0] if at else "?"))
    if not cues:
        fails.append(f"{path.name}: no captions found")
    last_end = 0
    for start, end, lines, n in cues:
        where = f"{path.name} cue {n} ({start:g} s)"
        chars = sum(len(x) for x in lines)
        if not lines:
            fails.append(f"{where}: no text")
        if len(lines) > lim["max-lines"]:
            fails.append(f"{where}: {len(lines)} lines; the limit is {lim['max-lines']}")
        for x in lines:
            if len(x) > width:
                fails.append(f"{where}: a line of {len(x)} characters; the limit is {width}: {x!r}")
        length = end - start
        if length <= 0:
            fails.append(f"{where}: ends before it starts")
            continue
        if round(length * fps) < lim["min-frames"]:
            fails.append(f"{where}: on screen for {round(length * fps)} frames; the minimum is {lim['min-frames']}")
        if chars / length > lim["max-chars-per-second"] + 1e-9:
            need = chars / lim["max-chars-per-second"]
            fails.append(f"{where}: {chars / length:.1f} characters a second; the limit is {lim['max-chars-per-second']}. Give it {need:.1f} s or cut words")
        if start < last_end - 1e-9:
            fails.append(f"{where}: starts before the cue before it ends")
        last_end = end
    return fails


BANNED = [
    (re.compile(r"\b(rotate[XYZ3d]*|skew[XY]?)\s*\(", re.I), "rotation or skew"),
    (re.compile(r"bounce|elastic|glitch|wobble|jello|shake", re.I), "a bounce, elastic or glitch effect"),
    (re.compile(r"\banimate\.css|animista|\bwow\.js", re.I), "a software preset library"),
    (re.compile(r"""(?:src|href)\s*=\s*["']https?://""", re.I), "a remote file (renders use local files only)"),
    (re.compile(r"@import\s+url\(\s*['\"]?https?://", re.I), "a remote stylesheet (renders use local files only)"),
]
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
        fails.append(f'{name}: <html> needs class "airi"')
    if "style-square" in classes or re.search(r'class="[^"]*\bairi-reveal\b', text):
        warns.append(f"{name}: uses a square-step transition (style-square or airi-reveal); these were dropped and now do nothing")
    try:
        size = [int(attr("data-width")), int(attr("data-height"))]
    except (TypeError, ValueError):
        size = None
    if size not in lim["formats"]:
        fails.append(f"{name}: frame is {size}; the kit defines " + ", ".join(f"{w} x {h}" for w, h in lim["formats"]))
    elif size[0] < size[1] and "format-vertical" not in classes:
        fails.append(f'{name}: a vertical frame needs class "format-vertical" on <html>')
    elif size[0] == size[1] and "format-square" not in classes:
        fails.append(f'{name}: a square frame needs class "format-square" on <html>')
    fps = attr("data-fps")
    if fps is None or int(float(fps)) not in lim["fps"]:
        fails.append(f"{name}: data-fps is {fps}; use " + " or ".join(str(x) for x in lim["fps"]))
    if "airi-video.css" not in text:
        fails.append(f"{name}: airi-video.css is not linked")
    # Motion rules apply to code, not to words on screen: a slide may say "No bounce".
    code = "\n".join(body for _, body in re.findall(r"<(style|script)\b[^>]*>(.*?)</\1>", text, re.S | re.I))
    code += "\n" + "\n".join(re.findall(r'\b(?:class|style)\s*=\s*"([^"]*)"', text))  # not data-at: it names spoken words
    for pattern, what in BANNED:
        m = pattern.search(text if "remote" in what else code)
        if m:
            fails.append(f"{name}: uses {what}: {m.group(0)!r}")
    for m in BEZIER.finditer(text):
        if not all(0 <= float(x) <= 1 for x in m.groups()):
            fails.append(f"{name}: {m.group(0)} overshoots; use the kit's curves (--airi-ease, --airi-ease-in, --airi-ease-out)")
    if re.search(r'class="[^"]*airi-logo\b[^"]*"[^>]*data-enter', text):
        fails.append(f"{name}: the logo has a data-enter entrance; the logo cuts in or builds from its squares, nothing else")
    moments = len(re.findall(r'class="[^"]*\bairi-(?:card|reveal|endcard|logocard)\b(?!-)', text))
    if moments > lim["brand-moments-max"]:
        warns.append(f"{name}: {moments} brand moments (cards, reveals, end card); aim for {lim['brand-moments-max']}")
    if "airi-endcard" not in text:
        warns.append(f"{name}: no end card; every external video ends on one")
    if not have_srt and not list(path.parent.glob("*.srt")):
        fails.append(f"{name}: no .srt file beside it; captions ship with every video")
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
            fails.append(f"{a}: no such file")
        elif p.suffix.lower() == ".srt":
            fails += check_srt(p, lim, fps, "--narrow" in argv)
        elif p.suffix.lower() in (".html", ".htm"):
            f, w = check_comp(p, lim, bool(srts))
            fails += f
            warns += w
        else:
            fails.append(f"{a}: expected an .html composition or an .srt file")
    for w in warns:
        print("warn", w)
    for f in fails:
        print("FAIL", f)
    print("ok" if not fails else f"{len(fails)} problem(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
