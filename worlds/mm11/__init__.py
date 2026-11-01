import hashlib
import logging
from copy import deepcopy
from typing import Any, Sequence, ClassVar, TYPE_CHECKING, TextIO

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
from .rules import set_rules, robot_masters, weapons_to_name, bosses
import os
import threading
import base64
logger = logging.getLogger("Mega Man 11")

if TYPE_CHECKING:
    from .boss import Boss, DamageType


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
        print(multiworld.seed)
        self.rom_name = bytearray()
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)
        self.bosses: dict[int, "Boss"] = bosses.copy()
        self.wily_3_weapons: dict[int, list[DamageType]] = {}
        self.wily_4_weapons: dict[int, list[DamageType]] = {}

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
        total_checks = 48
        if self.options.consumables in (Consumables.option_1up_etank,
                                        Consumables.option_all):
            total_checks += 21
        if self.options.consumables in (Consumables.option_weapon_health,
                                        Consumables.option_all):
            total_checks += 148
        remaining = total_checks - len(itempool)
        itempool.extend([self.create_item(name)
                         for name in self.random.choices(list(filler_item_weights.keys()),
                                                         weights=list(filler_item_weights.values()),
                                                         k=remaining)])
        self.multiworld.itempool += itempool

    set_rules = set_rules

    def pre_output(self):
        check_for_known_worlds()

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\n\nWeaknesses for {self.player_name}:\n")
        for boss in self.bosses.values():
            spoiler_handle.write(f"{boss.name}: {', '.join(x.name for x in boss.get_weaknesses())}\n")
        spoiler_handle.write("\n")

    def fill_slot_data(self) -> dict[str, Any]:
        slot_data = self.options.as_dict("energy_link", "consumables", )
        slot_data.update({
            "wily_3_weapons": self.wily_3_weapons,
            "wily_4_weapons": self.wily_4_weapons,
            "DeathLink": self.options.death_link.value,
        })
        if self.options.strict_weakness or self.options.random_weakness or self.options.plando_weakness:
            slot_data.update({
                "BlockManWeakness": self.bosses[0].damage,
                "AcidManWeakness": self.bosses[1].damage,
                "ImpactManWeakness": self.bosses[2].damage,
                "BounceManWeakness": self.bosses[3].damage,
                "FuseManWeakness": self.bosses[4].damage,
                "TundraManWeakness": self.bosses[5].damage,
                "TorchManWeakness": self.bosses[6].damage,
                "BlastManWeakness": self.bosses[7].damage,
                "YellowDevilWeakness": self.bosses[8].damage,
                "MawverneWeakness": self.bosses[9].damage,
                "WilyMachine1Weakness": self.bosses[10].damage,
                "WilyMachine2Weakness": self.bosses[11].damage,
            })
        return slot_data

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:

        local_wily_3 = {int(key): value for key, value in slot_data["wily_3_weapons"].items()}
        local_wily_4 = {int(key): value for key, value in slot_data["wily_3_weapons"].items()}
        return {"wily_3_weapons": local_wily_3, "wily_4_weapons": local_wily_4}

