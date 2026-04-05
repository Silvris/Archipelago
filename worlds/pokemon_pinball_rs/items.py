from BaseClasses import Item, ItemClassification
from .names import (RUBY_BOARD, SAPPHIRE_BOARD, AREAS, EXTRA_STARTING_LIFE, STARTING_COINS, STARTING_BALL_MODIFIER,
                    PICHU_UPGRADE, SPECIAL_GUESTS, ENCOUNTER_RATE_UP, RUINS_AREA_CARD, GET_ARROW, EVO_ARROW,
                    CHIKORITA_DEX, CYNDAQUIL_DEX, TOTODILE_DEX, AERODACTYL_DEX, EGG_BUNCH_1, EGG_BUNCH_2, EGG_BUNCH_3,
                    EGG_BUNCH_4, EGG_BUNCH_RUBY, EGG_BUNCH_SAPPHIRE, BIG, SMALL, BALL_SAVER, EXTRA_BALL,
                    EVOLUTION_METHODS, EVO_MODE, HELPER_ZIGZAGOON, HELPER_MAKUHITA, HELPER_PELIPPER, HELPER_WHISCASH)
from typing import NamedTuple


class PinballRSItem(Item):
    game = "Pokemon Pinball Ruby & Sapphire"


class ItemData(NamedTuple):
    idx: int
    classification: ItemClassification
    num: int = 1


MAIN_ITEMS: dict[str, ItemData] = {
    RUBY_BOARD: ItemData(1, ItemClassification.progression | ItemClassification.useful),
    SAPPHIRE_BOARD: ItemData(2, ItemClassification.progression | ItemClassification.useful),
    EXTRA_STARTING_LIFE: ItemData(3, ItemClassification.progression, num=9),
    STARTING_COINS: ItemData(4, ItemClassification.progression, num=9),
    STARTING_BALL_MODIFIER: ItemData(5, ItemClassification.useful, num=3),
    PICHU_UPGRADE: ItemData(6, ItemClassification.progression),
    SPECIAL_GUESTS: ItemData(7, ItemClassification.progression),
    ENCOUNTER_RATE_UP: ItemData(8, ItemClassification.progression),
    RUINS_AREA_CARD: ItemData(9, ItemClassification.progression),
    GET_ARROW: ItemData(10, ItemClassification.progression),
    EVO_ARROW: ItemData(11, ItemClassification.progression, num=3),
    EVO_MODE: ItemData(12, ItemClassification.progression),
    CHIKORITA_DEX: ItemData(13, ItemClassification.progression),
    CYNDAQUIL_DEX: ItemData(14, ItemClassification.progression),
    TOTODILE_DEX: ItemData(15, ItemClassification.progression),
    AERODACTYL_DEX: ItemData(16, ItemClassification.progression),
    EGG_BUNCH_1: ItemData(17, ItemClassification.progression),
    EGG_BUNCH_2: ItemData(18, ItemClassification.progression),
    EGG_BUNCH_3: ItemData(19, ItemClassification.progression),
    EGG_BUNCH_4: ItemData(20, ItemClassification.progression),
    EGG_BUNCH_RUBY: ItemData(21, ItemClassification.progression),
    EGG_BUNCH_SAPPHIRE: ItemData(22, ItemClassification.progression),
}

AREA_ITEMS: dict[str, ItemData] = {
    area: ItemData(0x100 + idx, ItemClassification.progression) for idx, area in AREAS.items()
}

EVOLUTION_ITEMS: dict[str, ItemData] = {
    evo_item: ItemData(0x400 + idx, ItemClassification.progression) for idx, evo_item in EVOLUTION_METHODS.items()
}

HELPER_ITEMS: dict[str, ItemData] = {
    HELPER_ZIGZAGOON: ItemData(0x800, ItemClassification.useful),
    HELPER_MAKUHITA: ItemData(0x801, ItemClassification.progression),
    HELPER_PELIPPER: ItemData(0x802, ItemClassification.progression),
    HELPER_WHISCASH: ItemData(0x803, ItemClassification.progression),
}

FILLER_ITEMS: dict[str, ItemData] = {
    EXTRA_BALL: ItemData(0x200, ItemClassification.filler),
    BIG: ItemData(0x201, ItemClassification.filler),
    SMALL: ItemData(0x202, ItemClassification.filler),
    BALL_SAVER: ItemData(0x203, ItemClassification.filler),
}

FILLER_ITEM_WEIGHTS: dict[str, int] = {
    EXTRA_BALL: 3,
    BIG: 10,
    SMALL: 15,
    BALL_SAVER: 10,
}

ALL_ITEMS: dict[str, ItemData] = {
    **MAIN_ITEMS,
    **AREA_ITEMS,
    **EVOLUTION_ITEMS,
    **FILLER_ITEMS,
}

item_lookup: dict[str, int] = {
    key: data.idx for key, data in ALL_ITEMS.items()
}
