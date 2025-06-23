from .quests import get_quest_by_id, get_proper_name, get_star_name, goal_quests, hub_rank_max
from .data.monsters import flying_wyverns, piscene_wyverns, bird_wyverns, monster_ids
from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from BaseClasses import CollectionState
    from . import MHFUWorld


def can_complete_quest(state: "CollectionState", qid: str, player: int):
    return state.can_reach(get_proper_name(get_quest_by_id(qid)), "Location", player)


def can_complete_all_quests(state: "CollectionState", qids: list[str], player: int):
    for qid in qids:
        if not can_complete_quest(state, qid, player):
            return False
    return True


def can_hunt_monsters(state: "CollectionState", quest_monsters: dict[str, dict[str, list[int]]],
                      monsters: list[str], player: int, any_monster=False):
    # any means return true if any, else return true if all
    relevant_mons = [monster_ids[monster] for monster in monsters]
    if any_monster:
        for monster in relevant_mons:
            monster_quests = [f"m{quest}" for quest in quest_monsters if monster in quest_monsters[quest]["monsters"]]
            if any(can_complete_quest(state, quest, player) for quest in monster_quests):
                return True
        return False
    else:
        for monster in relevant_mons:
            monster_quests = [f"m{quest}" for quest in quest_monsters if monster in quest_monsters[quest]["monsters"]]
            if not any(can_complete_quest(state, quest, player) for quest in monster_quests):
                return False
        return True


