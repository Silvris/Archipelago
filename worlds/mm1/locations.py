from BaseClasses import Location, Region, CollectionState
from typing import NamedTuple, Callable


class MM1Region(Region):
    game = "Mega Man"


class MM1Location(Location):
    game = "Mega Man"


class LocationData(NamedTuple):
    location_id: int | None
    consumable: bool = False


class RegionData(NamedTuple):
    name: str
    locations: dict[str, LocationData]
    required_items: list[str]
    parent: str = ""


mm1_regions: list[RegionData] = [
    RegionData("Cut Man Stage", {
        "Cut Man - Defeated": LocationData(0x1),
        "Rolling Cutter - Received": LocationData(0x11),
        "Cut Man Stage - Health Energy 1": LocationData(0x101, True),
    }, ["Cut Man Access Codes"]),
    RegionData("Ice Man Stage", {
        "Ice Man - Defeated": LocationData(0x2),
        "Ice Slasher - Received": LocationData(0x12),
        "Ice Man Stage - Health Energy 1": LocationData(0x102, True),
        "Ice Man Stage - Weapon Energy 1": LocationData(0x103, True),
        "Ice Man Stage - 1-Up": LocationData(0x104, True),
        "Ice Man Stage - Health Energy 2": LocationData(0x105, True),
        "Ice Man Stage - Health Energy 3": LocationData(0x106, True),
        "Ice Man Stage - Health Energy 4": LocationData(0x107, True),
        "Ice Man Stage - Weapon Energy 2": LocationData(0x108, True),
        "Ice Man Stage - Weapon Energy 3": LocationData(0x109, True),
        "Ice Man Stage - Weapon Energy 4": LocationData(0x10A, True),
    }, ["Ice Man Access Codes"]),
    RegionData("Bomb Man Stage", {
        "Bomb Man - Defeated": LocationData(0x3),
        "Hyper Bomb - Received": LocationData(0x13),
        "Bomb Man Stage - Health Energy 1": LocationData(0x10B, True),
        "Bomb Man Stage - Health Energy 2": LocationData(0x10C, True),
        "Bomb Man Stage - Weapon Energy 1": LocationData(0x10D, True),
        "Bomb Man Stage - Health Energy 3": LocationData(0x10E, True),
        "Bomb Man Stage - 1-Up": LocationData(0x10F, True),
    }, ["Bomb Man Access Codes"]),
    RegionData("Fire Man Stage", {
        "Fire Man - Defeated": LocationData(0x4),
        "Fire Storm - Received": LocationData(0x14),
        "Fire Man Stage - Health Energy 1": LocationData(0x110, True),
        "Fire Man Stage - Health Energy 2": LocationData(0x111, True),
        "Fire Man Stage - Health Energy 3": LocationData(0x112, True),
        "Fire Man Stage - Weapon Energy 1": LocationData(0x113, True),
        "Fire Man Stage - Weapon Energy 2": LocationData(0x114, True),
        "Fire Man Stage - Health Energy 4": LocationData(0x115, True),
        "Fire Man Stage - Health Energy 5": LocationData(0x116, True),
        "Fire Man Stage - Health Energy 6": LocationData(0x117, True),
        "Fire Man Stage - Weapon Energy 3": LocationData(0x118, True),
    }, ["Fire Man Access Codes"]),
    RegionData("Elec Man Stage", {
        "Elec Man - Defeated": LocationData(0x5),
        "Elec Beam - Received": LocationData(0x15),
        "Elec Man Stage - Magnet Beam": LocationData(0x17),
        "Elec Man Stage - Health Energy 1": LocationData(0x119, True),
        "Elec Man Stage - Weapon Energy 1": LocationData(0x11A, True),
        "Elec Man Stage - Weapon Energy 2": LocationData(0x11B, True),
        "Elec Man Stage - Weapon Energy 3": LocationData(0x11C, True),
        "Elec Man Stage - Health Energy 2": LocationData(0x11D, True),
    }, ["Elec Man Access Codes"]),
    RegionData("Guts Man Stage", {
        "Guts Man - Defeated": LocationData(0x6),
        "Super Arm - Received": LocationData(0x16),
        "Guts Man Stage - Health Energy 1": LocationData(0x11E, True),
        "Guts Man Stage - Health Energy 2": LocationData(0x11F, True),
        "Guts Man Stage - Health Energy 3": LocationData(0x120, True),
        "Guts Man Stage - Weapon Energy 1": LocationData(0x121, True),
        "Guts Man Stage - Health Energy 4": LocationData(0x122, True),
        "Guts Man Stage - 1-Up": LocationData(0x123, True),
        "Guts Man Stage - Health Energy 5": LocationData(0x124, True),

    }, ["Guts Man Access Codes"]),
    RegionData("Wily Stage 1", {
        "Yellow Devil - Defeated": LocationData(0x7),
        "Wily Stage 1 - Complete": LocationData(None),
        "Wily Stage 1 - Health Energy 1": LocationData(0x125, True),
        "Wily Stage 1 - Health Energy 2": LocationData(0x126, True),
        "Wily Stage 1 - Weapon Energy 1": LocationData(0x127, True),
        "Wily Stage 1 - Weapon Energy 2": LocationData(0x128, True),
    }, []),
    RegionData("Wily Stage 2", {
        "Wily Stage 2 - Cut Man Rematch": LocationData(0x8),
        "Wily Stage 2 - Elec Man Rematch": LocationData(0x9),
        "Copy Robot - Defeated": LocationData(0xA),
        "Wily Stage 2 - Complete": LocationData(None),
        "Wily Stage 2 - Health Energy 1": LocationData(0x129, True),
        "Wily Stage 2 - Weapon Energy 1": LocationData(0x12A, True),
        "Wily Stage 2 - Weapon Energy 2": LocationData(0x12B, True),
        "Wily Stage 2 - Health Energy 2": LocationData(0x12C, True),
        "Wily Stage 2 - Weapon Energy 3": LocationData(0x12D, True),
        "Wily Stage 2 - Weapon Energy 4": LocationData(0x12E, True),
        "Wily Stage 2 - Weapon Energy 5": LocationData(0x12F, True),
        "Wily Stage 2 - Weapon Energy 6": LocationData(0x130, True),
        "Wily Stage 2 - 1-Up": LocationData(0x131, True),
        "Wily Stage 2 - Weapon Energy 7": LocationData(0x132, True),
    }, ["Wily Stage 1 - Complete"], "Wily Stage 1"),
    RegionData("Wily Stage 3", {
        "CWU-01P - Defeated": LocationData(0xB),
        "Wily Stage 3 - Complete": LocationData(None),
    }, ["Wily Stage 2 - Complete"], "Wily Stage 2"),
    RegionData("Wily Stage 4", {
        "Wily Stage 4 - Bomb Man Rematch": LocationData(0xC),
        "Wily Stage 4 - Fire Man Rematch": LocationData(0xD),
        "Wily Stage 4 - Ice Man Rematch": LocationData(0xE),
        "Wily Stage 4 - Guts Man Rematch": LocationData(0xF),
        "Wily Machine - Defeated": LocationData(None),
        "Wily Stage 4 - Weapon Energy 1": LocationData(0x133, True),
        "Wily Stage 4 - 1-Up": LocationData(0x134, True),
        "Wily Stage 4 - Yashichi": LocationData(0x135, True),
        "Wily Stage 4 - Weapon Energy 2": LocationData(0x136, True),
    }, ["Wily Stage 3 - Complete"], "Wily Stage 3")
]

all_locations: dict[str, LocationData] = {key: value for region in mm1_regions
                                          for key, value in region.locations.items()}

location_lookup: dict[str, int] = {name: data.location_id for name, data in all_locations.items() if data.location_id}
