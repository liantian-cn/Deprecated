import colorsys
from typing import List, Tuple


def generate_hsv_color_ring(
        hue_step: int = 9,
        saturation: float = 1.0,
        value: float = 1.0
) -> List[Tuple[int, int, int]]:
    colors = []
    for degree in range(0, 360, hue_step):
        hue = degree / 360.0
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        rgb = (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))
        colors.append(rgb)
    return colors


print(generate_hsv_color_ring())
