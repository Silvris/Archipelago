import typing
import pkgutil
import orjson

from collections import defaultdict
from BaseClasses import Location, Region, ItemClassification
from .data.monster_habitats import monster_habitats
from .data.monsters import bird_wyverns, flying_wyverns, piscene_wyverns, monster_ids, monster_lookup
from .items import MHFUItem
from .options import VillageQuestDepth, GuildQuestDepth

if typing.TYPE_CHECKING:
    from . import MHFUWorld

hubs: dict[int, str] = {
    0: "Guild",
    1: "Village",
    2: "Training"
}
ranks: dict[int, str] = {
    0: "Unrank",
    1: "Low",
    2: "High",
    3: "G",
    4: "Treasure"
}
hub_rank_start: dict[tuple[int, int], int] = {
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
hub_max: dict[int, int] = {
    0: 5,
    1: 2,
    2: 3
}
hub_rank_max: dict[tuple[int, int], int] = {
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

goal_quests: dict[int, str] = {
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

goal_ranks: dict[int, tuple[int, int, int]] = {
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

rank_sort: typing.DefaultDict[tuple[int, int, int], int] = defaultdict(lambda: 99, {
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


class QuestInfo:
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

    def __init__(self, dct: dict[str, typing.Any]) -> None:
        for key, val in dct.items():
            setattr(self, key, val)

    @property
    def proper_name(self) -> str:
        base_name = self.name
        hub = hubs[self.hub]
        rank = ranks[self.rank + (1 if hub != "Guild" else 0)]
        star = hub_rank_start[(self.hub, self.rank)] + self.star + 1
        if self.rank != 4 and self.hub != 2:
            return f"({hub} {rank} {star}*) {base_name}"
        else:
            return f"({hub} {rank}) {base_name}"


class SlotQuestInfo(typing.TypedDict):
    monsters: list[int]
    mon_num: int
    targets: list[int]


def get_star_name(hub: int, rank: int, star: int) -> str:
    return f"{hubs[hub]} {ranks[rank + (1 if hub == 1 else 0)]} {hub_rank_start[(hub, rank)] + star + 1}"


def get_location_ids() -> dict[str, int]:
    # filter out treasure
    location_names = {info.proper_name: base_id + idx for idx, info in enumerate(quest_data)
                      if (info.hub, info.rank) != (0, 4)}

    # now handle manually
    next_id = max(location_names.values()) + 1
    for quest_idx, treasure in enumerate([quest for quest in quest_data if quest.hub == 0 and quest.rank == 4]):
        quest_name = treasure.proper_name
        location_names[f"{quest_name} - Silver Crown"] = next_id + (quest_idx * 2)
        location_names[f"{quest_name} - Gold Crown"] = next_id + (quest_idx * 2) + 1

    return location_names


quest_data: list[QuestInfo] = \
    [QuestInfo(quest) for quest in orjson.loads(pkgutil.get_data(__name__, "data/quests.json"))]

base_id = 24700000
location_name_to_id = get_location_ids()


def get_quest_by_id(idx: str) -> QuestInfo:
    return next((quest for quest in quest_data if quest.qid == idx))


def get_area_quests(valid_ranks: typing.Iterable[tuple[int, int, int]], areas: typing.Iterable[int]) -> list[QuestInfo]:
    return [quest for quest in quest_data if ((quest.hub, quest.rank, quest.star) in valid_ranks and
                                              quest.stage in areas)]


def get_quest_areas(valid_ranks: typing.Iterable[tuple[int, int, int]]) -> list[int]:
    return [quest.stage for quest in quest_data if ((quest.hub, quest.rank, quest.star) in valid_ranks)]


class MHFULocation(Location):
    game = "Monster Hunter Freedom Unite"
    monsters: list[int] | None = None
    qid: int | None = None


class MHFURegion(Region):
    game = "Monster Hunter Freedom Unite"


def create_ranks(world: "MHFUWorld") -> None:
    menu_region = MHFURegion(world.origin_region_name, world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)
    # we only write 0 into rank requirements, since we need to know how many quests we have access to
    # we properly fill them in create_items, then apply in set_rules
    required_mons: set[str] = set()
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
    if world.options.village_depth:
        required_mons.add("Yian Kut-Ku")
        if world.options.training_quests:
            required_mons.update(["Cephadrome", "Blangonga", "Rathalos", "Rajang", "Plesioth"])
    elif world.options.guild_depth:
        # don't have to check for a bird if village depth
        # cause kut-ku is valid
        # apparently can't pop on dromes
        if world.options.quest_randomization:
            areas = get_quest_areas([rank for rank in world.rank_requirements.keys() if rank[0] != 2
                                     and (rank[0], rank[1]) != (0, 4)])
            max_mons = set()
            for area in areas:
                max_mons.update([monster_lookup[mon] for mon in monster_habitats[area]])
            valid_mons = {*flying_wyverns.keys(), *bird_wyverns.keys(),
                          *piscene_wyverns.keys()}.difference(["Velocidrome", "Gendrome", "Giadrome", "Iodrome"])
            random_mon = world.random.choice(sorted(max_mons.intersection(valid_mons)))
            required_mons.add(random_mon)
        else:
            # We'll just add Rathalos in this case, he's around a lot
            required_mons.add("Rathalos")
    if world.options.training_quests:
        if world.options.guild_depth >= GuildQuestDepth.option_high_rank:
            required_mons.update({"Rathian", "Shogun Ceanataur", "Cephadrome"})
            if world.options.guild_depth == GuildQuestDepth.option_g_rank:
                required_mons.add("Tigrex")
    req_mons = {}
    for monster in sorted(required_mons):
        # perform reverse lookup for areas
        valid_areas: list[int] = [area for area, mons in monster_habitats.items() if monster_ids[monster] in mons]
        area_quests = [quest for quest in get_area_quests([rank for rank in world.rank_requirements.keys()
                                                           if rank[0] != 2
                                                           and (rank[0], rank[1]) != (0, 4)],
                                                          valid_areas) if quest.monsters]
        req_mons[world.random.choice(area_quests).qid] = monster
    for hub, rank, star in world.rank_requirements:
        valid_quests = [quest for quest in quest_data if quest.hub == hub
                        and quest.rank == rank and quest.star == star]
        world.location_num[hub, rank, star] = len(valid_quests)
        region = MHFURegion(get_star_name(hub, rank, star),
                            world.player, world.multiworld)
        if (hub, rank, star) == (0, 4, 0):
            # treasure quests are a little weird
            # 1 is default, 5 are LR Village, 1 is G
            if not world.options.village_depth:
                valid_quests = [quest for quest in valid_quests if quest.qid in ("m04001", "m04007")]
            if world.options.guild_depth.value != GuildQuestDepth.option_g_rank:
                valid_quests = [quest for quest in valid_quests if quest.qid != "m04007"]
            world.location_num[hub, rank, star] = len(valid_quests) * 2
            region.add_locations({f"{quest.proper_name} - {qtype}":
                                  location_name_to_id[f"{quest.proper_name} - {qtype}"]
                                  for quest in valid_quests for qtype in ("Silver Crown", "Gold Crown")}, MHFULocation)
        elif (hub, rank, star) == (2, 1, 0):
            # Solo/Group Training has some special casing
            # namely, guild required
            if not world.options.guild_depth:
                valid_quests = [quest for quest in valid_quests if quest.qid not in ("m22002", "m22003", "m22004",
                                                                                     "m22005", "m22006")]
            elif world.options.guild_depth == GuildQuestDepth.option_low_rank:
                valid_quests = [quest for quest in valid_quests if quest.qid not in ("m22005", "m22006")]
            elif world.options.guild_depth == GuildQuestDepth.option_high_rank:
                valid_quests = [quest for quest in valid_quests if quest.qid != "m22006"]
            world.location_num[hub, rank, star] = len(valid_quests)
            region.add_locations({quest.proper_name: location_name_to_id[quest.proper_name]
                                  for quest in valid_quests}, MHFULocation)
        else:
            region.add_locations({quest.proper_name: location_name_to_id[quest.proper_name]
                                  for quest in valid_quests}, MHFULocation)

        if world.options.quest_randomization:
            for i, quest in enumerate(valid_quests):
                quest_info: SlotQuestInfo = {
                    "monsters": world.random.choices(monster_habitats[quest.stage],
                                                     k=len(quest.monsters)) if quest.monsters else [],
                    "mon_num": world.random.choice(range(1, len(quest.monsters) + 1)) if quest.monsters else 0,
                    "targets": []
                }
                if quest_info["monsters"] and quest.qid in req_mons:
                    quest_info["monsters"][0] = monster_ids[req_mons[quest.qid]]
                if quest.qid == "m10501":
                    # Special case: this quest crashes if the first monster isn't a Rathalos
                    if 11 in quest_info["monsters"] or 49 in quest_info["monsters"]:
                        quest_info["monsters"].sort(key=lambda x: x in (11, 49), reverse=True)
                    else:
                        if quest.qid in req_mons:
                            quest_info["monsters"][1] = quest_info["monsters"][0]
                        quest_info["monsters"][0] = world.random.choice([11, 49])

                if quest_info["mon_num"]:
                    quest_info["targets"] = world.random.choices(quest_info["monsters"], k=quest_info["mon_num"])

                world.quest_info[quest.qid[1:]] = quest_info
                if quest.rank != 4:
                    loc = world.get_location(quest.proper_name)
                    assert isinstance(loc, MHFULocation)
                    loc.monsters = quest_info["monsters"].copy()
                    loc.qid = int(quest.qid[1:])
        else:
            # only need monsters for the resulting quest info
            for quest in valid_quests:

                world.quest_info[quest.qid[1:]] = {"monsters": quest.monsters,
                                                   "mon_num": len(quest.monsters),
                                                   "targets": []}
                if quest.rank != 4:
                    loc = world.get_location(quest.proper_name)
                    assert isinstance(loc, MHFULocation)
                    loc.monsters = quest.monsters.copy()
                    loc.qid = int(quest.qid[1:])

        world.multiworld.regions.append(region)
    for hub, rank, star in world.rank_requirements:
        region = world.get_region(get_star_name(hub, rank, star))
        if star != hub_rank_max[(hub, rank)] - 1:
            region.add_exits({get_star_name(hub, rank, star + 1): f"To {get_star_name(hub, rank, star + 1)}"})
        if star == 0:
            menu_region.connect(region, f"To {region.name}")
    goal_quest = goal_quests[world.options.goal.value]
    goal_name = get_quest_by_id(goal_quest).proper_name
    goal_location = world.get_location(goal_name)
    goal_location.address = None  # This lets us keep the id reserved, even though it's an event this playthrough
    goal_location.place_locked_item(world.create_item("Victory"))
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)

    monster_access = MHFURegion("Monsters", world.player, world.multiworld)
    world.multiworld.regions.append(monster_access)
    menu_region.connect(monster_access, f"Huntable")
    monster_access.add_locations({monster: None for monster in sorted(required_mons)}, MHFULocation)
    for monster in sorted(required_mons):
        world.get_location(monster).place_locked_item(MHFUItem(monster, ItemClassification.progression,
                                                               None, world.player))
