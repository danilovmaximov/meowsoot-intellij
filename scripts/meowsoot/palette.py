from dataclasses import dataclass


@dataclass(frozen=True)
class Variant:
    id: str
    dark: bool
    palette: dict

    @property
    def name(self):
        return f"Meowsoot {self.id.capitalize()}"


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

NIGHT = {
    "frame": (0, 3, 6),
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
}

TWILIGHT = {
    "frame": (0, 0, 18),
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
}

MOON = {
    "frame": (230, 20, 8),
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
}

DAWN = {
    "frame": (30, 18, 89),
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
}

VARIANTS = [
    Variant("night", dark=True, palette=NIGHT),
    Variant("twilight", dark=True, palette=TWILIGHT),
    Variant("moon", dark=True, palette=MOON),
    Variant("dawn", dark=False, palette=DAWN),
]
