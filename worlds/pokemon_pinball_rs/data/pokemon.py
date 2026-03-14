# Habitat:
#   Pokemon: min arrows
habitats: dict[int, dict[int, int]] = {
    0: {
        22: 2,
        11: 2,
        14: 2,
        16: 2,
        147: 2,
        144: 2,
        0: 3,
        41: 3,
    },
    1: {
        102: 2,
        152: 2,
        104: 2,
        100: 2,
        107: 2,
        114: 2,
        3: 3,
    },
    2: {
        86: 2,
        77: 2,
        9: 2,
        81: 2,
        83: 2,
        24: 2,
        141: 2,
        122: 3,
    },
    3: {
        98: 2,
        26: 2,
        65: 2,
        96: 2,
        182: 2,
        132: 2,
        142: 3,
        178: 3,
    },
    4: {
        157: 2,
        167: 2,
        163: 2,
        166: 2,
        168: 2,
        91: 2,
        160: 2,
        155: 3,
    },
    5: {
        125: 2,
        68: 2,
        72: 2,
        105: 2,
        187: 2,
        45: 2,
        59: 2,
        38: 3,
    },
    6: {
        189: 2,
        192: 2,
        193: 2,
        194: 3,
        200: 2,  # Not actually through Catch, but it shows up on roulette in this area
    },
    7: {
        35: 2,
        93: 2,
        14: 2,
        16: 2,
        147: 2,
        144: 2,
        149: 3,
        41: 3,
    },
    8: {
        49: 2,
        54: 2,
        19: 2,
        126: 2,
        128: 2,
        139: 2,
        6: 3
    },
    9: {
        137: 2,
        77: 2,
        9: 2,
        81: 2,
        83: 2,
        24: 2,
        141: 2,
        85: 3,
        123: 3,
    },
    10: {
        51: 2,
        26: 2,
        65: 2,
        96: 2,
        182: 2,
        134: 2,
        175: 3,
        178: 3,
    },
    11: {
        130: 2,
        75: 2,
        116: 2,
        118: 2,
        56: 2,
        151: 2,
        120: 3,
    },
    12: {
        124: 2,
        67: 3,
        47: 2,
        105: 2,
        187: 2,
        45: 2,
        59: 2,
        38: 3,
    },
    13: {
        189: 2,
        192: 2,
        193: 2,
        194: 3,
        200: 2,  # Not actually through Catch, but it shows up on roulette in this area
    },
}

egg_by_board: dict[int, list[int]] = {
    0: [  # Ruby
        13,  # Wurmple
        21,  # Seedot
        28,  # Ralts
        33,  # Shroomish
        44,  # Whismur
        60,  # Skitty
        62,  # Zubat
        69,  # Aron
        79,  # Plusle
        80,  # Minun
        87,  # Oddish
        109,  # Spoink
        111,  # Sandshrew
        113,  # Spinda
        115,  # Trapinch
        145,  # Shuppet
        150,  # Chimecho
        159,  # Wynaut
        161,  # Natu
        164,  # Phanpy
        170,  # Snorunt
        172,  # Spheal
        179,  # Corsola
        183,  # Horsea
        186,  # Bagon
    ],
    1: [  # Sapphire
        13,  # Wurmple
        18,  # Lotad
        28,  # Ralts
        31,  # Surskit
        44,  # Whismur
        53,  # Azurill
        62,  # Zubat
        69,  # Aron
        87,  # Oddish
        94,  # Gulpin
        109,  # Spoink
        111,  # Sandshrew
        113,  # Spinda
        115,  # Trapinch
        136,  # Igglybuff
        145,  # Shuppet
        150,  # Chimecho
        161,  # Natu
        164,  # Phanpy
        170,  # Snorunt
        172,  # Spheal
        179,  # Corsola
        180,  # Chinchou
        183,  # Horsea
        186,  # Bagon
    ]
}

# Evolved: unevolved
evolutions: dict[int, int] = {
    1: 0,
    2: 1,
    4: 3,
    5: 4,
    7: 6,
    8: 7,
    10: 9,
    12: 11,
    14: 13,
    15: 14,
    16: 13,
    17: 16,
    19: 18,
    20: 19,
    22: 21,
    23: 22,
    25: 24,
    27: 26,
    29: 28,
    30: 29,
    32: 31,
    34: 33,
    36: 35,
    37: 36,
    39: 38,
    40: 39,
    42: 41,
    43: 41,  # Notable special case: you can't "evolve" into a Shedinja, it just gets put in the pokedex on Ninjask evo
    45: 44,
    46: 45,
    48: 47,
    50: 49,
    52: 51,
    54: 53,
    55: 54,
    57: 56,
    58: 57,
    61: 60,
    63: 62,
    64: 63,
    66: 65,
    70: 69,
    71: 70,
    73: 72,
    74: 73,
    76: 75,
    78: 77,
    82: 81,
    84: 83,
    88: 87,
    89: 88,  # Ruby Board
    90: 88,  # Sapphire Board
    92: 91,
    95: 94,
    97: 96,
    99: 98,
    101: 100,
    103: 102,
    106: 105,
    108: 107,
    110: 109,
    112: 111,
    116: 115,
    117: 116,
    119: 118,
    121: 120,
    127: 126,
    129: 128,
    131: 130,
    133: 132,
    135: 133,
    137: 136,
    138: 137,
    140: 139,
    143: 142,
    146: 145,
    148: 147,
    153: 152,
    155: 154,  # lmao, you're never doing this
    156: 155,
    158: 157,
    160: 159,
    162: 161,
    165: 164,
    169: 168,
    171: 170,
    173: 172,
    174: 173,
    176: 175,
    177: 175,
    181: 180,
    184: 183,
    185: 184,
    187: 186,
    188: 187,
    190: 189,
    191: 190,
}

special_encounters: list[int] = [
    195,  # Latios
    196,  # Latias
    154,  # Pichu
    201,  # Chikorita
    202,  # Cyndaquil
    203,  # Totodile
    204,  # Aerodactyl
]

rare_encounters: list[int] = [
    # Affected by the Encounter Rate UP
    59,   # Nosepass
    114,  # Skarmory
    132,  # Lileep
    134,  # Anorith
    139,  # Feebas
    141,  # Castform
    144,  # Kecleon
    151,  # Absol
    160,  # Wobbuffet
]
