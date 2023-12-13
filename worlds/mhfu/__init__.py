from typing import Dict

from BaseClasses import Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import launch_subprocess, components, Component, Type
from .Quests import create_ranks, location_name_to_id, base_id
from .Items import MHFUItem


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="MHFUClient")


components.append(Component("MHFU Client", "MHFUClient", func=launch_client, component_type=Type.CLIENT))


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
    data_version = 1

    item_name_to_id: Dict[str, int] = {
        "Nothing": base_id
    }
    location_name_to_id: Dict[str, int] = location_name_to_id

    create_regions = create_ranks

    def create_item(self, name: str) -> MHFUItem:
        return MHFUItem(name, ItemClassification.filler, base_id, self.player)

    def create_items(self) -> None:
        self.multiworld.itempool += [self.create_item("Nothing") for _ in range(len(location_name_to_id))]

