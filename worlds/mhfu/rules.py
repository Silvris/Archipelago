from .quests import get_quest_by_id, get_proper_name, get_star_name, goal_quests, hub_rank_max, get_area_quests
from .data.monsters import flying_wyverns, piscene_wyverns, bird_wyverns, monster_ids
from .options import VillageQuestDepth, GuildQuestDepth
from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from BaseClasses import CollectionState
    from . import MHFUWorld


def can_complete_quest(state: "CollectionState", qid: str, player: int) -> bool:
    return state.can_reach_location(get_proper_name(get_quest_by_id(qid)), player)


def can_complete_all_quests(state: "CollectionState", qids: list[str], player: int) -> bool:
    for qid in qids:
        if not can_complete_quest(state, qid, player):
            return False
    return True


def can_reach_area(state: "CollectionState", areas: tuple[int],
                   rank_requirements: dict[tuple[int, int, int], int], player: int) -> bool:
    # this can be very slow
    possible_quests = get_area_quests(rank_requirements.keys(), areas)
    for quest in possible_quests:
        if state.can_reach_location(get_proper_name(quest), player):
            return True
    return False


def can_hunt_any_monster(state: "CollectionState", quest_info: dict[str, dict[str, list[int] | int]],
                         monsters: list[str], player: int, quest_id: str) -> bool:
    relevant_mons = [monster_ids[monster] for monster in monsters]
    for monster in relevant_mons:
        monster_quests = [f"m{quest}" for quest in quest_info if monster in quest_info[quest]["monsters"]
                          and f"m{quest}" != quest_id
                          and get_quest_by_id(f"m{quest}")["rank"] != 4]
        if any(can_complete_quest(state, quest, player) for quest in monster_quests):
            return True
    return False


def can_hunt_all_monsters(state: "CollectionState", quest_info: dict[str, dict[str, list[int] | int]],
                          monsters: list[str], player: int, quest_id: str) -> bool:
    relevant_mons = [monster_ids[monster] for monster in monsters]
    for monster in relevant_mons:
        monster_quests = [f"m{quest}" for quest in quest_info if monster in quest_info[quest]["monsters"]
                          and f"m{quest}" != quest_id
                          and get_quest_by_id(f"m{quest}")["rank"] != 4]
        if not any(can_complete_quest(state, quest, player) for quest in monster_quests):
            return False
    return True


