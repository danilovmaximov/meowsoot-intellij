from types import SimpleNamespace

from .hsl import blend, brighten, hsl_to_hex


class Colors(SimpleNamespace):
    def __init__(self, variant):
        super().__init__(**{name: hsl_to_hex(*hsl) for name, hsl in variant.palette.items()})
        self.dark = variant.dark
        self.hsl = variant.palette

        self.search = self.tint(self.yellow, 0.35)
        self.search_current = self.tint(self.peach, 0.45)
        self.diff_add = self.tint(self.green, 0.18)
        self.diff_change = self.tint(self.blue, 0.18)
        self.diff_delete = self.tint(self.red, 0.18)
        self.red_br = brighten(self.red, 8)
        self.green_br = brighten(self.green, 10)
        self.blue_br = brighten(self.blue, 8)
        self.rainbow = [self.pink, self.peach, self.yellow, self.cyan, self.blue, self.lavender]

    def tint(self, color, alpha):
        return blend(color, alpha, self.bg_0)

    def by_mode(self, dark, light):
        return dark if self.dark else light
