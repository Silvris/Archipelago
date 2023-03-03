from BaseClasses import MultiWorld
mhrs_regions = [
    ("Menu", ["MR1 Urgent"]),
    ("MR1 Urgent", ["To MR1"]),
    ("MR1", ["To MR2"]),
    ("MR2", ["To MR3"]),
    ("MR3", ["To MR4"]),
    ("MR4", ["To MR5"]),
    ("MR5", ["To MR6"]),
    ("MR6", []),
    # ("MR1 Requests", []),
    # ("MR2 Requests", []),
    # ("MR3 Requests", []),
    # ("MR4 Requests", []),
    # ("MR5 Requests", []),
    # ("MR6 Requests", [])
]

entrances = {
    "MR1 Urgent": "MR1 Urgent",
    "To MR1": "MR1",
    "To MR2": "MR2",
    "To MR3": "MR3",
    "To MR4": "MR4",
    "To MR5": "MR5",
    "To MR6": "MR6",
}


def link_mhrs_regions(multiworld: MultiWorld, player: int):
    multiworld.get_entrance("MR1 Urgent", player).connect(multiworld.get_region("MR1 Urgent", player))
    for entrance in [f"To MR{i}" for i in range(1, multiworld.master_rank_requirement[player].value + 1)]:
        multiworld.get_entrance(entrance, player).connect(multiworld.get_region(entrances[entrance], player))

