import sys
from . import names

HTML_TO_NES: dict[str, int] = {
    'SNOW': 0x20,
    'LINEN': 0x36,
    'SEASHELL': 0x36,
    'AZURE': 0x3C,
    'LAVENDER': 0x33,
    'WHITE': 0x30,
    'BLACK': 0x0F,
    'GREY': 0x00,
    'GRAY': 0x00,
    'ROYALBLUE': 0x12,
    'BLUE': 0x11,
    'SKYBLUE': 0x21,
    'LIGHTBLUE': 0x31,
    'TURQUOISE': 0x2B,
    'CYAN': 0x2C,
    'AQUAMARINE': 0x3B,
    'DARKGREEN': 0x0A,
    'GREEN': 0x1A,
    'YELLOW': 0x28,
    'GOLD': 0x28,
    'WHEAT': 0x37,
    'TAN': 0x37,
    'CHOCOLATE': 0x07,
    'BROWN': 0x07,
    'SALMON': 0x26,
    'ORANGE': 0x27,
    'CORAL': 0x36,
    'TOMATO': 0x16,
    'RED': 0x16,
    'PINK': 0x25,
    'MAROON': 0x06,
    'MAGENTA': 0x24,
    'FUSCHIA': 0x24,
    'VIOLET': 0x24,
    'PLUM': 0x33,
    'PURPLE': 0x14,
    'THISTLE': 0x34,
    'DARKBLUE': 0x01,
    'SILVER': 0x10,
    'NAVY': 0x02,
    'TEAL': 0x1C,
    'OLIVE': 0x18,
    'LIME': 0x2A,
    'AQUA': 0x2C,
    # can add more as needed
}

MM11_NES_COLORS: dict[str, tuple[int, int]] = {
    names.block_dropper: (0x3D, 0x2C),
    names.acid_barrier: (0x04, 0x1A),
    names.pile_driver: (0x10, 0x16),
    names.bounce_ball: (0x38, 0x15),
    names.scramble_thunder: (0x00, 0x28),
    names.tundra_storm: (0x34, 0x24),
    names.blazing_torch: (0x2D, 0x16),
    names.chain_blast: (0x04, 0x27),
    names.rush_coil: (0x30, 0x15),
    names.rush_jet: (0x30, 0x15),
    names.charge_buster: (0x3A, 0x2A),
    names.block_man_stage: (0x3D, 0x2C),
    names.acid_man_stage: (0x04, 0x1A),
    names.impact_man_stage: (0x10, 0x16),
    names.bounce_man_stage: (0x38, 0x15),
    names.fuse_man_stage: (0x00, 0x28),
    names.tundra_man_stage: (0x3C, 0x04),
    names.torch_man_stage: (0x2D, 0x16),
    names.blast_man_stage: (0x04, 0x27),
}


def check_for_known_worlds():
    if "worlds.mm1" in sys.modules:
        try:
            mm1 = sys.modules["worlds.mm1"]
            for item in MM11_NES_COLORS:
                mm1.color.add_color_to_mm1(item, MM11_NES_COLORS[item])
        except AttributeError:
            pass
    if "worlds.mm2" in sys.modules:
        try:
            mm2 = sys.modules["worlds.mm2"]
            for item in MM11_NES_COLORS:
                mm2.color.add_color_to_mm2(item, MM11_NES_COLORS[item])
        except AttributeError:
            # pass through if an old MM2 is found
            pass
    if "worlds.mm3" in sys.modules:
        try:
            mm3 = sys.modules["worlds.mm3"]
            for item in MM11_NES_COLORS:
                mm3.color.add_color_to_mm3(item, MM11_NES_COLORS[item])
        except AttributeError:
            pass
    if "worlds.mm4" in sys.modules:
        try:
            mm4 = sys.modules["worlds.mm4"]
            for item in MM11_NES_COLORS:
                mm4.color.add_color_to_mm4(item, MM11_NES_COLORS[item])
        except AttributeError:
            pass

# Maybe we expand this in the future, but MM11 doesn't use color masking and just has 8 different textures per weapon
