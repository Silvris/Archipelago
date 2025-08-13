from worlds.LauncherComponents import components, Component, launch_subprocess, Type


def launch_client():
    from .client import launch
    launch_subprocess(launch, "Docs Viewer")


if not any(component.display_name == "Docs Viewer" for component in components):
    components.append(Component("Docs Viewer", "DocsViewer", func=launch_client, component_type=Type.TOOL,
                                description="Visual display for Archipelago and world documentation."), )