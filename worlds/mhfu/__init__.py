import typing
from typing import Dict
import settings
from BaseClasses import Tutorial, ItemClassification, MultiWorld
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import launch_subprocess, components, Component, Type
from .Quests import create_ranks, location_name_to_id, base_id, goal_quests, get_quest_by_id, get_proper_name
from .Items import MHFUItem, item_table, filler_item_table, filler_weights, item_name_to_id, weapons
from .Options import MHFUOptions


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
    settings: typing.ClassVar[MHFUSettings]

    item_name_to_id: Dict[str, int] = item_name_to_id
    location_name_to_id: Dict[str, int] = location_name_to_id

    create_regions = create_ranks

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.location_num = 0

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
        if self.options.weapons.value in (0, 2):
            if self.options.weapons.value == 2:
                itempool += [self.create_item(f"Weapons Rarity {x}") for x in range(1, 11)]
            else:
                for weapon in weapons:
                    itempool += [self.create_item(f"{weapon} Rarity {x}") for x in range(1, 11)]
        else:
            if self.options.weapons.value == 3:
                itempool += [self.create_item("Progressive Weapons") for _ in range(10)]
            else:
                for weapon in weapons:
                    itempool += [self.create_item(f"Progressive {weapon}") for _ in range(10)]

        itempool += [self.create_item(self.get_filler_item_name()) for _ in range(self.location_num - len(itempool))]
        self.multiworld.itempool += itempool

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(filler_item_table.keys()), weights=list(filler_weights.values()))[0]

    def generate_basic(self) -> None:
        goal_quest = goal_quests[self.options.goal.value]
        quest_name = get_proper_name(get_quest_by_id(goal_quest))
        self.multiworld.get_location(quest_name, self.player)\
            .place_locked_item(self.create_item("Victory"))

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
