#!/usr/bin/env python3
"""Generate the Meowsoot UI themes and editor color schemes.

The palettes are ported from meowsoot.nvim (https://github.com/marekh19/meowsoot.nvim, MIT).

The UI themes extend the bundled "Islands Dark"/"Islands Light" themes. To recolor everything the parent
themes and schemes hard-code, the script reads them from an installed IntelliJ IDEA (2025.3+) and re-maps
each inherited color onto the meowsoot palette. Hand-written meowsoot mappings are layered on top.

Usage:
    scripts/generate.py [--ide PATH] [--plugins DIR ...]

Outputs are written to src/main/resources/themes and are committed, so building the plugin does not need
this script.
"""

import argparse
import colorsys
import glob
import json
import math
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "src", "main", "resources", "themes")

# --------------------------------------------------------------------------------------------------
# Color math (ported from meowsoot.nvim lua/meowsoot/hsl.lua and util.lua)
# --------------------------------------------------------------------------------------------------


def _round(x):
    return math.floor(x + 0.5)


def hsl_to_hex(hsl):
    h = (hsl[0] % 360) / 60
    s = hsl[1] / 100
    lum = hsl[2] / 100
    c = (1 - abs(2 * lum - 1)) * s
    x = c * (1 - abs(h % 2 - 1))
    m = lum - c / 2
    if h < 1:
        r, g, b = c, x, 0
    elif h < 2:
        r, g, b = x, c, 0
    elif h < 3:
        r, g, b = 0, c, x
    elif h < 4:
        r, g, b = 0, x, c
    elif h < 5:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return "#%02x%02x%02x" % (_round((r + m) * 255), _round((g + m) * 255), _round((b + m) * 255))


def rgb(hex_):
    hex_ = hex_.lstrip("#")
    return tuple(int(hex_[i : i + 2], 16) for i in (0, 2, 4))


def hex_to_hsl(hex_):
    """Unrounded HSL (h 0-360, s 0-100, l 0-100)."""
    r, g, b = (v / 255 for v in rgb(hex_))
    h, lum, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s * 100, lum * 100


def from_hex(hex_):
    """Rounded HSL, like hsl.lua's from_hex."""
    return [_round(v) for v in hex_to_hsl(hex_)]


def brighten(hex_, amount):
    h, s, lum = from_hex(hex_)
    return hsl_to_hex([h % 360, s, max(0, min(100, lum + amount))])


def blend(fg, alpha, bg):
    f, b = rgb(fg), rgb(bg)
    ch = [_round(min(max(0, alpha * f[i] + (1 - alpha) * b[i]), 255)) for i in range(3)]
    return "#%02x%02x%02x" % tuple(ch)


