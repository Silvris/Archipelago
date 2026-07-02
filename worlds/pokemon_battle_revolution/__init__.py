from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import components, Component, launch_subprocess


def launch(*args):
    from .client import launch_pbr_client
    launch_subprocess(launch_pbr_client, "PBR Client", args)


components.append(Component("Pokémon Battle Revolution Client", func=launch, ))


class PBRWebWorld(WebWorld):
    pass


class PBRWorld(World):
    game = "Pokemon Battle Revolution"
    item_name_to_id = {1: "None"}
    location_name_to_id = {1: "None"}