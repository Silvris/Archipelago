from typing import Dict, Tuple, List, TYPE_CHECKING, Union
from zlib import crc32
import struct
import sys
import logging

if TYPE_CHECKING:
    from . import MM1World
    from .rom import MM1ProcedurePatch

HTML_TO_NES: Dict[str, int] = {
    "SNOW": 0x20,
    "LINEN": 0x36,
    "SEASHELL": 0x36,
    "AZURE": 0x3C,
    "LAVENDER": 0x33,
    "WHITE": 0x30,
    "BLACK": 0x0F,
    "GREY": 0x00,
    "GRAY": 0x00,
    "ROYALBLUE": 0x12,
    "BLUE": 0x11,
    "SKYBLUE": 0x21,
    "LIGHTBLUE": 0x31,
    "TURQUOISE": 0x2B,
    "CYAN": 0x2C,
    "AQUAMARINE": 0x3B,
    "DARKGREEN": 0x0A,
    "GREEN": 0x1A,
    "YELLOW": 0x28,
    "GOLD": 0x28,
    "WHEAT": 0x37,
    "TAN": 0x37,
    "CHOCOLATE": 0x07,
    "BROWN": 0x07,
    "SALMON": 0x26,
    "ORANGE": 0x27,
    "CORAL": 0x36,
    "TOMATO": 0x16,
    "RED": 0x16,
    "PINK": 0x25,
    "MAROON": 0x06,
    "MAGENTA": 0x24,
    "FUSCHIA": 0x24,
    "VIOLET": 0x24,
    "PLUM": 0x33,
    "PURPLE": 0x14,
    "THISTLE": 0x34,
    "DARKBLUE": 0x01,
    "SILVER": 0x10,
    "NAVY": 0x02,
    "TEAL": 0x1C,
    "OLIVE": 0x18,
    "LIME": 0x2A,
    "AQUA": 0x2C,
    # can add more as needed
}

MM1_COLORS: Dict[str, Tuple[int, int]] = {
    "Rolling Cutter": (0x30, 0x00),
    "Ice Slasher": (0x30, 0x12),
    "Hyper Bomb": (0x30, 0x19),
    "Fire Storm": (0x28, 0x16),
    "Thunder Beam": (0x38, 0x00),
    "Super Arm": (0x30, 0x17),
    "Magnet Beam": (0x2C, 0x11),
    "Cut Man Access Codes": (0x30, 0x15),
    "Ice Man Access Codes": (0x20, 0x21),
    "Bomb Man Access Codes": (0x27, 0x15),
    "Fire Man Access Codes": (0x30, 0x15),
    "Elec Man Access Codes": (0x00, 0x27),
    "Guts Man Access Codes": (0x27, 0x15),
}

palette_pointers: Dict[str, List[int]] = {
    "Mega Buster": [0x1D495, 0xCF1], # 0xCC1 might also?
    "Rolling Cutter":  [0x1D497],
    "Ice Slasher":  [0x1D499],
    "Hyper Bomb":  [0x1D49B],
    "Fire Storm":  [0x1D49D],
    "Thunder Beam":  [0x1D49F],
    "Super Arm":  [0x1D4A1],
    "Magnet Beam":  [0x1D4A3],
    "Cut Man": [0x4DD7, 0x0DD7],
    "Ice Man": [0xCDCC, 0x4DB6],
    "Bomb Man": [0xCDC1, ],
    "Fire Man": [0xCDB6, ],
    "Elec Man": [0x4DE3, 0x10DC1],
    "Guts Man": [0xCDD7, 0x14DB6],
}

if "worlds.mm2" in sys.modules:
    # is this the proper way to do this? who knows!
    try:
        mm2 = sys.modules["worlds.mm2"]
        for item in MM1_COLORS:
            mm2.color.add_color_to_mm2(item, MM1_COLORS[item])
    except AttributeError:
        # pass through if an old MM2 is found
        pass

if "worlds.mm3" in sys.modules:
    try:
        mm3 = sys.modules["worlds.mm3"]
        for item in MM1_COLORS:
            mm3.color.add_color_to_mm3(item, MM1_COLORS[item])
    except AttributeError:
        # pass through if an old MM3 is found
        pass

