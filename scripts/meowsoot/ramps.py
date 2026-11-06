from .hsl import WHITE, blend, hsl_to_hex

STEPS = range(10, 170, 10)
LIGHTNESS = [10, 14, 16, 22, 27, 32, 39, 47, 56, 64, 73, 78, 84, 88, 92, 97]
SATURATION_CEILING = [30, 32, 34, 36, 38, 40, 45, 55, 70, 85, 100, 100, 100, 100, 100, 100]

HUE_RAMP_ACCENTS = {
    "blue": "blue",
    "green": "green",
    "red": "red",
    "yellow": "yellow",
    "orange": "peach",
    "purple": "lavender",
    "teal": "cyan",
}

LEGACY_ALIASES_DARK = {
    "Gray{}": ("gray", [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 130, 140, 160, 160]),
    "Blue{}": ("blue", [40, 60, 70, 80, 80, 90, 100, 100, 110, 110, 120, 130, 150]),
    "Green{}": ("green", [30, 30, 50, 60, 70, 80, 90, 90, 100, 110, 130, 150]),
    "Yellow{}": ("yellow", [30, 50, 70, 80, 90, 90, 100, 110, 120, 130, 140]),
    "Red{}": ("red", [40, 40, 50, 70, 80, 90, 100, 100, 110, 120, 140, 150]),
    "Orange{}": ("orange", [40, 60, 70, 80, 90, 100, 100, 110, 120, 130, 140]),
    "Purple{}": ("purple", [30, 40, 50, 70, 80, 90, 100, 100, 110, 120, 130, 150]),
    "Teal{}": ("teal", [30, 30, 40, 50, 60, 60, 70, 80, 90, 100, 110, 130]),
}

LEGACY_ALIASES_LIGHT = {
    "grey{:02}": ("gray", [80, 80, 90, 90, 100, 110, 110, 120, 130, 130, 130, 140, 150, 150, 160, 160, 160, 160]),
    "Gray{}": ("gray", [10, 30, 40, 60, 70, 80, 90, 110, 130, 130, 140, 150, 160, 160]),
    "Blue{}": ("blue", [70, 80, 90, 90, 100, 100, 110, 110, 120, 140, 150, 160, 160]),
    "Green{}": ("green", [50, 50, 60, 60, 70, 80, 100, 120, 130, 150, 160]),
    "Yellow{}": ("yellow", [60, 70, 80, 90, 100, 110, 130, 150, 150, 160]),
    "Red{}": ("red", [70, 80, 80, 90, 100, 100, 120, 130, 150, 160, 160, 160]),
    "Orange{}": ("orange", [70, 70, 80, 80, 100, 110, 130, 160, 160]),
    "Teal{}": ("teal", [40, 50, 50, 60, 80, 100, 120, 150, 160]),
    "Purple{}": ("purple", [70, 80, 90, 100, 110, 120, 140, 160, 160, 160]),
}


def gray_ramp(c):
    if c.dark:
        return [
            c.bg_0,
            blend(c.bg_1, 1 / 2, c.bg_0),
            c.bg_1,
            c.bg_3,
            c.bg_4,
            blend(c.fg_faint, 1 / 3, c.bg_4),
            blend(c.fg_faint, 2 / 3, c.bg_4),
            c.fg_faint,
            blend(c.fg_mute, 1 / 2, c.fg_faint),
            c.fg_mute,
            blend(c.fg, 1 / 3, c.fg_mute),
            blend(c.fg, 2 / 3, c.fg_mute),
            c.fg,
            blend(WHITE, 1 / 4, c.fg),
            blend(WHITE, 2 / 4, c.fg),
            blend(WHITE, 3 / 4, c.fg),
        ]
    return [
        c.fg,
        blend(c.fg_mute, 0.1, c.fg),
        blend(c.fg_mute, 0.15, c.fg),
        blend(c.fg_mute, 0.25, c.fg),
        blend(c.fg_mute, 0.4, c.fg),
        blend(c.fg_mute, 0.65, c.fg),
        c.fg_mute,
        c.comment,
        c.fg_faint,
        c.bg_4,
        blend(c.bg_3, 1 / 3, c.bg_4),
        blend(c.bg_3, 2 / 3, c.bg_4),
        c.bg_3,
        blend(c.bg_deep, 1 / 2, c.bg_3),
        c.bg_deep,
        c.bg_2,
    ]


def hue_ramp(c, accent):
    hue, saturation, _ = c.hsl[accent]
    return [
        hsl_to_hex(hue, min(saturation, ceiling), lightness)
        for lightness, ceiling in zip(LIGHTNESS, SATURATION_CEILING)
    ]


def white_and_black(c):
    if c.dark:
        return {"white": blend(WHITE, 0.875, c.fg), "black": c.bg_deep}
    return {"white": c.bg_0, "black": c.fg}


def legacy_aliases(c):
    table = LEGACY_ALIASES_DARK if c.dark else LEGACY_ALIASES_LIGHT
    return {
        name.format(index): f"{ramp}-{step}"
        for name, (ramp, steps) in table.items()
        for index, step in enumerate(steps, start=1)
    }


def ramp_colors(c):
    colors = {f"gray-{step}": color for step, color in zip(STEPS, gray_ramp(c))}
    for ramp, accent in HUE_RAMP_ACCENTS.items():
        colors.update({f"{ramp}-{step}": color for step, color in zip(STEPS, hue_ramp(c, accent))})
    colors.update(white_and_black(c))
    colors.update(legacy_aliases(c))
    return colors
