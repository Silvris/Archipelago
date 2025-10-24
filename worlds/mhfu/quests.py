import typing
import pkgutil
import orjson

from collections import defaultdict
from BaseClasses import Location, Region, CollectionState
from .data.monster_habitats import monster_habitats
from .data.monsters import bird_wyverns, flying_wyverns, piscene_wyverns, monster_ids
from .options import VillageQuestDepth, GuildQuestDepth

if typing.TYPE_CHECKING:
    from . import MHFUWorld
    from .rules import MHFULogicMixin

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


class QuestInfo(typing.TypedDict):
    qid: str
    name: str
    hub: int
    rank: int
    star: int
    idx: int
    flag: int
    mask: int
    stage: int
    monsters: list[int]
    max_mon: int


class SlotQuestInfo(typing.TypedDict):
    monsters: list[int]
    mon_num: int
    targets: list[int]


def get_proper_name(info: QuestInfo) -> str:
    base_name = info["name"]
    hub = hubs[info["hub"]]
    rank = ranks[info["rank"] + (1 if hub != "Guild" else 0)]
    star = hub_rank_start[(info["hub"], info["rank"])] + info["star"] + 1
    if info["rank"] != 4 and info["hub"] != 2:
        return f"({hub} {rank} {star}*) {base_name}"
    else:
        return f"({hub} {rank}) {base_name}"


def get_star_name(hub: int, rank: int, star: int) -> str:
    return f"{hubs[hub]} {ranks[rank]} {hub_rank_start[(hub, rank)] + star + 1}"


def get_location_ids():
    # filter out treasure
    location_names = {get_proper_name(info): base_id + idx for idx, info in enumerate(quest_data)
                      if (info["hub"], info["rank"]) != (0, 4)}

    # now handle manually
    next_id = max(location_names.values()) + 1
    for quest_idx, treasure in enumerate([quest for quest in quest_data if quest["hub"] == 0 and quest["rank"] == 4]):
        quest_name = get_proper_name(treasure)
        location_names[f"{quest_name} - Silver Crown"] = next_id + (quest_idx * 2)
        location_names[f"{quest_name} - Gold Crown"] = next_id + (quest_idx * 2) + 1

    return location_names


quest_data: list[QuestInfo] = \
    orjson.loads(pkgutil.get_data(__name__, "data/quests.json"))

base_id = 24700000
location_name_to_id = get_location_ids()


def get_quest_by_id(idx: str) -> QuestInfo:
    return next((quest for quest in quest_data if quest["qid"] == idx))


def get_area_quests(valid_ranks: typing.Iterable[tuple[int, int, int]], areas: tuple[int]) -> list[QuestInfo]:
    return [quest for quest in quest_data if ((quest["hub"], quest["rank"], quest["star"]) in valid_ranks and
                                              quest["stage"] in areas)]


def mhfu_sweep_monsters(state: "CollectionState | MHFULogicMixin", player: int):
    world: "MHFUWorld" = state.multiworld.worlds[player]
    # it should now be safe to check can_reach, for the most part
    world_locations = {location.name for location in world.get_locations()}
    monsters = set()
    for quest in quest_data:
        proper_name = get_proper_name(quest)
        if proper_name in world_locations:
            location = world.get_location(proper_name)
            if location.can_reach(state):
                quest_mons = world.quest_info[quest["qid"][1:]].get("monsters", [])
                monsters.update(quest_mons)
    state.mhfu_monsters[player] = monsters


class MHFULocation(Location):
    game = "Monster Hunter Freedom Unite"

    def can_reach(self, state: "CollectionState | MHFULogicMixin") -> bool:
        if state.mhfu_stale[self.player]:
            state.mhfu_stale[self.player] = False
            mhfu_sweep_monsters(state, self.player)
        return super().can_reach(state)


class MHFURegion(Region):
    game = "Monster Hunter Freedom Unite"


