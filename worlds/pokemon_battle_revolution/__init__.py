from worlds.LauncherComponents import components, Component, launch_subprocess
from .client import launch_pbr_client


def launch(*args):
    launch_subprocess(launch_pbr_client, "PBR Client", args)


components.append(Component("Pokémon Battle Revolution Client", func=launch, ))