def lerp_hsl(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


# --------------------------------------------------------------------------------------------------
# Palettes (ported from meowsoot.nvim lua/meowsoot/palette.lua)
# --------------------------------------------------------------------------------------------------

DARK_ACCENTS = {
    "pink": (328, 62, 78),
    "lavender": (275, 58, 78),
    "cyan": (189, 58, 74),
    "peach": (20, 58, 74),
    "blue": (208, 53, 73),
    "yellow": (51, 58, 70),
    "peach_dim": (20, 58, 70),
    "cyan_br": (190, 55, 85),
    "lavender_br": (274, 55, 85),
    "pink_br": (329, 55, 85),
    "peach_br": (20, 55, 85),
    "yellow_br": (50, 55, 85),
    "green": (140, 35, 70),
    "red": (0, 65, 75),
}

PALETTES = {
    "night": {
        "bg_deep": (0, 3, 6),
        "bg_0": (0, 2, 9),
        "bg_1": (40, 5, 12),
        "bg_2": (20, 4, 15),
        "bg_3": (30, 4, 20),
        "bg_4": (24, 4, 26),
        "fg": (20, 5, 88),
        "fg_mute": (30, 5, 68),
        "comment": (30, 5, 49),
        "fg_faint": (33, 4, 50),
        "indent": (33, 4, 27),
        **DARK_ACCENTS,
    },
    # Night's colors on the terminal's #333333 background; the bg ladder is raised to stay distinguishable
    # (bg_3, the selection color, is the terminal's #55514e).
    "twilight": {
        "bg_deep": (0, 3, 16),
        "bg_0": (0, 0, 20),
        "bg_1": (40, 4, 23),
        "bg_2": (20, 4, 26),
        "bg_3": (26, 4, 32),
        "bg_4": (24, 4, 38),
        "fg": (20, 5, 88),
        "fg_mute": (30, 5, 68),
        "comment": (30, 5, 49),
        "fg_faint": (33, 4, 50),
        "indent": (33, 4, 37),
        **DARK_ACCENTS,
    },
    "moon": {
        "bg_deep": (230, 20, 8),
        "bg_0": (230, 18, 11),
        "bg_1": (230, 16, 15),
        "bg_2": (230, 15, 18),
        "bg_3": (230, 14, 24),
        "bg_4": (230, 13, 29),
        "fg": (230, 25, 88),
        "fg_mute": (230, 16, 68),
        "comment": (232, 14, 54),
        "fg_faint": (230, 12, 53),
        "indent": (230, 12, 30),
        **DARK_ACCENTS,
    },
    "dawn": {
        "bg_deep": (30, 18, 89),
        "bg_0": (38, 38, 96),
        "bg_1": (28, 18, 88),
        "bg_2": (35, 25, 93),
        "bg_3": (25, 22, 80),
        "bg_4": (22, 18, 62),
        "fg": (25, 18, 20),
        "fg_mute": (30, 12, 44),
        "comment": (30, 12, 48),
        "fg_faint": (30, 8, 58),
        "indent": (30, 8, 79),
        "pink": (328, 78, 32),
        "lavender": (275, 55, 38),
        "cyan": (189, 70, 32),
        "peach": (20, 78, 36),
        "blue": (208, 62, 38),
        "yellow": (45, 78, 32),
        "peach_dim": (20, 60, 45),
        "cyan_br": (190, 75, 26),
        "lavender_br": (275, 65, 30),
        "pink_br": (329, 82, 28),
        "peach_br": (20, 88, 30),
        "yellow_br": (45, 88, 28),
        "green": (140, 60, 30),
        "red": (0, 75, 36),
    },
}

VARIANTS = {
    "night": {"title": "Night", "dark": True},
    "twilight": {"title": "Twilight", "dark": True},
    "moon": {"title": "Moon", "dark": True},
    "dawn": {"title": "Dawn", "dark": False},
}


def resolve_colors(variant):
    """Hex palette plus the derived colors from meowsoot.nvim lua/meowsoot/colors.lua."""
    p = {k: hsl_to_hex(v) for k, v in PALETTES[variant].items()}
    c = dict(p)
    c["bg_search"] = blend(p["yellow"], 0.35, p["bg_0"])
    c["bg_search_current"] = blend(p["peach"], 0.45, p["bg_0"])
    c["bg_match"] = blend(p["cyan"], 0.3, p["bg_0"])
    c["border"] = p["bg_4"]
    c["border_highlight"] = blend(p["pink"], 0.6, p["bg_0"])
    c["diff_add"] = blend(p["green"], 0.18, p["bg_0"])
    c["diff_change"] = blend(p["blue"], 0.18, p["bg_0"])
    c["diff_delete"] = blend(p["red"], 0.18, p["bg_0"])
    c["diff_text"] = blend(p["blue"], 0.35, p["bg_0"])
    c["rainbow"] = [p["pink"], p["peach"], p["yellow"], p["cyan"], p["blue"], p["lavender"]]
    c["red_bright"] = brighten(p["red"], 8)
    c["green_bright"] = brighten(p["green"], 10)
    c["blue_bright"] = brighten(p["blue"], 8)
    return c


# --------------------------------------------------------------------------------------------------
# Ramps: the Islands themes define gray/blue/green/... ramps in steps 10..160. We rebuild every ramp
# from the meowsoot palette and use them to re-map any parent color.
# --------------------------------------------------------------------------------------------------

STEPS = list(range(10, 170, 10))
FAMILIES = ["blue", "green", "red", "yellow", "orange", "purple", "teal"]
# JetBrains hue family -> meowsoot accent supplying hue/saturation
FAMILY_ACCENT = {
    "blue": "blue",
    "green": "green",
    "red": "red",
    "yellow": "yellow",
    "orange": "peach",
    "purple": "lavender",
    "teal": "cyan",
    "pink": "pink",
}
# Neutral ramp anchors: step -> palette name or HSL lightness (interpolated between named neutrals).
GRAY_SPEC = {
    "night": {10: "bg_0", 20: 10.5, 30: "bg_1", 40: "bg_3", 50: "bg_4", 60: 32, 70: 40, 80: "fg_faint",
              90: 59, 100: "fg_mute", 110: 75, 120: 81, 130: "fg", 140: 91, 150: 94, 160: 97},
    "twilight": {10: "bg_0", 20: 21.5, 30: "bg_1", 40: "bg_3", 50: "bg_4", 60: 42, 70: 46, 80: "fg_faint",
                 90: 59, 100: "fg_mute", 110: 75, 120: 81, 130: "fg", 140: 91, 150: 94, 160: 97},
    "moon": {10: "bg_0", 20: 13, 30: "bg_1", 40: "bg_3", 50: "bg_4", 60: 35, 70: 43, 80: "fg_faint",
             90: 61, 100: "fg_mute", 110: 75, 120: 81, 130: "fg", 140: 91, 150: 94, 160: 97},
    "dawn": {10: "fg", 20: 22, 30: 24, 40: 26, 50: 30, 60: 36, 70: "fg_mute", 80: "comment", 90: "fg_faint",
             100: "bg_4", 110: 68, 120: 74, 130: "bg_3", 140: 85, 150: "bg_deep", 160: "bg_2"},
}
NEUTRALS = ["bg_deep", "bg_0", "bg_1", "bg_2", "bg_3", "bg_4", "fg", "fg_mute", "comment", "fg_faint"]


class Ramps:
    def __init__(self, variant, jb_colors):
        self.variant = variant
        self.dark = VARIANTS[variant]["dark"]
        self.pal = PALETTES[variant]
        self.c = resolve_colors(variant)
        self.jb = {}  # family -> [(step, (h,s,l))]
        for fam in ["gray"] + FAMILIES:
            self.jb[fam] = [(s, hex_to_hsl(jb_colors[f"{fam}-{s}"])) for s in STEPS]
        self.jb["pink"] = [(s, (320, hsl[1], hsl[2])) for s, hsl in self.jb["purple"]]
        self.hue = {fam: sum(h for _, (h, _, _) in self.jb[fam]) / len(STEPS) for fam in FAMILIES + ["pink"]}
        self.hue["red"] = 356  # the red ramp wraps around 0
        self.target = {"gray": self._gray()}
        for fam in FAMILIES + ["pink"]:
            self.target[fam] = self._chroma(fam)
        if self.dark:
            self.white = self._neutral_at(98.5)
            self.black = tuple(self.pal["bg_deep"])
        else:
            self.white = tuple(self.pal["bg_0"])
            self.black = tuple(self.pal["fg"])

    def _neutral_at(self, lum):
        anchors = sorted((self.pal[n] for n in NEUTRALS), key=lambda x: x[2])
        if lum <= anchors[0][2]:
            return (anchors[0][0], anchors[0][1], lum)
        for a, b in zip(anchors, anchors[1:]):
            if a[2] <= lum <= b[2]:
                t = 0 if b[2] == a[2] else (lum - a[2]) / (b[2] - a[2])
                return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, lum)
        return (anchors[-1][0], anchors[-1][1], lum)

    def _gray(self):
        out = []
        for step in STEPS:
            spec = GRAY_SPEC[self.variant][step]
            out.append((step, tuple(self.pal[spec]) if isinstance(spec, str) else self._neutral_at(spec)))
        return out

    def _chroma(self, fam):
        h, s, _ = self.pal[FAMILY_ACCENT[fam]]
        cap = s + (5 if self.dark else 0)
        return [(step, (h, min(jb_s, cap), jb_l)) for step, (_, jb_s, jb_l) in self.jb[fam]]

    def named_colors(self):
        out = {}
        for fam in ["gray"] + FAMILIES:
            for step, hsl in self.target[fam]:
                out[f"{fam}-{step}"] = hsl_to_hex(hsl).upper()
        return out

    def family_of(self, hex_):
        r, g, b = rgb(hex_)
        if max(r, g, b) - min(r, g, b) < 18:
            return "gray"
        h, _, _ = hex_to_hsl(hex_)
        return min(self.hue, key=lambda fam: min(abs(h - self.hue[fam]), 360 - abs(h - self.hue[fam])))

    def remap_hsl(self, hex_):
        """Map a JetBrains color onto the equivalent position of the meowsoot ramps (lightness-preserving)."""
        fam = self.family_of(hex_)
        _, _, lum = hex_to_hsl(hex_)
        src = [hsl for _, hsl in self.jb[fam]]
        dst = [hsl for _, hsl in self.target[fam]]
        if fam == "gray":
            src = [(0, 0, 0)] + src + [(0, 0, 100)]
            dst = [self.black] + dst + [self.white]
        if lum <= src[0][2]:
            return dst[0]
        for i in range(len(src) - 1):
            a, b = src[i][2], src[i + 1][2]
            if a <= lum <= b:
                t = 0 if b == a else (lum - a) / (b - a)
                return lerp_hsl(dst[i], dst[i + 1], t)
        return dst[-1]

    def remap(self, value):
        """Re-map '#RRGGBB[AA]' / 'RRGGBB' preserving the alpha suffix and the '#' style."""
        if not isinstance(value, str):
            return value
        m = re.fullmatch(r"(#?)([0-9A-Fa-f]{6})([0-9A-Fa-f]{2})?", value.strip())
        if not m:
            return value
        new = hsl_to_hex(self.remap_hsl("#" + m.group(2)))
        return (m.group(1) or "") + new.lstrip("#").upper() + (m.group(3) or "").upper()

    def remap_fg(self, value):
        """Re-map a syntax foreground onto the closest meowsoot accent (keeps code legible and pastel)."""
        hex_ = "#" + value.lstrip("#").rjust(6, "0")
        fam = self.family_of(hex_)
        if fam == "gray":
            return self.remap(hex_)
        _, _, lum = hex_to_hsl(hex_)
        if (self.dark and lum > 45) or (not self.dark and lum < 60):
            return self.c[FAMILY_ACCENT[fam]]
        return self.remap(hex_)


# --------------------------------------------------------------------------------------------------
# Reading the parent themes/schemes from the IDE
# --------------------------------------------------------------------------------------------------


class Ide:
    def __init__(self, path, plugin_dirs):
        self.jars = sorted(glob.glob(os.path.join(path, "lib", "*.jar")))
        self.jars += sorted(glob.glob(os.path.join(path, "plugins", "*", "lib", "**", "*.jar"), recursive=True))
        for d in plugin_dirs:
            self.jars += sorted(glob.glob(os.path.join(d, "*", "lib", "**", "*.jar"), recursive=True))
        self._index = None

    def index(self):
        if self._index is None:
            self._index = {}
            for jar in self.jars:
                try:
                    with zipfile.ZipFile(jar) as z:
                        for n in z.namelist():
                            self._index.setdefault(n, jar)
                except zipfile.BadZipFile:
                    pass
        return self._index

    def read(self, name):
        name = name.lstrip("/")
        jar = self.index().get(name)
        if not jar:
            raise FileNotFoundError(name)
        with zipfile.ZipFile(jar) as z:
            return z.read(name)

    def theme(self, name):
        return json.loads(self.read(name))

    def additional_attributes(self, scheme):
        """Files registered through <additionalTextAttributes scheme="..."> in plugin descriptors."""
        tag = re.compile(rb"<additionalTextAttributes\b[^>]*>")
        files = []
        for jar in self.jars:
            try:
                with zipfile.ZipFile(jar) as z:
                    for n in z.namelist():
                        if not n.endswith(".xml") or not (n.startswith("META-INF/") or "/" not in n):
                            continue
                        data = z.read(n)
                        if b"additionalTextAttributes" not in data:
                            continue
                        for t in tag.findall(data):
                            s = re.search(rb'scheme="([^"]+)"', t)
                            f = re.search(rb'file="([^"]+)"', t)
                            if s and f and s.group(1).decode() == scheme:
                                files.append(f.group(1).decode())
            except zipfile.BadZipFile:
                pass
        return files


