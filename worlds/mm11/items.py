from BaseClasses import Item
from typing import NamedTuple
from .names import (block_dropper, acid_barrier, pile_driver, bounce_ball, scramble_thunder, tundra_storm,
                    blazing_torch, chain_blast, charge_buster, speed_gear, power_gear, rush_coil, rush_jet, e_tank,
                    weapon_energy, health_energy, one_up, w_tank, small_bolt, big_bolt, block_man_stage, acid_man_stage,
                    impact_man_stage, bounce_man_stage, fuse_man_stage, tundra_man_stage, torch_man_stage,
                    blast_man_stage, energy_balancer, energy_balancer_neo, auto_charge, buster_plus, power_shield,
                    spike_boots, shock_absorber, speed_gear_booster, energy_dispenser, awakener, screws_up, health_up,
                    weapon_up, cooling_fan, cooling_infinite, mystery, buddy_plus, tank_container, lives_schematic,
                    etank_schematic, mtank_schematic, wtank_schematic, pierce_protect_schematic, super_guard_schematic,
                    eddie_call_schematic, beat_call_schematic)


class ItemData(NamedTuple):
    code: int
    progression: bool
    useful: bool = False  # primarily use this for incredibly useful items of their class, like Metal Blade
    skip_balancing: bool = False


class MM11Item(Item):
    game = "Mega Man 11"


robot_master_weapon_table = {
    block_dropper: ItemData(0x0001, True),
    acid_barrier: ItemData(0x0002, True),
    pile_driver: ItemData(0x0003, True, True),
    bounce_ball: ItemData(0x0004, True),
    scramble_thunder: ItemData(0x0005, True),
    tundra_storm: ItemData(0x0006, True),
    blazing_torch: ItemData(0x0007, True),
    chain_blast: ItemData(0x0008, True),
}

stage_access_table = {
    block_man_stage: ItemData(0x0101, True),
    acid_man_stage: ItemData(0x0102, True),
    impact_man_stage: ItemData(0x0103, True),
    bounce_man_stage: ItemData(0x0104, True),
    fuse_man_stage: ItemData(0x0105, True),
    tundra_man_stage: ItemData(0x0106, True),
    torch_man_stage: ItemData(0x0107, True),
    blast_man_stage: ItemData(0x0108, True),
}

extra_item_table = {
    rush_coil: ItemData(0x0011, True),
    rush_jet: ItemData(0x0012, True),
    speed_gear: ItemData(0x0013, True, True),
    power_gear: ItemData(0x0014, True, True),
    charge_buster: ItemData(0x0015, True, True),
    energy_balancer: ItemData(0x0030, False, True),
    energy_balancer_neo: ItemData(0x0031, False, True),
    auto_charge: ItemData(0x0032, False, True),
    buster_plus: ItemData(0x0033, False, True),
    power_shield: ItemData(0x0034, False, True),
    spike_boots: ItemData(0x0035, True),
    shock_absorber: ItemData(0x0036, False, True),
    speed_gear_booster: ItemData(0x0037, False, True),
    energy_dispenser: ItemData(0x0038, False, True),
    awakener: ItemData(0x0039, False, True),
    screws_up: ItemData(0x003A, False, True),
    health_up: ItemData(0x003B, False, True),
    weapon_up: ItemData(0x003C, False, True),
    cooling_fan: ItemData(0x003D, False, True),
    cooling_infinite: ItemData(0x003E, False, True),
    mystery: ItemData(0x003F, False, True),
    buddy_plus: ItemData(0x0040, False, True),
    tank_container: ItemData(0x0041, False, True),
    lives_schematic: ItemData(0x0042, False, True),
    etank_schematic: ItemData(0x0043, False, True),
    mtank_schematic: ItemData(0x0044, False, True),
    wtank_schematic: ItemData(0x0045, False, True),
    pierce_protect_schematic: ItemData(0x0046, False, True),
    super_guard_schematic: ItemData(0x0047, False, True),
    eddie_call_schematic: ItemData(0x0048, False, True),
    beat_call_schematic: ItemData(0x0049, False, True),
}

filler_item_table = {
    one_up: ItemData(0x0020, False),
    weapon_energy: ItemData(0x0021, False),
    health_energy: ItemData(0x0022, False),
    e_tank: ItemData(0x0023, False, True),
    w_tank: ItemData(0x0024, False, True),
    small_bolt: ItemData(0x0025, False),
    big_bolt: ItemData(0x0026, False),
}

filler_item_weights = {
    one_up: 2,
    weapon_energy: 4,
    health_energy: 3,
    e_tank: 1,
    w_tank: 1,
    small_bolt: 10,
    big_bolt: 5,
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