def set_rules(world: "MHFUWorld"):
    for hub, rank, star in world.rank_requirements:
        if (hub, rank, star + 1) in world.rank_requirements:
            add_rule(world.multiworld.get_entrance(f"To {get_star_name(hub, rank, star + 1)}", world.player),
                     lambda state, req=world.rank_requirements[hub, rank, star]:
                     state.has("Key Quest", world.player, req))
        elif star + 1 == hub_rank_max[hub, rank] and (hub, rank + 1, 0) in world.rank_requirements \
                and (hub, rank) != (0, 3):
            add_rule(world.multiworld.get_entrance(f"To {get_star_name(hub, rank + 1, 0)}", world.player),
                     lambda state, req=world.rank_requirements[hub, rank, star]:
                     state.has("Key Quest", world.player, req))

    # set goal requirement
    add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id(goal_quests[world.options.goal.value])),
                                           world.player),
             lambda state: state.has("Key Quest", world.player, world.required_keys))

    # now additional requirements
    # Village
    if world.options.village_depth:
        # Village Low
        # some basic quest requirements
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10206")), world.player),
                 lambda state: can_complete_quest(state, "m10210", world.player))
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10207")), world.player),
                 lambda state: can_complete_quest(state, "m10211", world.player))
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10209")), world.player),
                 lambda state: can_complete_quest(state, "m10213", world.player))
        # needs access to Yian Kut-Ku, unlock req is 10 Kut-Ku killed
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10304")), world.player),
                 lambda state: can_hunt_monsters(state, world.quest_info, ["Yian Kut-Ku"], world.player))
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10308")), world.player),
                 lambda state: can_complete_quest(state, "m10307", world.player))
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10309")), world.player),
                 lambda state: can_complete_quest(state, "m10313", world.player))
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10318")), world.player),
                 lambda state: can_complete_quest(state, "m10317", world.player))
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10407")), world.player),
                 lambda state: can_complete_quest(state, "m10406", world.player))
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10409")), world.player),
                 lambda state: can_complete_quest(state, "m10411", world.player))
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10414")), world.player),
                 lambda state: can_complete_quest(state, "m10413", world.player))
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10416")), world.player),
                 lambda state: can_complete_quest(state, "m10415", world.player))
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10505")), world.player),
                 lambda state: can_complete_quest(state, "m10506", world.player))
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10511")), world.player),
                 lambda state: can_complete_quest(state, "m10509", world.player))  # 6* Urgent, effectively postgame.
        # bit of a hack for this one, it needs all village low quests completed,
        # but we can just check the only quests with actual requirements
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m10510")), world.player),
                 lambda state: can_complete_all_quests(state, ["m10206", "m10207", "m10209", "m10304", "m10308",
                                                               "m10309", "m10318", "m10407", "m10409", "m10414",
                                                               "m10416", "m10505", "m10511"], world.player))
        if world.options.village_depth.value > 1:
            # Village High
            # m11005 has a requirement...that will always be met because it's village 6* urgent
            for quest in ("m11116", "m11117", "m11118"):
                add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id(quest)), world.player),
                         lambda state: can_complete_quest(state, "m11005", world.player))
            add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m11119")), world.player),
                     lambda state: can_complete_all_quests(state, ["m11116", "m11117", "m11118"], world.player))
            for quest in ("m11211", "m11212"):
                add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id(quest)), world.player),
                         lambda state: can_hunt_monsters(state, world.quest_info,
                                                         [*list(piscene_wyverns.keys()), *list(flying_wyverns.keys()),
                                                          *list(bird_wyverns.keys())], world.player, True))
                # needs access to any Bird/Flying/Piscine that aren't a drome
            add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m11213")), world.player),
                     lambda state: can_complete_all_quests(state, ["m11211", "m11212"], world.player))
            for quest in ("m11220", "m11221", "m11222", "m11223"):
                # needs all of the village high quests
                add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id(quest)), world.player),
                         lambda state: can_complete_all_quests(state, ["m11119", "m11213"], world.player))
            # Monster Hunter needs all village low and high
            add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m11226")), world.player),
                     lambda state: can_complete_all_quests(state, ["m10510", "m11119", "m11213"], world.player))
    # Guild
    if world.options.guild_depth:
        # Guild Low
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m01009")), world.player),
                 lambda state: can_complete_quest(state, "m01020", world.player))
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m01106")), world.player),
                 lambda state: can_complete_quest(state, "m01105", world.player))
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m01112")), world.player),
                 lambda state: can_complete_quest(state, "m01109", world.player))
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m01114")), world.player),
                 lambda state: can_complete_quest(state, "m01116", world.player))
        add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m01124")), world.player),
                 lambda state: can_complete_all_quests(state, ["m01009", "m01106", "m01112", "m01114"], world.player))
        if world.options.guild_depth > 1:
            if world.options.village_depth == 2:
                # only cross-hub requirements
                # we "patch" out the requirement if village depth is lower than high
                add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m02124")), world.player),
                         lambda state: can_complete_quest(state, "m11005", world.player))
                add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m02228")), world.player),
                         lambda state: can_complete_quest(state, "m11201", world.player))
                add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m02229")), world.player),
                         lambda state: can_complete_quest(state, "m11201", world.player))

            for quest in ("m02214", "m02215"):
                add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id(quest)), world.player),
                         lambda state: can_hunt_monsters(state, world.quest_info,
                                                         [*list(piscene_wyverns.keys()), *list(flying_wyverns.keys()),
                                                          *list(bird_wyverns.keys())], world.player, True))
            for quest in ("m02217", "m02218", "m02219", "m02220", "m02221", "m02222"):
                add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id(quest)), world.player),
                         lambda state: can_complete_all_quests(state, ["m02214", "m02215", "m02124", "m02228",
                                                                       "m02229"], world.player))
            add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m01124")), world.player),
                     lambda state: can_complete_all_quests(state, ["m01009", "m01106", "m01112", "m01114"],
                                                           world.player))
            # special case here, this is actually the end of HR urgents. We can effectively duplicate the rules for it
            add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m02225")),
                                                   world.player),
                     lambda state: state.has("Key Quest", world.player, world.rank_requirements[0, 3, 0]
                     if (0, 3, 0) in world.rank_requirements else world.required_keys))
            add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m02226")), world.player),
                     lambda state: can_complete_quest(state, "m02225", world.player))

            if world.options.guild_depth.value == 3:
                # Lao, needs all G1/G2. Just wanna push it back a sphere
                add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id("m03127")), world.player),
                         lambda state: can_complete_quest(state, "m03109", world.player))
                for quest in ("m03222", "m03223", "m03224", "m03225", "m03226", "m03227"):
                    add_rule(world.multiworld.get_location(get_proper_name(get_quest_by_id(quest)), world.player),
                             lambda state: can_complete_quest(state, "m03127", world.player))
