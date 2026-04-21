from ..names import *
from typing import NamedTuple
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
        130: 2,
        75: 2,
        116: 2,
        118: 2,
        56: 2,
        151: 2,
        120: 3,
    },
    11: {
        51: 2,
        26: 2,
        65: 2,
        96: 2,
        182: 2,
        134: 2,
        175: 3,
        178: 3,
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
    1: [  # Ruby
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
    2: [  # Sapphire
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
    195,  # Latias
    196,  # Latios
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

bonus_catches: dict[int, list[int]] = {
    1: [198, 199],  # Ruby: Groudon and Rayquaza
    2: [197, 199]   # Sapphire: Kyogre and Rayquaza
}

eggs: list[int] = [
        13,  # Wurmple
        18,  # Lotad
        21,  # Seedot
        28,  # Ralts
        31,  # Surskit
        33,  # Shroomish
        44,  # Whismur
        53,  # Azurill
        60,  # Skitty
        62,  # Zubat
        69,  # Aron
        79,  # Plusle
        80,  # Minun
        87,  # Oddish
        94,  # Gulpin
        109,  # Spoink
        111,  # Sandshrew
        113,  # Spinda
        115,  # Trapinch
        136,  # Igglybuff
        145,  # Shuppet
        150,  # Chimecho
        159,  # Wynaut
        161,  # Natu
        164,  # Phanpy
        170,  # Snorunt
        172,  # Spheal
        179,  # Corsola
        180,  # Chinchou
        183,  # Horsea
        186,  # Bagon
    ]

egg_groups: dict[int, list[int]] = {
    1: [0, 3, 6, 9, 10],
    2: [13, 15, 20, 21, 23],
    3: [16, 17, 18, 24],
    4: [25, 26, 27, 29, 30],
    5: [2, 5, 8, 11, 12, 22],  # Ruby exclusives
    6: [1, 4, 7, 14, 19, 28],  # Sapphire exclusives
}

SPECIES_NONE = None

class Species(NamedTuple):
    speciesIdRS: int
    catchIndex: int
    eggIndex: int
    evolutionMethod: int
    evolutionTarget: str | None

species_info = {
    SPECIES_TREECKO: Species(
        277,
        0,
        0,
        1,
        SPECIES_GROVYLE
    ),
    SPECIES_GROVYLE: Species(
        278,
        0,
        0,
        1,
        SPECIES_SCEPTILE
    ),
    SPECIES_SCEPTILE: Species(
        279,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_TORCHIC: Species(
        280,
        1,
        0,
        1,
        SPECIES_COMBUSKEN
    ),
    SPECIES_COMBUSKEN: Species(
        281,
        0,
        0,
        1,
        SPECIES_BLAZIKEN
    ),
    SPECIES_BLAZIKEN: Species(
        282,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_MUDKIP: Species(
        283,
        2,
        0,
        1,
        SPECIES_MARSHTOMP
    ),
    SPECIES_MARSHTOMP: Species(
        284,
        0,
        0,
        1,
        SPECIES_SWAMPERT
    ),
    SPECIES_SWAMPERT: Species(
        285,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_POOCHYENA: Species(
        286,
        3,
        0,
        1,
        SPECIES_MIGHTYENA
    ),
    SPECIES_MIGHTYENA: Species(
        287,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_ZIGZAGOON: Species(
        288,
        4,
        0,
        1,
        SPECIES_LINOONE
    ),
    SPECIES_LINOONE: Species(
        289,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_WURMPLE: Species(
        290,
        0,
        0,
        11,
        SPECIES_SILCOON
    ),
    SPECIES_SILCOON: Species(
        291,
        5,
        0,
        1,
        SPECIES_BEAUTIFLY
    ),
    SPECIES_BEAUTIFLY: Species(
        292,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_CASCOON: Species(
        293,
        6,
        0,
        1,
        SPECIES_DUSTOX
    ),
    SPECIES_DUSTOX: Species(
        294,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_LOTAD: Species(
        295,
        0,
        1,
        1,
        SPECIES_LOMBRE
    ),
    SPECIES_LOMBRE: Species(
        296,
        7,
        0,
        6,
        SPECIES_LUDICOLO
    ),
    SPECIES_LUDICOLO: Species(
        297,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SEEDOT: Species(
        298,
        0,
        2,
        1,
        SPECIES_NUZLEAF
    ),
    SPECIES_NUZLEAF: Species(
        299,
        8,
        0,
        2,
        SPECIES_SHIFTRY
    ),
    SPECIES_SHIFTRY: Species(
        300,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_TAILLOW: Species(
        304,
        9,
        0,
        1,
        SPECIES_SWELLOW
    ),
    SPECIES_SWELLOW: Species(
        305,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_WINGULL: Species(
        309,
        10,
        0,
        1,
        SPECIES_PELIPPER
    ),
    SPECIES_PELIPPER: Species(
        310,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_RALTS: Species(
        392,
        0,
        3,
        1,
        SPECIES_KIRLIA
    ),
    SPECIES_KIRLIA: Species(
        393,
        0,
        0,
        1,
        SPECIES_GARDEVOIR
    ),
    SPECIES_GARDEVOIR: Species(
        394,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SURSKIT: Species(
        311,
        0,
        4,
        1,
        SPECIES_MASQUERAIN
    ),
    SPECIES_MASQUERAIN: Species(
        312,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SHROOMISH: Species(
        306,
        0,
        5,
        1,
        SPECIES_BRELOOM
    ),
    SPECIES_BRELOOM: Species(
        307,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SLAKOTH: Species(
        364,
        11,
        0,
        1,
        SPECIES_VIGOROTH
    ),
    SPECIES_VIGOROTH: Species(
        365,
        0,
        0,
        1,
        SPECIES_SLAKING
    ),
    SPECIES_SLAKING: Species(
        366,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_ABRA: Species(
        63,
        12,
        0,
        1,
        SPECIES_KADABRA
    ),
    SPECIES_KADABRA: Species(
        64,
        0,
        0,
        4,
        SPECIES_ALAKAZAM
    ),
    SPECIES_ALAKAZAM: Species(
        65,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_NINCADA: Species(
        301,
        13,
        0,
        1,
        SPECIES_NINJASK
    ),
    SPECIES_NINJASK: Species(
        302,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SHEDINJA: Species(
        303,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_WHISMUR: Species(
        370,
        0,
        6,
        1,
        SPECIES_LOUDRED
    ),
    SPECIES_LOUDRED: Species(
        371,
        14,
        0,
        1,
        SPECIES_EXPLOUD
    ),
    SPECIES_EXPLOUD: Species(
        372,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_MAKUHITA: Species(
        335,
        15,
        0,
        1,
        SPECIES_HARIYAMA
    ),
    SPECIES_HARIYAMA: Species(
        336,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_GOLDEEN: Species(
        118,
        16,
        0,
        1,
        SPECIES_SEAKING
    ),
    SPECIES_SEAKING: Species(
        119,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_MAGIKARP: Species(
        129,
        17,
        0,
        1,
        SPECIES_GYARADOS
    ),
    SPECIES_GYARADOS: Species(
        130,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_AZURILL: Species(
        350,
        0,
        7,
        9,
        SPECIES_MARILL
    ),
    SPECIES_MARILL: Species(
        183,
        18,
        0,
        1,
        SPECIES_AZUMARILL
    ),
    SPECIES_AZUMARILL: Species(
        184,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_GEODUDE: Species(
        74,
        19,
        0,
        1,
        SPECIES_GRAVELER
    ),
    SPECIES_GRAVELER: Species(
        75,
        0,
        0,
        4,
        SPECIES_GOLEM
    ),
    SPECIES_GOLEM: Species(
        76,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_NOSEPASS: Species(
        320,
        20,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SKITTY: Species(
        315,
        0,
        8,
        5,
        SPECIES_DELCATTY
    ),
    SPECIES_DELCATTY: Species(
        316,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_ZUBAT: Species(
        41,
        0,
        9,
        1,
        SPECIES_GOLBAT
    ),
    SPECIES_GOLBAT: Species(
        42,
        0,
        0,
        9,
        SPECIES_CROBAT
    ),
    SPECIES_CROBAT: Species(
        169,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_TENTACOOL: Species(
        72,
        21,
        0,
        1,
        SPECIES_TENTACRUEL
    ),
    SPECIES_TENTACRUEL: Species(
        73,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SABLEYE: Species(
        322,
        22,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_MAWILE: Species(
        355,
        23,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_ARON: Species(
        382,
        0,
        10,
        1,
        SPECIES_LAIRON
    ),
    SPECIES_LAIRON: Species(
        383,
        0,
        0,
        1,
        SPECIES_AGGRON
    ),
    SPECIES_AGGRON: Species(
        384,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_MACHOP: Species(
        66,
        24,
        0,
        1,
        SPECIES_MACHOKE
    ),
    SPECIES_MACHOKE: Species(
        67,
        0,
        0,
        4,
        SPECIES_MACHAMP
    ),
    SPECIES_MACHAMP: Species(
        68,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_MEDITITE: Species(
        356,
        25,
        0,
        1,
        SPECIES_MEDICHAM
    ),
    SPECIES_MEDICHAM: Species(
        357,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_ELECTRIKE: Species(
        337,
        26,
        0,
        1,
        SPECIES_MANECTRIC
    ),
    SPECIES_MANECTRIC: Species(
        338,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_PLUSLE: Species(
        353,
        0,
        11,
        0,
        SPECIES_NONE
    ),
    SPECIES_MINUN: Species(
        354,
        0,
        12,
        0,
        SPECIES_NONE
    ),
    SPECIES_MAGNEMITE: Species(
        81,
        27,
        0,
        1,
        SPECIES_MAGNETON
    ),
    SPECIES_MAGNETON: Species(
        82,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_VOLTORB: Species(
        100,
        28,
        0,
        1,
        SPECIES_ELECTRODE
    ),
    SPECIES_ELECTRODE: Species(
        101,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_VOLBEAT: Species(
        386,
        29,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_ILLUMISE: Species(
        387,
        30,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_ODDISH: Species(
        43,
        0,
        13,
        1,
        SPECIES_GLOOM
    ),
    SPECIES_GLOOM: Species(
        44,
        0,
        0,
        11,
        SPECIES_VILEPLUME
    ),
    SPECIES_VILEPLUME: Species(
        45,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_BELLOSSOM: Species(
        182,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_DODUO: Species(
        84,
        31,
        0,
        1,
        SPECIES_DODRIO
    ),
    SPECIES_DODRIO: Species(
        85,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_ROSELIA: Species(
        363,
        32,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_GULPIN: Species(
        367,
        0,
        14,
        1,
        SPECIES_SWALOT
    ),
    SPECIES_SWALOT: Species(
        368,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_CARVANHA: Species(
        330,
        33,
        0,
        1,
        SPECIES_SHARPEDO
    ),
    SPECIES_SHARPEDO: Species(
        331,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_WAILMER: Species(
        313,
        34,
        0,
        1,
        SPECIES_WAILORD
    ),
    SPECIES_WAILORD: Species(
        314,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_NUMEL: Species(
        339,
        35,
        0,
        1,
        SPECIES_CAMERUPT
    ),
    SPECIES_CAMERUPT: Species(
        340,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SLUGMA: Species(
        218,
        36,
        0,
        1,
        SPECIES_MAGCARGO
    ),
    SPECIES_MAGCARGO: Species(
        219,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_TORKOAL: Species(
        321,
        37,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_GRIMER: Species(
        88,
        38,
        0,
        1,
        SPECIES_MUK
    ),
    SPECIES_MUK: Species(
        89,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_KOFFING: Species(
        109,
        39,
        0,
        1,
        SPECIES_WEEZING
    ),
    SPECIES_WEEZING: Species(
        110,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SPOINK: Species(
        351,
        0,
        15,
        1,
        SPECIES_GRUMPIG
    ),
    SPECIES_GRUMPIG: Species(
        352,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SANDSHREW: Species(
        27,
        0,
        16,
        1,
        SPECIES_SANDSLASH
    ),
    SPECIES_SANDSLASH: Species(
        28,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SPINDA: Species(
        308,
        0,
        17,
        0,
        SPECIES_NONE
    ),
    SPECIES_SKARMORY: Species(
        227,
        40,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_TRAPINCH: Species(
        332,
        0,
        18,
        1,
        SPECIES_VIBRAVA
    ),
    SPECIES_VIBRAVA: Species(
        333,
        41,
        0,
        1,
        SPECIES_FLYGON
    ),
    SPECIES_FLYGON: Species(
        334,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_CACNEA: Species(
        344,
        42,
        0,
        1,
        SPECIES_CACTURNE
    ),
    SPECIES_CACTURNE: Species(
        345,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SWABLU: Species(
        358,
        43,
        0,
        1,
        SPECIES_ALTARIA
    ),
    SPECIES_ALTARIA: Species(
        359,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_ZANGOOSE: Species(
        380,
        44,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SEVIPER: Species(
        379,
        45,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_LUNATONE: Species(
        348,
        46,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SOLROCK: Species(
        349,
        47,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_BARBOACH: Species(
        323,
        48,
        0,
        1,
        SPECIES_WHISCASH
    ),
    SPECIES_WHISCASH: Species(
        324,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_CORPHISH: Species(
        326,
        49,
        0,
        1,
        SPECIES_CRAWDAUNT
    ),
    SPECIES_CRAWDAUNT: Species(
        327,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_BALTOY: Species(
        318,
        50,
        0,
        1,
        SPECIES_CLAYDOL
    ),
    SPECIES_CLAYDOL: Species(
        319,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_LILEEP: Species(
        388,
        51,
        0,
        1,
        SPECIES_CRADILY
    ),
    SPECIES_CRADILY: Species(
        389,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_ANORITH: Species(
        390,
        52,
        0,
        1,
        SPECIES_ARMALDO
    ),
    SPECIES_ARMALDO: Species(
        391,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_IGGLYBUFF: Species(
        174,
        0,
        19,
        9,
        SPECIES_JIGGLYPUFF
    ),
    SPECIES_JIGGLYPUFF: Species(
        39,
        53,
        0,
        5,
        SPECIES_WIGGLYTUFF
    ),
    SPECIES_WIGGLYTUFF: Species(
        40,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_FEEBAS: Species(
        328,
        54,
        0,
        10,
        SPECIES_MILOTIC
    ),
    SPECIES_MILOTIC: Species(
        329,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_CASTFORM: Species(
        385,
        55,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_STARYU: Species(
        120,
        56,
        0,
        6,
        SPECIES_STARMIE
    ),
    SPECIES_STARMIE: Species(
        121,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_KECLEON: Species(
        317,
        57,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SHUPPET: Species(
        377,
        0,
        20,
        1,
        SPECIES_BANETTE
    ),
    SPECIES_BANETTE: Species(
        378,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_DUSKULL: Species(
        361,
        58,
        0,
        1,
        SPECIES_DUSCLOPS
    ),
    SPECIES_DUSCLOPS: Species(
        362,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_TROPIUS: Species(
        369,
        59,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_CHIMECHO: Species(
        411,
        0,
        21,
        0,
        SPECIES_NONE
    ),
    SPECIES_ABSOL: Species(
        376,
        60,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_VULPIX: Species(
        37,
        61,
        0,
        3,
        SPECIES_NINETALES
    ),
    SPECIES_NINETALES: Species(
        38,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_PICHU: Species(
        172,
        0,
        22,
        9,
        SPECIES_PIKACHU
    ),
    SPECIES_PIKACHU: Species(
        25,
        62,
        0,
        7,
        SPECIES_RAICHU
    ),
    SPECIES_RAICHU: Species(
        26,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_PSYDUCK: Species(
        54,
        63,
        0,
        1,
        SPECIES_GOLDUCK
    ),
    SPECIES_GOLDUCK: Species(
        55,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_WYNAUT: Species(
        360,
        0,
        23,
        1,
        SPECIES_WOBBUFFET
    ),
    SPECIES_WOBBUFFET: Species(
        202,
        64,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_NATU: Species(
        177,
        0,
        24,
        1,
        SPECIES_XATU
    ),
    SPECIES_XATU: Species(
        178,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_GIRAFARIG: Species(
        203,
        65,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_PHANPY: Species(
        231,
        0,
        25,
        1,
        SPECIES_DONPHAN
    ),
    SPECIES_DONPHAN: Species(
        232,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_PINSIR: Species(
        127,
        66,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_HERACROSS: Species(
        214,
        67,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_RHYHORN: Species(
        111,
        68,
        0,
        1,
        SPECIES_RHYDON
    ),
    SPECIES_RHYDON: Species(
        112,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SNORUNT: Species(
        346,
        0,
        26,
        1,
        SPECIES_GLALIE
    ),
    SPECIES_GLALIE: Species(
        347,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_SPHEAL: Species(
        341,
        0,
        27,
        1,
        SPECIES_SEALEO
    ),
    SPECIES_SEALEO: Species(
        342,
        0,
        0,
        1,
        SPECIES_WALREIN
    ),
    SPECIES_WALREIN: Species(
        343,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_CLAMPERL: Species(
        373,
        69,
        0,
        11,
        SPECIES_HUNTAIL
    ),
    SPECIES_HUNTAIL: Species(
        374,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_GOREBYSS: Species(
        375,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_RELICANTH: Species(
        381,
        70,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_CORSOLA: Species(
        222,
        0,
        28,
        0,
        SPECIES_NONE
    ),
    SPECIES_CHINCHOU: Species(
        170,
        0,
        29,
        1,
        SPECIES_LANTURN
    ),
    SPECIES_LANTURN: Species(
        171,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_LUVDISC: Species(
        325,
        71,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_HORSEA: Species(
        116,
        0,
        30,
        1,
        SPECIES_SEADRA
    ),
    SPECIES_SEADRA: Species(
        117,
        0,
        0,
        4,
        SPECIES_KINGDRA
    ),
    SPECIES_KINGDRA: Species(
        230,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_BAGON: Species(
        395,
        0,
        31,
        1,
        SPECIES_SHELGON
    ),
    SPECIES_SHELGON: Species(
        396,
        72,
        0,
        1,
        SPECIES_SALAMENCE
    ),
    SPECIES_SALAMENCE: Species(
        397,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_BELDUM: Species(
        398,
        73,
        0,
        1,
        SPECIES_METANG
    ),
    SPECIES_METANG: Species(
        399,
        0,
        0,
        1,
        SPECIES_METAGROSS
    ),
    SPECIES_METAGROSS: Species(
        400,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_REGIROCK: Species(
        401,
        74,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_REGICE: Species(
        402,
        75,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_REGISTEEL: Species(
        403,
        76,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_LATIAS: Species(
        407,
        77,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_LATIOS: Species(
        408,
        78,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_KYOGRE: Species(
        404,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_GROUDON: Species(
        405,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_RAYQUAZA: Species(
        406,
        0,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_JIRACHI: Species(
        409,
        79,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_CHIKORITA: Species(
        152,
        80,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_CYNDAQUIL: Species(
        155,
        81,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_TOTODILE: Species(
        158,
        82,
        0,
        0,
        SPECIES_NONE
    ),
    SPECIES_AERODACTYL: Species(
        142,
        83,
        0,
        0,
        SPECIES_NONE
    )
}