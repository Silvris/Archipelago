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
        names.block_man_c1: LocationData(0x1001, energy=True),
        names.block_man_c2: LocationData(0x1002, energy=True),
        names.block_man_c3: LocationData(0x1003, energy=True),
        names.block_man_c4: LocationData(0x1004, energy=True),
        names.block_man_c5: LocationData(0x1005, energy=True),
        names.block_man_c6: LocationData(0x1006, energy=True),
        names.block_man_c7: LocationData(0x1007, energy=True),
        names.block_man_c8: LocationData(0x1008, energy=True),
        names.block_man_c9: LocationData(0x1009, oneup_tank=True),
        names.block_man_c10: LocationData(0x100A, oneup_tank=True),
        names.block_man_c11: LocationData(0x100B, energy=True),
        names.block_man_c12: LocationData(0x100C, energy=True),
    }, [names.block_man_stage], []),

    "Acid Man Stage": RegionData({
        names.acid_man: LocationData(0x0002),
        names.get_acid_barrier: LocationData(0x0102),
        names.acid_man_c1: LocationData(0x2001, energy=True),
        names.acid_man_c2: LocationData(0x2002, energy=True),
        names.acid_man_c3: LocationData(0x2003, energy=True),
        names.acid_man_c4: LocationData(0x2004, energy=True),
        names.acid_man_c5: LocationData(0x2005, energy=True),
        names.acid_man_c6: LocationData(0x2006, oneup_tank=True),
        names.acid_man_c7: LocationData(0x2007, energy=True),
        names.acid_man_c8: LocationData(0x2008, energy=True),
        names.acid_man_c9: LocationData(0x2009, energy=True),
        names.acid_man_c10: LocationData(0x200A, energy=True),
        names.acid_man_c11: LocationData(0x200B, energy=True),
        names.acid_man_c12: LocationData(0x200C, energy=True),
        names.acid_man_c13: LocationData(0x200D, energy=True),
        names.acid_man_c14: LocationData(0x200E, energy=True),
        names.acid_man_c15: LocationData(0x200F, energy=True),
    }, [names.acid_man_stage], []),

    "Impact Man Stage": RegionData({
        names.impact_man: LocationData(0x0003),
        names.get_pile_driver: LocationData(0x0103),
        names.impact_man_c1: LocationData(0x3001, energy=True),
        names.impact_man_c2: LocationData(0x3002, energy=True),
        names.impact_man_c3: LocationData(0x3003, energy=True),
        names.impact_man_c4: LocationData(0x3004, energy=True),
        names.impact_man_c5: LocationData(0x3005, energy=True),
        names.impact_man_c6: LocationData(0x3006, energy=True),
        names.impact_man_c7: LocationData(0x3007, energy=True),
        names.impact_man_c8: LocationData(0x3008, energy=True),
        names.impact_man_c9: LocationData(0x3009, energy=True),
        names.impact_man_c10: LocationData(0x300A, energy=True),
        names.impact_man_c11: LocationData(0x300B, energy=True),
        names.impact_man_c12: LocationData(0x300C, energy=True),
        names.impact_man_c13: LocationData(0x300D, energy=True),
        names.impact_man_c14: LocationData(0x300E, energy=True),
        names.impact_man_c15: LocationData(0x300F, energy=True),
        names.impact_man_c16: LocationData(0x3010, energy=True),
        names.impact_man_c17: LocationData(0x3011, energy=True),
        names.impact_man_c18: LocationData(0x3012, energy=True),
        names.impact_man_c19: LocationData(0x3013, energy=True),
        names.impact_man_c20: LocationData(0x3014, oneup_tank=True),
        names.impact_man_c21: LocationData(0x3015, energy=True),
        names.impact_man_c22: LocationData(0x3016, energy=True),
    }, [names.impact_man_stage], []),

    "Bounce Man Stage": RegionData({
        names.bounce_man: LocationData(0x0004),
        names.get_bounce_ball: LocationData(0x0104),
        names.bounce_man_c1: LocationData(0x4001, oneup_tank=True),
        names.bounce_man_c2: LocationData(0x4002, energy=True),
        names.bounce_man_c3: LocationData(0x4003, energy=True),
        names.bounce_man_c4: LocationData(0x4004, energy=True),
        names.bounce_man_c5: LocationData(0x4005, energy=True),
        names.bounce_man_c6: LocationData(0x4006, energy=True),
        names.bounce_man_c7: LocationData(0x4007, energy=True),
        names.bounce_man_c8: LocationData(0x4008, energy=True),
        names.bounce_man_c9: LocationData(0x4009, energy=True),
        names.bounce_man_c10: LocationData(0x400A, energy=True),
        names.bounce_man_c11: LocationData(0x400B, oneup_tank=True),
        names.bounce_man_c12: LocationData(0x400C, energy=True),
        names.bounce_man_c13: LocationData(0x400D, energy=True),
        names.bounce_man_c14: LocationData(0x400E, oneup_tank=True),
        names.bounce_man_c15: LocationData(0x400F, energy=True),
    }, [names.bounce_man_stage], []),

    "Fuse Man Stage": RegionData({
        names.fuse_man: LocationData(0x0005),
        names.get_scramble_thunder: LocationData(0x0105),
        names.fuse_man_c1: LocationData(0x5001, energy=True),
        names.fuse_man_c2: LocationData(0x5002, energy=True),
        names.fuse_man_c3: LocationData(0x5003, energy=True),
        names.fuse_man_c4: LocationData(0x5004, energy=True),
        names.fuse_man_c5: LocationData(0x5005, energy=True),
        names.fuse_man_c6: LocationData(0x5006, energy=True),
        names.fuse_man_c7: LocationData(0x5007, energy=True),
        names.fuse_man_c8: LocationData(0x5008, energy=True),
        names.fuse_man_c9: LocationData(0x5009, oneup_tank=True),
        names.fuse_man_c10: LocationData(0x500A, energy=True),
    }, [names.fuse_man_stage], []),

    "Tundra Man Stage": RegionData({
        names.tundra_man: LocationData(0x0006),
        names.get_tundra_storm: LocationData(0x0106),
        names.tundra_man_c1: LocationData(0x6001, energy=True),
        names.tundra_man_c2: LocationData(0x6002, oneup_tank=True),
        names.tundra_man_c3: LocationData(0x6003, energy=True),
        names.tundra_man_c4: LocationData(0x6004, energy=True),
        names.tundra_man_c5: LocationData(0x6005, energy=True),
        names.tundra_man_c6: LocationData(0x6006, energy=True),
        names.tundra_man_c7: LocationData(0x6007, energy=True),
        names.tundra_man_c8: LocationData(0x6008, energy=True),
        names.tundra_man_c9: LocationData(0x6009, energy=True),
        names.tundra_man_c10: LocationData(0x600A, energy=True),
        names.tundra_man_c11: LocationData(0x600B, energy=True),
        names.tundra_man_c12: LocationData(0x600C, energy=True),
        names.tundra_man_c13: LocationData(0x600D, energy=True),
        names.tundra_man_c14: LocationData(0x600E, energy=True),
        names.tundra_man_c15: LocationData(0x600F, energy=True),
        names.tundra_man_c16: LocationData(0x6010, energy=True),
        names.tundra_man_c17: LocationData(0x6011, oneup_tank=True),
        names.tundra_man_c18: LocationData(0x6012, energy=True),
        names.tundra_man_c19: LocationData(0x6013, energy=True),
        names.tundra_man_c20: LocationData(0x6014, energy=True),
        names.tundra_man_c21: LocationData(0x6015, energy=True),
        names.tundra_man_c22: LocationData(0x6016, energy=True),
        names.tundra_man_c23: LocationData(0x6017, energy=True),
        names.tundra_man_c24: LocationData(0x6018, oneup_tank=True),
        names.tundra_man_c25: LocationData(0x6019, oneup_tank=True),
    }, [names.tundra_man_stage], []),

    "Torch Man Stage": RegionData({
        names.torch_man: LocationData(0x0007),
        names.get_blazing_torch: LocationData(0x0107),
        names.torch_man_c1: LocationData(0x7001, energy=True),
        names.torch_man_c2: LocationData(0x7002, energy=True),
        names.torch_man_c3: LocationData(0x7003, energy=True),
        names.torch_man_c4: LocationData(0x7004, energy=True),
        names.torch_man_c5: LocationData(0x7005, energy=True),
        names.torch_man_c6: LocationData(0x7006, energy=True),
        names.torch_man_c7: LocationData(0x7007, energy=True),
        names.torch_man_c8: LocationData(0x7008, energy=True),
        names.torch_man_c9: LocationData(0x7009, oneup_tank=True),
        names.torch_man_c10: LocationData(0x700A, energy=True),
        names.torch_man_c11: LocationData(0x700B, oneup_tank=True),
        names.torch_man_c12: LocationData(0x700C, energy=True),
        names.torch_man_c13: LocationData(0x700D, energy=True),
        names.torch_man_c14: LocationData(0x700E, energy=True),
        names.torch_man_c15: LocationData(0x700F, oneup_tank=True),
        names.torch_man_c16: LocationData(0x7010, energy=True),
        names.torch_man_c17: LocationData(0x7011, energy=True),
        names.torch_man_c18: LocationData(0x7012, energy=True),
        names.torch_man_c19: LocationData(0x7013, energy=True),
        names.torch_man_c20: LocationData(0x7014, energy=True),
    }, [names.torch_man_stage], []),

    "Blast Man Stage": RegionData({
        names.blast_man: LocationData(0x0008),
        names.get_chain_blast: LocationData(0x0108),
        names.blast_man_c1: LocationData(0x8001, energy=True),
        names.blast_man_c2: LocationData(0x8002, oneup_tank=True),
        names.blast_man_c3: LocationData(0x8003, energy=True),
        names.blast_man_c4: LocationData(0x8004, energy=True),
        names.blast_man_c5: LocationData(0x8005, energy=True),
        names.blast_man_c6: LocationData(0x8006, energy=True),
        names.blast_man_c7: LocationData(0x8007, energy=True),
        names.blast_man_c8: LocationData(0x8008, oneup_tank=True),
        names.blast_man_c9: LocationData(0x8009, energy=True),
        names.blast_man_c10: LocationData(0x800A, energy=True),
        names.blast_man_c11: LocationData(0x800B, energy=True),
        names.blast_man_c12: LocationData(0x800C, energy=True),
        names.blast_man_c13: LocationData(0x800D, oneup_tank=True),
        names.blast_man_c14: LocationData(0x800E, energy=True),
        names.blast_man_c15: LocationData(0x800F, energy=True),
        names.blast_man_c16: LocationData(0x8010, energy=True),
        names.blast_man_c17: LocationData(0x8011, energy=True),
        names.blast_man_c18: LocationData(0x8012, oneup_tank=True),
    }, [names.blast_man_stage], []),

    "Wily Stage 1": RegionData({
        names.wily_1_boss: LocationData(0x0009),
        names.wily_1_c1: LocationData(0x9001, energy=True),
        names.wily_1_c2: LocationData(0x9002, energy=True),
        names.wily_1_c3: LocationData(0x9003, energy=True),
        names.wily_1_c4: LocationData(0x9004, energy=True),
        names.wily_1_c5: LocationData(0x9005, oneup_tank=True),
        names.wily_1_c6: LocationData(0x9006, energy=True),
        names.wily_1_c7: LocationData(0x9007, energy=True),
        names.wily_1_c8: LocationData(0x9008, energy=True),
        names.wily_1_c9: LocationData(0x9009, energy=True),
    }, [], [names.block_man, names.acid_man,
            names.impact_man, names.bounce_man,
            names.fuse_man, names.tundra_man,
            names.torch_man, names.blast_man,]),

    "Wily Stage 2": RegionData({
        names.wily_2_boss: LocationData(0x000A),
        names.wily_2_c1: LocationData(0xA001, energy=True),
        names.wily_2_c2: LocationData(0xA002, energy=True),
        names.wily_2_c3: LocationData(0xA003, energy=True),
        names.wily_2_c4: LocationData(0xA004, energy=True),
        names.wily_2_c5: LocationData(0xA005, oneup_tank=True),
        names.wily_2_c6: LocationData(0xA006, energy=True),
        names.wily_2_c7: LocationData(0xA007, energy=True),
        names.wily_2_c8: LocationData(0xA008, energy=True),
        names.wily_2_c9: LocationData(0xA009, energy=True),
        names.wily_2_c10: LocationData(0xA00A, energy=True),
        names.wily_2_c11: LocationData(0xA00B, energy=True),
        names.wily_2_c12: LocationData(0xA00C, energy=True),
        names.wily_2_c13: LocationData(0xA00D, energy=True),


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
        names.wily_3_c1: LocationData(0xB001, energy=True),
    }, [], [names.wily_2_boss], parent="Wily Stage 2"),

    "Wily Stage 4": RegionData({
        names.wily_4_boss: LocationData(None),
        names.wily_4_c1: LocationData(0xC001, energy=True),
        names.wily_4_c2: LocationData(0xC002, energy=True),
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
