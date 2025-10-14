import typing
from BaseClasses import Location
from .names import LocationName


class K64Location(Location):
    game: str = "Kirby 64 - The Crystal Shards"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address


stage_locations = {
    0x0001: LocationName.pop_star_1,
    0x0002: LocationName.pop_star_2,
    0x0003: LocationName.pop_star_3,
    0x0004: LocationName.rock_star_1,
    0x0005: LocationName.rock_star_2,
    0x0006: LocationName.rock_star_3,
    0x0007: LocationName.rock_star_4,
    0x0008: LocationName.aqua_star_1,
    0x0009: LocationName.aqua_star_2,
    0x000A: LocationName.aqua_star_3,
    0x000B: LocationName.aqua_star_4,
    0x000C: LocationName.neo_star_1,
    0x000D: LocationName.neo_star_2,
    0x000E: LocationName.neo_star_3,
    0x000F: LocationName.neo_star_4,
    0x0010: LocationName.shiver_star_1,
    0x0011: LocationName.shiver_star_2,
    0x0012: LocationName.shiver_star_3,
    0x0013: LocationName.shiver_star_4,
    0x0014: LocationName.ripple_star_1,
    0x0015: LocationName.ripple_star_2,
    0x0016: LocationName.ripple_star_3,
}

crystal_shard_locations = {
    0x0101: LocationName.pop_star_1_s1,
    0x0102: LocationName.pop_star_1_s2,
    0x0103: LocationName.pop_star_1_s3,
    0x0104: LocationName.pop_star_2_s1,
    0x0105: LocationName.pop_star_2_s2,
    0x0106: LocationName.pop_star_2_s3,
    0x0107: LocationName.pop_star_3_s1,
    0x0108: LocationName.pop_star_3_s2,
    0x0109: LocationName.pop_star_3_s3,
    0x010A: LocationName.rock_star_1_s1,
    0x010B: LocationName.rock_star_1_s2,
    0x010C: LocationName.rock_star_1_s3,
    0x010D: LocationName.rock_star_2_s1,
    0x010E: LocationName.rock_star_2_s2,
    0x010F: LocationName.rock_star_2_s3,
    0x0110: LocationName.rock_star_3_s1,
    0x0111: LocationName.rock_star_3_s2,
    0x0112: LocationName.rock_star_3_s3,
    0x0113: LocationName.rock_star_4_s1,
    0x0114: LocationName.rock_star_4_s2,
    0x0115: LocationName.rock_star_4_s3,
    0x0116: LocationName.aqua_star_1_s1,
    0x0117: LocationName.aqua_star_1_s2,
    0x0118: LocationName.aqua_star_1_s3,
    0x0119: LocationName.aqua_star_2_s1,
    0x011A: LocationName.aqua_star_2_s2,
    0x011B: LocationName.aqua_star_2_s3,
    0x011C: LocationName.aqua_star_3_s1,
    0x011D: LocationName.aqua_star_3_s2,
    0x011E: LocationName.aqua_star_3_s3,
    0x011F: LocationName.aqua_star_4_s1,
    0x0120: LocationName.aqua_star_4_s2,
    0x0121: LocationName.aqua_star_4_s3,
    0x0122: LocationName.neo_star_1_s1,
    0x0123: LocationName.neo_star_1_s2,
    0x0124: LocationName.neo_star_1_s3,
    0x0125: LocationName.neo_star_2_s1,
    0x0126: LocationName.neo_star_2_s2,
    0x0127: LocationName.neo_star_2_s3,
    0x0128: LocationName.neo_star_3_s1,
    0x0129: LocationName.neo_star_3_s2,
    0x012A: LocationName.neo_star_3_s3,
    0x012B: LocationName.neo_star_4_s1,
    0x012C: LocationName.neo_star_4_s2,
    0x012D: LocationName.neo_star_4_s3,
    0x012E: LocationName.shiver_star_1_s1,
    0x012F: LocationName.shiver_star_1_s2,
    0x0130: LocationName.shiver_star_1_s3,
    0x0131: LocationName.shiver_star_2_s1,
    0x0132: LocationName.shiver_star_2_s2,
    0x0133: LocationName.shiver_star_2_s3,
    0x0134: LocationName.shiver_star_3_s1,
    0x0135: LocationName.shiver_star_3_s2,
    0x0136: LocationName.shiver_star_3_s3,
    0x0137: LocationName.shiver_star_4_s1,
    0x0138: LocationName.shiver_star_4_s2,
    0x0139: LocationName.shiver_star_4_s3,
    0x013A: LocationName.ripple_star_1_s1,
    0x013B: LocationName.ripple_star_1_s2,
    0x013C: LocationName.ripple_star_1_s3,
    0x013D: LocationName.ripple_star_2_s1,
    0x013E: LocationName.ripple_star_2_s2,
    0x013F: LocationName.ripple_star_2_s3,
    0x0140: LocationName.ripple_star_3_s1,
    0x0141: LocationName.ripple_star_3_s2,
    0x0142: LocationName.ripple_star_3_s3,
}

boss_locations = {
    0x0200: LocationName.pop_star_boss,
    0x0201: LocationName.rock_star_boss,
    0x0202: LocationName.aqua_star_boss,
    0x0203: LocationName.neo_star_boss,
    0x0204: LocationName.shiver_star_boss,
    0x0205: LocationName.ripple_star_boss,
}

location_table = {
    **stage_locations,
    **crystal_shard_locations,
    **boss_locations,
}
