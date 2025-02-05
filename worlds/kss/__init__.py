import logging
import settings
import os
import base64
import threading
from typing import Dict, List, ClassVar, Any
from BaseClasses import Tutorial, MultiWorld, CollectionState, Item
from worlds.AutoWorld import World, WebWorld
from Options import OptionError
from .items import (lookup_item_to_id, item_table, item_groups, KSSItem, filler_item_weights, copy_abilities,
                    sub_games, dyna_items, planets, treasures, sub_game_completion)
from .locations import location_table, KSSLocation
from .names import item_names
from .options import KSSOptions, subgame_mapping
from .regions import create_regions
from .rom import KSS_UHASH, KSSProcedurePatch, patch_rom, KSS_VCHASH
from .rules import set_rules
from .client import KSSSNIClient

logger = logging.getLogger("Kirby Super Star")


class KSSSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the KSS JP or EN rom"""
        description = "Kirby Super Star ROM File"
        copy_to = "Kirby Super Star.sfc"
        md5s = [KSS_UHASH, KSS_VCHASH]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class KSSWebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [

        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Kirby Super Star randomizer connected to an Archipelago Multiworld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Silvris"]
        )
    ]
    #options_presets = kss_options_presets
    #option_groups = kss_option_groups


class KSSWorld(World):
    game = "Kirby Super Star"
    item_name_to_id = lookup_item_to_id
    location_name_to_id = {location: location_table[location]
                           for location in location_table if location_table[location]}
    item_name_groups = item_groups
    web = KSSWebWorld()
    settings: ClassVar[KSSSettings]
    options_dataclass = KSSOptions
    options: KSSOptions
    treasure_value: List[int]

    create_regions = create_regions

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.rom_name: bytes = bytes()
        self.rom_name_available_event = threading.Event()
        self.treasure_value = []

    def generate_early(self) -> None:
        # lots here
        if self.options.included_subgames.value.union(
                {"The Great Cave Offensive", "Milky Way Wishes", "The Arena"}) == {}:
            raise OptionError("At least one of Great Cave Offensive, Milky Way Wishes, or The Arena must be included")

        if self.options.starting_subgame.current_option_name not in self.options.included_subgames:
            logger.warning("Starting subgame not included, choosing random.")
            self.options.starting_subgame.value = self.random.choice([value[0] for value in subgame_mapping.items()
                                                                      if value[1] in self.options.included_subgames])

        for game in sorted(self.options.required_subgames.value):
            if game not in self.options.included_subgames.value:
                logger.warning(F"Required subgame {game} not included, adding to included subgames")
                self.options.included_subgames.value.add(game)

        if self.options.required_subgame_completions > len(self.options.included_subgames.value):
            logger.warning("Required subgames greater than included subgames, reducing to all included.")
            self.options.required_subgames.value = len(self.options.included_subgames.value)

    def create_item(self, name):
        if name not in item_table:
            raise Exception(f"{name} is not a valid item name for Kirby Super Star.")
        data = item_table[name]
        return KSSItem(name, data.classification, data.code, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(filler_item_weights.keys()), weights=list(filler_item_weights.values()), k=1)[0]

    def create_items(self) -> None:
        itempool = []
        modes = [self.create_item(name) for name in sub_games if name in self.options.included_subgames]
        starting_mode = self.create_item(subgame_mapping[self.options.starting_subgame])
        modes.remove(starting_mode)
        self.multiworld.push_precollected(starting_mode)
        itempool.extend([self.create_item(name) for name in copy_abilities])
        itempool.extend(modes)

        treasure_value = 0

        if "Dyna Blade" in self.options.included_subgames:
            itempool.extend([self.create_item(name) for name in dyna_items])
        if "The Great Cave Offensive" in self.options.included_subgames:
            for name, treasure in treasures.items():
                itempool.append(self.create_item(name))
                treasure_value += treasure.value
        if "Milky Way Wishes" in self.options.included_subgames:
            planet = [self.create_item(name) for name in planets]
            starting_planet = self.random.choice(planet)
            planet.remove(starting_planet)
            self.multiworld.push_precollected(starting_planet)
            itempool.extend(planet)

            if self.options.milky_way_wishes_mode == "multiworld":
                itempool.extend(self.create_item(item_names.rainbow_star) for _ in range(7))

        location_count = len(list(self.multiworld.get_unfilled_locations(self.player))) - len(itempool)
        if location_count < 0:
            if "The Great Cave Offensive" in self.options.included_subgames:
                # with TGCO we can just remove treasures until we can hit 0
                sorted_treasures = sorted(treasures.items(), key=lambda treasure: treasure[1].value)
                while location_count < 0:
                    name, treasure = sorted_treasures.pop(0)
                    item = next((item for item in itempool if item.name == name), None)
                    if item:
                        itempool.remove(item)
                        treasure_value -= treasure.value
                        location_count += 1
            else:
                raise OptionError("Unable to create item pool with current settings.")
        itempool.extend([self.create_item(filler) for filler in
                         self.random.choices(list(filler_item_weights.keys()),
                                             weights=list(filler_item_weights.values()),
                                             k=location_count)])

        self.treasure_value = [(treasure_value // 4) * i for i in range(1, 5)]
        self.multiworld.itempool += itempool

    set_rules = set_rules

    def generate_output(self, output_directory: str) -> None:
        try:
            patch = KSSProcedurePatch(player=self.player, player_name=self.player_name)
            patch_rom(self, patch)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        assert isinstance(self.rom_name, bytes)
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(self.rom_name).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        value = super().collect(state, item)

        if item.name in treasures:
            state.prog_items[self.player]["Gold"] += treasures[item.name].value

        return value

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        value = super().remove(state, item)

        if item.name in treasures:
            state.prog_items[self.player]["Gold"] -= treasures[item.name].value
            if not state.prog_items[self.player]["Gold"]:
                del state.prog_items[self.player]["Gold"]

        return value
