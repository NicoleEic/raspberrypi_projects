import sys
from colorthief import ColorThief



color_thief = ColorThief('sunflower.jpeg')
# get the dominant color
dominant_color = color_thief.get_color(quality=1)
# build a color palette
palette = color_thief.get_palette(color_count=20)