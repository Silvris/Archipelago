import logging
import math
from typing import Dict, Any, List, ClassVar
from operator import itemgetter
import settings
from BaseClasses import Tutorial, ItemClassification, MultiWorld
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import launch_subprocess, components, Component, Type
from .Quests import create_ranks, location_name_to_id, base_id, goal_quests,\
    get_quest_by_id, get_proper_name, goal_ranks, hub_rank_max
from .Items import MHFUItem, item_table, filler_item_table, filler_weights, item_name_to_id, weapons, item_name_groups
from .Options import MHFUOptions
from .Rules import set_rules


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="MHFUClient")


components.append(Component("MHFU Client", "MHFUClient", func=launch_client, component_type=Type.CLIENT))


class MHFUSettings(settings.Group):
    class PPSSPPSaveDirectory(settings.UserFolderPath):
        """PPSSPP Save Directory, for automatic mod loading"""
        description = "PPSSPP Save Directory"

    save_directory: PPSSPPSaveDirectory = PPSSPPSaveDirectory("C:/Program Files/PPSSPP/memstick/PSP")


class MHFUWebWorld(WebWorld):
    theme = 'stone'
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Monster Hunter Freedom Unite randomizer connected to an Archipelago Multiworld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Silvris", "IncognitoMan"]
        )
    ]


class MHFUWorld(World):
    """
    Monster Hunter Freedom Unite description goes here.
    """
    game = "Monster Hunter Freedom Unite"
    web = MHFUWebWorld()
    data_version = 0
    options_dataclass = MHFUOptions
    options: MHFUOptions
    settings: ClassVar[MHFUSettings]

    item_name_to_id: Dict[str, int] = item_name_to_id
    location_name_to_id: Dict[str, int] = location_name_to_id
    item_names = item_name_groups

    create_regions = create_ranks

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.location_num: Dict[(int, int, int), int] = {}
        self.rank_requirements: Dict[(int, int, int), int] = {}
        self.quest_monsters: Dict[str, List[int]] = {}
        self.required_keys: int = 0

    def generate_early(self) -> None:
        # there's an impossible set of options, so we just need to block it
        if not self.options.guild_depth and not self.options.village_depth:
            raise Exception("Must have at least one rank of quests to play through.")
        goal_rank = goal_ranks[self.options.goal.value]
        if goal_rank[0] == 0 and goal_rank[1] > self.options.guild_depth:
            self.options.guild_depth.value = goal_rank[1]
            logging.warning(f"Guild Depth too low for goal, increasing to {self.options.guild_depth.get_option_name(goal_rank[1])}")
        elif goal_rank[0] == 1 and goal_rank[1] > self.options.village_depth:
            self.options.village_depth.value = goal_rank[1]
            logging.warning(f"Village Depth too low for goal, increasing to {self.options.village_depth.get_option_name(goal_rank[1])}")

    def create_item(self, name: str, force_non_progression=False) -> MHFUItem:
        item = item_table[name]
        classification = ItemClassification.filler
        if item.progression and not force_non_progression:
            classification = ItemClassification.progression_skip_balancing \
                if item.skip_balancing else ItemClassification.progression
        elif item.trap:
            classification = ItemClassification.trap
        return MHFUItem(name, classification, item.code, self.player)

    def create_items(self) -> None:
        itempool = []

        # first, determine our quest depth
        if self.options.guild_depth:
            max_guild = (0, self.options.guild_depth.value, hub_rank_max[0, self.options.guild_depth.value])
        else:
            max_guild = (-1, -1, -1)
        if self.options.village_depth:
            max_village = (1, self.options.village_depth.value, hub_rank_max[1, self.options.village_depth.value -1])
        else:
            max_village = (-1, -1, -1)
        if max_guild[1] == 3:
            max_rarity = 10
        elif max_guild[1] == 2 or max_village[1] == 1:
            max_rarity = 7
        else:
            max_rarity = 3
        if self.options.weapons.value in (0, 2):
            if self.options.weapons.value == 2:
                itempool += [self.create_item(f"Weapons Rarity {x}") for x in range(1, max_rarity + 1)]
            else:
                for weapon in weapons:
                    itempool += [self.create_item(f"{weapon} Rarity {x}") for x in range(1, max_rarity + 1)]
        else:
            if self.options.weapons.value == 3:
                itempool += [self.create_item("Progressive Weapons") for _ in range(max_rarity)]
            else:
                for weapon in weapons:
                    itempool += [self.create_item(f"Progressive {weapon}") for _ in range(max_rarity)]
        if self.options.progressive_armor:
            itempool += [self.create_item("Progressive Armor") for _ in range(max_rarity)]
        else:
            itempool += [self.create_item(f"Armor Rarity {i}") for i in range(1, max_rarity + 1)]
        free_items = sum(self.location_num.values()) - len(itempool) - 1
        self.required_keys = int(free_items * (self.options.required_keys.value / 100))
        non_required = free_items - self.required_keys
        filler_items = int(non_required * (self.options.filler_percentage / 100))
        non_required -= filler_items
        # notes about the special cases
        # training is either always open aside from each individual quest unlocks, or locked behind GR access
        # so we lock the entrance by can_reach(Region), which opens a can of worms for rules
        # treasure is sphere 1 always if enabled, since there's only one set of them
        location_count = self.location_num.copy()
        running_total = 0
        for key in ((0, 0, 0), (0, 0, 1), (0, 4, 0), (2, 0, 0), (2, 1, 0), (2, 2, 0)):
            if key in location_count:
                running_total += location_count.pop(key)
        all_locs = sum(self.location_num.values())
        rank_order = sorted(location_count, key=lambda tup: tup[1] if tup[0] == 0 else tup[1] + 1)
        for i, rank in enumerate(rank_order):
            running_total += location_count[rank]
            accessible = running_total / all_locs
            self.rank_requirements[rank] = max(
                math.floor(self.required_keys * accessible), i)
        itempool += [self.create_item("Key Quest") for _ in range(self.required_keys)]
        itempool += [self.create_item("Key Quest", True) for _ in range(non_required)]
        itempool += [self.create_item(self.get_filler_item_name()) for _ in range(filler_items)]
        self.multiworld.itempool += itempool

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(filler_item_table.keys()), weights=list(filler_weights.values()))[0]

    def generate_basic(self) -> None:
        goal_quest = goal_quests[self.options.goal.value]
        quest_name = get_proper_name(get_quest_by_id(goal_quest))
        goal_location = self.multiworld.get_location(quest_name, self.player)
        goal_location.address = None  # This lets us keep the id reserved, even though it's an event this playthrough
        goal_location.place_locked_item(self.create_item("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    set_rules = set_rules

    def fill_slot_data(self) -> Dict[str, Any]:
        options = self.options.as_dict(
            "death_link",
            "goal",
            "weapons",
            "quest_randomization",
            "quest_difficulty_multiplier",
            "cash_only_equipment"
        )
        options["required_keys"] = self.required_keys
        rank_requirements = {}
        for rank in self.rank_requirements:
            rank_requirements[f"{rank[0]},{rank[1]},{rank[2]}"] = self.rank_requirements[rank]
        options["rank_requirements"] = rank_requirements
        options["quest_monsters"] = self.quest_monsters if self.options.quest_randomization else {}
        return options
