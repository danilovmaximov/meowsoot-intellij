from xml.sax.saxutils import quoteattr

from .editor import editor_attributes, editor_colors
from .languages import language_attributes

OPTION_ORDER = [
    ("FOREGROUND", "foreground"),
    ("BACKGROUND", "background"),
    ("FONT_TYPE", "font"),
    ("ERROR_STRIPE_COLOR", "stripe"),
    ("EFFECT_COLOR", "effect"),
    ("EFFECT_TYPE", "effect_type"),
]


def _scheme_value(value):
    if isinstance(value, int):
        return str(value)
    return value.lstrip("#").lower()


def _option(name, value, indent):
    return f"{' ' * indent}<option name={quoteattr(name)} value={quoteattr(_scheme_value(value))} />"


def _attribute_lines(name, text_style):
    base = f" baseAttributes={quoteattr(text_style.base)}" if text_style.base else ""
    options = [(key, getattr(text_style, field)) for key, field in OPTION_ORDER]
    options = [(key, value) for key, value in options if value is not None]
    if not options:
        return [f"    <option name={quoteattr(name)}{base} />"]
    return [
        f"    <option name={quoteattr(name)}{base}>",
        "      <value>",
        *(_option(key, value, 8) for key, value in options),
        "      </value>",
        "    </option>",
    ]


def build_scheme(variant, c):
    colors = editor_colors(c)
    attributes = {**editor_attributes(c), **language_attributes(c)}
    parent = "Darcula" if variant.dark else "Default"
    lines = [
        f'<scheme name={quoteattr(variant.name)} version="142" parent_scheme="{parent}">',
        "  <colors>",
        *(_option(name, colors[name], 4) for name in sorted(colors)),
        "  </colors>",
        "  <attributes>",
    ]
    for name in sorted(attributes):
        lines.extend(_attribute_lines(name, attributes[name]))
    lines += ["  </attributes>", "</scheme>", ""]
    return "\n".join(lines)
