from worlds.generic.Rules import set_rule
from BaseClasses import MultiWorld
from .Locations import mhr_quests


def set_mhrs_rules(world: MultiWorld, player: int):
    # just set it on the region entrances, as they are the only logical barriers to finishing
    set_rule(world.get_entrance("MR2 Urgent", player), lambda state: state.has("MR2 Urgent", player))
    set_rule(world.get_entrance("MR3 Urgent", player), lambda state: state.has("MR3 Urgent", player))
    set_rule(world.get_entrance("MR4 Urgent", player), lambda state: state.has("MR4 Urgent", player))
    set_rule(world.get_entrance("MR5 Urgent", player), lambda state: state.has("MR5 Urgent", player))
    set_rule(world.get_entrance("MR6 Urgent", player), lambda state: state.has("MR6 Urgent", player))

    set_rule(world.get_entrance("To MR1", player), lambda state: state.has("Master Rank 1", player))
    set_rule(world.get_entrance("To MR2", player), lambda state: state.has("Master Rank 2", player))
    set_rule(world.get_entrance("To MR3", player), lambda state: state.has("Master Rank 3", player))
    set_rule(world.get_entrance("To MR4", player), lambda state: state.has("Master Rank 4", player))
    set_rule(world.get_entrance("To MR5", player), lambda state: state.has("Master Rank 5", player))
    set_rule(world.get_entrance("To MR6", player), lambda state: state.has("Master Rank 6", player))
    set_rule(world.get_entrance("To Final Quest", player), lambda state: state.has("Proof of a Hero", player))
