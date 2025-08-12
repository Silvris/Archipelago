from worlds.LauncherComponents import components, Component, launch_subprocess, Type


def launch_client():
    from .client import launch
    launch_subprocess(launch, "Options Creator")


if not any(component.display_name == "Options Creator" for component in components):
    components.append(Component("Options Creator", "OptionsCreator", func=launch_client, component_type=Type.TOOL,
                                description="Visual creator for Archipelago option files."), )
