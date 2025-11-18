import base64
import logging
import os
import settings
import threading
import Utils
from worlds.AutoWorld import World, WebWorld
from BaseClasses import ItemClassification, Item, Location, Tutorial
from copy import deepcopy
from hashlib import md5
from Options import OptionError
from typing import Any, ClassVar, Sequence
from .client import MegaMan1Client
from .items import MM1Item, all_items, item_lookup, stage_access, weapons, item_groups
from .locations import location_lookup, MM1Location, MM1Region, mm1_regions
from .options import MM1Options, robot_masters
from .rom import MM1ProcedurePatch, MM1NESHASH, MM1LCHASH, PROTEUSHASH, patch_rom
from .rules import set_rules, weapon_damage, minimum_weakness_requirement, weapons_to_name


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
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Mega Man randomizer connected to an Archipelago Multiworld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Silvris"]
        )
    ]


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

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.rom_name = bytearray()
        self.rom_name_available_event = threading.Event()
        self.weapon_damage = deepcopy(weapon_damage)

    def generate_early(self) -> None:
        if self.multiworld.players == 1 and self.options.required_weapons >= 4:
            num = 3
            logging.warning(f"Player {self.player} ({self.player_name}): "
                            f"Required weapons too high for singleplayer game, reducing to {num}")
            self.options.required_weapons.value = num

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

    def fill_hook(self,
                  progitempool: list[Item],
                  usefulitempool: list[Item],
                  filleritempool: list[Item],
                  fill_locations: list[Location]) -> None:
        # on a solo gen, fill can try to force Wily into sphere 2, but for most generations this is impossible
        # since MM1 can have a 2 item sphere 1, and at least 3 items are required for Wily
        if self.multiworld.players > 1:
            return  # Don't need to change anything on a multi gen, fill should be able to solve it with a 4 sphere 1
        # emphasis on should
        rbm_to_item = {
            0: "Cut Man Access Codes",
            1: "Ice Man Access Codes",
            2: "Bomb Man Access Codes",
            3: "Fire Man Access Codes",
            4: "Elec Man Access Codes",
            5: "Guts Man Access Codes",
        }
        valid_second = [item for item in progitempool
                            if item.name in rbm_to_item.values()
                            and item.player == self.player]
        placed_item = self.random.choice(valid_second)
        valid_second.remove(placed_item)
        rbm_location = self.get_location(f"{robot_masters[self.options.starting_robot_master.value]} - Defeated")
        rbm_location.place_locked_item(placed_item)
        progitempool.remove(placed_item)
        fill_locations.remove(rbm_location)
        target_rbm = (placed_item.code & 0xF) - 1
        # have to place a second one to reach max items required for Wily (5)
        second_location = self.get_location(f"{robot_masters[target_rbm]} - Defeated")
        placed_second = self.random.choice(valid_second)
        second_location.place_locked_item(placed_second)
        progitempool.remove(placed_second)
        fill_locations.remove(second_location)
        for boss, target in ((self.options.starting_robot_master.value, target_rbm),
                             (target_rbm, (placed_second.code & 0xF) - 1)):
            if self.options.strict_weakness or (self.options.random_weakness
                                                and not (self.weapon_damage[0][target] > 0)):
                # we need to find a weakness for this boss
                weaknesses = [weapon for weapon in range(1, 6)
                                if self.weapon_damage[weapon][target] >= minimum_weakness_requirement[weapon]]
                weapons = list(map(lambda s: weapons_to_name[s], weaknesses))
                valid_weapons = [item for item in progitempool
                                 if item.name in weapons
                                 and item.player == self.player
                                 and not item.location]
                if not valid_weapons:
                    continue # This should mean that we have already placed the weapon that can deal damage to the RBM
                placed_weapon = self.random.choice(valid_weapons)
                weapon_name = next(name for name, idx in location_lookup.items()
                                   if idx == 0x11 + boss)
                weapon_location = self.get_location(weapon_name)
                weapon_location.place_locked_item(placed_weapon)
                progitempool.remove(placed_weapon)
                fill_locations.remove(weapon_location)

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
