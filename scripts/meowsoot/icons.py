from .hsl import blend


def dark_icon_colors(c):
    def fill(color):
        return c.tint(color, 0.25)

    return {
        "#CED0D6": "icon-default-stroke",
        "#9DA0A8": c.fg_mute,
        "#868A91": blend(c.fg_mute, 0.5, c.fg_faint),
        "#6F737A": c.fg_faint,
        "#43454A": c.bg_4,
        "#548AF7": c.blue,
        "#3574F0": c.blue,
        "#25324D": fill(c.blue),
        "#DB5C5C": c.red,
        "#E55765": c.red,
        "#402929": fill(c.red),
        "#5FAD65": c.green,
        "#57965C": c.green,
        "#253627": fill(c.green),
        "#F2C55C": c.yellow,
        "#D6AE58": c.yellow,
        "#3D3223": fill(c.yellow),
        "#E08855": c.peach,
        "#C77D55": c.peach,
        "#45322B": fill(c.peach),
        "#B589EC": c.lavender,
        "#A571E6": c.lavender,
        "#2F2936": fill(c.lavender),
    }


def light_icon_colors(c):
    def fill(color):
        return c.tint(color, 0.1)

    return {
        "#6C707E": "icon-default-stroke",
        "#818594": c.fg_faint,
        "#A8ADBD": c.bg_4,
        "#EBECF0": c.bg_2,
        "#3574F0": c.blue,
        "#4682FA": c.blue,
        "#EDF3FF": fill(c.blue),
        "#E7EFFD": fill(c.blue),
        "#DB3B4B": c.red,
        "#E55765": c.red,
        "#FFF7F7": fill(c.red),
        "#208A3C": c.green,
        "#369650": c.green,
        "#55A76A": c.green,
        "#F2FCF3": fill(c.green),
        "#FFAF0F": c.yellow,
        "#C27D04": c.yellow,
        "#FFFAEB": fill(c.yellow),
        "#E66D17": c.peach,
        "#FFF4EB": fill(c.peach),
        "#834DF0": c.lavender,
        "#FAF5FF": fill(c.lavender),
    }


def checkbox_colors(c):
    return {
        "Checkbox.Background.Default": c.bg_0,
        "Checkbox.Border.Default": c.by_mode(c.bg_4, c.fg_faint),
        "Checkbox.Background.Selected": c.pink,
        "Checkbox.Border.Selected": c.pink,
        "Checkbox.Foreground.Selected": c.bg_0,
        "Checkbox.Focus.Wide": c.tint(c.pink, 0.6),
        "Checkbox.Background.Disabled": c.bg_1,
        "Checkbox.Border.Disabled": c.bg_3,
        "Checkbox.Foreground.Disabled": c.fg_faint,
    }


def icon_palette(c):
    icon_colors = dark_icon_colors(c) if c.dark else light_icon_colors(c)
    return {**icon_colors, **checkbox_colors(c)}
