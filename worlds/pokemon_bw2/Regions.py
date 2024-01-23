import orjson
import typing
import pkgutil
import os

import Utils
from BaseClasses import Region, Location

if typing.TYPE_CHECKING:
    from . import PokemonBW2World

region_data = orjson.loads(pkgutil.get_data(__name__, os.path.join("data", "regions.json")))
BASE_OFFSET = 6490000
location_data = {}

free_fly_locations = [
    "Castelia City",
    "Nimbasa City",
    "Driftveil City",
    "Mistralton City",
    "Icirrus City",
    "Opelucid City",
    "Undella Town",
    "Lacunosa Town",
    "Humilau City",
    "Nuvema Town",
    "Striaton City",
    "Nacrene City",
]


def define_location_data():
    current_idx = 0
    for region in region_data:
        for location in region_data[region]["locations"]:
            location["name"] = f"{region} - {location['name']}"
            if "EVENT" in location["tags"]:
                idx = None
            else:
                idx = BASE_OFFSET + current_idx
            location["idx"] = idx
            location_data[location["name"]] = location
            current_idx += 1


define_location_data()


def create_regions(world: "PokemonBW2World"):
    tags = {"BADGE", "HM", "KEY", "EVENT"}  # need to always consider the logical placement of these, even if vanilla
    regions = [Region(region, world.player, world.multiworld) for region in region_data]
    menu = Region("Menu", world.player, world.multiworld)
    sky = Region("Unovan Skies", world.player, world.multiworld)
    world.multiworld.regions.extend([menu, sky, *regions])
    menu.connect(next(x for x in regions if x.name == "Aspertia City"))
    menu.connect(sky)
    if world.options.free_fly_location.value in [1, 2]:
        free_fly_location = world.random.choice(free_fly_locations)
        sky.connect(next(x for x in regions if x.name == free_fly_location),
                    rule=lambda state: state.has("HM02 Fly", world.player))
        if world.options.free_fly_location.value == 2:
            second_free_fly = world.random.choice(free_fly_locations)
            while second_free_fly == free_fly_location:
                second_free_fly = world.random.choice(free_fly_locations)
            sky.connect(next(x for x in regions if x.name == second_free_fly),
                        rule=lambda state: state.has_all(["HM02 Fly", "Town Map"], world.player))
    for region in regions:
        region.add_locations({location["name"]: location_data[location["name"]]["idx"]
                              for location in region_data[region.name]["locations"]
                              if tags.issuperset(location["tags"])})
        # all regions exist at this point, so we can just create connections here too
        region.add_exits(region_data[region.name]["connections"])
    Utils.visualize_regions(menu, "pkmnb2w2.puml")