import logging
import math
from typing import Any, ClassVar
import settings
from BaseClasses import Tutorial, ItemClassification, MultiWorld, CollectionState, Item
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import launch_subprocess, components, Component, Type
from .quests import create_ranks, location_name_to_id, base_id, goal_quests, \
    get_quest_by_id, goal_ranks, hub_rank_max, rank_sort, SlotQuestInfo
from .items import MHFUItem, item_table, filler_item_table, filler_weights, item_name_to_id, weapons, item_name_groups
from .options import MHFUOptions
from .rules import set_rules, MHFULogicMixin
from .data.trap_link import local_trap_to_type


def launch_client(*args: str) -> None:
    from .client import launch
    launch_subprocess(launch, name="MHFUClient", args=args)


components.append(Component("MHFU Client", "MHFUClient", func=launch_client,
                            supports_uri=True, game_name="Monster Hunter Freedom Unite", component_type=Type.CLIENT))


class MHFUSettings(settings.Group):
    class PPSSPPExe(settings.OptionalUserFilePath):
        """PPSSPP Executable, for automatic launching"""
        description = "PPSSPP Executable"

    ppsspp_exe: PPSSPPExe = PPSSPPExe("C:/Program Files/PPSSPP/PPSSPPWindows64.exe")
    auto_start: bool = True


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

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id
    item_name_groups = item_name_groups
    create_regions = create_ranks

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.location_num: dict[tuple[int, int, int], int] = {}
        self.rank_requirements: dict[tuple[int, int, int], int] = {}
        self.quest_info: dict[str, SlotQuestInfo] = {}
        self.required_keys: int = 0

    def generate_early(self) -> None:
        # there's an impossible set of options, so we just need to block it
        if not self.options.guild_depth and not self.options.village_depth:
            raise OptionError(f"{self.player_name}) Must have at least one rank of quests to play through.")
        goal_rank = goal_ranks[self.options.goal.value]
        if goal_rank[0] == 0 and goal_rank[1] > self.options.guild_depth:
            self.options.guild_depth.value = goal_rank[1]
            logging.warning(f"({self.player_name}) Guild Depth too low for goal, increasing to "
                            f"{self.options.guild_depth.get_option_name(goal_rank[1])}")
        elif goal_rank[0] == 1 and (goal_rank[1] + 1) > self.options.village_depth:
            self.options.village_depth.value = goal_rank[1] + 1
            logging.warning(f"{self.player_name}) Village Depth too low for goal, increasing to "
                            f"{self.options.village_depth.get_option_name(goal_rank[1] + 1)}")

    def create_item(self, name: str, force_non_progression: bool = False) -> MHFUItem:
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
            max_village = (1, self.options.village_depth.value, hub_rank_max[1, self.options.village_depth.value - 1])
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
        self.required_keys = max(len(self.location_num), int(free_items * (self.options.required_keys.value / 100)))
        non_required = free_items - self.required_keys
        filler_items = int(non_required * (self.options.filler_percentage / 100))
        non_required -= filler_items
        trap_amount = math.floor(filler_items * (self.options.trap_percentage / 100.0))
        filler_items -= trap_amount
        # notes about the special cases
        # training is either always open aside from each individual quest unlocks, or locked behind GR access
        # so we lock the entrance by can_reach(Region), which opens a can of worms for rules
        # treasure is sphere 1 always if enabled, since there's only one set of them
        location_count = self.location_num.copy()
        running_total = 0
        for key in ((0, 0, 0), (0, 0, 1), (0, 4, 0), (2, 0, 0), (2, 1, 0), (2, 2, 0)):
            if key in location_count:
                if key in ((0, 0, 0), (0, 0, 1)):
                    running_total += location_count.pop(key)
                else:
                    # ignore treasure and arena for calculating key counts
                    # we'll probably want to make this smarter eventually, but being a little lax doesn't hurt for now
                    location_count.pop(key)
        all_locs = sum(self.location_num.values())
        rank_order = sorted(location_count, key=lambda tup: rank_sort[tup])
        for i, rank in enumerate(rank_order):
            running_total += location_count[rank]
            accessible = running_total / all_locs
            self.rank_requirements[rank] = max(
                math.floor(self.required_keys * accessible), i)
        itempool += [self.create_item("Key Quest") for _ in range(self.required_keys)]
        itempool += [self.create_item("Key Quest", True) for _ in range(non_required)]
        itempool += [self.create_item(self.get_filler_item_name()) for _ in range(filler_items)]
        itempool += [self.create_item(name) for name in self.get_trap_item_names(trap_amount)]
        self.multiworld.itempool += itempool

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(filler_item_table.keys()), weights=list(filler_weights.values()))[0]

    def get_trap_item_names(self, num: int = 1) -> list[str]:
        return self.random.choices(list(self.options.trap_weights.keys()),
                                   weights=list(self.options.trap_weights.values()), k=num)

    set_rules = set_rules

    def fill_slot_data(self) -> dict[str, Any]:
        slot_info = self.options.as_dict(
            "death_link",
            "goal",
            "weapons",
            "quest_randomization",
            "quest_difficulty_multiplier",
            "cash_only_equipment",
            "trap_link",
        )
        allowed_traps = set()
        if self.options.trap_link:
            allowed_traps.update([local_trap_to_type[key]
                                  for key, value in self.options.trap_weights.items() if value > 0])
        slot_info["allowed_traps"] = allowed_traps
        slot_info["required_keys"] = self.required_keys
        rank_requirements = {}
        for rank in self.rank_requirements:
            rank_requirements[f"{rank[0]},{rank[1]},{rank[2]}"] = self.rank_requirements[rank]
        slot_info["rank_requirements"] = rank_requirements
        slot_info["quest_info"] = self.quest_info if self.options.quest_randomization else {}
        slot_info["set_cutscene"] = not self.options.village_depth.value == 2
        return slot_info
