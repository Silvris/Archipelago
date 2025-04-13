import typing

from BaseClasses import Region
from .locations import MHRSQuest, mhr_quests

if typing.TYPE_CHECKING:
    from . import MHRSWorld


class MHRSRegion(Region):
    game = "Monster Hunter Rise Sunbreak"


def create_regions(world: "MHRSWorld") -> None:
    mr = world.options.master_rank_requirement.value
    for i in range(mr, 0, -1):
        region = MHRSRegion(f"Master Rank {i}", world.player, world.multiworld)
        region.add_locations({quest: mhr_quests[quest].id
                              for quest in mhr_quests if mhr_quests[quest].region == region.name
                              and mhr_quests[quest].MR <= mr}, MHRSQuest)
        # edge case: goal
        if i == mr:
            region.add_locations({world.get_final_quest(): None}, MHRSQuest)
        else:
            region.add_exits([f"Master Rank {i + 1}"],
                             {f"Master Rank {i + 1}": lambda state, i=i: state.has(f"Master Rank {i + 1}",
                                                                                   world.player)})
        world.multiworld.regions.append(region)
    # now just create our MR1 Urgent region
    menu = MHRSRegion("Master Rank 1 Urgent", world.player, world.multiworld)
    menu.add_exits(["Master Rank 1"], {"Master Rank 1": lambda state: state.has(f"Master Rank 1", world.player)})
    menu.add_locations({quest: mhr_quests[quest].id
                        for quest in mhr_quests if mhr_quests[quest].region == "MR1 Urgent"}, MHRSQuest)
    world.multiworld.regions.append(menu)
    # while we're here, place our locked event items
    for i in range(1, mr + 1):
        world.multiworld.get_location(f"MR {i} Urgent", world.player)\
            .place_locked_item(world.create_item(f"Master Rank {i}"))
