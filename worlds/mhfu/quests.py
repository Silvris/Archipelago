import typing
import pkgutil
import orjson
import os

from collections import defaultdict
from BaseClasses import Location, Region
from .data.monster_habitats import monster_habitats
from .options import VillageQuestDepth, GuildQuestDepth

if typing.TYPE_CHECKING:
    from . import MHFUWorld

hubs = {
    0: "Guild",
    1: "Village",
    2: "Training"
}
ranks = {
    0: "Unrank",
    1: "Low",
    2: "High",
    3: "G",
    4: "Treasure"
}
hub_rank_start = {
    (0, 0): 0,
    (0, 1): 2,
    (0, 2): 5,
    (0, 3): 0,
    (0, 4): 0,
    (1, 0): 0,
    (1, 1): 6,
    (2, 0): 0,
    (2, 1): 0,
    (2, 2): 0,
}
hub_max = {
    0: 5,
    1: 2,
    2: 3
}
hub_rank_max = {
    (0, 0): 2,
    (0, 1): 3,
    (0, 2): 3,
    (0, 3): 3,
    (0, 4): 1,
    (1, 0): 6,
    (1, 1): 3,
    (2, 0): 1,
    (2, 1): 1,
    (2, 2): 1,
}
goal_quests = {
    0: "m10509",
    1: "m11225",
    2: "m11226",
    3: "m01218",
    4: "m02226",
    5: "m03233",
    6: "m03230",
    7: "m03231",
    8: "m03232"
}
goal_ranks = {
    0: (1, 0, 5),
    1: (1, 1, 2),
    2: (1, 1, 2),
    3: (0, 1, 2),
    4: (0, 2, 2),
    5: (0, 3, 2),
    6: (0, 3, 2),
    7: (0, 3, 2),
    8: (0, 3, 2),
}

rank_sort = defaultdict(lambda: 99, {
    (0, 0, 0): 0,
    (0, 0, 1): 1,
    (0, 0, 2): 2,
    (0, 1, 0): 3,
    (1, 0, 0): 4,
    (1, 0, 1): 5,
    (0, 1, 1): 6,
    (1, 0, 2): 7,
    (1, 0, 3): 8,
    (1, 0, 4): 9,
    (1, 0, 5): 10,
    (0, 1, 2): 11,
    (1, 1, 0): 12,
    (0, 2, 0): 13,
    (1, 1, 1): 14,
    (0, 2, 1): 15,
    (1, 1, 2): 16,
    (0, 2, 2): 17,
    (0, 3, 0): 18,
    (0, 3, 1): 19,
    (0, 3, 2): 20,
})


class MHFULocation(Location):
    game: str = "Monster Hunter Freedom Unite"


def get_proper_name(info):
    base_name = info["name"]
    hub = hubs[int(info["hub"])]
    rank = ranks[int(info["rank"]) + (1 if hub != "Guild" else 0)]
    star = hub_rank_start[(int(info["hub"]), int(info["rank"]))] + int(info["star"]) + 1
    if int(info["rank"]) != 4 and int(info["hub"]) != 2:
        return f"({hub} {rank} {star}*) {base_name}"
    else:
        return f"({hub} {rank}) {base_name}"


def get_star_name(hub, rank, star):
    return f"{hubs[hub]} {ranks[rank]} {hub_rank_start[(hub, rank)] + star + 1}"


quest_data: typing.List[typing.Dict[str, str]] = \
    orjson.loads(pkgutil.get_data(__name__, os.path.join("data", "quests.json")))

base_id = 24700000

# filter out treasure and training
location_name_to_id = {get_proper_name(info): base_id + id for id, info in enumerate(quest_data)
                       if (info["hub"], info["rank"]) != ("0", "4")}

# now handle manually
next_id = max(location_name_to_id.values()) + 1
for i, treasure in enumerate([quest for quest in quest_data if quest["hub"] == "0" and quest["rank"] == "4"]):
    quest_name = get_proper_name(treasure)
    location_name_to_id[f"{quest_name} - Silver Crown"] = next_id + (i * 2)
    location_name_to_id[f"{quest_name} - Gold Crown"] = next_id + (i * 2) + 1


def get_quest_by_id(idx: str) -> dict[str, str] | None:
    return next((quest for quest in quest_data if quest["qid"] == idx), None)


def get_area_quests(ranks: typing.Iterable[tuple[int, int, int]], areas: tuple[int]) -> list[dict[str, typing.Any]]:
    return [quest for quest in quest_data if (int(quest["hub"]), int(quest["rank"]), int(quest["star"]) in ranks and
                                              int(quest["stage"]) in areas)]


