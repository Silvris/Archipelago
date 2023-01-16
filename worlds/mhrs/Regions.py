from BaseClasses import MultiWorld
mhrs_regions = [
    ("Menu", ["To MR1"]),
    ("MR1", ["MR2 Urgent"]),
    ("MR2", ["MR3 Urgent"]),
    ("MR3", ["MR4 Urgent"]),
    ("MR4", ["MR5 Urgent"]),
    ("MR5", ["MR6 Urgent"]),
    ("MR6", []),
    ("Final", [])
    # ("MR1 Requests", []),
    # ("MR2 Requests", []),
    # ("MR3 Requests", []),
    # ("MR4 Requests", []),
    # ("MR5 Requests", []),
    # ("MR6 Requests", [])
]

mandatory_connections = [
    ("To MR1", "MR1"),
    ("MR2 Urgent", "MR2"),
    ("MR3 Urgent", "MR3"),
    ("MR4 Urgent", "MR4"),
    ("MR5 Urgent", "MR5"),
    ("MR6 Urgent", "MR6"),
    ("To Final", "Final")
]


def link_mhrs_regions(world: MultiWorld, player: int):
    for exit, region in mandatory_connections:
        e = world.get_entrance(exit, player)
        r = world.get_region(region, player)
        world.get_entrance(exit, player).connect(world.get_region(region, player))
    # now apply final goal region
    print(world.get_entrance("To Final", player).name, world.get_entrance("To Final", player).connected_region, world.get_entrance("To Final", player).parent_region, player)
