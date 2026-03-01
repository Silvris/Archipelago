import logging
import typing

from BaseClasses import Tutorial, ItemClassification, MultiWorld
from Fill import fill_restrictive
from worlds.AutoWorld import World, WebWorld
from .Items import all_items, key_items, filler_items, item_groups, PokemonBW2Item, generate_itempool
from .Regions import create_regions, location_data
from .Client import PokemonBW2Client
from .Options import PokemonBW2Options
from .Rules import set_rules
from .Rom import patch_rom, get_base_rom_path, PokemonBlack2ProcedurePatch, PokemonWhite2ProcedurePatch
from typing import Dict, TextIO, Optional, List
import os
import math
import threading
import base64
import settings

logger = logging.getLogger("Pokemon Black 2 and White 2")


class PokemonBW2Settings(settings.Group):
    class BlackRomFile(settings.UserFilePath):
        """File name of the Pokémon Black 2 EN rom"""
        description = "Pokémon Black 2 ROM File"
        copy_to = "Pokémon Black 2.nds"
        md5s = []

    class WhiteRomFile(settings.UserFilePath):
        """File name of the Pokémon White 2 EN rom"""
        description = "Pokémon White 2 ROM File"
        copy_to = "Pokémon White 2.nds"
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
    Set 2 years after the first game, a new Pokémon adventure begins in the Unova region. Gather the gym badges, defeat
    the evil Team Plasma, encounter over 600 unique Pokémon, and become the Unova League champion!
    """

    game = "Pokemon Black 2 and White 2"
    options_dataclass = PokemonBW2Options
    options: PokemonBW2Options
    item_name_to_id = {item: all_items[item].code for item in all_items}
    location_name_to_id = {location: location_data[location]["idx"] for location in location_data}
    item_name_groups = item_groups
    web = PokemonBW2WebWorld()
    settings: typing.ClassVar[PokemonBW2Settings]

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name = None
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

    create_regions = create_regions

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        pass
        #rom_file: str = get_base_rom_path()
        #if not os.path.exists(rom_file):
            #raise FileNotFoundError(f"Could not find base ROM for {cls.game}: {rom_file}")

    def create_item(self, name: str, is_event=False) -> PokemonBW2Item:
        if is_event:
            return PokemonBW2Item(name, ItemClassification.progression, None, self.player)
        item = all_items[name]
        return PokemonBW2Item(name, item.classification, item.code, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(list(filler_items.keys()))

    create_items = generate_itempool

    set_rules = set_rules

    def generate_output(self, output_directory: str):
        rom_path = ""
        try:
            world = self.multiworld
            player = self.player

            if self.options.version == 1:
                patch = PokemonWhite2ProcedurePatch(player=self.player, player_name=self.player_name)
            else:
                patch = PokemonBlack2ProcedurePatch(player=self.player, player_name=self.player_name)
            patch_rom(self, patch)

            patch_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}")
            patch.write(patch_path)
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected
            if os.path.exists(rom_path):
                os.unlink(rom_path)

    #def modify_multidata(self, multidata: dict):
    #    # wait for self.rom_name to be available.
    #    self.rom_name_available_event.wait()
    #    rom_name = getattr(self, "rom_name", None)
    #    # we skip in case of error, so that the original error in the output thread is the one that gets raised
    #    if rom_name:
    #        new_name = base64.b64encode(bytes(self.rom_name)).decode()
    #        multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
