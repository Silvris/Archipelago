from typing import NamedTuple
from BaseClasses import Item


class MM1Item(Item):
    game = "Mega Man"


class ItemData(NamedTuple):
    item_id: int
    progression: bool
    useful: bool = False


weapons: dict[str, ItemData] = {
    "Rolling Cutter": ItemData(0x1, True),
    "Ice Slasher": ItemData(0x2, True),
    "Hyper Bomb": ItemData(0x3, True),
    "Fire Storm": ItemData(0x4, True),
    "Thunder Beam": ItemData(0x5, True),
    "Super Arm": ItemData(0x6, True),
}

stage_access: dict[str, ItemData] = {
    "Cut Man Access Codes": ItemData(0x11, True),
    "Ice Man Access Codes": ItemData(0x12, True),
    "Bomb Man Access Codes": ItemData(0x13, True),
    "Fire Man Access Codes": ItemData(0x14, True),
    "Elec Man Access Codes": ItemData(0x15, True),
    "Guts Man Access Codes": ItemData(0x16, True),
}

misc_items: dict[str, ItemData] = {
    "Magnet Beam": ItemData(0x7, True, True),
    "1-Up": ItemData(0x20, False),
    "Weapon Energy (L)": ItemData(0x21, False),
    "Health Energy (L)": ItemData(0x22, False),
}

all_items: dict[str, ItemData] = {
    **weapons,
    **stage_access,
    **misc_items
}

item_lookup: dict[str, int] = {item: data.item_id for item, data in all_items.items() if data.item_id}
