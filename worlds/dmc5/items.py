from .names import items, locations
from BaseClasses import Item
from typing import NamedTuple


class DMC5Item(Item):
    game = "Devil May Cry 5"


class ItemData(NamedTuple):
    code: int | None
    progression: bool
    useful: bool = False
    count: int = 1


chapter_items: dict[str, ItemData] = {
    locations.prologue: ItemData(1, True),
    locations.chapter1: ItemData(2, True),
    locations.chapter2: ItemData(3, True),
    locations.chapter3: ItemData(4, True),
    locations.chapter4: ItemData(5, True),
    locations.chapter5: ItemData(6, True),
    locations.chapter6: ItemData(7, True),
    items.chapter7: ItemData(8, True),
    locations.chapter8: ItemData(9, True),
    locations.chapter9: ItemData(10, True),
    locations.chapter10: ItemData(11, True),
    locations.chapter11: ItemData(12, True),
    locations.chapter12: ItemData(13, True),
    items.chapter13: ItemData(14, True),
    locations.chapter14: ItemData(15, True),
    locations.chapter15: ItemData(16, True),
    locations.chapter16: ItemData(17, True),
    locations.chapter17: ItemData(18, True),
    locations.chapter18: ItemData(19, True),
    locations.chapter19: ItemData(20, True),
    locations.chapter20: ItemData(None, True),
}

vergil_chapter_items: dict[str, ItemData] = {
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

nero_upgrades: dict[str, ItemData] = {
    items.nero_devil_trigger: ItemData(100, True, True),
    items.nero_speed: ItemData(101, False, True),
    items.nero_enemy_step: ItemData(102, False, True),
    items.nero_air_hike: ItemData(103, True, True),
    items.nero_more_orbs: ItemData(104, True, True),
    items.nero_trigger_heart: ItemData(105, False, True),
    items.nero_ex_provocation: ItemData(106, False, True),
    items.nero_table_hopper: ItemData(110, False, False, 3),
    items.nero_charge_shot: ItemData(113, True, True, 3),
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
    items.nero_wire_snatch: ItemData(132, True, False, 2),
    items.nero_flat_top: ItemData(135, True, True),
    items.nero_showdown: ItemData(137, True, True),
    items.nero_maximum_bet: ItemData(138, True, True),
    items.nero_holster: ItemData(148, False, True, 5),
    items.nero_color_up: ItemData(153, True, True, 2),
}

dante_weapons: dict[str, ItemData] = {
    items.devil_sword_sparda: ItemData(1001, False, True),
    items.devil_sword_dante: ItemData(1002, True, True),
    items.balrog: ItemData(1003, True, True),
    items.cavaliere: ItemData(1004, True, True),
    items.cerberus: ItemData(1005, True, True),
    items.coyote: ItemData(1006, True, True),
    items.kalina_ann: ItemData(1007, True, True),
    items.w_kalina_ann: ItemData(1008, True, True),
    items.dr_faust: ItemData(1009, True, True),
}

dante_upgrades: dict[str, ItemData] = {
    items.dante_speed: ItemData(201, False, True),
    items.dante_enemy_step: ItemData(202, False, True),
    items.dante_air_hike: ItemData(203, True, True),
    items.dante_more_orbs: ItemData(204, True, True),
    items.dante_trigger_heart: ItemData(205, False, True),
    items.dante_ex_provocation: ItemData(206, True, True),
    items.dante_irregular_full_custom: ItemData(209, False, False),
    items.dante_stinger: ItemData(210, True, True, 2),
    items.dante_million_stab: ItemData(212, True, True),
    items.dante_drive: ItemData(213, True, True, 2),
    items.dante_swords_formation: ItemData(215, True, True, 3),
    items.dante_rolling_blaze: ItemData(218, True, True),
    items.dante_bantam_revenge: ItemData(219, True, True),
    items.dante_fly_dragon: ItemData(220, True, False),
    items.dante_updraft: ItemData(221, True, False),
    items.dante_ignition: ItemData(222, True, True, 2),
    items.dante_cross_line: ItemData(224, True, True),
    items.dante_slipstream: ItemData(227, True, True),
    items.dante_highside: ItemData(228, True, True),
    items.dante_braking: ItemData(229, True, True),
    items.dante_revolver: ItemData(230, True, True, 2),
    items.dante_crystal: ItemData(232, True, True),
    items.dante_ice_age: ItemData(233, True, True),
    items.dante_long_revolver: ItemData(234, True, True),
    items.dante_thunder_clap: ItemData(235, True, True),
    items.dante_charge_shot: ItemData(236, True, True, 3),
    items.dante_coyote_charge_shot: ItemData(239, True, True, 3),
    items.dante_high_explosive: ItemData(242, True, True),  # shared across kalinas?
    items.dante_hat_trick: ItemData(244, True, True),
    items.dante_man_in_the_red: ItemData(245, True, True),
    items.dante_faust: ItemData(246, True, True),
    items.dante_trickster: ItemData(249, True, True, 3),
    items.dante_swordmaster: ItemData(252, True, True, 3),
    items.dante_gunslinger: ItemData(255, True, True, 3),
    items.dante_royalguard: ItemData(258, True, True, 3),
    items.dante_sin_stinger: ItemData(261, True, True),
    items.dante_sin_inferno: ItemData(262, True, True),
    items.dante_demolition: ItemData(263, True, True),
    items.dante_the_luce: ItemData(264, True, True),
    items.dante_quadruple_s: ItemData(265, False, True),
}

v_upgrades: dict[str, ItemData] = {

}

vergil_upgrades: dict[str, ItemData] = {

}

misc_items: dict[str, ItemData] = {
    items.red_orb: ItemData(800, False, False),
    items.gold_orb: ItemData(801, False, False),
    items.purple_orb_shard: ItemData(802, False, True),
    items.purple_orb: ItemData(803, False, True),
    items.blue_orb_shard: ItemData(804, False, True),
    items.blue_orb: ItemData(805, False, True),
    items.nidhogg_hatchling: ItemData(806, True, False),
}

filler_item_weights: dict[str, int] = {
    items.red_orb: 10,
    items.gold_orb: 1,
}

all_items: dict[str, ItemData] = {
    **chapter_items,
    **vergil_chapter_items,
    **nero_upgrades,
    **misc_items,
}

item_lookup = {key: data.code for key, data in all_items.items() if data.code}

item_groups = {
    "Chapters": {name for name in chapter_items if chapter_items[name].code},
    "Vergil Chapters": {name for name in vergil_chapter_items if vergil_chapter_items[name].code},
    "Nero Upgrades": {name for name in nero_upgrades},
    "Dante Weapons": {name for name in dante_weapons},
    "Dante Upgrades": {name for name in dante_upgrades},
    "V Upgrades": {name for name in v_upgrades},
    "Vergil Upgrades": {name for name in vergil_upgrades},
}
