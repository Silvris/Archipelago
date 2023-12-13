import typing
import pkgutil
import orjson
import os

from BaseClasses import Location, Region

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


class MHFULocation(Location):
    game: str = "Monster Hunter Freedom Unite"


def get_proper_name(info):
    base_name = info["name"]
    hub = hubs[int(info["hub"])]
    rank = ranks[int(info["rank"]) + (1 if hub != "Guild" else 0)]
    star = hub_rank_start[(int(info["hub"]), int(info["rank"]))] + int(info["star"]) + 1
    if int(info["rank"]) != 4:
        return f"({hub} {rank} {star}*) {base_name}"
    else:
        return f"({hub} {rank}) {base_name}"


quest_data: typing.List[typing.Dict[str,str]] = \
    orjson.loads(pkgutil.get_data(__name__, os.path.join("data", "quests.json")))

base_id = 24700000

location_name_to_id = {get_proper_name(info): base_id + id for id, info in enumerate(quest_data)}


def create_ranks(world: "MHFUWorld"):
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)
    # TODO: write this not inverted so spoiler looks nicer
    for hub in range(3):
        for rank in range(hub_max[hub] - 1, -1, -1):
            for star in range(hub_rank_max[(hub, rank)] - 1, -1, -1):
                valid_quests = [quest for quest in quest_data if int(quest["hub"]) == hub
                                and int(quest["rank"]) == rank and int(quest["star"]) == star]
                region = Region(f"{hubs[hub]} {ranks[rank]} {hub_rank_start[(hub,rank)] + star + 1}",
                                world.player, world.multiworld)
                region.add_locations({get_proper_name(quest): location_name_to_id[get_proper_name(quest)]
                                      for quest in valid_quests})
                if star != hub_rank_max[(hub, rank)] - 1:
                    region.add_exits([f"{hubs[hub]} {ranks[rank]} {hub_rank_start[(hub,rank)] + star + 2}"],
                                     {f"{hubs[hub]} {ranks[rank]} {hub_rank_start[(hub,rank)] + star + 2}":
                                      lambda state: True})
                if star == 0:
                    menu_region.connect(region)
                world.multiworld.regions.append(region)
