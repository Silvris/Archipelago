from BaseClasses import Location, Region
from typing import NamedTuple
from . import names


class MM4Location(Location):
    game = "Mega Man 4"


class MM4Region(Region):
    game = "Mega Man 4"


class LocationData(NamedTuple):
    location_id: int | None
    energy: bool = False
    oneup_tank: bool = False


class RegionData(NamedTuple):
    locations: dict[str, LocationData]
    required_items: list[str]
    required_locations: list[str]
    parent: str = ""


mm4_regions: dict[str, RegionData] = {
    "Bright Man Stage": RegionData({
        names.bright_man: LocationData(0x0001),
        names.get_flash_stopper: LocationData(0x0101),
        names.bright_man_c1: LocationData(0x0200, energy=True),
        names.bright_man_c2: LocationData(0x0201, oneup_tank=True),
        names.bright_man_c3: LocationData(0x0202, oneup_tank=True),
        names.bright_man_c4: LocationData(0x0203, energy=True),
    }, [names.bright_man_stage], []),

    "Toad Man Stage": RegionData({
        names.toad_man: LocationData(0x0002),
        names.get_rain_flush: LocationData(0x0102),
        names.get_rush_marine: LocationData(0x0112),
    }, [names.toad_man_stage], []),

    "Drill Man Stage": RegionData({
        names.drill_man: LocationData(0x0003),
        names.get_drill_bomb: LocationData(0x0103),
        names.get_rush_jet: LocationData(0x0111),
        names.drill_man_c1: LocationData(0x0204, energy=True),
        names.drill_man_c2: LocationData(0x0205, oneup_tank=True),
        names.drill_man_c3: LocationData(0x0206, oneup_tank=True),
    }, [names.drill_man_stage], []),

    "Pharaoh Man Stage": RegionData({
        names.pharaoh_man: LocationData(0x0004),
        names.get_pharaoh_shot: LocationData(0x0104),
        names.get_balloon_adapter: LocationData(0x113),
    }, [names.pharaoh_man_stage], []),

    "Ring Man Stage": RegionData({
        names.ring_man: LocationData(0x0005),
        names.get_ring_boomerang: LocationData(0x0105),
        names.ring_man_c1: LocationData(0x0207, energy=True),
        names.ring_man_c2: LocationData(0x0208, oneup_tank=True),
    }, [names.ring_man_stage], []),

    "Dust Man Stage": RegionData({
        names.dust_man: LocationData(0x0006),
        names.get_dust_crusher: LocationData(0x0106),
        names.dust_man_c1: LocationData(0x0209, energy=True),
        names.dust_man_c2: LocationData(0x020A, oneup_tank=True),
    }, [names.dust_man_stage], []),

    "Dive Man Stage": RegionData({
        names.dive_man: LocationData(0x0007),
        names.get_dive_missile: LocationData(0x0107),
        names.get_wire_adapter: LocationData(0x0114),
        names.dive_man_c1: LocationData(0x020B, oneup_tank=True),
    }, [names.dive_man_stage], []),

    "Skull Man Stage": RegionData({
        names.skull_man: LocationData(0x0008),
        names.get_skull_barrier: LocationData(0x0108),
        names.skull_man_c1: LocationData(0x020C, energy=True),
        names.skull_man_c2: LocationData(0x020D, oneup_tank=True),
        names.skull_man_c3: LocationData(0x020E, oneup_tank=True),
        names.skull_man_c4: LocationData(0x020F, energy=True),
        names.skull_man_c5: LocationData(0x0210, oneup_tank=True),
        names.skull_man_c6: LocationData(0x0211, energy=True),
        names.skull_man_c7: LocationData(0x0212, energy=True),
        names.skull_man_c8: LocationData(0x0213, energy=True),
        names.skull_man_c9: LocationData(0x0214, energy=True),
        names.skull_man_c10: LocationData(0x0215, energy=True),
        names.skull_man_c11: LocationData(0x0216, energy=True),
    }, [names.skull_man_stage], []),

    "Dr. Cossack's Fortress 1": RegionData({
        names.cossack_1_boss: LocationData(0x0009),
        names.cossack_1_c1: LocationData(0x0217, energy=True),
        names.cossack_1_c2: LocationData(0x0218, energy=True),
        names.cossack_1_c3: LocationData(0x0219, energy=True),
    }, [names.cossack_1_stage], []),

    "Dr. Cossack's Fortress 2": RegionData({
        names.cossack_2_boss: LocationData(0x0010),
        names.cossack_2_c1: LocationData(0x021A, energy=True),
        names.cossack_2_c2: LocationData(0x021B, energy=True),
        names.cossack_2_c3: LocationData(0x021C, energy=True),
        names.cossack_2_c4: LocationData(0x021D, energy=True),
        names.cossack_2_c5: LocationData(0x021E, energy=True),
        names.cossack_2_c6: LocationData(0x021F, energy=True),
        names.cossack_2_c7: LocationData(0x0220, energy=True),
        names.cossack_2_c8: LocationData(0x0221, energy=True),
        names.cossack_2_c9: LocationData(0x0222, oneup_tank=True),
        names.cossack_2_c10: LocationData(0x0223, oneup_tank=True),
    }, [names.cossack_2_stage], []),

    "Dr. Cossack's Fortress 3": RegionData({
        names.cossack_3_boss: LocationData(0x0011),
        names.cossack_3_c1: LocationData(0x0224, energy=True),
        names.cossack_3_c2: LocationData(0x0225, energy=True),
        names.cossack_3_c3: LocationData(0x0226, energy=True),
        names.cossack_3_c4: LocationData(0x0227, oneup_tank=True),
    }, [names.cossack_3_stage], []),

    "Dr. Cossack's Fortress 4": RegionData({
        names.cossack_4_boss: LocationData(0x0012),
        names.cossack_4_c1: LocationData(0x0228, energy=True),
        names.cossack_4_c2: LocationData(0x0229, energy=True),
        names.cossack_4_c3: LocationData(0x022A, oneup_tank=True),
        names.cossack_4_c4: LocationData(0x022B, energy=True),
        names.cossack_4_c5: LocationData(0x022C, oneup_tank=True),
        names.cossack_4_c6: LocationData(0x022D, energy=True),
        names.cossack_4_c7: LocationData(0x022E, energy=True),
        names.cossack_4_c8: LocationData(0x022F, energy=True),
    }, [names.cossack_4_stage], []),

    "Wily Stage 1": RegionData({
        names.wily_1_boss: LocationData(0x0013),
        names.wily_1_c1: LocationData(0x0230, energy=True),
        names.wily_1_c2: LocationData(0x0231, energy=True),
        names.wily_1_c3: LocationData(0x0232, energy=True),
        names.wily_1_c4: LocationData(0x0233, oneup_tank=True),
    }, [], [names.cossack_1_boss, names.cossack_2_boss,
            names.cossack_3_boss, names.cossack_4_boss,]),

    "Wily Stage 2": RegionData({
        names.wily_2_boss: LocationData(0x0014),
        names.wily_2_c1: LocationData(0x0234, oneup_tank=True),
        names.wily_2_c2: LocationData(0x0235, oneup_tank=True),
    }, [], [names.wily_1_boss], parent="Wily Stage 1"),

    "Wily Stage 3": RegionData({
        names.wily_3_boss: LocationData(0x0015),
        names.wily_3_c1: LocationData(0x0236, oneup_tank=True),
        names.wily_3_c2: LocationData(0x0237, oneup_tank=True),
        names.wily_3_c3: LocationData(0x0238, energy=True),
        names.wily_3_c4: LocationData(0x0239, energy=True),
        names.wily_3_c5: LocationData(0x023A, energy=True),
        names.wily_3_c6: LocationData(0x023B, energy=True),
        names.wily_3_c7: LocationData(0x023C, energy=True),
        names.wily_3_c8: LocationData(0x023D, energy=True),
        names.wily_3_c9: LocationData(0x023E, energy=True),
        names.wily_3_c10: LocationData(0x023F, energy=True),
        names.wily_3_c11: LocationData(0x0240, energy=True),
        names.wily_3_c12: LocationData(0x0241, energy=True),
        names.wily_3_c13: LocationData(0x0242, energy=True),
    }, [], [names.wily_2_boss], parent="Wily Stage 2"),

    "Wily Stage 4": RegionData({
        names.wily_4_boss: LocationData(None),
    }, [], [names.wily_3_boss], parent="Wily Stage 3"),
}


def get_boss_locations(region: str) -> list[str]:
    return [location for location, data in mm4_regions[region].locations.items()
            if not data.energy and not data.oneup_tank]


def get_energy_locations(region: str) -> list[str]:
    return [location for location, data in mm4_regions[region].locations.items() if data.energy]


def get_oneup_locations(region: str) -> list[str]:
    return [location for location, data in mm4_regions[region].locations.items() if data.oneup_tank]


location_table: dict[str, int | None] = {
    location: data.location_id for region in mm4_regions.values() for location, data in region.locations.items()
}


location_groups = {
    "Get Equipped": {
        names.get_needle_cannon,
        names.get_magnet_missile,
        names.get_gemini_laser,
        names.get_hard_knuckle,
        names.get_top_spin,
        names.get_search_snake,
        names.get_spark_shock,
        names.get_shadow_blade,
        names.get_rush_marine,
        names.get_rush_jet,
        names.get_balloon_adapter,
        names.get_wire_adapter,
    },
    **{name: {location for location, data in region.locations.items() if data.location_id} for name, region in mm4_regions.items()}
}

lookup_location_to_id: dict[str, int] = {location: idx for location, idx in location_table.items() if idx is not None}
