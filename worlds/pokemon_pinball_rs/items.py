from BaseClasses import Item, ItemClassification
from .names import (RUBY_BOARD, SAPPHIRE_BOARD, AREAS, EXTRA_STARTING_LIFE, STARTING_COINS, STARTING_BALL_MODIFIER,
                    PICHU_UPGRADE, SPECIAL_GUESTS, ENCOUNTER_RATE_UP, RUINS_AREA_CARD, GET_ARROW, EVO_ARROW, HATCH_MODE,
                    CHIKORITA_DEX, CYNDAQUIL_DEX, TOTODILE_DEX, AERODACTYL_DEX)
from typing import NamedTuple


class PinballRSItem(Item):
    game = "Pokemon Pinball Ruby & Sapphire"


class ItemData(NamedTuple):
    idx: int
    classification: ItemClassification
    count: int = 1


MAIN_ITEMS: dict[str, ItemData] = {
    RUBY_BOARD: ItemData(1, ItemClassification.progression | ItemClassification.useful),
    SAPPHIRE_BOARD: ItemData(2, ItemClassification.progression | ItemClassification.useful),
    EXTRA_STARTING_LIFE: ItemData(3, ItemClassification.progression, count=9),
    STARTING_COINS: ItemData(4, ItemClassification.progression, count=9),
    STARTING_BALL_MODIFIER: ItemData(5, ItemClassification.useful, count=3),
    PICHU_UPGRADE: ItemData(6, ItemClassification.progression),
    SPECIAL_GUESTS: ItemData(7, ItemClassification.progression),
    ENCOUNTER_RATE_UP: ItemData(8, ItemClassification.progression),
    RUINS_AREA_CARD: ItemData(9, ItemClassification.progression),
    GET_ARROW: ItemData(10, ItemClassification.progression),
    EVO_ARROW: ItemData(11, ItemClassification.progression, count=3),
    HATCH_MODE: ItemData(12, ItemClassification.progression),
    CHIKORITA_DEX: ItemData(13, ItemClassification.progression),
    CYNDAQUIL_DEX: ItemData(14, ItemClassification.progression),
    TOTODILE_DEX: ItemData(15, ItemClassification.progression),
    AERODACTYL_DEX: ItemData(16, ItemClassification.progression),
}

AREA_ITEMS: dict[str, ItemData] = {
    area: ItemData(0x100 + idx, ItemClassification.progression) for idx, area in AREAS.items()
}

ALL_ITEMS: dict[str, ItemData] = {
    **MAIN_ITEMS,
    **AREA_ITEMS,
}

item_lookup: dict[str, int] = {
    key: data.idx for key, data in ALL_ITEMS.items()
}
