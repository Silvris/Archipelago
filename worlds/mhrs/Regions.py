from BaseClasses import MultiWorld
mhrs_regions = [
    ("Menu", ["MR1 Urgent"]),
    ("MR1", ["MR2 Urgent"]),
    ("MR2", ["MR3 Urgent"]),
    ("MR3", ["MR4 Urgent"]),
    ("MR4", ["MR5 Urgent"]),
    ("MR5", ["MR6 Urgent"]),
    ("MR6", []),
    ("Final", []),
    ("MR1 Urgent", ["To MR1"]),
    ("MR2 Urgent", ["To MR2"]),
    ("MR3 Urgent", ["To MR3"]),
    ("MR4 Urgent", ["To MR4"]),
    ("MR5 Urgent", ["To MR5"]),
    ("MR6 Urgent", ["To MR6"])
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
    ("MR2 Urgent", "MR2 Urgent"),
    ("MR3 Urgent", "MR3 Urgent"),
    ("MR4 Urgent", "MR4 Urgent"),
    ("MR5 Urgent", "MR5 Urgent"),
    ("MR6 Urgent", "MR6 Urgent"),
    ("To Final Quest", "Final")
]


def link_mhrs_regions(world: MultiWorld, player: int):
    for exit, region in mandatory_connections:
        world.get_entrance(exit, player).connect(world.get_region(region, player))