def create_ranks(world: "MHFUWorld") -> None:
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
        valid_quests = [quest for quest in quest_data if quest["hub"] == hub
                        and quest["rank"] == rank and quest["star"] == star]
        world.location_num[hub, rank, star] = len(valid_quests)
        region = MHFURegion(get_star_name(hub, rank, star),
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
            world.location_num[hub, rank, star] = len(valid_quests)
            region.add_locations({get_proper_name(quest): location_name_to_id[get_proper_name(quest)]
                                  for quest in valid_quests}, MHFULocation)
        else:
            region.add_locations({get_proper_name(quest): location_name_to_id[get_proper_name(quest)]
                                  for quest in valid_quests}, MHFULocation)
        if world.options.quest_randomization:
            required_mons: set[str] = set()
            if world.options.village_depth:
                required_mons.add("Yian Kut-Ku")
                if world.options.training_quests:
                    required_mons.update(["Cephadrome", "Blangonga", "Rathalos", "Rajang", "Plesioth"])
            elif world.options.guild_depth:
                # don't have to check for a bird if village depth
                # cause kut-ku is valid
                random_mon = world.random.choice(sorted({*flying_wyverns.keys(),
                                                         *bird_wyverns.keys(),
                                                         *piscene_wyverns.keys()}.difference(["Velocidrome", "Gendrome",
                                                                                              "Giadrome", "Iodrome"])))
                required_mons.add(random_mon)
            if world.options.training_quests:
                if world.options.guild_depth >= GuildQuestDepth.option_high_rank:
                    required_mons.update({"Rathian", "Shogun Ceanataur", "Cephadrome"})
                    if world.options.guild_depth == GuildQuestDepth.option_g_rank:
                        required_mons.add("Tigrex")

            for i, quest in enumerate(valid_quests):
                quest_info: SlotQuestInfo = {
                    "monsters": world.random.choices(monster_habitats[quest["stage"]],
                                                     k=len(quest["monsters"])) if quest["monsters"] else [],
                    "mon_num": world.random.choice(range(1, len(quest["monsters"]) + 1)) if quest["monsters"] else 0,
                    "targets": []
                }
                if quest_info["monsters"] and required_mons and world.random.random() > 0.5:
                    # this isn't guaranteed but it should make it so everything isn't piled up at the start
                    # failing a 50/50 400+ is nigh impossible
                    quest_info["monsters"][0] = monster_ids[world.random.choice(sorted(required_mons))]
                if quest["qid"] == "m10501":
                    # Special case: this quest crashes if the first monster isn't a Rathalos
                    if 11 in quest_info["monsters"] or 49 in quest_info["monsters"]:
                        quest_info["monsters"].sort(key=lambda x: x in (11, 49), reverse=True)
                    else:
                        quest_info["monsters"][0] = world.random.choice([11, 49])
                if quest_info["mon_num"]:
                    quest_info["targets"] = world.random.choices(quest_info["monsters"], k=quest_info["mon_num"])

                required_mons.difference_update(quest_info["monsters"])

                world.quest_info[quest["qid"][1:]] = quest_info
        else:
            # only need monsters for the resulting quest info
            world.quest_info.update({quest["qid"][1:]: {"monsters": quest["monsters"],
                                                        "mon_num": len(quest["monsters"]),
                                                        "targets": []}
                                     for quest in valid_quests})
        world.multiworld.regions.append(region)
    for hub, rank, star in world.rank_requirements:
        region = world.get_region(get_star_name(hub, rank, star))
        if star != hub_rank_max[(hub, rank)] - 1:
            region.add_exits({get_star_name(hub, rank, star + 1): f"To {get_star_name(hub, rank, star + 1)}"})
        if star == 0:
            menu_region.connect(region, f"To {region.name}")
    goal_quest = goal_quests[world.options.goal.value]
    goal_name = get_proper_name(get_quest_by_id(goal_quest))
    goal_location = world.get_location(goal_name)
    goal_location.address = None  # This lets us keep the id reserved, even though it's an event this playthrough
    goal_location.place_locked_item(world.create_item("Victory"))
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
