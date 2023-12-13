from typing import Dict

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import launch_subprocess, components, Component, Type


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
    Play a little Sudoku while you're in BK mode to maybe get some useful hints
    """
    game = "Monster Hunter Freedom Unite"
    web = MHFUWebWorld()
    data_version = 1

    item_name_to_id: Dict[str, int] = {}
    location_name_to_id: Dict[str, int] = {}

    @classmethod
    def stage_assert_generate(cls, multiworld):
        raise Exception("MHFU cannot be used for generating worlds")
