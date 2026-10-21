from BaseClasses import Location, Region
from typing import NamedTuple
from . import names


class MM11Location(Location):
    game = "Mega Man 11"


class MM11Region(Region):
    game = "Mega Man 11"


class LocationData(NamedTuple):
    location_id: int | None
    energy: bool = False
    oneup_tank: bool = False


class RegionData(NamedTuple):
    locations: dict[str, LocationData]
    required_items: list[str]
    required_locations: list[str]
    parent: str = ""


mm11_regions: dict[str, RegionData] = {
    "Block Man Stage": RegionData({
        names.block_man: LocationData(0x0001),
        names.get_block_dropper: LocationData(0x0101),
    }, [names.block_man_stage], []),

    "Acid Man Stage": RegionData({
        names.acid_man: LocationData(0x0002),
        names.get_acid_barrier: LocationData(0x0102),
    }, [names.acid_man_stage], []),

    "Impact Man Stage": RegionData({
        names.impact_man: LocationData(0x0003),
        names.get_pile_driver: LocationData(0x0103),
    }, [names.impact_man_stage], []),

    "Bounce Man Stage": RegionData({
        names.bounce_man: LocationData(0x0004),
        names.get_bounce_ball: LocationData(0x0104),
    }, [names.bounce_man_stage], []),

    "Fuse Man Stage": RegionData({
        names.fuse_man: LocationData(0x0005),
        names.get_scramble_thunder: LocationData(0x0105),
    }, [names.fuse_man_stage], []),

    "Tundra Man Stage": RegionData({
        names.tundra_man: LocationData(0x0006),
        names.get_tundra_storm: LocationData(0x0106),
    }, [names.tundra_man_stage], []),

    "Torch Man Stage": RegionData({
        names.torch_man: LocationData(0x0007),
        names.get_blazing_torch: LocationData(0x0107),
    }, [names.torch_man_stage], []),

    "Blast Man Stage": RegionData({
        names.blast_man: LocationData(0x0008),
        names.get_chain_blast: LocationData(0x0108),
    }, [names.blast_man_stage], []),

    "Wily Stage 1": RegionData({
        names.wily_1_boss: LocationData(0x0009),
    }, [], [names.block_man, names.acid_man,
            names.impact_man, names.bounce_man,
            names.fuse_man, names.tundra_man,
            names.torch_man, names.blast_man,]),

    "Wily Stage 2": RegionData({
        names.wily_2_boss: LocationData(0x000A),

    }, [], [names.wily_1_boss], parent="Wily Stage 1"),

    "Wily Stage 3": RegionData({
        names.wily_3_b1: LocationData(0x000B),
        names.wily_3_b2: LocationData(0x000C),
        names.wily_3_b3: LocationData(0x000D),
        names.wily_3_b4: LocationData(0x000E),
        names.wily_3_b5: LocationData(0x000F),
        names.wily_3_b6: LocationData(0x0010),
        names.wily_3_b7: LocationData(0x0011),
        names.wily_3_b8: LocationData(0x0012),
    }, [], [names.wily_2_boss], parent="Wily Stage 2"),

    "Wily Stage 4": RegionData({
        names.wily_4_boss: LocationData(None),
    }, [], [], parent="Wily Stage 3"),

    "Dr. Light's Lab": RegionData({
        names.shop_energy_balancer: LocationData(0x0020),
        names.shop_energy_balancer_neo: LocationData(0x0021),
        names.shop_auto_charge: LocationData(0x0022),
        names.shop_buster_plus: LocationData(0x0023),
        names.shop_power_shield: LocationData(0x0024),
        names.shop_spike_boots: LocationData(0x0025),
        names.shop_shock_absorber: LocationData(0x0026),
        names.shop_speed_gear_booster: LocationData(0x0027),
        names.shop_energy_dispenser: LocationData(0x0028),
        names.shop_awakener: LocationData(0x0029),
        names.shop_screws_up: LocationData(0x002A),
        names.shop_health_up: LocationData(0x002B),
        names.shop_weapon_up: LocationData(0x002C),
        names.shop_cooling_fan: LocationData(0x002D),
        names.shop_cooling_infinite: LocationData(0x002E),
        names.shop_mystery: LocationData(0x002F),
        names.shop_buddy_plus: LocationData(0x0030),
        names.shop_tank_container: LocationData(0x0031),
    }, [], [])
}


def get_boss_locations(region: str) -> list[str]:
    return [location for location, data in mm11_regions[region].locations.items()
            if not data.energy and not data.oneup_tank]


def get_energy_locations(region: str) -> list[str]:
    return [location for location, data in mm11_regions[region].locations.items() if data.energy]


def get_oneup_locations(region: str) -> list[str]:
    return [location for location, data in mm11_regions[region].locations.items() if data.oneup_tank]


location_table: dict[str, int | None] = {
    location: data.location_id for region in mm11_regions.values() for location, data in region.locations.items()
}


location_groups = {
    "Get Equipped": {
        names.get_block_dropper,
        names.get_acid_barrier,
        names.get_pile_driver,
        names.get_bounce_ball,
        names.get_scramble_thunder,
        names.get_tundra_storm,
        names.get_blazing_torch,
        names.get_chain_blast,
        names.get_rush_jet,
    },
    **{name: {location for location, data in region.locations.items() if data.location_id} for name, region in mm11_regions.items()
       if name != "Wily Stage 4"}
}

lookup_location_to_id: dict[str, int] = {location: idx for location, idx in location_table.items() if idx is not None}