def parse_scheme(data):
    el = ET.fromstring(data)
    if el.tag != "scheme":
        found = el.find(".//scheme")
        el = found if found is not None else el
    colors = {o.get("name"): o.get("value") or "" for o in el.findall("./colors/option")}
    attrs = {}
    for o in el.findall("./attributes/option"):
        d = {}
        if o.get("baseAttributes"):
            d["base"] = o.get("baseAttributes")
        v = o.find("value")
        if v is not None:
            for x in v.findall("option"):
                d[x.get("name")] = x.get("value")
        attrs[o.get("name")] = d
    return colors, attrs


def parent_scheme(ide, base_name, extra_files):
    root = ET.fromstring(ide.read("DefaultColorSchemesManager.xml"))
    base = next(s for s in root.findall("scheme") if s.get("name") == base_name)
    colors, attrs = parse_scheme(ET.tostring(base))
    for f in ide.additional_attributes(base_name) + extra_files:
        try:
            c, a = parse_scheme(ide.read(f))
        except (FileNotFoundError, ET.ParseError):
            print(f"  skipped {f}", file=sys.stderr)
            continue
        colors.update(c)
        attrs.update(a)
    return colors, attrs


def flatten(ui, prefix=""):
    out = {}
    for k, v in ui.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict) and not any(x.startswith("os.") for x in v):
            out.update(flatten(v, key))
        else:
            out[key] = v
    return out


# --------------------------------------------------------------------------------------------------
# UI theme
# --------------------------------------------------------------------------------------------------

THEME_CHAINS = {
    True: ["themes/darcula.theme.json", "themes/expUI/expUI_dark.theme.json",
           "themes/islands/ManyIslandsDark.theme.json"],
    False: ["themes/intellijlaf.theme.json", "themes/expUI/expUI_light.theme.json",
            "themes/expUI/expUI_light_with_light_header.theme.json", "themes/islands/ManyIslandsLight.theme.json"],
}
RAMP_RE = re.compile(r"(gray|blue|green|red|yellow|orange|purple|teal)-\d+")
HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?")

# Colors used in the New UI icons (lib/intellij.platform.ide.jar, expui/**.svg).
ICON_COLORS = {
    True: ["#548AF7", "#3574F0", "#25324D", "#43454A", "#DB5C5C", "#E55765", "#402929", "#57965C", "#5FAD65",
           "#253627", "#F2C55C", "#D6AE58", "#3D3223", "#C77D55", "#E08855", "#45322B", "#B589EC", "#A571E6",
           "#2F2936", "#868A91", "#6F737A", "#9DA0A8"],
    False: ["#3574F0", "#4682FA", "#EBECF0", "#DB3B4B", "#E55765", "#208A3C", "#369650", "#55A76A", "#E66D17",
            "#FFAF0F", "#C27D04", "#834DF0", "#F2FCF3", "#EDF3FF", "#FFF7F7", "#FFF4EB", "#E7EFFD", "#FFFAEB",
            "#FAF5FF", "#A8ADBD", "#818594"],
}


def with_alpha(hex_, a):
    return "%s%02X" % (hex_.upper(), _round(a * 255))


def build_theme(variant, ide):
    meta = VARIANTS[variant]
    dark = meta["dark"]
    chain = [ide.theme(n) for n in THEME_CHAINS[dark]]
    r = Ramps(variant, chain[-1]["colors"])
    c = r.c

    merged_colors, merged_ui = {}, {}
    for t in chain:
        merged_colors.update(t.get("colors", {}))
        merged_ui.update(flatten(t.get("ui", {})))

    # 1. Named palette: Islands ramps rebuilt from meowsoot, every other hard-coded named color re-mapped.
    colors = {}
    for name, value in merged_colors.items():
        if isinstance(value, str) and HEX_RE.fullmatch(value) and not RAMP_RE.fullmatch(name):
            colors[name] = r.remap(value)
    colors.update(r.named_colors())
    colors["white"] = hsl_to_hex(r.white).upper()
    colors["black"] = hsl_to_hex(r.black).upper()

    # 2. meowsoot semantics on top of the Islands token layer. Pink is the brand accent.
    pink, bg0 = c["pink"], c["bg_0"]

    def tint(col, a):
        return blend(col, a, bg0)

    sem = {
        "text-default": c["fg"],
        "text-muted": c["fg_mute"],
        "text-secondary": c["comment"],
        "text-link": c["cyan"],
        "text-error": c["red"],
        "text-warning": c["yellow"] if dark else c["yellow_br"],
        "text-success": c["green"],
        "editor-text": c["fg"],
        "accent-brand-bg": pink,
        "accent-brand-border": pink,
        "accent-brand-bg-secondary": tint(pink, 0.16 if dark else 0.08),
        "accent-brand-border-secondary": tint(pink, 0.45 if dark else 0.3),
        "accent-error-bg": c["red"],
        "accent-error-border": c["red"],
        "accent-error-bg-secondary": tint(c["red"], 0.16 if dark else 0.08),
        "accent-error-border-secondary": tint(c["red"], 0.45 if dark else 0.3),
        "accent-warning-bg": c["yellow"],
        "accent-warning-border": c["yellow"],
        "accent-warning-bg-secondary": tint(c["yellow"], 0.16 if dark else 0.08),
        "accent-warning-border-secondary": tint(c["yellow"], 0.45 if dark else 0.3),
        "accent-success-bg": c["green"],
        "accent-success-border": c["green"],
        "accent-success-bg-secondary": tint(c["green"], 0.16 if dark else 0.08),
        "accent-success-border-secondary": tint(c["green"], 0.45 if dark else 0.3),
        "accent-ai-bg": tint(c["lavender"], 0.14 if dark else 0.08),
        "accent-ai-border": tint(c["lavender"], 0.5),
        "selection-bg-active": tint(pink, 0.24 if dark else 0.16),
        "selection-bg-active-muted": tint(pink, 0.14 if dark else 0.09),
        "selection-bg-inactive": c["bg_3"] if dark else c["bg_1"],
        "tab-selected-bg-active": tint(pink, 0.14 if dark else 0.09),
        "tab-selected-border-active": pink,
        "toolbar-selected-bg": tint(pink, 0.3 if dark else 0.2),
        "toolbar-selected-bg-hovered": tint(pink, 0.38 if dark else 0.27),
        "popup-completion-match-text": pink,
        "search-match-bg": c["yellow"] if dark else tint(c["yellow"], 0.3),
        "icon-green-stroke": c["green"],
        "text-over-accent": bg0,
        "icon-over-accent": bg0,
        "tab-file-color-mask-bg": with_alpha(bg0, 0.5),
    }
    if dark:
        sem.update({
            "main-window-bg": c["bg_deep"],
            "main-window-bg-alt": c["bg_2"],
            "got-it-bg": tint(pink, 0.3),
            "got-it-border": tint(pink, 0.45),
            "got-it-text-link": c["cyan_br"],
            "presentation-assistant-bg": tint(pink, 0.3),
        })
    else:
        sem.update({
            "layer-2-bg": c["bg_0"],
            "main-window-bg-alt": c["bg_1"],
            "tool-window-bg-alt": c["bg_2"],
            "editor-border-alt": c["bg_1"],
            "presentation-assistant-bg": c["fg_mute"],
        })
    colors.update({k: v.upper() for k, v in sem.items()})

    # 3. UI keys: re-map hard-coded parent values, then meowsoot-specific overrides.
    # Inherited UI keys that reference named colors are NOT re-resolved against this theme's color map
    # (the IDE keeps the parent's resolution), so every color-valued key of the chain is re-declared here.
    def ui_color(v):
        if isinstance(v, str):
            if HEX_RE.fullmatch(v):
                return r.remap(v)
            if v in merged_colors or v in colors:
                return v
        elif isinstance(v, dict):
            out = {k: ui_color(x) for k, x in v.items()}
            if any(x is not None for x in out.values()):
                return {k: v[k] if out[k] is None else out[k] for k in v}
        return None

    ui = {k: nv for k, v in merged_ui.items() if (nv := ui_color(v)) is not None}
    ui.update({
        # these use text/icon-over-accent but sit on a subtle tint rather than on the brand color
        "SearchEverywhere.Tab.selectedForeground": c["fg"],
        "PresentationAssistant.Bright.Popup.foreground": c["fg"] if dark else bg0,
        "PresentationAssistant.Pale.Popup.foreground": c["fg"],
        "ParameterInfo.currentParameterForeground": c["fg"],
        "ToolWindow.Button.selectedForeground": c["fg"],
        "GotItTooltip.iconBorderColor": c["fg"],
        "Tooltip.Learning.iconBorderColor": c["fg"],
        "MainWindow.Tab.background": c["bg_deep"] if dark else c["bg_1"],
        "Editor.ToolTip.selectionBackground": c["bg_3"],
        "EditorTabs.underlineColor": pink,
        "EditorTabs.inactiveUnderlineColor": c["fg_faint"],
        "Component.focusColor": tint(pink, 0.6),
        "Component.focusedBorderColor": tint(pink, 0.6),
        "Link.activeForeground": c["cyan"],
        "Link.hoverForeground": c["cyan_br"],
        "Link.pressedForeground": c["cyan_br"],
        "Link.visitedForeground": c["lavender"],
        "Link.secondaryForeground": c["fg_faint"],
        "Counter.background": pink,
        "Counter.foreground": bg0,
        "ProgressBar.progressColor": pink,
        "ProgressBar.indeterminateStartColor": tint(pink, 0.5),
        "ProgressBar.indeterminateEndColor": pink,
        "ProgressBar.passedColor": c["green"],
        "ProgressBar.passedEndColor": tint(c["green"], 0.5),
        "ProgressBar.failedColor": c["red"],
        "ProgressBar.failedEndColor": tint(c["red"], 0.5),
        "VersionControl.GitLog.headIconColor": c["yellow"],
        "VersionControl.GitLog.localBranchIconColor": c["green"],
        "VersionControl.GitLog.remoteBranchIconColor": c["lavender"],
        "VersionControl.GitLog.tagIconColor": c["fg_mute"],
        "VersionControl.GitLog.otherIconColor": c["fg_faint"],
        "FileColor.Blue": tint(c["blue"], 0.14),
        "FileColor.Green": tint(c["green"], 0.14),
        "FileColor.Orange": tint(c["peach"], 0.14),
        "FileColor.Rose": tint(c["pink"], 0.14),
        "FileColor.Violet": tint(c["lavender"], 0.14),
        "FileColor.Yellow": tint(c["yellow"], 0.14),
        "FileColor.Gray": c["bg_2"],
    })
    ui = {k: (v.upper() if isinstance(v, str) and v.startswith("#") else v) for k, v in ui.items()}

    # 4. Icons: re-map the colors used by the New UI icon set; checkboxes/radios use the brand accent.
    palette = {h: r.remap(h) for h in ICON_COLORS[dark]}
    palette["#CED0D6" if dark else "#6C707E"] = "icon-default-stroke"
    checkbox = {
        "Checkbox.Background.Default": c["bg_0"],
        "Checkbox.Border.Default": c["bg_4"] if dark else c["fg_faint"],
        "Checkbox.Background.Selected": pink,
        "Checkbox.Border.Selected": pink,
        "Checkbox.Foreground.Selected": bg0,
        "Checkbox.Focus.Wide": tint(pink, 0.6),
        "Checkbox.Background.Disabled": c["bg_1"],
        "Checkbox.Border.Disabled": c["bg_3"],
        "Checkbox.Foreground.Disabled": c["fg_faint"],
    }
    palette.update({k: v.upper() for k, v in checkbox.items()})

    return {
        "name": f"Meowsoot {meta['title']}",
        "dark": dark,
        "author": "Meowsoot contributors",
        "parentTheme": "Islands Dark" if dark else "Islands Light",
        "editorScheme": f"/themes/meowsoot-{variant}.xml",
        "colors": dict(sorted(colors.items())),
        "ui": dict(sorted(ui.items())),
        "icons": {"ColorPalette": dict(sorted(palette.items()))},
    }