def create_ranks(world: "MHFUWorld"):
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)
    # we only write 0 into rank requirements, since we need to know how many quests we have access to
    # we properly fill them in create_items, then apply in set_rules
    if world.options.guild_depth:
        # if any guild depth, we write low rank
        for i in range(hub_rank_max[0, 0]):
            world.rank_requirements[0, 0, i] = 0
        for i in range(hub_rank_max[0, 1]):
            world.rank_requirements[0, 1, i] = 0
        if world.options.guild_depth.value > 1:
            # write high rank
            for i in range(hub_rank_max[0, 2]):
                world.rank_requirements[0, 2, i] = 0
            if world.options.guild_depth.value == 3:
                # write g rank
                for i in range(hub_rank_max[0, 3]):
                    world.rank_requirements[0, 3, i] = 0
    # check treasure quests
    if world.options.treasure_quests:
        world.rank_requirements[0, 4, 0] = 0
    if world.options.village_depth:
        # if any village depth, we write low rank
        for i in range(hub_rank_max[1, 0]):
            world.rank_requirements[1, 0, i] = 0
        if world.options.village_depth == VillageQuestDepth.option_high_rank:
            for i in range(hub_rank_max[1, 1]):
                world.rank_requirements[1, 1, i] = 0
    if world.options.training_quests:
        for i in range(3 if world.options.guild_depth.value == GuildQuestDepth.option_g_rank else 2):
            world.rank_requirements[2, i, 0] = 0
    for hub, rank, star in world.rank_requirements:
        valid_quests = [quest for quest in quest_data if int(quest["hub"]) == hub
                        and int(quest["rank"]) == rank and int(quest["star"]) == star]
        world.location_num[hub, rank, star] = len(valid_quests)
        region = Region(get_star_name(hub, rank, star),
                        world.player, world.multiworld)
        if (hub, rank, star) == (0, 4, 0):
            # treasure quests are a little weird
            # 1 is default, 5 are LR Village, 1 is G
            if not world.options.village_depth:
                valid_quests = [quest for quest in valid_quests if quest["qid"] in ("m04001", "m04007")]
            if world.options.guild_depth.value != GuildQuestDepth.option_g_rank:
                valid_quests = [quest for quest in valid_quests if quest["qid"] != "m04007"]
            world.location_num[hub, rank, star] = len(valid_quests) * 2
            region.add_locations({f"{get_proper_name(quest)} - {qtype}":
                                  location_name_to_id[f"{get_proper_name(quest)} - {qtype}"]
                                  for quest in valid_quests for qtype in ("Silver Crown", "Gold Crown")}, MHFULocation)
        elif (hub, rank, star) == (2, 1, 0):
            # Solo/Group Training has some special casing
            # namely, guild required
            if not world.options.guild_depth:
                valid_quests = [quest for quest in valid_quests if quest["qid"] not in ("m22002", "m22003", "m22004",
                                                                                        "m22005", "m22006")]
            elif world.options.guild_depth == GuildQuestDepth.option_low_rank:
                valid_quests = [quest for quest in valid_quests if quest["qid"] not in ("m22005", "m22006")]
            elif world.options.guild_depth == GuildQuestDepth.option_high_rank:
                valid_quests = [quest for quest in valid_quests if quest["qid"] != "m22006"]
            region.add_locations({get_proper_name(quest): location_name_to_id[get_proper_name(quest)]
                                  for quest in valid_quests}, MHFULocation)
        else:
            region.add_locations({get_proper_name(quest): location_name_to_id[get_proper_name(quest)]
                                  for quest in valid_quests}, MHFULocation)
        if world.options.quest_randomization:
            for quest in valid_quests:
                quest_info = {
                    "monsters": world.random.choices(monster_habitats[quest["stage"]],
                                                     k=len(quest["monsters"])) if quest["monsters"] else [],
                    "mon_num": world.random.choice(range(1, len(quest["monsters"]) + 1)) if quest["monsters"] else 0
                }
                if quest["qid"] == "m10501":
                    # Special case: this quest crashes if the first monster isn't a Rathalos
                    if 11 in quest_info["monsters"] or 49 in quest_info["monsters"]:
                        quest_info["monsters"].sort(key=lambda x: x in (11, 49), reverse=True)
                    else:
                        quest_info["monsters"][0] = world.random.choice([11, 49])
                if quest_info["mon_num"]:
                    quest_info["targets"] = world.random.choices(quest_info["monsters"], k=quest_info["mon_num"])

                world.quest_info[quest["qid"][1:]] = quest_info
        else:
            # only need monsters for the resulting quest info
            world.quest_info.update({quest["qid"][1:]: {"monsters": quest["monsters"]}
                                     for quest in valid_quests})
        world.multiworld.regions.append(region)
    for hub, rank, star in world.rank_requirements:
        region = world.multiworld.get_region(get_star_name(hub, rank, star), world.player)
        if star != hub_rank_max[(hub, rank)] - 1:
            region.add_exits({get_star_name(hub, rank, star + 1): f"To {get_star_name(hub, rank, star + 1)}"})
        if star == 0:
            menu_region.connect(region, f"To {region.name}")
