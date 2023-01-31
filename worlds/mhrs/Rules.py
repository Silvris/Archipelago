from worlds.generic.Rules import set_rule
from BaseClasses import MultiWorld
from worlds.mhrs.Quests import UrgentQuests


def set_mhrs_rules(multiworld: MultiWorld, player: int, final_quest: str):
    # region rules

    set_rule(multiworld.get_entrance("To MR1", player), lambda state: state.has("Master Rank 1", player))
    set_rule(multiworld.get_entrance("To MR2", player), lambda state: state.has("Master Rank 2", player))
    set_rule(multiworld.get_entrance("To MR3", player), lambda state: state.has("Master Rank 3", player))
    set_rule(multiworld.get_entrance("To MR4", player), lambda state: state.has("Master Rank 4", player))
    set_rule(multiworld.get_entrance("To MR5", player), lambda state: state.has("Master Rank 5", player))
    set_rule(multiworld.get_entrance("To MR6", player), lambda state: state.has("Master Rank 6", player))
    # set urgent rules
    mr = multiworld.master_rank_requirement[player].value
    if mr >= 2:
        set_rule(multiworld.get_location(UrgentQuests[315900], player), lambda state: state.has("MR2 Urgent", player))
        if mr >= 3:
            set_rule(multiworld.get_location((UrgentQuests[315901]), player),
                     lambda state: state.has("MR3 Urgent", player))
            if mr >= 4:
                set_rule(multiworld.get_location(UrgentQuests[315902], player),
                         lambda state: state.has("MR4 Urgent", player))
                if mr >= 5:
                    set_rule(multiworld.get_location(UrgentQuests[315903], player),
                             lambda state: state.has("MR5 Urgent", player))
                    if mr == 6:
                        set_rule(multiworld.get_location(UrgentQuests[315904], player),
                                 lambda state: state.has("MR6 Urgent", player))

    set_rule(multiworld.get_location(final_quest, player),
             lambda state: state.has("Proof of a Hero", player, multiworld.required_proofs[player].value))
