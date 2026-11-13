"""AIRI brand kit 2.0.0. Generated from tokens.json by dev/build-kit/build.py. Do not edit by hand.

AIRI colours for matplotlib. Put this file next to airi.mplstyle.

    import matplotlib.pyplot as plt
    import airi_mpl                      # registers the colour maps
    plt.style.use(airi_mpl.STYLE)

    ax.bar(x, y, color=airi_mpl.CONTEXT)             # everything else
    ax.bar(x[3], y[3], color=airi_mpl.RED)           # the finding
    ax.imshow(m, cmap="airi_red")                    # more means more risk
    ax.imshow(m, cmap="airi_blue")                   # more is only more
    airi_mpl.use_categorical()                       # named categories, no red
"""
from pathlib import Path

import matplotlib as mpl
from cycler import cycler
from matplotlib.colors import ListedColormap, to_rgb

STYLE = str(Path(__file__).with_name("airi.mplstyle"))

RED = "#A32035"
RED_PALE = "#E29CA8"       # the second condition beside RED
CONTEXT = "#898A8D"
BLUE = "#2171B5"
INK = "#1A1A1A"
MUTED = "#666666"
NO_DATA = "#F3F3F3"

CATEGORICAL = {"blue": "#2171B5", "sky": "#6BAED6", "violet": "#55399E", "pink": "#CC6699", "orange": "#D4762C", "gold": "#D9A531", "teal": "#138A73"}
OTHER = "#898A8D"
SEVERITY = ["#E29CA8", "#D07886", "#B8455A", "#A32035", "#5E0E20"]
GOOD, PARTIAL, POOR = "#3A8F5C", "#E8A317", "#A32035"

_STOPS = {
    "airi_red": ["#FBF3F4", "#E29CA8", "#D07886", "#B8455A", "#A32035", "#5E0E20"],
    "airi_blue": ["#EFF6FF", "#C6DBEF", "#9ECAE1", "#6BAED6", "#4292C6", "#2171B5", "#084594"],
    "airi_div": ["#084594", "#4292C6", "#9ECAE1", "#F3F3F3", "#E29CA8", "#B8455A", "#5E0E20"],
}


def _to_oklab(c):
    r, g, b = [(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in to_rgb(c)]
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def _from_oklab(L, a, b):
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
    return tuple(min(1.0, max(0.0, 12.92 * v if v <= 0.0031308 else 1.055 * max(v, 0) ** (1 / 2.4) - 0.055)) for v in rgb)


def _ramp(stops, n=256):
    """Interpolate between the stops in OKLab, so steps look even."""
    lab = [_to_oklab(c) for c in stops]
    out = []
    for i in range(n):
        t = i / (n - 1) * (len(lab) - 1)
        k = min(int(t), len(lab) - 2)
        f = t - k
        out.append(_from_oklab(*[lab[k][j] + (lab[k + 1][j] - lab[k][j]) * f for j in range(3)]))
    return out


def register():
    for name, stops in _STOPS.items():
        for cmap in (ListedColormap(_ramp(stops), name=name), ListedColormap(_ramp(stops)[::-1], name=name + "_r")):
            if cmap.name not in mpl.colormaps:
                mpl.colormaps.register(cmap)
    if "airi_severity" not in mpl.colormaps:
        mpl.colormaps.register(ListedColormap(SEVERITY, name="airi_severity"))


def use_categorical():
    """Colour cycle for named categories: the seven slots in order, then grey for Other."""
    mpl.rcParams["axes.prop_cycle"] = cycler(color=list(CATEGORICAL.values()) + [OTHER])


register()
