from BaseClasses import Region, Location, ItemClassification
from typing import Optional, NamedTuple, Dict, Tuple, Callable, TYPE_CHECKING
from .names import locations, regions, items
from .items import DMC5Item
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import DMC5World


class DMC5Region(Region):
    game = "Devil May Cry 5"


class DMC5Location(Location):
    game = "Devil May Cry 5"
    cost: Optional[int] = None

    def __init__(self, player: int, name: str, address: Optional[int], parent: Optional[Region]):
        super().__init__(player, name, address, parent)
        self.cost = None


class LocationData(NamedTuple):
    code: Optional[int]
    vergil: bool = False
    shop: bool = False
    event_item: Optional[str] = None


class RegionData(NamedTuple):
    locations: Dict[str, LocationData]
    required_item: Optional[str] = None,
    vergil: Optional[bool] = None


chapter_regions: Dict[str, RegionData] = {
    regions.prologue: RegionData({
        locations.prologue: LocationData(1),
        locations.prologuev: LocationData(24, True),
    }, locations.prologue),
    regions.chapter1: RegionData({
        locations.chapter1: LocationData(2),
        locations.chapter1v: LocationData(25, True),
    }, locations.chapter1),
    regions.chapter2: RegionData({
        locations.chapter2: LocationData(3),
        locations.chapter2v: LocationData(26, True),
    }, locations.chapter2),
    regions.chapter3: RegionData({
        locations.chapter3: LocationData(4),
        locations.chapter3v: LocationData(27, True),
    }, locations.chapter3),
    regions.chapter4: RegionData({
        locations.chapter4: LocationData(5),
        locations.chapter4v: LocationData(28, True),
    }, locations.chapter4),
    regions.chapter5: RegionData({
        locations.chapter5: LocationData(6),
        locations.chapter5v: LocationData(29, True),
    }, locations.chapter5),
    regions.chapter6: RegionData({
        locations.chapter6: LocationData(7),
        locations.chapter6v: LocationData(30, True),
    }, locations.chapter6),
    regions.chapter7: RegionData({
        locations.chapter7n: LocationData(8),
        locations.chapter7g: LocationData(9),
        locations.chapter7v: LocationData(31, True),
    }, items.chapter7),
    regions.chapter8: RegionData({
        locations.chapter8: LocationData(10),
        locations.chapter8v: LocationData(32, True),
    }, locations.chapter8),
    regions.chapter9: RegionData({
        locations.chapter9: LocationData(11),
        locations.chapter9v: LocationData(33, True),
    }, locations.chapter9),
    regions.chapter10: RegionData({
        locations.chapter10: LocationData(12),
        locations.chapter10v: LocationData(34, True),
    }, locations.chapter10),
    regions.chapter11: RegionData({
        locations.chapter11: LocationData(13),
        locations.chapter11v: LocationData(35, True),
    }, locations.chapter11),
    regions.chapter12: RegionData({
        locations.chapter12: LocationData(14),
        locations.chapter12v: LocationData(36, True),
    }, locations.chapter12),
    regions.chapter13: RegionData({
        locations.chapter13n: LocationData(15),
        locations.chapter13g: LocationData(16),
        locations.chapter13d: LocationData(17),
        locations.chapter13v: LocationData(37, True),
    }, items.chapter13),
    regions.chapter14: RegionData({
        locations.chapter14: LocationData(18),
        locations.chapter14v: LocationData(38, True),
    }, locations.chapter14),
    regions.chapter15: RegionData({
        locations.chapter15: LocationData(19),
        locations.chapter15v: LocationData(39, True),
    }, locations.chapter15),
    regions.chapter16: RegionData({
        locations.chapter16: LocationData(20),
        locations.chapter16v: LocationData(40, True),
    }, locations.chapter16),
    regions.chapter17: RegionData({
        locations.chapter17: LocationData(21),
        locations.chapter17v: LocationData(41, True),
    }, locations.chapter17),
    regions.chapter18: RegionData({
        locations.chapter18: LocationData(22),
        locations.chapter18v: LocationData(42, True),
    }, locations.chapter18),
    regions.chapter19: RegionData({
        locations.chapter19: LocationData(23),
    }, locations.chapter19, False),
    regions.chapter19v: RegionData({
        locations.chapter19v: LocationData(None, True, False, "Victory against Dante"),
    }, None, True),
    regions.chapter20: RegionData({
        locations.chapter20: LocationData(None, False, False, "Victory against Vergil"),
    }, None, False),
}

shop_regions = {

}

all_regions: Dict[str, RegionData] = {
    **chapter_regions,
    **shop_regions
}

all_locations: Dict[str, LocationData] = {loc_name: location for region_name, region in all_regions.items()
                                          for loc_name, location in region.locations.items()}

location_lookup: Dict[str, int] = {loc_name: location.code
                                   for loc_name, location in all_locations.items() if location.code}


def create_regions(world: "DMC5World"):
    menu = DMC5Region("Menu", world.player, world.multiworld)
    my_regions = [menu]
    for name, region in chapter_regions.items():
        if region.vergil is True and True:  # world.options.mode in [GameMode.option_classic, GameMode.option_all]
            continue
        elif region.vergil is False and False:  # world.options.mode in [GameMode.option_vergil, GameMode.option_all]
            continue
        new_region = DMC5Region(name, world.player, world.multiworld)
        new_region.add_locations({loc_name: loc.code for loc_name, loc in region.locations.items()
                                  if not loc.vergil and True  # world.options.mode in [GameMode.option_classic, GameMode.option_all]
                                  or loc.vergil and False  # world.options.mode in [GameMode.option_vergil, GameMode.option_all]
                                  }, DMC5Location)
        for location in new_region.locations:
            if region.locations[location.name].event_item:
                location.place_locked_item(DMC5Item(region.locations[location.name].event_item,
                                                    ItemClassification.progression, None, world.player))

        entrance = menu.connect(new_region)
        if region.required_item:
            set_rule(entrance, lambda state, item=region.required_item: state.has(item, world.player))
        my_regions.append(new_region)

    world.multiworld.regions.extend(my_regions)
