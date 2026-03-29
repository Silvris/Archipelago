from .quests import get_quest_by_id, get_star_name, goal_quests, hub_rank_max, get_area_quests
from .data.monsters import flying_wyverns, piscene_wyverns, bird_wyverns, monster_ids
from .options import VillageQuestDepth, GuildQuestDepth
from BaseClasses import Collection
from typing import TYPE_CHECKING, Iterable
from rule_builder.rules import CanReachLocation, Rule, True_, False_, Has, HasAny, HasAll, CanReachRegion

if TYPE_CHECKING:
    from . import MHFUWorld


def can_complete_quest(qid: str) -> Rule:
    return CanReachLocation(get_quest_by_id(qid).proper_name)


def can_complete_any_quest(qids: list[str]) -> Rule:
    rule = False_()
    for qid in qids:
        rule |= can_complete_quest(qid)
    return rule


def can_complete_all_quests(qids: list[str]) -> Rule:
    rule = True_()
    for qid in qids:
        rule &= can_complete_quest(qid)
    return rule


def can_reach_area(areas: Iterable[int],
                   rank_requirements: Iterable[tuple[int, int, int]]) -> Rule:
    # this can be very slow
    possible_quests = get_area_quests(rank_requirements, areas)
    return can_complete_any_quest([quest.qid for quest in possible_quests])


def can_hunt_any_monster(monsters: list[str]) -> Rule:
    return HasAny(*monsters)


def can_hunt_all_monsters(monsters: list[str]) -> Rule:
    return HasAll(*monsters)


def can_reach_rank(hub: int, rank: int, star: int) -> Rule:
    return CanReachRegion(get_star_name(hub, rank, star))


