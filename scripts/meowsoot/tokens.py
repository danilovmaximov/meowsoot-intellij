from .hsl import with_alpha

PROJECT_GRADIENT_ACCENTS = {
    "g1-amber": "peach",
    "g2-rust": "yellow",
    "g3-olive": "green",
    "g4-sky": "cyan",
    "g5-cobalt": "blue",
    "g6-plum": "pink",
    "g7-violet": "lavender",
    "g8-ocean": "cyan",
    "g9-grass": "green",
}


def accent_tokens(c, name, color):
    return {
        f"accent-{name}-bg": color,
        f"accent-{name}-border": color,
        f"accent-{name}-bg-secondary": c.tint(color, c.by_mode(0.16, 0.08)),
        f"accent-{name}-border-secondary": c.tint(color, c.by_mode(0.45, 0.3)),
    }


def semantic_tokens(c):
    tokens = {
        "main-window-bg": c.frame,
        "text-default": c.fg,
        "text-muted": c.fg_mute,
        "text-secondary": c.comment,
        "text-link": c.cyan,
        "text-error": c.red,
        "text-warning": c.by_mode(c.yellow, c.yellow_br),
        "text-success": c.green,
        "text-over-accent": c.bg_0,
        "editor-text": c.fg,
        **accent_tokens(c, "brand", c.pink),
        **accent_tokens(c, "error", c.red),
        **accent_tokens(c, "warning", c.yellow),
        **accent_tokens(c, "success", c.green),
        "accent-ai-bg": c.tint(c.lavender, c.by_mode(0.14, 0.08)),
        "accent-ai-border": c.tint(c.lavender, 0.5),
        "selection-bg-active": c.tint(c.pink, c.by_mode(0.24, 0.16)),
        "selection-bg-active-muted": c.tint(c.pink, c.by_mode(0.14, 0.09)),
        "selection-bg-inactive": c.by_mode(c.bg_3, c.bg_1),
        "tab-selected-bg-active": c.tint(c.pink, c.by_mode(0.14, 0.09)),
        "tab-selected-border-active": c.pink,
        "tab-file-color-mask-bg": with_alpha(c.bg_0, 0.5),
        "toolbar-selected-bg": c.tint(c.pink, c.by_mode(0.3, 0.2)),
        "toolbar-selected-bg-hovered": c.tint(c.pink, c.by_mode(0.38, 0.27)),
        "popup-completion-match-text": c.pink,
        "search-match-bg": c.by_mode(c.yellow, c.tint(c.yellow, 0.3)),
        "icon-green-stroke": c.green,
        "icon-over-accent": c.bg_0,
        "linkForeground": c.cyan,
        "windowsPopupBorder": c.bg_4,
    }
    if c.dark:
        tokens.update({
            "main-window-bg-alt": c.bg_2,
            "got-it-bg": c.tint(c.pink, 0.3),
            "got-it-border": c.tint(c.pink, 0.45),
            "got-it-text-link": c.cyan_br,
            "presentation-assistant-bg": c.tint(c.pink, 0.3),
        })
    else:
        tokens.update({
            "layer-2-bg": c.bg_0,
            "main-window-bg-alt": c.bg_1,
            "tool-window-bg-alt": c.bg_2,
            "editor-border-alt": c.bg_1,
            "presentation-assistant-bg": c.fg_mute,
        })
    return tokens


def project_gradient_tokens(c):
    tokens = {
        "grad-hor-left": with_alpha(c.frame, 0.2),
        "grad-hor-right": with_alpha(c.frame, 0.3),
        "grad-ver-top": with_alpha(c.frame, 0.1),
        "grad-ver-bottom": with_alpha(c.frame, 0.5),
    }
    for gradient, accent in PROJECT_GRADIENT_ACCENTS.items():
        color = getattr(c, accent)
        highlight = c.tint(color, c.by_mode(0.35, 0.2))
        tokens.update({
            f"grad-{gradient}-a1": with_alpha(highlight, 1),
            f"grad-{gradient}-a1-transparent": with_alpha(highlight, 0),
            f"grad-{gradient}-a1-secondary": c.tint(color, 0.1),
            f"grad-{gradient}-a2": c.tint(color, c.by_mode(0.14, 0.12)),
            f"grad-{gradient}-bg": c.tint(color, c.by_mode(0.07, 0.14)),
        })
    return tokens
