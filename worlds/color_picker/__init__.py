from worlds.LauncherComponents import components, Component, launch_subprocess, Type


def launch_client():
    from .client import launch
    launch_subprocess(launch, "Color Picker")


if not any(component.display_name == "Color Picker" for component in components):
    components.append(Component("Color Picker", func=launch_client, component_type=Type.TOOL,
                                description="Visual adjuster for background and text color for Archipelago."), )