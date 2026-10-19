from BaseClasses import Item
from typing import NamedTuple
from .names import (flash_stopper, rain_flush, drill_bomb, pharaoh_shot, ring_boomerang, dust_crusher, dive_missile,
                    skull_barrier, rush_coil, rush_marine, rush_jet, wire_adaptor, balloon_adaptor, charge_buster,
                    bright_man_stage, toad_man_stage, drill_man_stage, pharaoh_man_stage, ring_man_stage,
                    dust_man_stage, dive_man_stage, skull_man_stage, cossack_1_stage, cossack_2_stage, cossack_3_stage,
                    cossack_4_stage, e_tank, weapon_energy, health_energy, one_up)


class ItemData(NamedTuple):
    code: int
    progression: bool
    useful: bool = False  # primarily use this for incredibly useful items of their class, like Metal Blade
    skip_balancing: bool = False


class MM4Item(Item):
    game = "Mega Man 4"


robot_master_weapon_table = {
    flash_stopper: ItemData(0x0001, True),
    rain_flush: ItemData(0x0002, True, True),
    drill_bomb: ItemData(0x0003, True),
    pharaoh_shot: ItemData(0x0004, True),
    ring_boomerang: ItemData(0x0005, True),
    dust_crusher: ItemData(0x0006, True),
    dive_missile: ItemData(0x0007, True, True),
    skull_barrier: ItemData(0x0008, True),
}

stage_access_table = {
    bright_man_stage: ItemData(0x0101, True),
    toad_man_stage: ItemData(0x0102, True),
    drill_man_stage: ItemData(0x0103, True),
    pharaoh_man_stage: ItemData(0x0104, True),
    ring_man_stage: ItemData(0x0105, True),
    dust_man_stage: ItemData(0x0106, True),
    dive_man_stage: ItemData(0x0107, True),
    skull_man_stage: ItemData(0x0108, True),
    cossack_1_stage: ItemData(0x0110, True, True),
    cossack_2_stage: ItemData(0x0111, True, True),
    cossack_3_stage: ItemData(0x0112, True, True),
    cossack_4_stage: ItemData(0x0113, True, True),
}

extra_item_table = {
    rush_coil: ItemData(0x0011, True, True),
    rush_marine: ItemData(0x0012, False, True),
    rush_jet: ItemData(0x0013, True, True),
    balloon_adaptor: ItemData(0x0014, True, True),
    wire_adaptor: ItemData(0x0015, True),
    charge_buster: ItemData(0x0024, False, True),
}

filler_item_table = {
    one_up: ItemData(0x0020, False),
    weapon_energy: ItemData(0x0021, False),
    health_energy: ItemData(0x0022, False),
    e_tank: ItemData(0x0023, False, True),
}

filler_item_weights = {
    one_up: 1,
    weapon_energy: 4,
    health_energy: 1,
    e_tank: 2,
}

item_table = {
    **robot_master_weapon_table,
    **stage_access_table,
    **extra_item_table,
    **filler_item_table,
}

item_names = {
    "Weapons": {name for name in robot_master_weapon_table.keys()},
    "Stages": {name for name in stage_access_table.keys()},
    "Rush": {name for name in extra_item_table.keys() if "Rush" in name}
}

lookup_item_to_id: dict[str, int] = {item_name: data.code for item_name, data in item_table.items() if data.code}
