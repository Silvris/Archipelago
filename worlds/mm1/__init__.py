import base64
import os

import Utils
import settings
import threading
from worlds.AutoWorld import World, WebWorld
from BaseClasses import ItemClassification
from copy import deepcopy
from hashlib import md5
from Options import OptionError
from typing import Any, ClassVar, Sequence
from .client import MegaMan1Client
from .items import MM1Item, all_items, item_lookup, stage_access, weapons, item_groups
from .locations import location_lookup, MM1Location, MM1Region, mm1_regions
from .options import MM1Options
from .rom import MM1ProcedurePatch, MM1NESHASH, MM1LCHASH, PROTEUSHASH, patch_rom
from .rules import set_rules, weapon_damage


class MM1Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the MM1 EN rom"""
        description = "Mega Man 1 ROM File"
        copy_to: str | None = "Mega Man (USA).nes"
        md5s = [MM1NESHASH, MM1LCHASH, PROTEUSHASH]

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
                    basemd5 = md5()
                    basemd5.update(base_rom_bytes)
                    if basemd5.hexdigest() == PROTEUSHASH:
                        # we need special behavior here
                        cls.copy_to = None
                except ValueError:
                    raise ValueError(f"File hash does not match for {path}")

    rom_file: RomFile = RomFile(RomFile.copy_to)


class MM1WebWorld(WebWorld):
    theme = "partyTime"


class MM1World(World):
    game = "Mega Man"
    item_name_to_id = item_lookup
    item_name_groups = item_groups
    location_name_to_id = location_lookup
    options: MM1Options
    options_dataclass = MM1Options
    settings: ClassVar[MM1Settings]
    web = MM1WebWorld()
    weapon_damage: dict[int, list[int]]
    if Utils.version_tuple < (0, 6, 4):
        world_version = (0, 0, 1)

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.rom_name = bytearray()
        self.rom_name_available_event = threading.Event()
        self.weapon_damage = deepcopy(weapon_damage)

    def create_item(self, name: str) -> MM1Item:
        if name not in all_items:
            raise OptionError(f"{name} is not a valid item name for Mega Man.")
        item_data = all_items.get(name)
        classification = ItemClassification.filler
        if item_data.progression:
            classification |= ItemClassification.progression
        if item_data.useful:
            classification |= ItemClassification.useful
        return MM1Item(name, classification, item_data.item_id, self.player)

    def create_regions(self):
        menu = MM1Region(self.origin_region_name, self.player, self.multiworld)
        regions = [menu]
        for region in mm1_regions:
            stage = MM1Region(region.name, self.player, self.multiworld)
            stage.add_locations({name: data.location_id for name, data in region.locations.items()
                                 if (not data.consumable) or self.options.consumables}, MM1Location)
            for name, data in region.locations.items():
                if not data.location_id:
                    self.get_location(name).place_locked_item(MM1Item(name, ItemClassification.progression,
                                                                      None, self.player))
            regions.append(stage)
        self.multiworld.regions.extend(regions)

        for region in mm1_regions:
            if region.parent:
                parent_region = self.get_region(region.parent)
            else:
                parent_region = menu
            parent_region.connect(self.get_region(region.name), f"To {region.name}",
                                  lambda state, req=tuple(region.required_items): state.has_all(req, self.player))

    def create_items(self):
        # Define our local itempool
        itempool = []
        starting_robot_master = self.item_id_to_name[self.options.starting_robot_master.value + 0x11]
        self.multiworld.push_precollected(self.create_item(starting_robot_master))
        itempool.extend([self.create_item(name) for name in stage_access.keys()
                         if name != starting_robot_master])
        itempool.extend([self.create_item(name) for name in weapons.keys()])
        itempool.append(self.create_item("Magnet Beam"))
        filler_count = len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool)
        itempool.extend(self.create_item(item)
                        for item in self.random.choices(["1-Up", "Health Energy (L)", "Weapon Energy (L)"],
                                                        k=filler_count))
        self.multiworld.itempool.extend(itempool)

    set_rules = set_rules

    def generate_output(self, output_directory: str) -> None:
        try:
            patch = MM1ProcedurePatch(player=self.player, player_name=self.player_name)
            patch_rom(self, patch)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def modify_multidata(self, multidata: dict[str, Any]) -> None:
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.player_name]
