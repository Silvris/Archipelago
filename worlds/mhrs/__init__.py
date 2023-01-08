from typing import Dict, Any

from worlds.AutoWorld import World, WebWorld
from .Options import mhrs_options
from .Items import lookup_name_to_id as items_lookup
from .Items import filler_item_table, filler_weights, follower_table, useful_item_table, progression_item_table, MHRSItem
from .Locations import mhr_quests, get_exclusion_table, MHRSQuest
from .Rules import set_mhrs_rules
from .Regions import mhrs_regions, link_mhrs_regions
from worlds.generic.Rules import exclusion_rules
from BaseClasses import Item, ItemClassification, Region, RegionType, Entrance
import os
import json

MultiplayerGroupSeeds = dict()


class MHRSWebWorld(WebWorld):
    theme = "stone"


class MHRSWorld(World):
    """
    Monster Hunter Rise: Sunbreak is an action RPG by CAPCOM. Players take the role of a hunter tasked with defeating a
    plethora of fantastical monsters in an effort to protect their village, crafting weapons and armor along the way.
    This randomizer focuses specifically on the Sunbreak expansion.
    """
    game: str = "Monster Hunter Rise Sunbreak"
    option_definitions = mhrs_options
    web = MHRSWebWorld()
    topology_present = True
    data_version = 0
    base_id = 315100

    item_name_to_id = items_lookup
    location_name_to_id = {name: mhr_quests[name].id for name in mhr_quests}

    def _get_alphanumeric_seed(self):
        length = 23
        chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        seed = ""
        for _ in range(length):
            seed += chars[self.multiworld.slot_seeds[self.player].randrange(0, len(chars) - 1, 1)]
        return seed

    def get_quest_seed(self, group: str):
        if group == "":
            return self._get_alphanumeric_seed()
        elif group in MultiplayerGroupSeeds:
            return MultiplayerGroupSeeds[group]
        else:
            seed = self._get_alphanumeric_seed()
            MultiplayerGroupSeeds[group] = seed
            return seed

    def create_item(self, name: str) -> Item:
        classification = ItemClassification.filler
        if name in progression_item_table:
            classification = ItemClassification.progression
        if name in useful_item_table or name in follower_table:
            classification = ItemClassification.useful
        item = MHRSItem(name, classification, items_lookup[name], self.player)
        return item

    def create_regions(self) -> None:
        def MHRSRegion(region_name: str, exits=[]):
            if region_name == f"MR{self.multiworld.master_rank_requirement[self.player]}":
                exits.append("To Final")
            region = Region(region_name, RegionType.Generic, region_name, self.player, self.multiworld)
            region.locations = [
                MHRSQuest(self.player, name, mhr_quests[name].id, region)
                for name in mhr_quests if mhr_quests[name].region == region_name
            ]
            for exit in exits:
                region.exits.append(Entrance(self.player, exit, region))
            return region
        self.multiworld.regions += [MHRSRegion(*r) for r in mhrs_regions]
        link_mhrs_regions(self.multiworld, self.player)

    def generate_basic(self) -> None:
        itempool = []
        for i in range(2, self.multiworld.master_rank_requirement[self.player].value + 1):
            itempool += [self.create_item(f"MR{i} Urgent")]

        # now handle player options for weapons
        weapons = [
            "Great Sword",
            "Long Sword",
            "Sword and Shield",
            "Dual Blades",
            "Hammer",
            "Hunting Horn",
            "Lance",
            "Gunlance",
            "Switch Axe",
            "Charge Blade",
            "Insect Glaive",
            "Light Bowgun",
            "Heavy Bowgun",
            "Bow"
        ]
        consolidate = self.multiworld.consolidate_weapons[self.player].value
        progressive = self.multiworld.progressive_weapons[self.player].value
        if consolidate:
            weapons = ["Weapon"]

        if progressive:
            for weapon in weapons:
                itempool += [
                    self.create_item(f"Progressive {weapon}") for _ in range(4)
                ]
        else:
            for weapon in weapons:
                itempool += [
                    self.create_item(f"{weapon} Rarities 1-3"),
                    self.create_item(f"{weapon} Rarities 4-5"),
                    self.create_item(f"{weapon} Rarities 6-7"),
                    self.create_item(f"{weapon} Rarities 8-10")
                ]
        # handle follower randomization if enabled
        if self.multiworld.enable_followers[self.player].value == 0:
            for follower in follower_table:
                itempool.append(self.create_item(follower))
        exclusion_pool = set()
        exclusion_pool.update(get_exclusion_table(self.multiworld.master_rank_requirement[self.player].value))
        exclusion_rules(self.multiworld, self.player, exclusion_pool)
        # place filler items at the excluded quests
        for quest in exclusion_pool:
            self.multiworld.get_location(quest, self.player).place_locked_item(self.create_item(self.get_filler_item_name()))

        quest_num = len(mhr_quests) - 1 - len(exclusion_pool)
        itempool += [self.create_item(self.get_filler_item_name()) for _ in range(quest_num - len(itempool))]
        self.multiworld.get_location("The Final Quest", self.player).place_locked_item(self.create_item("Victory's Flame"))

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory's Flame", self.player)
        self.multiworld.itempool += itempool

    def set_rules(self):
        set_mhrs_rules(self.multiworld, self.player)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choices(list(filler_item_table.keys()), weights=list(filler_weights.values()))[0]

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = {
            "quest_seed": self.get_quest_seed(self.multiworld.multiplayer_group[self.player].value),
            "item_seed": self._get_alphanumeric_seed(),
            "death_link": self.multiworld.death_link[self.player].value,
            "final_quest_target": self.multiworld.final_quest_target[self.player].value,
            "master_rank_requirement": self.multiworld.master_rank_requirement[self.player].value,
            "enable_affliction": self.multiworld.enable_affliction[self.player].value,
            "include_apex": self.multiworld.include_apex[self.player].value,
            "include_risen": self.multiworld.include_risen[self.player].value,
            "progressive_weapons": self.multiworld.progressive_weapons[self.player].value,
            "consolidate_weapons": self.multiworld.consolidate_weapons[self.player].value,
            "average_monster_difficulty": self.multiworld.average_monster_difficulty[self.player].value,
            "monster_difficulty_deviation": self.multiworld.monster_difficulty_deviation[self.player].value,
            "enable_followers": self.multiworld.enable_followers[self.player].value,
            "disable_multiplayer_scaling": self.multiworld.disable_multiplayer_scaling[self.player].value,
            "multiplayer_group": self.multiworld.multiplayer_group[self.player].value,
            "give_khezu_music": self.multiworld.give_khezu_music[self.player].value
        }
        return slot_data

    def generate_output(self, output_directory: str):
        if self.multiworld.players != 1:
            return
        data = {
            "slot_data": self.fill_slot_data(),
            "location_to_item": {
                self.location_name_to_id[i.name]: items_lookup[i.item.name] for i in self.multiworld.get_locations()
            },
            "data_package": {
                "data": {
                    "games": {
                        self.game: {
                            "item_name_to_id": self.item_name_to_id,
                            "location_name_to_id": self.location_name_to_id
                        }
                    }
                }
            }
        }
        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apmhrs"
        with open(os.path.join(output_directory, filename), 'w') as f:
            json.dump(data, f)
