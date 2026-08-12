import hashlib
import logging
from copy import deepcopy
from typing import Any, Sequence, ClassVar

from BaseClasses import Tutorial, ItemClassification, MultiWorld, Item, Location
from worlds.AutoWorld import World, WebWorld
from .items import (item_table, item_names, MM4Item, filler_item_weights, robot_master_weapon_table,
                    stage_access_table, rush_item_table, lookup_item_to_id)
from .locations import (MM4Location, mm4_regions, MM4Region, lookup_location_to_id,
                        location_groups)
from .names import wily_4_boss
from .rom import patch_rom, MM4ProcedurePatch, MM4LCHASH, MM4VCHASH, PROTEUSHASH, MM4NESHASH
from .options import MM4Options, Consumables
#from .client import MegaMan4Client
from .rules import set_rules, weapon_damage, robot_masters, weapons_to_name, minimum_weakness_requirement
import os
import threading
import base64
import settings
logger = logging.getLogger("Mega Man 4")


class MM4Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the MM4 EN rom"""
        description = "Mega Man 4 ROM File"
        copy_to: str | None = "Mega Man 4 (USA).nes"
        md5s = [MM4NESHASH, MM4LCHASH, PROTEUSHASH, MM4VCHASH]

        def browse(self: settings.T,
                   filetypes: Sequence[tuple[str, Sequence[str]]] | None = None,
                   **kwargs: Any) -> settings.T | None:
            if not filetypes:
                file_types = [("NES", [".nes"]), ("Program", [".exe"])]  # LC1 is only a windows executable, no linux
                return super().browse(file_types, **kwargs)
            else:
                return super().browse(filetypes, **kwargs)

        @classmethod
        def validate(cls, path: str) -> None:
            """Try to open and validate file against hashes"""
            with open(path, "rb", buffering=0) as f:
                try:
                    f.seek(0)
                    if f.read(4) == b"NES\x1A":
                        f.seek(16)
                    else:
                        f.seek(0)
                    cls._validate_stream_hashes(f)
                    base_rom_bytes = f.read()
                    basemd5 = hashlib.md5()
                    basemd5.update(base_rom_bytes)
                    if basemd5.hexdigest() == PROTEUSHASH:
                        # we need special behavior here
                        cls.copy_to = None
                except ValueError:
                    raise ValueError(f"File hash does not match for {path}")

    rom_file: RomFile = RomFile(RomFile.copy_to)


class MM4WebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [

        Tutorial(
           "Multiworld Setup Guide",
           "A guide to setting up the Mega Man 4 randomizer connected to an Archipelago Multiworld.",
           "English",
           "setup_en.md",
           "setup/en",
           ["Silvris"]
        )
    ]


class MM4World(World):
    """
    MM4 description
    """

    game = "Mega Man 4"
    settings: ClassVar[MM4Settings]
    options_dataclass = MM4Options
    options: MM4Options
    item_name_to_id = lookup_item_to_id
    location_name_to_id = lookup_location_to_id
    item_name_groups = item_names
    location_name_groups = location_groups
    web = MM4WebWorld()
    rom_name: bytearray

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name = bytearray()
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)
        self.weapon_damage = deepcopy(weapon_damage)
        self.wily_4_weapons: dict[int, list[int]] = {}

    def create_regions(self) -> None:
        menu = MM4Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        location: MM4Location
        for name, region in mm4_regions.items():
            stage = MM4Region(name, self.player, self.multiworld)
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
        goal_location.place_locked_item(MM4Item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_item(self, name: str, force_non_progression: bool = False) -> MM4Item:
        item = item_table[name]
        classification = ItemClassification.filler
        if item.progression and not force_non_progression:
            classification = ItemClassification.progression_skip_balancing \
                if item.skip_balancing else ItemClassification.progression
        if item.useful:
            classification |= ItemClassification.useful
        return MM4Item(name, classification, item.code, self.player)

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
        itempool.extend([self.create_item(name) for name in rush_item_table.keys()])
        total_checks = 27
        if self.options.consumables in (Consumables.option_1up_etank,
                                        Consumables.option_all):
            total_checks += 23
        if self.options.consumables in (Consumables.option_weapon_health,
                                        Consumables.option_all):
            total_checks += 47
        remaining = total_checks - len(itempool)
        itempool.extend([self.create_item(name)
                         for name in self.random.choices(list(filler_item_weights.keys()),
                                                         weights=list(filler_item_weights.values()),
                                                         k=remaining)])
        self.multiworld.itempool += itempool

    set_rules = set_rules

    """def generate_early(self) -> None:
        if (self.options.starting_robot_master.current_key == "gemini_man"
            and not any(item in self.options.start_inventory for item in rush_item_table.keys())) or \
                (self.options.starting_robot_master.current_key == "hard_man"
                 and not any(item in self.options.start_inventory for item in [rush_coil, rush_jet])):
            robot_master_pool = [0, 1, 4, 5, 6, 7, ]
            if rush_marine in self.options.start_inventory:
                robot_master_pool.append(2)
            self.options.starting_robot_master.value = self.random.choice(robot_master_pool)
            logger.warning(
                f"Incompatible starting Robot Master, changing to "
                f"{self.options.starting_robot_master.current_key.replace('_', ' ').title()}")"""

    def fill_hook(self,
                  prog_item_pool: list["Item"],
                  useful_item_pool: list["Item"],
                  filler_item_pool: list["Item"],
                  fill_locations: list["Location"]) -> None:
        #TODO: see if MM4 has the same issues
        pass

    def generate_output(self, output_directory: str) -> None:
        try:
            patch = MM4ProcedurePatch(player=self.player, player_name=self.player_name)
            patch_rom(self, patch)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

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

    def modify_multidata(self, multidata: dict[str, Any]) -> None:
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.player_name]
