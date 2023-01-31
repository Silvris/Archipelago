from BaseClasses import MultiWorld
mhrs_regions = [
    ("Menu", ["MR1 Urgent"]),
    ("MR1", ["To MR2"]),
    ("MR2", ["To MR3"]),
    ("MR3", ["To MR4"]),
    ("MR4", ["To MR5"]),
    ("MR5", ["To MR6"]),
    ("MR6", []),
    ("MR1 Urgent", ["To MR1"]),
    # ("MR1 Requests", []),
    # ("MR2 Requests", []),
    # ("MR3 Requests", []),
    # ("MR4 Requests", []),
    # ("MR5 Requests", []),
    # ("MR6 Requests", [])
]

mandatory_connections = [
    ("To MR1", "MR1"),
    ("To MR2", "MR2"),
    ("To MR3", "MR3"),
    ("To MR4", "MR4"),
    ("To MR5", "MR5"),
    ("To MR6", "MR6"),
    ("MR1 Urgent", "MR1 Urgent"),
]


def link_mhrs_regions(multiworld: MultiWorld, player: int):
    for exit, region in mandatory_connections:
        multiworld.get_entrance(exit, player).connect(multiworld.get_region(region, player))