# --------------------------------------------------------------------------------------------------
# Editor color scheme
# --------------------------------------------------------------------------------------------------

BOLD, ITALIC, BOLD_ITALIC = 1, 2, 3
BOXED, UNDERLINE, WAVE, STRIKE, BOLD_UNDERLINE, DOTTED = 0, 1, 2, 3, 4, 5


def A(fg=None, bg=None, font=None, effect=None, etype=None, stripe=None):
    d = {}
    if fg:
        d["FOREGROUND"] = fg
    if bg:
        d["BACKGROUND"] = bg
    if font:
        d["FONT_TYPE"] = str(font)
    if effect:
        d["EFFECT_COLOR"] = effect
        d["EFFECT_TYPE"] = str(UNDERLINE if etype is None else etype)
    if stripe:
        d["ERROR_STRIPE_COLOR"] = stripe
    return d


def B(base):
    return {"base": base}


def scheme_colors(c):
    def t(col, a):
        return blend(col, a, c["bg_0"])

    return {
        "CARET_COLOR": c["pink"],
        "CARET_ROW_COLOR": c["bg_2"],
        "SELECTION_BACKGROUND": c["bg_3"],
        "SELECTION_FOREGROUND": "",
        "GUTTER_BACKGROUND": c["bg_0"],
        "EDITOR_GUTTER_BACKGROUND": "",
        "CONSOLE_BACKGROUND_KEY": c["bg_0"],
        "LINE_NUMBERS_COLOR": c["fg_faint"],
        "LINE_NUMBER_ON_CARET_ROW_COLOR": c["fg"],
        "INDENT_GUIDE": c["indent"],
        "SELECTED_INDENT_GUIDE": t(c["fg_faint"], 0.7),
        "MATCHED_BRACES_INDENT_GUIDE_COLOR": t(c["lavender"], 0.5),
        "VISUAL_INDENT_GUIDE": c["bg_2"],
        "STRING_CONTENT_INDENT_GUIDE": c["bg_2"],
        "RIGHT_MARGIN_COLOR": c["bg_2"],
        "WHITESPACES": c["bg_4"],
        "WHITESPACES_MODIFIED_LINES_COLOR": t(c["peach"], 0.4),
        "METHOD_SEPARATORS_COLOR": c["bg_3"],
        "TEARLINE_COLOR": c["bg_3"],
        "SELECTED_TEARLINE_COLOR": c["fg_faint"],
        "FOLDED_TEXT_BORDER_COLOR": c["bg_3"],
        "LOOKUP_COLOR": c["bg_1"],
        "DOCUMENTATION_COLOR": c["bg_1"],
        "NOTIFICATION_BACKGROUND": c["bg_1"],
        "PROMOTION_PANE": c["bg_1"],
        "QUESTION_HINT": c["diff_change"],
        "INFORMATION_HINT": c["bg_1"],
        "ERROR_HINT": c["diff_delete"],
        "HINT_BORDER": c["bg_4"],
        "ADDED_LINES_COLOR": c["green"],
        "MODIFIED_LINES_COLOR": c["blue"],
        "DELETED_LINES_COLOR": c["red"],
        "IGNORED_ADDED_LINES_BORDER_COLOR": c["green"],
        "IGNORED_MODIFIED_LINES_BORDER_COLOR": c["blue"],
        "IGNORED_DELETED_LINES_BORDER_COLOR": c["red"],
        "REVIEW_CHANGED_LINES_COLOR": c["lavender"],
        "ANNOTATIONS_COLOR": c["fg_faint"],
        "ANNOTATIONS_LAST_COMMIT_COLOR": c["fg"],
        "VCS_ANNOTATIONS_COLOR_1": t(c["lavender"], 0.40),
        "VCS_ANNOTATIONS_COLOR_2": t(c["lavender"], 0.30),
        "VCS_ANNOTATIONS_COLOR_3": t(c["lavender"], 0.22),
        "VCS_ANNOTATIONS_COLOR_4": t(c["lavender"], 0.14),
        "VCS_ANNOTATIONS_COLOR_5": t(c["lavender"], 0.07),
        "FILESTATUS_ADDED": c["green"],
        "FILESTATUS_COPIED": c["green"],
        "FILESTATUS_addedOutside": c["green"],
        "FILESTATUS_MODIFIED": c["blue"],
        "FILESTATUS_RENAMED": c["blue"],
        "FILESTATUS_modifiedOutside": c["blue"],
        "FILESTATUS_NOT_CHANGED_IMMEDIATE": c["blue"],
        "FILESTATUS_NOT_CHANGED_RECURSIVE": c["blue"],
        "FILESTATUS_DELETED": c["fg_faint"],
        "FILESTATUS_IDEA_FILESTATUS_DELETED_FROM_FILE_SYSTEM": c["fg_faint"],
        "FILESTATUS_IDEA_FILESTATUS_IGNORED": c["peach_dim"],
        "FILESTATUS_MERGED": c["lavender"],
        "FILESTATUS_IDEA_FILESTATUS_MERGED_WITH_CONFLICTS": c["red"],
        "FILESTATUS_IDEA_FILESTATUS_MERGED_WITH_BOTH_CONFLICTS": c["red"],
        "FILESTATUS_IDEA_FILESTATUS_MERGED_WITH_PROPERTY_CONFLICTS": c["red"],
        "FILESTATUS_changelistConflict": c["red"],
        "FILESTATUS_UNKNOWN": c["peach"],
        "MODIFIED_TAB_ICON": c["pink"],
        "DOC_COMMENT_GUIDE": c["bg_3"],
        "DOC_COMMENT_LINK": c["cyan"],
        "RECENT_LOCATIONS_SELECTION": c["bg_2"],
        "INLINE_REFACTORING_SETTINGS_DEFAULT": c["bg_3"],
        "INLINE_REFACTORING_SETTINGS_FOCUSED": c["bg_3"],
        "INLINE_REFACTORING_SETTINGS_HOVERED": c["bg_3"],
        "DIFF_SEPARATORS_BACKGROUND": c["bg_1"],
        "READONLY_FRAGMENT_BACKGROUND": c["bg_1"],
    }


