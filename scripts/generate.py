#!/usr/bin/env python3
import json
from pathlib import Path

from meowsoot.colors import Colors
from meowsoot.palette import VARIANTS
from meowsoot.scheme import build_scheme
from meowsoot.theme import build_theme

THEMES_DIR = Path(__file__).resolve().parent.parent / "src" / "main" / "resources" / "themes"


def main():
    THEMES_DIR.mkdir(parents=True, exist_ok=True)
    for variant in VARIANTS:
        colors = Colors(variant)
        theme_path = THEMES_DIR / f"meowsoot-{variant.id}.theme.json"
        scheme_path = THEMES_DIR / f"meowsoot-{variant.id}.xml"
        theme_path.write_text(json.dumps(build_theme(variant, colors), indent=2) + "\n")
        scheme_path.write_text(build_scheme(variant, colors))
        print(f"{variant.name}: {theme_path.name}, {scheme_path.name}")


if __name__ == "__main__":
    main()
