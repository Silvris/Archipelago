from .Quests import get_quest_by_id, get_proper_name, get_star_name, goal_quests, hub_rank_max
from typing import TYPE_CHECKING, List
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from BaseClasses import CollectionState
    from . import MHFUWorld


def can_complete_quest(state: "CollectionState", qid: str, player: int):
    return state.can_reach(get_proper_name(get_quest_by_id(qid)), "Location", player)


def can_complete_all_quests(state: "CollectionState", qids: List[str], player: int):
    for qid in qids:
        if not can_complete_quest(state, qid, player):
            return False
    return True


def can_hunt_monsters(state: "CollectionState", monsters: List[str], player: int, any = False):
    # any means return true if any, else return true if all
    return True

def set_rules(world: "MHFUWorld"):
    for hub, rank, star in world.rank_requirements:
        if (hub, rank, star + 1) in world.rank_requirements:
            add_rule(world.multiworld.get_entrance(f"To {get_star_name(hub, rank, star + 1)}", world.player),
                     lambda state, req=world.rank_requirements[hub, rank, star + 1]:
                     state.has("Key Quest", world.player, req))
        elif star + 1 == hub_rank_max[hub, rank] and (hub, rank + 1, 0) in world.rank_requirements \
                and (hub, rank) != (0, 3):
            add_rule(world.multiworld.get_entrance(f"To {get_star_name(hub, rank + 1, 0)}", world.player),
                     lambda state, req=world.rank_requirements[hub, rank + 1, 0]:
                     state.has("Key Quest", world.player, req))

    # set goal requirement
    add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id(goal_quests[world.options.goal.value])),
                                           world.player),
             lambda state: state.has("Key Quest", world.player, world.required_keys))

    # now additional requirements
    # Village
    if world.options.village_depth:
        # Village Low
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10304")), world.player),
                 lambda state: can_hunt_monsters(state, ["Yian Kut-Ku"], world.player))  # needs access to Yian Kut-Ku
        # bit of a hack for this one, it needs all village low quests completed, but only one other quest has any lock
        # so we just check if we can hit it first
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10510")), world.player),
                 lambda state: can_complete_quest(state, "m10304", world.player))
        if world.options.village_depth.value > 1:
            # Village High
            for quest in ("m11211", "m11212", "m11213"):
                add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id(quest)), world.player),
                         lambda state: can_hunt_monsters(state, ["Yian Kut-Ku", "Rathalos", "Plesioth"], world.player,
                                                         True))
                # needs access to any Bird/Flying/Piscine that aren't a drome
            for quest in ("m11220", "m11221", "m11222", "m11223"):
                # needs all of the village high quests
                add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id(quest)), world.player),
                         lambda state: can_complete_all_quests(state, ["m11211", "m11212", "m11213"], world.player))
            # Monster Hunter needs all village low and high
            add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m11226")), world.player),
                     lambda state: can_complete_all_quests(state, ["m10510", "m11211", "m11212", "m11213"], world.player))
    # Guild
    if world.options.guild_depth:
        # Guild Low
        # Bit of a weird one, there's a couple of guild quests that rely on village progress
        for quest in ("m00108", "m00109"):
            add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id(quest)), world.player),
                     lambda state: True)  # requires m10203, we'll figure something out
        for quest in ("m01124", "m01213", "m01214", "m01215", "m01216", "m01217"):
            add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id(quest)), world.player),
                     lambda state: can_complete_all_quests(state, ["m00108", "m00109"], world.player))
        if world.options.guild_depth > 1:
            for quest in ("m02214", "m02215"):
                add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id(quest)), world.player),
                         lambda state: True)  # needs access to any Bird/Flying/Piscine that aren't a drome
            for quest in ("m02217", "m02218", "m02219", "m02220", "m02221", "m02222"):
                add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id(quest)), world.player),
                         lambda state: can_complete_all_quests(state, ["m02214", "m02215"], world.player))
            # the difficult requirements
