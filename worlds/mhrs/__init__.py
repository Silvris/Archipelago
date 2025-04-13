import math
from typing import Dict, Any, Optional

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule
from BaseClasses import Item, ItemClassification, Tutorial
from .options import MHRSOptions
from .items import lookup_name_to_id as items_lookup
from .items import filler_item_table, filler_weights, useful_item_table, follower_table,\
    progression_item_table, MHRSItem, item_table, item_name_groups
from .locations import mhr_quests, MHRSQuest, get_quest_table, get_mr_quest_num, urgent_quests
from .quests import FinalQuests, UrgentQuests
from .quest_gen import generate_quests
from .regions import create_regions


class MHRSWebWorld(WebWorld):
    theme = "stone"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Monster Hunter Rise Sunbreak randomizer connected to an Archipelago Multiworld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Silvris"]
        )
    ]


class MHRSWorld(World):
    """
    Monster Hunter Rise: Sunbreak is an action RPG by CAPCOM. Players take the role of a hunter tasked with defeating a
    plethora of fantastical monsters in an effort to protect their village, crafting weapons and armor along the way.
    This randomizer focuses specifically on the Sunbreak expansion.
    """
    game = "Monster Hunter Rise Sunbreak"
    options_dataclass = MHRSOptions
    options: MHRSOptions
    web = MHRSWebWorld()
    data_version = 0
    base_id = 315100

    item_name_to_id = items_lookup
    location_name_to_id = {name: mhr_quests[name].id for name in mhr_quests}
    item_name_groups = item_name_groups
    final_boss: Optional[int] = None
    requirements_base = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    key_requirements = dict()
    generate_output = generate_quests
    origin_region_name = "Master Rank 1 Urgent"

    def create_item(self, name: str, force_non_progression=False) -> Item:
        classification = ItemClassification.filler
        if name in progression_item_table and not force_non_progression:
            classification = ItemClassification.progression
        if name in useful_item_table and not force_non_progression:
            classification = ItemClassification.useful
        if name == "Key Quest" and not force_non_progression:
            classification = ItemClassification.progression_skip_balancing
        item = MHRSItem(name, classification, item_table[name].code, self.player)
        return item

    def get_final_boss(self):
        # first check if we have already defined this player's final boss
        if self.final_boss:
            return self.final_boss
        else:
            # define the player's final boss, is it a preset option?
            target = self.options.final_quest_target.value
            if target not in [0, 1]:
                self.final_boss = target
                return target
            else:
                # roll a random boss for the player
                boss_table = [i for i in range(2, 22 if target == 1 else 23)]

                boss = self.random.choice(boss_table)

                self.final_boss = boss
                return boss

    def get_final_quest(self):
        boss = self.get_final_boss()
        return f"{self.options.master_rank_requirement.value}★ - {FinalQuests[boss]}"

    create_regions = create_regions

    def create_items(self) -> None:
        itempool = []
        MR = self.options.master_rank_requirement.value

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
        consolidate = self.options.consolidate_weapons.value
        progressive = self.options.progressive_weapons.value
        if consolidate:
            weapons = ["Weapon"]

        if progressive:
            for weapon in weapons:
                itempool += [
                    self.create_item(f"Progressive {weapon}") for _ in range(8, 9 + (MR // 3))
                ]
        else:
            for weapon in weapons:
                itempool += [
                    self.create_item(f"{weapon} Rarity {i}") for i in range(8, 9 + (MR // 3))
                ]
        # handle armor
        if self.options.progressive_armor:
            itempool += [self.create_item("Progressive Armor Rarity") for _ in range(8, 9 + (MR // 3))]
        else:
            itempool += [self.create_item(f"Armor Rarity {i}") for i in range(8, 9 + (MR // 3))
                         ]

        # handle follower randomization if enabled
        if self.options.enable_followers == 0:
            for follower in follower_table:
                itempool.append(self.create_item(follower))
        quests = get_quest_table(self.options.master_rank_requirement.value)
        quest_num = len(quests)
        total_key_count = min(quest_num - len(itempool), self.options.total_keys.value)
        required_keys = math.floor(total_key_count * (self.options.required_keys.value / 100.0))
        non_required_keys = total_key_count - required_keys
        self.key_requirements[self.player] = self.requirements_base.copy()
        for i in range(1, MR + 1):
            quest_percentage = get_mr_quest_num(i) / quest_num  # percentage this MR has over the total
            self.key_requirements[i] = (self.key_requirements[i - 1] if i > 1 else 0) \
                                        + math.floor(quest_percentage * required_keys)
        self.key_requirements[MR] = required_keys
        filler_num = math.floor(non_required_keys * (self.options.filler_percentage.value / 100.0))
        non_required_keys -= filler_num
        itempool += [self.create_item("Key Quest") for _ in range(required_keys)]
        itempool += [self.create_item("Key Quest", True) for _ in range(non_required_keys)]
        itempool += [self.create_item(self.get_filler_item_name()) for _ in range(filler_num)]

        self.multiworld.itempool += itempool

    def generate_basic(self) -> None:
        self.get_location(self.get_final_quest()).place_locked_item(
            self.create_item("Victory's Flame"))

    def set_rules(self):
        # set urgent rules
        mr = self.options.master_rank_requirement.value
        for i in range(2, mr + 1):
            set_rule(self.get_location(f"MR {i} Urgent"),
                     lambda state, m=i: state.has("Key Quest", self.player, self.key_requirements[m - 1]))

        for urgent in urgent_quests:
            if urgent_quests[urgent].MR < self.options.master_rank_requirement.value:
                set_rule(self.get_location(urgent),
                         (lambda state: True) if urgent_quests[urgent].MR == 1 else
                         lambda state, m=urgent_quests[urgent].MR:
                         state.has("Key Quest", self.player, self.key_requirements[m - 1]))

        set_rule(self.get_location(self.get_final_quest()),
                 lambda state: state.has("Key Quest", self.player,
                                         self.key_requirements[
                                             self.options.master_rank_requirement.value]))

        # goal
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory's Flame", self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(filler_item_table.keys()), weights=list(filler_weights.values()))[0]

    def get_filler_hints(self):
        hints = list()
        for location in self.get_locations():
            if location.item.player == self.player and location.item.classification == ItemClassification.filler:
                hints.append(location.address)

        return hints

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict("death_link", "master_rank_requirement", "progressive_weapons",
                                         "consolidate_weapons", "progressive_armor", "enable_followers",
                                         "give_khezu_music")
        slot_data.update({
            "key_requirements": self.key_requirements[self.player],
            "filler_hint_table": self.get_filler_hints()
        })
        return slot_data
