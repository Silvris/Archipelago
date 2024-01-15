import itertools
import struct

def setup_gamevars(world):
    world.city_order = [0x04, 0x0B, 0x08, 0x0C, 0x00, 0x01, 0x0E, 0x06, 0x0D, 0x05, 0x02, 0x0A, 0x07, 0x09, 0x03]
    world.city_list = []
    if world.options.city_shuffle != 0:
        world.random.shuffle(world.city_order)

    city_code = {
        0x00: "Rome",
        0x01: "Paris",
        0x02: "London",
        0x03: "New York",
        0x04: "San Francisco",
        0x05: "Athens",
        0x06: "Sydney",
        0x07: "Tokyo",
        0x08: "Nairobi",
        0x09: "Rio de Janeiro",
        0x0A: "Cairo",
        0x0B: "Moscow",
        0x0C: "Beijing",
        0x0D: "Buenos Aires",
        0x0E: "Mexico City",
    }
    world.city_list = [city_code[world.city_order[i]] for i in range(15)]
    world.city_order = list(itertools.chain.from_iterable((x, 0x00) for x in world.city_order))

def rgb888_to_bgr555(red, green, blue) -> bytes:
    red = red >> 3
    green = green >> 3
    blue = blue >> 3
    outcol = (blue << 10) + (green << 5) + red
    return struct.pack("H", outcol)

def get_palette_bytes(palette, target, offset, factor):
    output_data = bytearray()
    for color in target:
        hexcol = palette[color]
        if hexcol.startswith("#"):
            hexcol = hexcol.replace("#", "")
        colint = int(hexcol, 16)
        col = ((colint & 0xFF0000) >> 16, (colint & 0xFF00) >> 8, colint & 0xFF)
        col = tuple(int(int(factor*x) + offset) for x in col)
        byte_data = rgb888_to_bgr555(col[0], col[1], col[2])
        output_data.extend(bytearray(byte_data))
    return output_data

shirt_color_data = {
    0x00E870: (["bright", "base", "dark"], 0, 1), #Normal play
    0x045E2A: (["bright", "base", "dark"], 0, 1), #Road north, Yoshi
    0x04642E: (["bright", "base", "dark"], 0, 1), #Road south, Yoshi
    0x047201: (["bright", "base", "dark"], 0, 1), #Road screech, Yoshi South
    0x01721B: (["bright", "base", "dark"], 0, 1), #Road screech, Yoshi North
    0x043D54: (["bright", "base", "dark"], 0, 1), #Road north
    0x0441FE: (["bright", "base", "dark"], 0, 1), #Road south
    0x044941: (["bright", "base", "dark"], 0, 1), #Road screech, North
    0x04522B: (["bright", "base", "dark"], 0, 1) #Road screech, South
    #0x04522B: (["3", "2", "1"], 0, 1)Intro Scene
}

pants_color_data = {
    0x00E876: (["bright", "base", "dark"], 0, 1), #Normal play
    0x045E30: (["bright", "base", "dark"], 0, 1), #Road north, Yoshi
    0x046434: (["bright", "base", "dark"], 0, 1), #Road south, Yoshi
    0x047207: (["bright", "base", "dark"], 0, 1), #Road screech, Yoshi South
    0x017221: (["bright", "base", "dark"], 0, 1), #Road screech, Yoshi North
    0x043D5A: (["bright", "base", "dark"], 0, 1), #Road north
    0x044204: (["bright", "base", "dark"], 0, 1), #Road south
    0x044947: (["bright", "base", "dark"], 0, 1), #Road screech, North
    0x045231: (["bright", "base", "dark"], 0, 1) #Road screech, South
    #0x04522B: (["3", "2", "1"], 0, 1)Intro Scene
}

def get_shirt_color(world):
    return world.options.shirt_color.value

def get_pants_color(world):
    return world.options.pants_color.value