def scheme_attrs(c):
    def t(col, a):
        return blend(col, a, c["bg_0"])

    fg, mute, faint, comment = c["fg"], c["fg_mute"], c["fg_faint"], c["comment"]
    pink, lav, cyan, peach = c["pink"], c["lavender"], c["cyan"], c["peach"]
    yellow, blue, red, green = c["yellow"], c["blue"], c["red"], c["green"]
    peach_dim, peach_br = c["peach_dim"], c["peach_br"]
    rb = c["rainbow"]
    underline_faint = t(faint, 0.8)
    a = {
        # ---- base ------------------------------------------------------------------------------
        "TEXT": A(fg, c["bg_0"]),
        "DEFAULT_IDENTIFIER": A(fg),
        "DEFAULT_KEYWORD": A(cyan),
        "DEFAULT_STRING": A(yellow),
        "DEFAULT_VALID_STRING_ESCAPE": A(peach),
        "DEFAULT_INVALID_STRING_ESCAPE": A(red, effect=red, etype=WAVE),
        "DEFAULT_NUMBER": A(peach_dim),
        "DEFAULT_CONSTANT": A(peach),
        "DEFAULT_PREDEFINED_SYMBOL": A(cyan, font=ITALIC),
        "DEFAULT_LINE_COMMENT": A(comment, font=ITALIC),
        "DEFAULT_BLOCK_COMMENT": A(comment, font=ITALIC),
        "DEFAULT_DOC_COMMENT": A(comment, font=ITALIC),
        "DEFAULT_DOC_COMMENT_TAG": A(mute, font=BOLD_ITALIC),
        "DEFAULT_DOC_COMMENT_TAG_VALUE": A(mute, font=ITALIC),
        "DEFAULT_DOC_MARKUP": A(mute, font=ITALIC),
        "DEFAULT_OPERATION_SIGN": A(faint),
        "DEFAULT_PARENTHS": A(faint),
        "DEFAULT_BRACES": A(faint),
        "DEFAULT_BRACKETS": A(faint),
        "DEFAULT_COMMA": A(faint),
        "DEFAULT_SEMICOLON": A(faint),
        "DEFAULT_DOT": A(faint),
        "DEFAULT_FUNCTION_DECLARATION": A(pink),
        "DEFAULT_FUNCTION_CALL": A(pink),
        "DEFAULT_INSTANCE_METHOD": B("DEFAULT_FUNCTION_CALL"),
        "DEFAULT_STATIC_METHOD": B("DEFAULT_FUNCTION_CALL"),
        "DEFAULT_CLASS_NAME": A(lav),
        "DEFAULT_CLASS_REFERENCE": A(lav),
        "DEFAULT_INTERFACE_NAME": A(lav),
        "DEFAULT_LOCAL_VARIABLE": A(fg),
        "DEFAULT_REASSIGNED_LOCAL_VARIABLE": A(fg, effect=underline_faint, etype=UNDERLINE),
        "DEFAULT_PARAMETER": A(fg, font=ITALIC),
        "DEFAULT_REASSIGNED_PARAMETER": A(fg, font=ITALIC, effect=underline_faint, etype=UNDERLINE),
        "DEFAULT_INSTANCE_FIELD": A(fg),
        "DEFAULT_STATIC_FIELD": A(peach),
        "DEFAULT_GLOBAL_VARIABLE": A(fg),
        "DEFAULT_LABEL": A(cyan),
        "DEFAULT_METADATA": A(peach_br, font=ITALIC),
        "DEFAULT_ATTRIBUTE": A(fg, font=ITALIC),
        "DEFAULT_TAG": A(cyan),
        "DEFAULT_ENTITY": A(peach),
        "DEFAULT_TEMPLATE_LANGUAGE_COLOR": A(bg=c["bg_1"]),
        "DEFAULT_HIGHLIGHTED_REFERENCE": A(effect=faint, etype=UNDERLINE),
        "CUSTOM_KEYWORD1_ATTRIBUTES": A(cyan),
        "CUSTOM_KEYWORD2_ATTRIBUTES": A(pink),
        "CUSTOM_KEYWORD3_ATTRIBUTES": A(lav),
        "CUSTOM_KEYWORD4_ATTRIBUTES": A(peach),
        "CUSTOM_STRING_ATTRIBUTES": B("DEFAULT_STRING"),
        "CUSTOM_VALID_STRING_ESCAPE_ATTRIBUTES": B("DEFAULT_VALID_STRING_ESCAPE"),
        "CUSTOM_INVALID_STRING_ESCAPE_ATTRIBUTES": B("DEFAULT_INVALID_STRING_ESCAPE"),
        "CUSTOM_LINE_COMMENT_ATTRIBUTES": B("DEFAULT_LINE_COMMENT"),
        "CUSTOM_MULTI_LINE_COMMENT_ATTRIBUTES": B("DEFAULT_BLOCK_COMMENT"),
        "CUSTOM_NUMBER_ATTRIBUTES": B("DEFAULT_NUMBER"),
        "DOC_CODE_BLOCK": A(fg, c["bg_1"], effect=c["bg_3"], etype=BOXED),
        "DOC_CODE_INLINE": A(lav, c["bg_1"]),
        "DOC_TIPS_SHORTCUT": A(fg, effect=faint, etype=BOXED),
        # ---- diagnostics -----------------------------------------------------------------------
        "ERRORS_ATTRIBUTES": A(effect=red, etype=WAVE, stripe=red),
        "WARNING_ATTRIBUTES": A(effect=yellow, etype=WAVE, stripe=yellow),
        "INFO_ATTRIBUTES": A(effect=t(yellow, 0.55), etype=WAVE, stripe=t(yellow, 0.55)),
        "GENERIC_SERVER_ERROR_OR_WARNING": A(effect=peach, etype=WAVE, stripe=peach),
        "WRONG_REFERENCES_ATTRIBUTES": A(red),
        "NOT_USED_ELEMENT_ATTRIBUTES": A(faint),
        "DEPRECATED_ATTRIBUTES": A(effect=mute, etype=STRIKE),
        "MARKED_FOR_REMOVAL_ATTRIBUTES": A(effect=red, etype=STRIKE),
        "TYPO": A(effect=cyan, etype=WAVE),
        "GRAMMAR_ERROR": A(effect=blue, etype=WAVE),
        "TEXT_STYLE_ERROR": A(effect=red, etype=DOTTED),
        "TEXT_STYLE_WARNING": A(effect=yellow, etype=DOTTED),
        "TEXT_STYLE_SUGGESTION": A(effect=cyan, etype=DOTTED),
        "RUNTIME_ERROR": A(effect=red, etype=DOTTED, stripe=red),
        "BAD_CHARACTER": A(red, effect=red, etype=WAVE),
        "Unresolved reference access": A(faint, effect=faint, etype=DOTTED),
        # ---- editor UI -------------------------------------------------------------------------
        "MATCHED_BRACE_ATTRIBUTES": A(lav, c["bg_3"], font=BOLD),
        "UNMATCHED_BRACE_ATTRIBUTES": A(red, c["diff_delete"], font=BOLD),
        "MATCHED_TAG_NAME": A(bg=c["bg_3"]),
        "TODO_DEFAULT_ATTRIBUTES": A(peach, font=BOLD_ITALIC, stripe=peach),
        "IDENTIFIER_UNDER_CARET_ATTRIBUTES": A(bg=c["bg_3"], stripe=lav),
        "WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES": A(bg=t(pink, 0.2), stripe=pink),
        "SEARCH_RESULT_ATTRIBUTES": A(bg=c["bg_search"], stripe=yellow),
        "WRITE_SEARCH_RESULT_ATTRIBUTES": A(bg=c["bg_search_current"], stripe=peach),
        "TEXT_SEARCH_RESULT_ATTRIBUTES": A(bg=c["bg_search"], stripe=yellow),
        "FOLDED_TEXT_ATTRIBUTES": A(mute, c["bg_1"]),
        "INLAY_DEFAULT": A(faint, c["bg_1"], font=ITALIC),
        "INLAY_TEXT_WITHOUT_BACKGROUND": A(faint, font=ITALIC),
        "INLINE_PARAMETER_HINT": A(faint, c["bg_1"], font=ITALIC),
        "INLINE_PARAMETER_HINT_HIGHLIGHTED": A(fg, c["bg_3"], font=ITALIC),
        "INLINE_PARAMETER_HINT_CURRENT": A(pink, t(pink, 0.18), font=ITALIC),
        "INLINE_SUGGESTION": A(faint, font=ITALIC),
        "HYPERLINK_ATTRIBUTES": A(cyan, effect=cyan, etype=UNDERLINE),
        "FOLLOWED_HYPERLINK_ATTRIBUTES": A(lav, effect=lav, etype=UNDERLINE),
        "INACTIVE_HYPERLINK_ATTRIBUTES": A(effect=faint, etype=UNDERLINE),
        "CTRL_CLICKABLE": A(cyan, effect=cyan, etype=UNDERLINE),
        "BREAKPOINT_ATTRIBUTES": A(bg=c["diff_delete"], stripe=red),
        "EXECUTIONPOINT_ATTRIBUTES": A(bg=t(blue, 0.32)),
        "NOT_TOP_FRAME_ATTRIBUTES": A(bg=c["diff_change"]),
        "INJECTED_LANGUAGE_FRAGMENT": A(bg=c["bg_1"]),
        "LIVE_TEMPLATE_ATTRIBUTES": A(effect=pink, etype=BOXED),
        "LIVE_TEMPLATE_INACTIVE_SEGMENT": A(effect=faint, etype=BOXED),
        "TEMPLATE_VARIABLE_ATTRIBUTES": A(lav),
        "BOOKMARKS_ATTRIBUTES": A(stripe=lav),
        "BREADCRUMBS_DEFAULT": A(mute),
        "BREADCRUMBS_CURRENT": A(fg, c["bg_3"]),
        "BREADCRUMBS_HOVERED": A(fg, c["bg_3"]),
        "BREADCRUMBS_INACTIVE": A(faint),
        "DEBUGGER_INLINED_VALUES": A(faint, font=ITALIC),
        "DEBUGGER_INLINED_VALUES_MODIFIED": A(peach, font=ITALIC),
        "DEBUGGER_INLINED_VALUES_EXECUTION_LINE": A(blue, font=ITALIC),
        "DIFF_INSERTED": A(bg=c["diff_add"], stripe=green),
        "DIFF_MODIFIED": A(bg=c["diff_change"], stripe=blue),
        "DIFF_DELETED": A(bg=c["diff_delete"], stripe=red),
        "DIFF_CONFLICT": A(bg=t(peach, 0.18), stripe=peach),
        # ---- console ---------------------------------------------------------------------------
        "CONSOLE_NORMAL_OUTPUT": A(fg),
        "CONSOLE_ERROR_OUTPUT": A(red),
        "CONSOLE_SYSTEM_OUTPUT": A(mute),
        "CONSOLE_USER_INPUT": A(cyan, font=ITALIC),
        "LOG_ERROR_OUTPUT": A(red),
        "LOG_WARNING_OUTPUT": A(yellow),
        "LOG_INFO_OUTPUT": A(blue),
        "LOG_VERBOSE_OUTPUT": A(mute),
        "LOG_DEBUG_OUTPUT": A(faint),
        "LOG_EXPIRED_ENTRY": A(faint),
        **{f"RAINBOW_COLOR{i}": A(rb[i]) for i in range(5)},
        # ---- Java ------------------------------------------------------------------------------
        "ENUM_CONST": A(peach),
        "STATIC_FINAL_FIELD_ATTRIBUTES": A(peach),
        "STATIC_FIELD_ATTRIBUTES": B("DEFAULT_STATIC_FIELD"),
        "STATIC_METHOD_ATTRIBUTES": B("DEFAULT_STATIC_METHOD"),
        "CONSTRUCTOR_CALL_ATTRIBUTES": A(lav),
        "CONSTRUCTOR_DECLARATION_ATTRIBUTES": A(lav),
        "TYPE_PARAMETER_NAME_ATTRIBUTES": A(lav, font=ITALIC),
        "ANNOTATION_NAME_ATTRIBUTES": B("DEFAULT_METADATA"),
        "ANNOTATION_ATTRIBUTE_NAME_ATTRIBUTES": A(fg, font=ITALIC),
        "IMPLICIT_ANONYMOUS_CLASS_PARAMETER_ATTRIBUTES": A(fg, effect=underline_faint, etype=UNDERLINE),
        # ---- Kotlin ----------------------------------------------------------------------------
        "KOTLIN_LABEL": A(cyan),
        "KOTLIN_NAMED_ARGUMENT": A(mute),
        "KOTLIN_CONSTRUCTOR": A(lav),
        "KOTLIN_ENUM_ENTRY": A(peach),
        "KOTLIN_TYPE_PARAMETER": B("TYPE_PARAMETER_NAME_ATTRIBUTES"),
        "KOTLIN_CLOSURE_DEFAULT_PARAMETER": A(cyan, font=ITALIC),
        "KOTLIN_PACKAGE_FUNCTION_CALL": B("DEFAULT_FUNCTION_CALL"),
        "KOTLIN_FUNCTION_LITERAL_BRACES_AND_ARROW": A(faint, font=BOLD),
        "KOTLIN_MUTABLE_VARIABLE": A(effect=underline_faint, etype=UNDERLINE),
        "KOTLIN_BACKING_FIELD_VARIABLE": A(fg),
        "KOTLIN_SMART_CAST_VALUE": A(bg=t(cyan, 0.12)),
        "KOTLIN_SMART_CAST_RECEIVER": A(bg=t(cyan, 0.12)),
        "KOTLIN_SMART_CONSTANT": A(bg=t(cyan, 0.12)),
        "KOTLIN_EXCLEXCL": A(red, font=BOLD),
        # ---- Scala -----------------------------------------------------------------------------
        "Scala Type Alias": A(lav),
        "Scala Type parameter": A(lav, font=ITALIC),
        "Scala Named Argument": A(mute),
        "Interpolated String Injection": A(peach),
        # ---- JavaScript / TypeScript -----------------------------------------------------------
        "JS.GLOBAL_VARIABLE": B("DEFAULT_GLOBAL_VARIABLE"),
        "JS.GLOBAL_FUNCTION": B("DEFAULT_FUNCTION_DECLARATION"),
        "JS.INSTANCE_MEMBER_FUNCTION": B("DEFAULT_INSTANCE_METHOD"),
        "JS.LOCAL_VARIABLE": B("DEFAULT_LOCAL_VARIABLE"),
        "JS.PARAMETER": B("DEFAULT_PARAMETER"),
        "JS.REGEXP": A(yellow),
        "JS.DECORATOR": B("DEFAULT_METADATA"),
        "JS.JSX_CLIENT_COMPONENT": A(lav),
        "TS.TYPE_PARAMETER": A(lav, font=ITALIC),
        "TS.MODULE_NAME": A(lav),
        "COFFEESCRIPT.GLOBAL_VARIABLE": B("DEFAULT_GLOBAL_VARIABLE"),
        # ---- Python ----------------------------------------------------------------------------
        "PY.SELF_PARAMETER": A(cyan, font=ITALIC),
        "PY.KEYWORD_ARGUMENT": A(mute),
        "PY.BUILTIN_NAME": A(pink, font=ITALIC),
        "PY.PREDEFINED_DEFINITION": A(pink, font=ITALIC),
        "PY.PREDEFINED_USAGE": A(pink, font=ITALIC),
        "PY.DECORATOR": A(peach_br, font=ITALIC),
        "PY.ANNOTATION": A(lav),
        # ---- Go --------------------------------------------------------------------------------
        "GO_BUILTIN_FUNCTION_CALL": A(pink, font=ITALIC),
        "GO_BUILTIN_TYPE_REFERENCE": A(lav, font=ITALIC),
        "GO_BUILTIN_CONSTANT": A(peach),
        "GO_BUILTIN_VARIABLE": A(cyan, font=ITALIC),
        "GO_PACKAGE": A(lav),
        "GO_METHOD_RECEIVER": A(cyan, font=ITALIC),
        "GO_PACKAGE_EXPORTED_CONSTANT": A(peach),
        "GO_PACKAGE_LOCAL_CONSTANT": A(peach),
        "GO_LOCAL_CONSTANT": A(peach),
        # ---- Rust ------------------------------------------------------------------------------
        "org.rust.MACRO": A(pink, font=ITALIC),
        "org.rust.LIFETIME": A(peach, font=ITALIC),
        "org.rust.SELF_PARAMETER": A(cyan, font=ITALIC),
        "org.rust.SELF_EXPRESSION": A(cyan, font=ITALIC),
        "org.rust.CRATE": A(lav),
        "org.rust.ENUM_VARIANT": A(peach),
        "org.rust.TYPE_PARAMETER": A(lav, font=ITALIC),
        "org.rust.STATIC": A(peach),
        "org.rust.Q_OPERATOR": A(peach),
        "org.rust.MUT_BINDING": A(effect=underline_faint, etype=UNDERLINE),
        "org.rust.UNSAFE_CODE": A(effect=red, etype=UNDERLINE),
        "org.rust.CFG_DISABLED_CODE": A(faint),
        # ---- data / config ---------------------------------------------------------------------
        "JSON.PROPERTY_KEY": A(fg),
        "YAML_SCALAR_KEY": A(fg),
        "YAML_ANCHOR": A(peach),
        "org.toml.KEY": A(fg),
        "PROPERTIES.KEY": A(fg),
        "PROPERTIES.KEY_VALUE_SEPARATOR": A(faint),
        "PROPERTIES.VALID_STRING_ESCAPE": B("DEFAULT_VALID_STRING_ESCAPE"),
        "PROPERTIES.INVALID_STRING_ESCAPE": B("DEFAULT_INVALID_STRING_ESCAPE"),
        # ---- XML / HTML / CSS ------------------------------------------------------------------
        "XML_TAG": A(faint),
        "XML_TAG_NAME": A(cyan),
        "XML_CUSTOM_TAG_NAME": A(lav),
        "XML_NS_PREFIX": A(lav),
        "XML_ATTRIBUTE_NAME": A(fg, font=ITALIC),
        "XML_ATTRIBUTE_VALUE": B("DEFAULT_STRING"),
        "XML_ENTITY_REFERENCE": A(peach),
        "XML_PROLOGUE": A(faint),
        "XML_TAG_DATA": A(fg),
        "HTML_TAG": A(faint),
        "HTML_TAG_NAME": A(cyan),
        "HTML_CUSTOM_TAG_NAME": A(lav),
        "HTML_ATTRIBUTE_NAME": A(fg, font=ITALIC),
        "HTML_ATTRIBUTE_VALUE": B("DEFAULT_STRING"),
        "HTML_ENTITY_REFERENCE": A(peach),
        "CSS.TAG_NAME": A(cyan),
        "CSS.CLASS_NAME": A(lav),
        "CSS.HASH": A(lav),
        "CSS.PSEUDO": A(cyan),
        "CSS.PROPERTY_NAME": A(fg),
        "CSS.PROPERTY_VALUE": A(peach),
        "CSS.FUNCTION": A(pink),
        "CSS.COLOR": A(peach),
        "CSS.URL": A(cyan, effect=cyan, etype=UNDERLINE),
        "CSS.IMPORTANT": A(red, font=BOLD),
        "CSS.KEYWORD": A(cyan),
        "LESS_VARIABLE": A(fg),
        "SASS_VARIABLE": A(fg),
        "SASS_MIXIN": A(pink),
        # ---- Markdown --------------------------------------------------------------------------
        "MARKDOWN_HEADER": A(pink, font=BOLD),
        "MARKDOWN_HEADER_BOLD": A(pink, font=BOLD),
        "MARKDOWN_HEADER_LEVEL_1": A(rb[0], font=BOLD),
        "MARKDOWN_HEADER_LEVEL_2": A(rb[0], font=BOLD),
        "MARKDOWN_HEADER_LEVEL_3": A(rb[1], font=BOLD),
        "MARKDOWN_HEADER_LEVEL_4": A(rb[1], font=BOLD),
        "MARKDOWN_HEADER_LEVEL_5": A(rb[2], font=BOLD),
        "MARKDOWN_HEADER_LEVEL_6": A(rb[2], font=BOLD),
        "MARKDOWN_BOLD": A(peach, font=BOLD),
        "MARKDOWN_ITALIC": A(yellow, font=ITALIC),
        "MARKDOWN_BOLD_MARKER": A(faint),
        "MARKDOWN_ITALIC_MARKER": A(faint),
        "MARKDOWN_CODE_SPAN": A(lav, c["bg_1"]),
        "MARKDOWN_CODE_SPAN_MARKER": A(faint, c["bg_1"]),
        "MARKDOWN_CODE_FENCE": A(faint),
        "MARKDOWN_LINK_TEXT": A(lav),
        "MARKDOWN_LINK_LABEL": A(lav),
        "MARKDOWN_LINK_DESTINATION": A(cyan, effect=cyan, etype=UNDERLINE),
        "MARKDOWN_LINK_TITLE": A(yellow),
        "MARKDOWN_AUTO_LINK": A(cyan, effect=cyan, etype=UNDERLINE),
        "MARKDOWN_REFERENCE_LINK": A(lav),
        "MARKDOWN_IMAGE": A(lav),
        "MARKDOWN_LIST_MARKER": A(cyan),
        "MARKDOWN_BLOCK_QUOTE_MARKER": A(faint),
        "MARKDOWN_BLOCK_QUOTE": A(mute, font=ITALIC),
        "MARKDOWN_HRULE": A(faint),
        "MARKDOWN_TABLE_SEPARATOR": A(faint),
        # ---- shell / regexp / misc -------------------------------------------------------------
        "BASH.SHEBANG": A(comment, font=ITALIC),
        "BASH.EXTERNAL_COMMAND": A(pink),
        "BASH.INTERNAL_COMMAND": A(pink, font=ITALIC),
        "BASH.FUNCTION_DEF_NAME": A(pink),
        "BASH.FUNCTION_CALL": A(pink),
        "BASH.HERE_DOC_START": A(cyan),
        "BASH.HERE_DOC_END": A(cyan),
        "BASH.CONDITIONAL": A(cyan),
        "REGEXP.CHAR_CLASS": A(peach),
        "REGEXP.META": B("DEFAULT_KEYWORD"),
        "REGEXP.ESC_CHARACTER": B("DEFAULT_VALID_STRING_ESCAPE"),
        "REGEXP.QUOTE_CHARACTER": B("DEFAULT_VALID_STRING_ESCAPE"),
        "REGEXP.REDUNDANT_ESCAPE": A(faint),
        "REGEXP.BRACES": B("DEFAULT_BRACES"),
        "REGEXP.BRACKETS": B("DEFAULT_BRACKETS"),
        "REGEXP.PARENTHS": B("DEFAULT_PARENTHS"),
        "Static method access": B("DEFAULT_STATIC_METHOD"),
        "Static property reference ID": B("DEFAULT_STATIC_FIELD"),
        "Groovy method declaration": B("DEFAULT_FUNCTION_DECLARATION"),
        "Closure braces": B("DEFAULT_BRACES"),
    }
    # ANSI colors follow meowsoot.nvim's terminal mapping; black is lifted so it stays visible.
    ansi = {
        "BLACK": (c["bg_3"], faint),
        "RED": (red, c["red_bright"]),
        "GREEN": (green, c["green_bright"]),
        "YELLOW": (yellow, c["yellow_br"]),
        "BLUE": (blue, c["blue_bright"]),
        "MAGENTA": (pink, c["pink_br"]),
        "CYAN": (cyan, c["cyan_br"]),
        "WHITE": (mute, fg),
    }
    for name, (normal, bright) in ansi.items():
        a[f"BLOCK_TERMINAL_{name}"] = A(normal)
        a[f"BLOCK_TERMINAL_{name}_BRIGHT"] = A(bright)
        if name not in ("BLACK", "WHITE"):
            a[f"CONSOLE_{name}_OUTPUT"] = A(normal)
            a[f"CONSOLE_{name}_BRIGHT_OUTPUT"] = A(bright)
    a["CONSOLE_BLACK_OUTPUT"] = A(c["bg_3"])
    a["CONSOLE_DARKGRAY_OUTPUT"] = A(faint)
    a["CONSOLE_GRAY_OUTPUT"] = A(mute)
    a["CONSOLE_WHITE_OUTPUT"] = A(fg)
    # Rainbow Brackets plugin
    for kind in ("ROUND", "SQUARE", "SQUIGGLY", "ANGLE"):
        for i in range(5):
            a[f"{kind}_BRACKETS_RAINBOW_COLOR{i}"] = A(rb[i])
    return a


