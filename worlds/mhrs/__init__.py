import math
from typing import Dict, Any

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule
from BaseClasses import Item, ItemClassification, Region, Entrance
from .Options import mhrs_options
from .Items import lookup_name_to_id as items_lookup
from .Items import filler_item_table, filler_weights, follower_table, progression_item_table, MHRSItem
from .Locations import mhr_quests, MHRSQuest, get_quest_table, get_mr_quest_num
from .Quests import FinalQuests, UrgentQuests
from .Regions import mhrs_regions, link_mhrs_regions
from .QuestGen import generate_quests


class MHRSWebWorld(WebWorld):
    theme = "stone"


class MHRSWorld(World):
    """
    Monster Hunter Rise: Sunbreak is an action RPG by CAPCOM. Players take the role of a hunter tasked with defeating a
    plethora of fantastical monsters in an effort to protect their village, crafting weapons and armor along the way.
    This randomizer focuses specifically on the Sunbreak expansion.
    """
    game = "Monster Hunter Rise Sunbreak"
    option_definitions = mhrs_options
    web = MHRSWebWorld()
    data_version = 0
    base_id = 315100

    item_name_to_id = items_lookup
    location_name_to_id = {name: mhr_quests[name].id for name in mhr_quests}
    final_bosses = dict()
    requirements_base = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    key_requirements = dict()
    generate_output = generate_quests

    def create_item(self, name: str, force_non_progression=False) -> Item:
        classification = ItemClassification.filler
        if name in progression_item_table and not force_non_progression:
            classification = ItemClassification.progression
        if name in follower_table and not force_non_progression:
            classification = ItemClassification.useful
        if name == "Key Quest" and not force_non_progression:
            classification = ItemClassification.progression_skip_balancing
        item = MHRSItem(name, classification, items_lookup[name], self.player)
        return item

    def get_final_boss(self, player):
        # first check if we have already defined this player's final boss
        if player in self.final_bosses:
            return self.final_bosses[player]
        else:
            # define the player's final boss, is it a preset option?
            target = self.multiworld.final_quest_target[player].value
            if target not in [0, 1]:
                return target
            else:
                # roll a random boss for the player
                boss_table = [i for i in range(2, 22 if target == 1 else 23)]

                boss = self.multiworld.per_slot_randoms[self.player].choice(boss_table)

                self.final_bosses[player] = boss
                return boss

    def get_final_quest(self, player):
        boss = self.get_final_boss(player)
        return f"{self.multiworld.master_rank_requirement[self.player].value}★ - {FinalQuests[boss]}"

    def create_regions(self) -> None:
        def MHRSRegion(region_name: str, exits=[]):
            region = Region(region_name, self.player, self.multiworld)
            region.locations = [
                MHRSQuest(self.player, name, mhr_quests[name].id, region)
                for name in mhr_quests
                if mhr_quests[name].region == region_name
                   and mhr_quests[name].MR <= self.multiworld.master_rank_requirement[self.player].value
                # this leaves quests higher than max MR out
            ]
            for exit in exits:
                region.exits.append(Entrance(self.player, exit, region))
            if region_name == f"MR{self.multiworld.master_rank_requirement[self.player].value}":
                region.exits = list()
                region.locations.append(MHRSQuest(self.player, self.get_final_quest(self.player), None, region))
            return region

        self.multiworld.regions += [MHRSRegion(*r) for r in mhrs_regions
                                    if r[0] not in [f"MR{i}"
                                                    for i in range(
                    self.multiworld.master_rank_requirement[self.player].value + 1, 7)]]
        link_mhrs_regions(self.multiworld, self.player)

    def create_items(self) -> None:
        itempool = []
        MR = self.multiworld.master_rank_requirement[self.player].value

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
                    self.create_item(f"Progressive {weapon}") for _ in range(8, 9 + (MR // 3))
                ]
        else:
            for weapon in weapons:
                itempool += [
                    self.create_item(f"{weapon} Rarity {i}") for i in range(8, 9 + (MR // 3))
                ]
        # handle armor
        if self.multiworld.progressive_armor[self.player]:
            itempool += [self.create_item("Progressive Armor Rarity") for _ in range(8, 9 + (MR // 3))]
        else:
            itempool += [self.create_item(f"Armor Rarity {i}") for i in range(8, 9 + (MR // 3))
                         ]

        # handle follower randomization if enabled
        if self.multiworld.enable_followers[self.player] == 0:
            for follower in follower_table:
                itempool.append(self.create_item(follower))
        quests = get_quest_table(self.multiworld.master_rank_requirement[self.player].value)
        quest_num = len(quests)
        total_key_count = min(quest_num - len(itempool), self.multiworld.total_keys[self.player].value)
        required_keys = math.floor(total_key_count * (self.multiworld.required_keys[self.player].value / 100.0))
        non_required_keys = total_key_count - required_keys
        self.key_requirements[self.player] = self.requirements_base.copy()
        for i in range(1, MR + 1):
            quest_percentage = get_mr_quest_num(i) / quest_num  # percentage this MR has over the total
            self.key_requirements[i] = (self.key_requirements[i - 1] if i > 1 else 0) \
                                       + math.floor(quest_percentage * required_keys)
        self.key_requirements[MR] = required_keys
        filler_num = math.floor(non_required_keys * (self.multiworld.filler_percentage[self.player].value / 100.0))
        non_required_keys -= filler_num
        itempool += [self.create_item("Key Quest") for _ in range(required_keys)]
        itempool += [self.create_item("Key Quest", True) for _ in range(non_required_keys)]
        itempool += [self.create_item(self.get_filler_item_name()) for _ in range(filler_num)]

        self.multiworld.itempool += itempool

    def generate_basic(self) -> None:
        self.multiworld.get_location("1★ - Uninvited Guest", self.player).place_locked_item(
            self.create_item("Master Rank 1"))
        mr = self.multiworld.master_rank_requirement[self.player].value
        if mr >= 2:
            self.multiworld.get_location("2★ - Scarlet Tengu in the Shrine Ruins", self.player).place_locked_item(
                self.create_item("Master Rank 2"))
            if mr >= 3:
                self.multiworld.get_location("3★ - A Rocky Rampage", self.player).place_locked_item(
                    self.create_item("Master Rank 3"))
                if mr >= 4:
                    self.multiworld.get_location("4★ - Ice Wolf, Red Moon", self.player).place_locked_item(
                        self.create_item("Master Rank 4"))
                    if mr >= 5:
                        self.multiworld.get_location("5★ - Witness by Moonlight", self.player).place_locked_item(
                            self.create_item("Master Rank 5"))
                        if mr == 6:
                            self.multiworld.get_location("6★ - Proof of Courage", self.player).place_locked_item(
                                self.create_item("Master Rank 6"))
        self.multiworld.get_location(self.get_final_quest(self.player), self.player).place_locked_item(
            self.create_item("Victory's Flame"))

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory's Flame", self.player)

    def set_rules(self):
        # set urgent rules
        mr = self.multiworld.master_rank_requirement[self.player].value
        for i in range(1, mr + 1):
            set_rule(self.multiworld.get_entrance(f"To MR{i}", self.player),
                     lambda state, m=i: state.has(f"Master Rank {m}", self.player))

        if mr >= 2:
            set_rule(self.multiworld.get_location("2★ - Scarlet Tengu in the Shrine Ruins", self.player),
                     lambda state: state.has("Key Quest", self.player, self.key_requirements[1]))
            if mr >= 3:
                set_rule(self.multiworld.get_location("3★ - A Rocky Rampage", self.player),
                         lambda state: state.has("Key Quest", self.player, self.key_requirements[2]))
                if mr >= 4:
                    set_rule(self.multiworld.get_location("4★ - Ice Wolf, Red Moon", self.player),
                             lambda state: state.has("Key Quest", self.player, self.key_requirements[3]))
                    if mr >= 5:
                        set_rule(self.multiworld.get_location("5★ - Witness by Moonlight", self.player),
                                 lambda state: state.has("Key Quest", self.player, self.key_requirements[4]))
                        if mr == 6:
                            set_rule(self.multiworld.get_location("6★ - Proof of Courage", self.player),
                                     lambda state: state.has("Key Quest", self.player, self.key_requirements[5]))

        set_rule(self.multiworld.get_location(self.get_final_quest(self.player), self.player),
                 lambda state: state.has("Key Quest", self.player,
                                         self.key_requirements[
                                             self.multiworld.master_rank_requirement[self.player].value]))

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choices(list(filler_item_table.keys()), weights=list(filler_weights.values()))[0]

    def get_filler_hints(self):
        hints = list()
        for location in self.multiworld.get_locations(self.player):
            if location.item.player == self.player and location.item.classification == ItemClassification.filler:
                hints.append(location.address)

        return hints

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = {
            "death_link": self.multiworld.death_link[self.player].value,
            "master_rank_requirement": self.multiworld.master_rank_requirement[self.player].value,
            "progressive_weapons": self.multiworld.progressive_weapons[self.player].value,
            "consolidate_weapons": self.multiworld.consolidate_weapons[self.player].value,
            "progressive_armor": self.multiworld.progressive_armor[self.player].value,
            "enable_followers": self.multiworld.enable_followers[self.player].value,
            "give_khezu_music": self.multiworld.give_khezu_music[self.player].value,
            "key_requirements": self.key_requirements[self.player],
            "filler_hint_table": self.get_filler_hints()
        }
        return slot_data
