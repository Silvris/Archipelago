import logging
import settings
from typing import Dict, List, ClassVar
from BaseClasses import Tutorial, MultiWorld, CollectionState, ItemClassification, Item
from worlds.AutoWorld import World, WebWorld
from Options import OptionError
from .items import (lookup_item_to_id, item_table, item_names, KSSItem, filler_item_weights, copy_abilities,
                    sub_games, dyna_items, planets, treasures, sub_game_completion)
from .locations import location_table, KSSLocation
from .options import KSSOptions, subgame_mapping
from .regions import create_regions
from .rom import KSS_UHASH
from .rules import set_rules

logger = logging.getLogger("Kirby Super Star")


class KSSSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the KSS JP or EN rom"""
        description = "Kirby Super Star ROM File"
        copy_to = "Kirby Super Star.sfc"
        md5s = [KSS_UHASH]

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
    item_name_groups = item_names
    web = KSSWebWorld()
    settings: ClassVar[KSSSettings]
    options_dataclass = KSSOptions
    options: KSSOptions
    treasure_value: List[int]

    create_regions = create_regions

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
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

        if self.options.required_subgames > len(self.options.included_subgames.value):
            logger.warning("Required subgames greater than included subgames, reducing to all included.")
            self.options.required_subgames.value = len(self.options.included_subgames.value)

    def create_item(self, name):
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

    def generate_basic(self) -> None:
        sub_game_complete = list(sub_game_completion.keys())
        self.multiworld.completion_condition[self.player] = lambda state: state.has_from_list(
            sub_game_complete, self.player, self.options.required_subgames)

    set_rules = set_rules

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