def extrapolate_color(color: int) -> Tuple[int, int]:
    if color > 0x1F:
        color_1 = color
        color_2 = color_1 - 0x10
    else:
        color_2 = color
        color_1 = color_2 + 0x10
    return color_1, color_2


def validate_colors(color_1: int, color_2: int, allow_match: bool = False) -> Tuple[int, int]:
    # Black should be reserved for outlines, a gray should suffice
    if color_1 in [0x0D, 0x0E, 0x0F, 0x1E, 0x2E, 0x3E, 0x1F, 0x2F, 0x3F]:
        color_1 = 0x10
    if color_2 in [0x0D, 0x0E, 0x0F, 0x1E, 0x2E, 0x3E, 0x1F, 0x2F, 0x3F]:
        color_2 = 0x10

    # one final check, make sure we don't have two matching
    if not allow_match and color_1 == color_2:
        color_1 = 0x30  # color 1 to white works with about any paired color

    return color_1, color_2


def parse_color(colors: List[str]) -> Tuple[int, int]:
    color_a = colors[0]
    if color_a.startswith("$"):
        color_1 = int(color_a[1:], 16)
    else:
        # assume it's in our list of colors
        color_1 = HTML_TO_NES[color_a.upper()]

    if len(colors) == 1:
        color_1, color_2 = extrapolate_color(color_1)
    else:
        color_b = colors[1]
        if color_b.startswith("$"):
            color_2 = int(color_b[1:], 16)
        else:
            color_2 = HTML_TO_NES[color_b.upper()]
    return color_1, color_2


def write_palette_shuffle(world: "MM1World", rom: "MM1ProcedurePatch") -> None:
    palette_shuffle: Union[int, str] = world.options.palette_shuffle.value
    palettes_to_write: Dict[str, Tuple[int, int]] = {}
    if isinstance(palette_shuffle, str):
        color_sets = palette_shuffle.split(";")
        if len(color_sets) == 1:
            palette_shuffle = world.options.palette_shuffle.option_none
            # singularity is more correct, but this is faster
        else:
            palette_shuffle = world.options.palette_shuffle.options[color_sets.pop()]
        for color_set in color_sets:
            if "-" in color_set:
                character, color = color_set.split("-")
                if character.title() not in palette_pointers:
                    logging.warning(f"Player {world.multiworld.get_player_name(world.player)} "
                                    f"attempted to set color for unrecognized option {character}")
                colors = color.split("|")
                real_colors = validate_colors(*parse_color(colors), allow_match=True)
                palettes_to_write[character.title()] = real_colors
            else:
                # If color is provided with no character, assume singularity
                colors = color_set.split("|")
                real_colors = validate_colors(*parse_color(colors), allow_match=True)
                for character in palette_pointers:
                    palettes_to_write[character] = real_colors
        # Now we handle the real values
    if palette_shuffle == 1:
        shuffled_colors = list(MM1_COLORS.values())
        shuffled_colors.append((0x2C, 0x11))  # Mega Buster
        world.random.shuffle(shuffled_colors)
        for character in palette_pointers:
            if character not in palettes_to_write:
                palettes_to_write[character] = shuffled_colors.pop()
    elif palette_shuffle > 1:
        if palette_shuffle == 2:
            for character in palette_pointers:
                if character not in palettes_to_write:
                    real_colors = validate_colors(world.random.randint(0, 0x3F), world.random.randint(0, 0x3F))
                    palettes_to_write[character] = real_colors
        else:
            # singularity
            real_colors = validate_colors(world.random.randint(0, 0x3F), world.random.randint(0, 0x3F))
            for character in palette_pointers:
                if character not in palettes_to_write:
                    palettes_to_write[character] = real_colors

    for character in palettes_to_write:
        for pointer in palette_pointers[character]:
            rom.write_bytes(pointer, bytes(palettes_to_write[character]))

        if character == "Atomic Fire":
            # special case, we need to update Atomic Fire's flashing routine
            rom.write_byte(0x3DE4A, palettes_to_write[character][1])
            rom.write_byte(0x3DE4C, palettes_to_write[character][1])
