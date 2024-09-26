import logging
import settings
from typing import Dict, List, ClassVar
from BaseClasses import Tutorial, MultiWorld, CollectionState, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .items import (lookup_item_to_id, item_table, item_names, KSSItem, filler_item_weights, copy_abilities,
                    sub_games, misc_other, planets, treasures, sub_game_completion)
from .locations import location_table, KSSLocation
from .options import KSSOptions
from .regions import create_regions
from .rom import KSS_UHASH
from .rules import set_rules

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
    #options_presets = kdl3_options_presets
    #option_groups = kdl3_option_groups

class KSSWorld(World):
    game = "Kirby Super Star"
    item_name_to_id = lookup_item_to_id
    location_name_to_id = {location: location_table[location] for location in location_table if location_table[location]}
    item_name_groups = item_names
    web = KSSWebWorld()
    settings: ClassVar[KSSSettings]
    options_dataclass = KSSOptions
    options: KSSOptions

    create_regions = create_regions

    def create_item(self, name):
        data = item_table[name]
        return KSSItem(name, data.classification, data.code, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(filler_item_weights.keys()), weights=list(filler_item_weights.values()), k=1)[0]

    def create_items(self) -> None:
        itempool = []
        modes = [self.create_item(name) for name in sub_games]
        starting_mode = self.random.choice(modes)
        modes.remove(starting_mode)
        self.multiworld.push_precollected(starting_mode)
        itempool.extend([self.create_item(name) for name in copy_abilities])
        itempool.extend(modes)
        itempool.extend([self.create_item(name) for name in misc_other])

        # if great cave
        itempool.extend([self.create_item(name) for name in treasures])
        # if milky way
        planet = [self.create_item(name) for name in planets]
        starting_planet = self.random.choice(planet)
        planet.remove(starting_planet)
        self.multiworld.push_precollected(starting_planet)
        itempool.extend(planet)

        location_count = len(list(self.multiworld.get_unfilled_locations(self.player)))
        itempool.extend([self.create_item(filler) for filler in
                         self.random.choices(list(filler_item_weights.keys()),
                                             weights=list(filler_item_weights.values()),
                                             k=location_count - len(itempool))])

        self.multiworld.itempool += itempool

    def generate_basic(self) -> None:
        sub_game_complete = list(sub_game_completion.keys())
        self.multiworld.completion_condition[self.player] = lambda state: state.has_from_list(sub_game_complete,
                                                                                              self.player,
                                                                                         self.options.required_subgames)

    set_rules = set_rules
