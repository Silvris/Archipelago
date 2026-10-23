import hashlib
import logging
from copy import deepcopy
from typing import Any, Sequence, ClassVar

from BaseClasses import Tutorial, ItemClassification, MultiWorld, Item, Location
from worlds.AutoWorld import World, WebWorld
from .color import check_for_known_worlds
from .items import (item_table, item_names, MM11Item, filler_item_weights, robot_master_weapon_table,
                    stage_access_table, extra_item_table, lookup_item_to_id)
from .locations import (MM11Location, mm11_regions, MM11Region, lookup_location_to_id,
                        location_groups)
from .names import (wily_4_boss, charge_buster, block_man_stage, acid_man_stage, impact_man_stage, bounce_man_stage,
                    fuse_man_stage, tundra_man_stage, torch_man_stage, blast_man_stage)
from .options import MM11Options, Consumables
from .rules import set_rules, weapon_damage, robot_masters, weapons_to_name, minimum_weakness_requirement
import os
import threading
import base64
logger = logging.getLogger("Mega Man 11")


class MM11WebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [

        Tutorial(
           "Multiworld Setup Guide",
           "A guide to setting up the Mega Man 11 randomizer connected to an Archipelago Multiworld.",
           "English",
           "setup_en.md",
           "setup/en",
           ["Silvris"]
        )
    ]


class MM11World(World):
    """
    MM11
    """

    game = "Mega Man 11"
    options_dataclass = MM11Options
    options: MM11Options
    item_name_to_id = lookup_item_to_id
    location_name_to_id = lookup_location_to_id
    item_name_groups = item_names
    location_name_groups = location_groups
    web = MM11WebWorld()
    rom_name: bytearray

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name = bytearray()
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)
        self.weapon_damage = deepcopy(weapon_damage)
        self.wily_3_weapons: dict[int, list[int]] = {}

    def create_regions(self) -> None:
        menu = MM11Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        location: MM11Location
        for name, region in mm11_regions.items():
            stage = MM11Region(name, self.player, self.multiworld)
            if not region.parent:
                menu.connect(stage, f"To {name}")
            else:
                old_stage = self.get_region(region.parent)
                old_stage.connect(stage, f"To {name}")
            stage.add_locations({loc: data.location_id for loc, data in region.locations.items()
                                 if (not data.energy or self.options.consumables.value in (Consumables.option_weapon_health, Consumables.option_all))
                                 and (not data.oneup_tank or self.options.consumables.value in (Consumables.option_1up_etank, Consumables.option_all))})
            self.multiworld.regions.append(stage)
        goal_location = self.get_location(wily_4_boss)
        goal_location.place_locked_item(MM11Item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_item(self, name: str, force_non_progression: bool = False) -> MM11Item:
        item = item_table[name]
        classification = ItemClassification.filler
        if item.progression and not force_non_progression:
            classification = ItemClassification.progression_skip_balancing \
                if item.skip_balancing else ItemClassification.progression
        if item.useful:
            classification |= ItemClassification.useful
        return MM11Item(name, classification, item.code, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(filler_item_weights.keys()),
                                   weights=list(filler_item_weights.values()))[0]

    def create_items(self) -> None:
        itempool = []
        # grab first robot master
        robot_master = self.item_id_to_name[0x0101 + self.options.starting_robot_master.value]
        self.multiworld.push_precollected(self.create_item(robot_master))
        itempool.extend([self.create_item(name) for name in stage_access_table.keys()
                         if name != robot_master])
        itempool.extend([self.create_item(name) for name in robot_master_weapon_table.keys()])
        itempool.extend([self.create_item(name) for name in extra_item_table.keys()])
        total_checks = 27
        if self.options.consumables in (Consumables.option_1up_etank,
                                        Consumables.option_all):
            total_checks += 22
        if self.options.consumables in (Consumables.option_weapon_health,
                                        Consumables.option_all):
            total_checks += 51
        remaining = total_checks - len(itempool)
        itempool.extend([self.create_item(name)
                         for name in self.random.choices(list(filler_item_weights.keys()),
                                                         weights=list(filler_item_weights.values()),
                                                         k=remaining)])
        self.multiworld.itempool += itempool

    set_rules = set_rules

    def fill_hook(self,
                  prog_item_pool: list["Item"],
                  useful_item_pool: list["Item"],
                  filler_item_pool: list["Item"],
                  fill_locations: list["Location"]) -> None:
        if self.multiworld.players:
            # testing this again
            return  # Don't need to change anything on a multi gen, fill should be able to solve it with a 4 sphere 1
        if self.options.consumables:
            return  # The only affected stages have both types of consumable
        rbm_to_item = {
            0: block_man_stage,
            1: acid_man_stage,
            2: impact_man_stage,
            3: bounce_man_stage,
            4: fuse_man_stage,
            5: tundra_man_stage,
            6: torch_man_stage,
            7: blast_man_stage
        }
        affected_rbm = [0, 4, 5, 7]
        possible_rbm = [1, 2, 3, 6]  # Marine/Jet/Balloon/Wire respectively
        if self.options.starting_robot_master.value in affected_rbm:
            rbm_names = list(map(lambda s: rbm_to_item[s], possible_rbm))
            valid_second = [item for item in prog_item_pool
                            if item.name in rbm_names
                            and item.player == self.player]
            placed_item = self.random.choice(valid_second)
            rbm_defeated = (f"{robot_masters[self.options.starting_robot_master.value].replace(' Defeated', '')}"
                            f" - Defeated")
            rbm_location = self.get_location(rbm_defeated)
            rbm_location.place_locked_item(placed_item)
            prog_item_pool.remove(placed_item)
            fill_locations.remove(rbm_location)
            target_rbm = (placed_item.code & 0xF) - 1
            if self.options.strict_weakness or (self.options.random_weakness
                                                and not (self.weapon_damage[0][target_rbm] > 0)):
                # we need to find a weakness for this boss
                weaknesses = [weapon for weapon in range(1, 9)
                              if self.weapon_damage[weapon][target_rbm] >= minimum_weakness_requirement[weapon]]
                weapons = list(map(lambda s: weapons_to_name[s], weaknesses))
                valid_weapons = [item for item in prog_item_pool
                                 if item.name in weapons
                                 and item.player == self.player]
                placed_weapon = self.random.choice(valid_weapons)
                weapon_name = next(name for name, idx in lookup_location_to_id.items()
                                   if idx == 0x0101 + self.options.starting_robot_master.value)
                weapon_location = self.get_location(weapon_name)
                weapon_location.place_locked_item(placed_weapon)
                prog_item_pool.remove(placed_weapon)
                fill_locations.remove(weapon_location)

    def pre_output(self):
        check_for_known_worlds()

    def fill_slot_data(self) -> dict[str, Any]:
        return {
            "weapon_damage": self.weapon_damage,
            "wily_3_weapons": self.wily_3_weapons
        }

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        local_weapon = {int(key): value for key, value in slot_data["weapon_damage"].items()}
        local_wily = {int(key): value for key, value in slot_data["wily_3_weapons"].items()}
        return {"weapon_damage": local_weapon, "wily_3_weapons": local_wily}