def set_rules(world: "MHFUWorld") -> None:
    for hub, rank, star in world.rank_requirements:
        if (hub, rank, star + 1) in world.rank_requirements:
            add_rule(world.get_entrance(f"To {get_star_name(hub, rank, star + 1)}"),
                     lambda state, req=world.rank_requirements[hub, rank, star]:
                     state.has("Key Quest", world.player, req))
        elif star + 1 == hub_rank_max[hub, rank] and (hub, rank + 1, 0) in world.rank_requirements \
                and (hub, rank) != (0, 3):
            add_rule(world.get_entrance(f"To {get_star_name(hub, rank + 1, 0)}"),
                     lambda state, req=world.rank_requirements[hub, rank, star]:
                     state.has("Key Quest", world.player, req))

    # set goal requirement
    add_rule(world.get_location(get_proper_name(get_quest_by_id(goal_quests[world.options.goal.value]))),
             lambda state: state.has("Key Quest", world.player, world.required_keys))

    # now additional requirements
    # Village
    if world.options.village_depth:
        # Village Low
        # some basic quest requirements
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m10206"))),
                 lambda state: can_complete_quest(state, "m10210", world.player))
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m10207"))),
                 lambda state: can_complete_quest(state, "m10211", world.player))
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m10209"))),
                 lambda state: can_complete_quest(state, "m10213", world.player))
        # needs access to Yian Kut-Ku, unlock req is 10 Kut-Ku killed
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m10304"))),
                 lambda state: can_hunt_all_monsters(state, world.quest_info, ["Yian Kut-Ku"], world.player, "m10304"))
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m10308"))),
                 lambda state: can_complete_quest(state, "m10307", world.player))
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m10309"))),
                 lambda state: can_complete_quest(state, "m10313", world.player))
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m10318"))),
                 lambda state: can_complete_quest(state, "m10317", world.player))
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m10407"))),
                 lambda state: can_complete_quest(state, "m10406", world.player))
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m10409"))),
                 lambda state: can_complete_quest(state, "m10411", world.player))
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m10414"))),
                 lambda state: can_complete_quest(state, "m10413", world.player))
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m10416"))),
                 lambda state: can_complete_quest(state, "m10415", world.player))
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m10505"))),
                 lambda state: can_complete_quest(state, "m10506", world.player))
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m10511"))),
                 lambda state: can_complete_quest(state, "m10509", world.player))  # 6* Urgent, effectively postgame.
        # bit of a hack for this one, it needs all village low quests completed,
        # but we can just check the only quests with actual requirements
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m10510"))),
                 lambda state: can_complete_all_quests(state, ["m10206", "m10207", "m10209", "m10304", "m10308",
                                                               "m10309", "m10318", "m10407", "m10409", "m10414",
                                                               "m10416", "m10505", "m10511"], world.player))
        if world.options.village_depth.value > VillageQuestDepth.option_low_rank:
            # Village High
            # m11005 has a requirement...that will always be met because it's village 6* urgent
            for quest in ("m11116", "m11117", "m11118"):
                add_rule(world.get_location(get_proper_name(get_quest_by_id(quest))),
                         lambda state: can_complete_quest(state, "m11005", world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m11119"))),
                     lambda state: can_complete_all_quests(state, ["m11116", "m11117", "m11118"], world.player))
            for quest in ("m11211", "m11212"):
                add_rule(world.get_location(get_proper_name(get_quest_by_id(quest))),
                         lambda state: can_hunt_any_monster(state, world.quest_info,
                                                            [*list(piscene_wyverns.keys()),
                                                             *list(flying_wyverns.keys()),
                                                             *list(bird_wyverns.keys())], world.player, quest))
                # needs access to any Bird/Flying/Piscine that aren't a drome
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m11213"))),
                     lambda state: can_complete_all_quests(state, ["m11211", "m11212"], world.player))
            for quest in ("m11220", "m11221", "m11222", "m11223"):
                # needs all of the village high quests
                add_rule(world.get_location(get_proper_name(get_quest_by_id(quest))),
                         lambda state: can_complete_all_quests(state, ["m11119", "m11213"], world.player))
            # Monster Hunter needs all village low and high
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m11226"))),
                     lambda state: can_complete_all_quests(state, ["m10510", "m11119", "m11213"], world.player))
        if world.options.treasure_quests:
            for qtype in ("Silver Crown", "Gold Crown"):
                for quest in ("m04002", "m04003"):
                    add_rule(world.get_location(f"{get_proper_name(get_quest_by_id(quest))} - {qtype}"),
                             lambda state: can_complete_quest(state, "m10104", world.player))
                for quest in ("m04004", "m04005"):
                    add_rule(world.get_location(f"{get_proper_name(get_quest_by_id(quest))} - {qtype}"),
                             lambda state: can_complete_quest(state, "m10203", world.player))
                add_rule(world.get_location(f"{get_proper_name(get_quest_by_id('m04006'))} - {qtype}"),
                         lambda state: can_complete_quest(state, "m10302", world.player))
    # Guild
    if world.options.guild_depth:
        # Guild Low
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m01009"))),
                 lambda state: can_complete_quest(state, "m01020", world.player))
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m01106"))),
                 lambda state: can_complete_quest(state, "m01105", world.player))
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m01112"))),
                 lambda state: can_complete_quest(state, "m01109", world.player))
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m01114"))),
                 lambda state: can_complete_quest(state, "m01116", world.player))
        add_rule(world.get_location(get_proper_name(get_quest_by_id("m01124"))),
                 lambda state: can_complete_all_quests(state, ["m01009", "m01106", "m01112", "m01114"], world.player))
        if world.options.guild_depth > GuildQuestDepth.option_low_rank:
            if world.options.village_depth == VillageQuestDepth.option_high_rank:
                # only cross-hub requirements
                # we "patch" out the requirement if village depth is lower than high
                add_rule(world.get_location(get_proper_name(get_quest_by_id("m02124"))),
                         lambda state: can_complete_quest(state, "m11005", world.player))
                add_rule(world.get_location(get_proper_name(get_quest_by_id("m02228"))),
                         lambda state: can_complete_quest(state, "m11201", world.player))
                add_rule(world.get_location(get_proper_name(get_quest_by_id("m02229"))),
                         lambda state: can_complete_quest(state, "m11201", world.player))

            for quest in ("m02214", "m02215"):
                add_rule(world.get_location(get_proper_name(get_quest_by_id(quest))),
                         lambda state: can_hunt_any_monster(state, world.quest_info,
                                                            [*list(piscene_wyverns.keys()),
                                                             *list(flying_wyverns.keys()),
                                                             *list(bird_wyverns.keys())], world.player, quest))
            for quest in ("m02217", "m02218", "m02219", "m02220", "m02221", "m02222"):
                add_rule(world.get_location(get_proper_name(get_quest_by_id(quest))),
                         lambda state: can_complete_all_quests(state, ["m02214", "m02215", "m02124", "m02228",
                                                                       "m02229"], world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m01124"))),
                     lambda state: can_complete_all_quests(state, ["m01009", "m01106", "m01112", "m01114"],
                                                           world.player))
            # special case here, this is actually the end of HR urgents. We can effectively duplicate the rules for it
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m02225"))),
                     lambda state: state.has("Key Quest", world.player, world.rank_requirements[0, 2, 2]))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m02226"))),
                     lambda state: can_complete_quest(state, "m02225", world.player))

            if world.options.guild_depth.value == GuildQuestDepth.option_g_rank:
                # Lao, needs all G1/G2. Just wanna push it back a sphere
                add_rule(world.get_location(get_proper_name(get_quest_by_id("m03127"))),
                         lambda state: can_complete_quest(state, "m03109", world.player))
                for quest in ("m03222", "m03223", "m03224", "m03225", "m03226", "m03227"):
                    add_rule(world.get_location(get_proper_name(get_quest_by_id(quest))),
                             lambda state: can_complete_quest(state, "m03127", world.player))
                if world.options.treasure_quests:
                    for qtype in ("Silver Crown", "Gold Crown"):
                        add_rule(world.get_location(f"{get_proper_name(get_quest_by_id('m04007'))} - {qtype}"),
                                 lambda state: can_complete_quest(state, "m03009", world.player))

    if world.options.training_quests:
        if world.options.village_depth:
            # pain and a half lmao
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m21001"))),
                     lambda state: can_complete_quest(state, "m10110", world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m21002"))),
                     lambda state: can_complete_quest(state, "m10111", world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m21003"))),
                     lambda state: can_complete_quest(state, "m10203", world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m21004"))),
                     lambda state: can_complete_quest(state, "m10210", world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m21005"))),
                     lambda state: can_complete_quest(state, "m10302", world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m21006"))),
                     lambda state: can_complete_quest(state, "m10304", world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m21007"))),
                     lambda state: can_complete_quest(state, "m10401", world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m21008"))),
                     lambda state: can_complete_quest(state, "m10406", world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m21009"))),
                     lambda state: can_complete_quest(state, "m10411", world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m21010"))),
                     lambda state: can_complete_quest(state, "m10402", world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m21011"))),
                     lambda state: can_hunt_all_monsters(state, world.quest_info, ["Cephadrome"],
                                                         world.player, "m21011")
                     and can_complete_all_quests(state, ["m21001", "m21002"], world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m21012"))),
                     lambda state: can_hunt_all_monsters(state, world.quest_info, ["Plesioth"], world.player, "m21012")
                     and can_complete_all_quests(state, ["m21003", "m21004"], world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m21013"))),
                     lambda state: can_hunt_all_monsters(state, world.quest_info, ["Blangonga"], world.player, "m21013")
                     and can_complete_all_quests(state, ["m21005", "m21006"], world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m21014"))),
                     lambda state: can_hunt_all_monsters(state, world.quest_info, ["Rathalos"], world.player, "m21014")
                     and can_complete_all_quests(state, ["m21007", "m21008"], world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m21015"))),
                     lambda state: can_hunt_all_monsters(state, world.quest_info, ["Rajang"], world.player, "m21015")
                     and can_complete_all_quests(state, ["m21009", "m21010"], world.player))

        if world.options.guild_depth.value > GuildQuestDepth.option_low_rank:
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m22002"))),
                     lambda state: can_hunt_all_monsters(state, world.quest_info, ["Cephadrome"],
                                                         world.player, "m22002")
                     and can_complete_quest(state, "m01015", world.player))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m22003"))),
                     lambda state: can_hunt_all_monsters(state, world.quest_info, ["Rathian"], world.player, "m22003")
                     and can_complete_quest(state, "m01209", world.player))
            # This is apparently available by default, no idea on the confirmation
            # add_rule(world.get_location(get_proper_name(get_quest_by_id("m22004"))),
            #         lambda state: can_hunt_all_monsters(state, world.quest_info, ["Congalala"],
            #                                             world.player, "m22004"))
            add_rule(world.get_location(get_proper_name(get_quest_by_id("m22005"))),
                     lambda state: can_hunt_all_monsters(state, world.quest_info, ["Shogun Ceanataur"],
                                                         world.player, "m22005")
                     and can_complete_quest(state, "m02117", world.player))

            if world.options.guild_depth.value == GuildQuestDepth.option_g_rank:
                add_rule(world.get_location(get_proper_name(get_quest_by_id("m22006"))),
                         lambda state: can_hunt_all_monsters(state, world.quest_info, ["Tigrex"],
                                                             world.player, "m22006")
                         and can_complete_quest(state, "m03202", world.player))

                add_rule(world.get_location(get_proper_name(get_quest_by_id("m21016"))),
                         lambda state: can_complete_quest(state, "m03009", world.player))
                add_rule(world.get_location(get_proper_name(get_quest_by_id("m21017"))),
                         lambda state: can_complete_quest(state, "m03020", world.player))
                add_rule(world.get_location(get_proper_name(get_quest_by_id("m21018"))),
                         lambda state: can_complete_quest(state, "m03012", world.player))
                add_rule(world.get_location(get_proper_name(get_quest_by_id("m21019"))),
                         lambda state: can_complete_quest(state, "m03103", world.player))
                add_rule(world.get_location(get_proper_name(get_quest_by_id("m21020"))),
                         lambda state: can_complete_quest(state, "m03120", world.player))
                add_rule(world.get_location(get_proper_name(get_quest_by_id("m21021"))),
                         lambda state: can_complete_quest(state, "m03106", world.player))
                add_rule(world.get_location(get_proper_name(get_quest_by_id("m21022"))),
                         lambda state: can_complete_quest(state, "m03110", world.player))
                add_rule(world.get_location(get_proper_name(get_quest_by_id("m21023"))),
                         lambda state: can_complete_quest(state, "m03212", world.player))