SCHEME_EXTRAS = {
    True: ["themes/islands/IslandSchemeDark.xml"],
    False: ["themes/expUI/expUI_lightScheme.xml"],
}


def hexval(v):
    return v.lstrip("#").lower()


def build_scheme(variant, ide, jb_colors, parents):
    dark = VARIANTS[variant]["dark"]
    r = Ramps(variant, jb_colors)
    c = r.c
    parent_name, (p_colors, p_attrs) = parents

    # Re-map everything the parent schemes set explicitly, then apply the meowsoot mapping.
    colors = {}
    for k, v in p_colors.items():
        if re.fullmatch(r"[0-9A-Fa-f]{1,6}|[0-9A-Fa-f]{8}", v or ""):
            colors[k] = hexval(r.remap(v.rjust(6, "0")))
        else:
            colors[k] = v
    colors.update({k: hexval(v) for k, v in scheme_colors(c).items()})

    attrs = {}
    for k, d in p_attrs.items():
        nd = {}
        for opt, v in d.items():
            if opt in ("FOREGROUND", "BACKGROUND", "EFFECT_COLOR", "ERROR_STRIPE_COLOR") and v:
                if not re.fullmatch(r"[0-9A-Fa-f]{1,6}", v):
                    nd[opt] = v
                elif opt == "FOREGROUND":
                    nd[opt] = hexval(r.remap_fg(v))
                else:
                    nd[opt] = hexval(r.remap(v.rjust(6, "0")))
            else:
                nd[opt] = v
        attrs[k] = nd
    for k, d in scheme_attrs(c).items():
        attrs[k] = {o: (v if o in ("base", "FONT_TYPE", "EFFECT_TYPE") else hexval(v)) for o, v in d.items()}

    name = f"Meowsoot {VARIANTS[variant]['title']}"
    lines = [f'<scheme name={quoteattr(name)} version="142" parent_scheme="{parent_name}">',
             "  <colors>"]
    for k in sorted(colors):
        lines.append(f"    <option name={quoteattr(k)} value={quoteattr(colors[k] or '')} />")
    lines += ["  </colors>", "  <attributes>"]
    for k in sorted(attrs):
        d = attrs[k]
        base = d.get("base")
        opts = {o: v for o, v in d.items() if o != "base" and v is not None}
        base_attr = f" baseAttributes={quoteattr(base)}" if base else ""
        if not opts:
            lines.append(f"    <option name={quoteattr(k)}{base_attr} />" if base else
                         f"    <option name={quoteattr(k)}>\n      <value />\n    </option>")
            continue
        lines.append(f"    <option name={quoteattr(k)}{base_attr}>")
        lines.append("      <value>")
        order = ("FOREGROUND", "BACKGROUND", "FONT_TYPE", "ERROR_STRIPE_COLOR", "EFFECT_COLOR", "EFFECT_TYPE")
        for o in sorted(opts, key=lambda o: order.index(o) if o in order else len(order)):
            lines.append(f"        <option name={quoteattr(o)} value={quoteattr(opts[o])} />")
        lines.append("      </value>")
        lines.append("    </option>")
    lines += ["  </attributes>", "</scheme>", ""]
    return "\n".join(lines)


