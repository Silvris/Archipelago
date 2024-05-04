from worlds.LauncherComponents import components, launch_subprocess, Component, Type


def launch_sub():
    from .client import launch
    launch_subprocess(launch, "DeathLink Multitool")


components.append(Component("DeathLink Multitool", func=launch_sub, component_type=Type.CLIENT))
