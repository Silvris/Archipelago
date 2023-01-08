from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import set_rule
from BaseClasses import MultiWorld
from .Locations import mhr_quests


class MHRSLogic(LogicMixin):
    def mhrs_can_access_rank(self, player: int, mr: int):
        return self.has(f"MR{mr} Urgent", player)


def set_mhrs_rules(world: MultiWorld, player: int):
    # just set it on the region entrances, as they are the only logical barriers to finishing
    set_rule(world.get_entrance("MR2 Urgent", player), lambda state: state.has("MR2 Urgent", player))
    set_rule(world.get_entrance("MR3 Urgent", player), lambda state: state.has("MR3 Urgent", player))
    set_rule(world.get_entrance("MR4 Urgent", player), lambda state: state.has("MR4 Urgent", player))
    set_rule(world.get_entrance("MR5 Urgent", player), lambda state: state.has("MR5 Urgent", player))
    set_rule(world.get_entrance("MR6 Urgent", player), lambda state: state.has("MR6 Urgent", player))
