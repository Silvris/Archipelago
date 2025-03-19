from .names import items, locations
from BaseClasses import Item
from typing import NamedTuple, Dict, Optional


class DMC5Item(Item):
    game = "Devil May Cry 5"


class ItemData(NamedTuple):
    code: Optional[int]
    progression: bool
    useful: bool = False
    count: int = 1


chapter_items: Dict[str, ItemData] = {
    locations.prologue: ItemData(1, True),
    locations.chapter1: ItemData(2, True),
    locations.chapter2: ItemData(3, True),
    locations.chapter3: ItemData(4, True),
    locations.chapter4: ItemData(5, True),
    locations.chapter5: ItemData(6, True),
    locations.chapter6: ItemData(7, True),
    items.chapter7: ItemData(8, True),
    locations.chapter8: ItemData(10, True),
    locations.chapter9: ItemData(11, True),
    locations.chapter10: ItemData(12, True),
    locations.chapter11: ItemData(13, True),
    locations.chapter12: ItemData(14, True),
    items.chapter13: ItemData(15, True),
    locations.chapter14: ItemData(18, True),
    locations.chapter15: ItemData(19, True),
    locations.chapter16: ItemData(20, True),
    locations.chapter17: ItemData(21, True),
    locations.chapter18: ItemData(22, True),
    locations.chapter19: ItemData(23, True),
    locations.chapter20: ItemData(None, True),
}

vergil_chapter_items: Dict[str, ItemData] = {
    locations.prologuev: ItemData(24, True),
    locations.chapter1v: ItemData(25, True),
    locations.chapter2v: ItemData(26, True),
    locations.chapter3v: ItemData(27, True),
    locations.chapter4v: ItemData(28, True),
    locations.chapter5v: ItemData(29, True),
    locations.chapter6v: ItemData(30, True),
    locations.chapter7v: ItemData(31, True),
    locations.chapter8v: ItemData(32, True),
    locations.chapter9v: ItemData(33, True),
    locations.chapter10v: ItemData(34, True),
    locations.chapter11v: ItemData(35, True),
    locations.chapter12v: ItemData(36, True),
    locations.chapter13v: ItemData(37, True),
    locations.chapter14v: ItemData(38, True),
    locations.chapter15v: ItemData(39, True),
    locations.chapter16v: ItemData(40, True),
    locations.chapter17v: ItemData(41, True),
    locations.chapter18v: ItemData(42, True),
    locations.chapter19v: ItemData(None, True),
}

nero_upgrades: Dict[str, ItemData] = {
    items.nero_devil_trigger: ItemData(100, True, True),
    items.nero_speed: ItemData(101, False, True),
    items.nero_enemy_step: ItemData(102, False, True),
    items.nero_air_hike: ItemData(103, True, True),
    items.nero_more_orbs: ItemData(104, True, True),
    items.nero_trigger_heart: ItemData(105, False, True),
    items.nero_ex_provocation: ItemData(106, True, False),
    items.nero_table_hopper: ItemData(110, False, False, 3),
    items.nero_charge_shot: ItemData(113, False, False, 3),
    items.nero_combo_b: ItemData(117, True, True),
    items.nero_combo_c: ItemData(118, True, True),
    items.nero_combo_d: ItemData(119, True, True),
    items.nero_roulette_spin: ItemData(120, True, True),
    items.nero_streak: ItemData(121, True, True, 2),
    items.nero_split: ItemData(123, True, True),
    items.nero_calibur: ItemData(124, True, True),
    items.nero_shuffle: ItemData(125, True, True),
    items.nero_hard_way: ItemData(126, True, True),
    items.nero_payline: ItemData(127, True, True),
    items.nero_exceed: ItemData(128, True, True, 2),
    items.nero_max_act: ItemData(130, True, True),
    items.nero_wire_snatch: ItemData(132, True, False, 3),
    items.nero_flat_top: ItemData(135, True, True),
    items.nero_showdown: ItemData(137, True, True),
    items.nero_maximum_bet: ItemData(138, True, True),
    items.nero_holster: ItemData(148, False, True, 5),
    items.nero_color_up: ItemData(153, True, True, 2),
}

misc_items: Dict[str, ItemData] = {
    items.red_orb: ItemData(800, False, False),
    items.gold_orb: ItemData(801, False, False),
    items.purple_orb_shard: ItemData(802, False, True),
    items.purple_orb: ItemData(803, False, True),
    items.blue_orb_shard: ItemData(804, False, True),
    items.blue_orb: ItemData(805, False, True),
    items.nidhogg_hatchling: ItemData(806, True, False),
}

filler_item_weights: Dict[str, int] = {
    items.red_orb: 10,
    items.gold_orb: 1,
}

all_items: Dict[str, ItemData] = {
    **chapter_items,
    **vergil_chapter_items,
    **nero_upgrades,
    **misc_items,
}

item_lookup = {key: data.code for key, data in all_items.items() if data.code}

item_groups = {
    "Chapters": {name for name in chapter_items},
    "Vergil Chapters": {name for name in vergil_chapter_items}
}