# --------------------------------------------------------------------------------------------------


def default_ide():
    for pattern in ["~/.local/share/JetBrains/Toolbox/apps/intellij-idea*", "/opt/idea*", "/usr/share/idea*",
                    "/Applications/IntelliJ IDEA*.app/Contents"]:
        for p in sorted(glob.glob(os.path.expanduser(pattern)), reverse=True):
            if os.path.isfile(os.path.join(p, "lib", "intellij.platform.ide.impl.jar")):
                return p
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ide", default=default_ide(), help="IntelliJ IDEA installation directory")
    ap.add_argument("--plugins", nargs="*", default=[], help="extra plugin directories (e.g. user-installed plugins)")
    args = ap.parse_args()
    if not args.ide:
        ap.error("could not find an IntelliJ IDEA installation; pass --ide")
    ide = Ide(args.ide, args.plugins)
    os.makedirs(OUT_DIR, exist_ok=True)
    parents = {}
    for dark, name in ((True, "Darcula"), (False, "Default")):
        parents[dark] = (name, parent_scheme(ide, name, SCHEME_EXTRAS[dark]))
    for variant, meta in VARIANTS.items():
        theme = build_theme(variant, ide)
        with open(os.path.join(OUT_DIR, f"meowsoot-{variant}.theme.json"), "w") as f:
            json.dump(theme, f, indent=2)
            f.write("\n")
        jb = ide.theme(THEME_CHAINS[meta["dark"]][-1])["colors"]
        with open(os.path.join(OUT_DIR, f"meowsoot-{variant}.xml"), "w") as f:
            f.write(build_scheme(variant, ide, jb, parents[meta["dark"]]))
        print(f"generated meowsoot-{variant}")


if __name__ == "__main__":
    main()
