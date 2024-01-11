import logging
import typing

from BaseClasses import Tutorial, ItemClassification, MultiWorld
from Fill import fill_restrictive
from worlds.AutoWorld import World, WebWorld
from .Items import item_table, item_names, copy_ability_table, filler_item_weights, K64Item, copy_ability_access_table,\
    power_combo_table, friend_table
from .Locations import location_table, K64Location
from .Names import LocationName, ItemName
from .Regions import create_levels, default_levels
from .Rom import K64DeltaPatch, get_base_rom_path, RomData, patch_rom, K64UHASH
from .Client import PokemonBW2Client
from .Options import PokemonBW2Options
from .Rules import set_rules
from typing import Dict, TextIO, Optional, List
import os
import math
import threading
import base64
import settings

logger = logging.getLogger("Pokemon Black 2 and White 2")


class PokemonBW2Settings(settings.Group):
    class BlackRomFile(settings.UserFilePath):
        """File name of the Pokemon Black 2 EN rom"""
        description = "Pokemon Black 2 ROM File"
        copy_to = "Pokemon Black 2.nds"
        md5s = []

    class WhiteRomFile(settings.UserFilePath):
        """File name of the Pokemon White 2 EN rom"""
        description = "Pokemon White 2 ROM File"
        copy_to = "Pokemon White 2.nds"
        md5s = []

    black_2_rom_file: BlackRomFile = BlackRomFile(BlackRomFile.copy_to)
    white_2_rom_file: WhiteRomFile = WhiteRomFile(WhiteRomFile.copy_to)


class PokemonBW2WebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [

        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Pokemon Black 2 and White 2 randomizer connected to an Archipelago Multiworld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Silvris"]
        )
    ]


class PokemonBW2World(World):
    """
    Set 2 years after the first game, a new Pokemon adventure begins in the Unova region. Gather the gym badges, defeat
    the evil Team Plasma, encounter over 600 unique Pokemon, and become the Unova League champion!
    """

    game = "Pokemon Black 2 and White 2"
    options_dataclass = PokemonBW2Options
    options: PokemonBW2Options
    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = {location_table[location]: location for location in location_table}
    item_name_groups = item_names
    data_version = 0
    web = PokemonBW2WebWorld()
    settings: typing.ClassVar[PokemonBW2Settings]

    def __init__(self, multiworld: MultiWorld, player: int):
        self.stage_shuffle_enabled: bool = False
        self.rom_name = None
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

    create_regions = create_levels

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        rom_file: str = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(f"Could not find base ROM for {cls.game}: {rom_file}")

    def create_item(self, name: str, force_non_progression=False) -> K64Item:
        item = item_table[name]
        classification = ItemClassification.filler
        if item.progression and not force_non_progression:
            classification = ItemClassification.progression_skip_balancing \
                if item.skip_balancing else ItemClassification.progression
        elif item.trap:
            classification = ItemClassification.trap
        return K64Item(name, classification, item.code, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(filler_item_weights.keys()),
                                   weights=list(filler_item_weights.values()))[0]

    def create_items(self) -> None:
        pass

    set_rules = set_rules

    def generate_output(self, output_directory: str):
        rom_path = ""
        try:
            world = self.multiworld
            player = self.player

            rom = RomData(get_base_rom_path())
            patch_rom(self, self.player, rom)

            rom_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.nds")
            rom.write_to_file(rom_path)
            self.rom_name = rom.name

            patch = PokemonBW2DeltaPatch(os.path.splitext(rom_path)[0] + PokemonBW2DeltaPatch.patch_file_ending, player=player,
                                   player_name=world.player_name[player], patched_path=rom_path)
            patch.write()
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected
            if os.path.exists(rom_path):
                os.unlink(rom_path)

    def modify_multidata(self, multidata: dict):
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
