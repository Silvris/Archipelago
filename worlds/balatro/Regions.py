from BaseClasses import Region, Location
from .Items import base_id
import typing
if typing.TYPE_CHECKING:
    from . import BalatroWorld

shop_locations = {f"Shop Location {i}": base_id + i for i in range(1, 150)}
antes = []
for i in range(1, 9):
    antes += [f"Ante {i} Small Blind", f"Ante {i} Big Blind", f"Ante {i} Boss"]
ante_locations = dict(zip(antes, range(base_id + 150, base_id + 150 + len(antes))))


class BalatroRegion(Region):
    game = "Balatro"


class BalatroLocation(Location):
    game = "Balatro"


def create_regions(world: "BalatroWorld"):
    menu = BalatroRegion("Menu", world.player, world.multiworld)

    shop = BalatroRegion("Shop", world.player, world.multiworld)

    regions = [menu, shop]

    # Create shop mainly for now, we'll need to come up with more interesting logic later
    shop.add_locations(shop_locations)
    menu.connect(shop)
    previous_ante: typing.Optional[BalatroRegion] = None
    for i in range(1, 9):
        ante = BalatroRegion(f"Ante {i}", world.player, world.multiworld)
        regions.append(ante)
        if previous_ante:
            previous_ante.connect(ante)
        else:
            menu.connect(ante)
        ante.add_locations({f"Ante {i} Small Blind": ante_locations[f"Ante {i} Small Blind"],
                            f"Ante {i} Big Blind": ante_locations[f"Ante {i} Big Blind"],
                            f"Ante {i} Boss": ante_locations[f"Ante {i} Boss"] if i != 8 and True else None})
        # TODO: alternative goals?

    world.multiworld.regions += regions

location_table = {
    **shop_locations,
    **ante_locations,
}