def set_rules(world: "MHFUWorld") -> None:
    for hub, rank, star in world.rank_requirements:
        if (hub, rank, star + 1) in world.rank_requirements:
            world.set_rule(world.get_entrance(f"To {get_star_name(hub, rank, star + 1)}"),
                           Has("Key Quest", count=world.rank_requirements[hub, rank, star]))
        elif star + 1 == hub_rank_max[hub, rank] and (hub, rank + 1, 0) in world.rank_requirements \
                and (hub, rank) != (0, 3):
            world.set_rule(world.get_entrance(f"To {get_star_name(hub, rank + 1, 0)}"),
                           Has("Key Quest", count=world.rank_requirements[hub, rank, star]))

    # now additional requirements
    # Village
    if world.options.village_depth:
        # Village Low
        # some basic quest requirements
        world.set_rule(world.get_location(get_quest_by_id("m10206").proper_name),
                       can_complete_quest("m10210"))
        world.set_rule(world.get_location(get_quest_by_id("m10207").proper_name),
                       can_complete_quest("m10211"))
        world.set_rule(world.get_location(get_quest_by_id("m10209").proper_name),
                       can_complete_quest("m10213"))
        # needs access to Yian Kut-Ku, unlock req is 10 Kut-Ku killed
        world.set_rule(world.get_location(get_quest_by_id("m10304").proper_name),
                       can_hunt_all_monsters(["Yian Kut-Ku"]))
        world.set_rule(world.get_location(get_quest_by_id("m10308").proper_name),
                       can_complete_quest("m10307"))
        world.set_rule(world.get_location(get_quest_by_id("m10309").proper_name),
                       can_complete_quest("m10313"))
        world.set_rule(world.get_location(get_quest_by_id("m10318").proper_name),
                       can_complete_quest("m10317"))
        world.set_rule(world.get_location(get_quest_by_id("m10407").proper_name),
                       can_complete_quest("m10406"))
        world.set_rule(world.get_location(get_quest_by_id("m10409").proper_name),
                       can_complete_quest("m10411"))
        world.set_rule(world.get_location(get_quest_by_id("m10414").proper_name),
                       can_complete_quest("m10413"))
        world.set_rule(world.get_location(get_quest_by_id("m10416").proper_name),
                       can_complete_quest("m10415"))
        world.set_rule(world.get_location(get_quest_by_id("m10505").proper_name),
                       can_complete_quest("m10506"))
        world.set_rule(world.get_location(get_quest_by_id("m10511").proper_name),
                       can_complete_quest("m10509"))  # 6* Urgent, effectively postgame.
        # bit of a hack for this one, it needs all village low quests completed,
        # but we can just check the only quests with actual requirements
        world.set_rule(world.get_location(get_quest_by_id("m10510").proper_name),
                       can_complete_all_quests(["m10206", "m10207", "m10209", "m10304", "m10308",
                                                "m10309", "m10318", "m10407", "m10409", "m10414",
                                                "m10416", "m10505", "m10511"]))
        if world.options.village_depth.value > VillageQuestDepth.option_low_rank:
            # Village High
            # m11005 has a requirement...that will always be met because it's village 6* urgent
            for quest in ("m11116", "m11117", "m11118"):
                world.set_rule(world.get_location(get_quest_by_id(quest).proper_name),
                               can_complete_quest("m11005"))
            world.set_rule(world.get_location(get_quest_by_id("m11119").proper_name),
                           can_complete_all_quests(["m11116", "m11117", "m11118"]))
            for quest in ("m11211", "m11212"):
                world.set_rule(world.get_location(get_quest_by_id(quest).proper_name),
                               can_hunt_any_monster(
                                   [*list(piscene_wyverns.keys()),
                                    *list(flying_wyverns.keys()),
                                    *list(bird_wyverns.keys())], ))
                # needs access to any Bird/Flying/Piscine that aren't a drome
            world.set_rule(world.get_location(get_quest_by_id("m11213").proper_name),
                           can_complete_all_quests(["m11211", "m11212"]))
            for quest in ("m11220", "m11221", "m11222", "m11223"):
                # needs all of the village high quests
                world.set_rule(world.get_location(get_quest_by_id(quest).proper_name),
                               can_complete_all_quests(["m11119", "m11213"]))
            # Monster Hunter needs all village low and high
            world.set_rule(world.get_location(get_quest_by_id("m11226").proper_name),
                           can_complete_all_quests(["m10510", "m11119", "m11213"]))
        if world.options.treasure_quests:
            for qtype in ("Silver Crown", "Gold Crown"):
                for quest in ("m04002", "m04003"):
                    world.set_rule(world.get_location(f"{get_quest_by_id(quest).proper_name} - {qtype}"),
                                   can_complete_quest("m10104"))
                for quest in ("m04004", "m04005"):
                    world.set_rule(world.get_location(f"{get_quest_by_id(quest).proper_name} - {qtype}"),
                                   can_complete_quest("m10203"))
                world.set_rule(world.get_location(f"{get_quest_by_id('m04006').proper_name} - {qtype}"),
                               can_complete_quest("m10302"))
    # Guild
    if world.options.guild_depth:
        # Guild Low
        world.set_rule(world.get_location(get_quest_by_id("m01009").proper_name),
                       can_complete_quest("m01020"))
        world.set_rule(world.get_location(get_quest_by_id("m01106").proper_name),
                       can_complete_quest("m01105"))
        world.set_rule(world.get_location(get_quest_by_id("m01112").proper_name),
                       can_complete_quest("m01109"))
        world.set_rule(world.get_location(get_quest_by_id("m01114").proper_name),
                       can_complete_quest("m01116"))
        world.set_rule(world.get_location(get_quest_by_id("m01124").proper_name),
                       can_complete_all_quests(["m01009", "m01106", "m01112", "m01114"], ))
        if world.options.guild_depth > GuildQuestDepth.option_low_rank:
            if world.options.village_depth == VillageQuestDepth.option_high_rank:
                # only cross-hub requirements
                # we "patch" out the requirement if village depth is lower than high
                world.set_rule(world.get_location(get_quest_by_id("m02124").proper_name),
                               can_complete_quest("m11005"))
                world.set_rule(world.get_location(get_quest_by_id("m02228").proper_name),
                               can_complete_quest("m11201"))
                world.set_rule(world.get_location(get_quest_by_id("m02229").proper_name),
                               can_complete_quest("m11201"))

            for quest in ("m02214", "m02215"):
                world.set_rule(world.get_location(get_quest_by_id(quest).proper_name),
                               can_hunt_any_monster(
                                   sorted({*flying_wyverns.keys(),
                                           *bird_wyverns.keys(),
                                           *piscene_wyverns.keys()}.difference(
                                       ["Velocidrome", "Gendrome",
                                        "Giadrome", "Iodrome"]))))
            for quest in ("m02217", "m02218", "m02219", "m02220", "m02221", "m02222"):
                world.set_rule(world.get_location(get_quest_by_id(quest).proper_name),
                               can_complete_all_quests(["m02214", "m02215", "m02124", "m02228",
                                                        "m02229"]))
            # special case here, this is actually the end of HR urgents. We can effectively duplicate the rules for it
            world.set_rule(world.get_location(get_quest_by_id("m02225").proper_name),
                           Has("Key Quest", count=world.rank_requirements[0, 2, 2]))
            world.set_rule(world.get_location(get_quest_by_id("m02226").proper_name),
                           can_complete_quest("m02225"))

            if world.options.guild_depth.value == GuildQuestDepth.option_g_rank:
                # Lao, needs all G1/G2. Just wanna push it back a sphere
                world.set_rule(world.get_location(get_quest_by_id("m03127").proper_name),
                               can_complete_quest("m03109"))
                for quest in ("m03222", "m03223", "m03224", "m03225", "m03226", "m03227"):
                    world.set_rule(world.get_location(get_quest_by_id(quest).proper_name),
                                   can_complete_quest("m03127"))
                if world.options.treasure_quests:
                    for qtype in ("Silver Crown", "Gold Crown"):
                        world.set_rule(world.get_location(f"{get_quest_by_id('m04007').proper_name} - {qtype}"),
                                       can_complete_quest("m03009"))

    # set goal requirement
    world.set_rule(world.get_location(get_quest_by_id(goal_quests[world.options.goal.value]).proper_name),
                   Has("Key Quest", count=world.required_keys))

    if world.options.training_quests:
        if world.options.village_depth:
            # pain and a half lmao
            world.set_rule(world.get_location(get_quest_by_id("m21001").proper_name),
                           can_complete_quest("m10110"))
            world.set_rule(world.get_location(get_quest_by_id("m21002").proper_name),
                           can_complete_quest("m10111"))
            world.set_rule(world.get_location(get_quest_by_id("m21003").proper_name),
                           can_complete_quest("m10203"))
            world.set_rule(world.get_location(get_quest_by_id("m21004").proper_name),
                           can_complete_quest("m10210"))
            world.set_rule(world.get_location(get_quest_by_id("m21005").proper_name),
                           can_complete_quest("m10302"))
            world.set_rule(world.get_location(get_quest_by_id("m21006").proper_name),
                           can_complete_quest("m10304"))
            world.set_rule(world.get_location(get_quest_by_id("m21007").proper_name),
                           can_complete_quest("m10401"))
            world.set_rule(world.get_location(get_quest_by_id("m21008").proper_name),
                           can_complete_quest("m10406"))
            world.set_rule(world.get_location(get_quest_by_id("m21009").proper_name),
                           can_complete_quest("m10411"))
            world.set_rule(world.get_location(get_quest_by_id("m21010").proper_name),
                           can_complete_quest("m10402"))
            world.set_rule(world.get_location(get_quest_by_id("m21011").proper_name),
                           can_hunt_all_monsters(["Cephadrome"]) & can_complete_all_quests(["m21001", "m21002"]))
            world.set_rule(world.get_location(get_quest_by_id("m21012").proper_name),
                           can_hunt_all_monsters(["Plesioth"]) & can_complete_all_quests(["m21003", "m21004"]))
            world.set_rule(world.get_location(get_quest_by_id("m21013").proper_name),
                           can_hunt_all_monsters(["Shogun Ceanataur"]) & can_complete_all_quests(["m21005", "m21006"]))
            world.set_rule(world.get_location(get_quest_by_id("m21014").proper_name),
                           can_hunt_all_monsters(["Rathalos"]) & can_complete_all_quests(["m21007", "m21008"]))
            world.set_rule(world.get_location(get_quest_by_id("m21015").proper_name),
                           can_hunt_all_monsters(["Rajang"]) & can_complete_all_quests(["m21009", "m21010"]))

        if world.options.guild_depth.value > GuildQuestDepth.option_low_rank:
            world.set_rule(world.get_location(get_quest_by_id("m22002").proper_name),
                           can_hunt_all_monsters(["Cephadrome"], ) & can_complete_quest("m01015"))
            world.set_rule(world.get_location(get_quest_by_id("m22003").proper_name),
                           can_hunt_all_monsters(["Rathian"]) & can_complete_quest("m01209"))
            # This is apparently available by default, no idea on the confirmation
            # world.set_rule(world.get_location(get_quest_by_id("m22004").proper_name),
            #         can_hunt_all_monsters( world.quest_info, ["Congalala"],
            #                                              "m22004"))
            world.set_rule(world.get_location(get_quest_by_id("m22005").proper_name),
                           can_hunt_all_monsters(["Shogun Ceanataur"]) & can_complete_quest("m02117"))

            if world.options.guild_depth.value == GuildQuestDepth.option_g_rank:
                world.set_rule(world.get_location(get_quest_by_id("m22006").proper_name),
                               can_hunt_all_monsters(["Tigrex"]) & can_complete_quest("m03202"))

                world.set_rule(world.get_location(get_quest_by_id("m21016").proper_name),
                               can_complete_quest("m03009"))
                world.set_rule(world.get_location(get_quest_by_id("m21017").proper_name),
                               can_complete_quest("m03020"))
                world.set_rule(world.get_location(get_quest_by_id("m21018").proper_name),
                               can_complete_quest("m03012"))
                world.set_rule(world.get_location(get_quest_by_id("m21019").proper_name),
                               can_complete_quest("m03103"))
                world.set_rule(world.get_location(get_quest_by_id("m21020").proper_name),
                               can_complete_quest("m03120"))
                world.set_rule(world.get_location(get_quest_by_id("m21021").proper_name),
                               can_complete_quest("m03106"))
                world.set_rule(world.get_location(get_quest_by_id("m21022").proper_name),
                               can_complete_quest("m03110"))
                world.set_rule(world.get_location(get_quest_by_id("m21023").proper_name),
                               can_complete_quest("m03212"))

    # Monster handling
    monster_access = world.get_region("Monsters")
    for location in monster_access.get_locations():
        relevant_quests = []
        for loc in world.get_locations():
            mons = getattr(loc, "monsters")
            qid = getattr(loc, "qid")
            if mons and qid:
                if monster_ids[location.name] in mons:
                    relevant_quests.append(f"m{qid:05}")
        world.set_rule(location, can_complete_any_quest(relevant_quests))
        location.quests = relevant_quests
