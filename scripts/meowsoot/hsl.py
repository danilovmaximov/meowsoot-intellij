import colorsys
import math

WHITE = "#ffffff"


def _round_half_up(value):
    return math.floor(value + 0.5)


def _rgb_to_hex(red, green, blue):
    return "#%02x%02x%02x" % (_round_half_up(red), _round_half_up(green), _round_half_up(blue))


def hsl_to_hex(hue, saturation, lightness):
    red, green, blue = colorsys.hls_to_rgb((hue % 360) / 360, lightness / 100, saturation / 100)
    return _rgb_to_hex(red * 255, green * 255, blue * 255)


def hex_to_rgb(color):
    digits = color.lstrip("#")
    return tuple(int(digits[i:i + 2], 16) for i in (0, 2, 4))


def hex_to_hsl(color):
    red, green, blue = (channel / 255 for channel in hex_to_rgb(color))
    hue, lightness, saturation = colorsys.rgb_to_hls(red, green, blue)
    return hue * 360, saturation * 100, lightness * 100


def blend(foreground, alpha, background):
    mixed = [alpha * f + (1 - alpha) * b for f, b in zip(hex_to_rgb(foreground), hex_to_rgb(background))]
    return _rgb_to_hex(*mixed)


def brighten(color, amount):
    hue, saturation, lightness = (_round_half_up(value) for value in hex_to_hsl(color))
    return hsl_to_hex(hue, saturation, min(100, max(0, lightness + amount)))


def with_alpha(color, alpha):
    return "%s%02x" % (color, _round_half_up(alpha * 255))
