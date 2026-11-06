from dataclasses import dataclass

BOLD, ITALIC, BOLD_ITALIC = 1, 2, 3
BOXED, UNDERLINE, WAVE, STRIKE, BOLD_UNDERLINE, DOTTED = 0, 1, 2, 3, 4, 5


@dataclass(frozen=True)
class TextStyle:
    foreground: str | None = None
    background: str | None = None
    font: int | None = None
    stripe: str | None = None
    effect: str | None = None
    effect_type: int | None = None
    base: str | None = None


def style(foreground=None, background=None, font=None, effect=None, effect_type=UNDERLINE, stripe=None):
    return TextStyle(
        foreground=foreground,
        background=background,
        font=font,
        stripe=stripe,
        effect=effect,
        effect_type=effect_type if effect else None,
    )


def inherit(base):
    return TextStyle(base=base)
