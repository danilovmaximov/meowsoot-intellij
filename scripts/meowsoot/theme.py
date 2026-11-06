from .icons import icon_palette
from .ramps import ramp_colors
from .tokens import project_gradient_tokens, semantic_tokens
from .ui import ui_keys


def _uppercase_hex(values):
    return {key: value.upper() if value.startswith("#") else value for key, value in sorted(values.items())}


def build_theme(variant, c):
    colors = {**ramp_colors(c), **project_gradient_tokens(c), **semantic_tokens(c)}
    return {
        "name": variant.name,
        "dark": variant.dark,
        "author": "Meowsoot contributors",
        "parentTheme": "Islands Dark" if variant.dark else "Islands Light",
        "editorScheme": f"/themes/meowsoot-{variant.id}.xml",
        "colors": _uppercase_hex(colors),
        "ui": _uppercase_hex(ui_keys(c)),
        "icons": {"ColorPalette": _uppercase_hex(icon_palette(c))},
    }
