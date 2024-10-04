from BaseClasses import Location
from .names import location_names, item_names
from .items import BASE_ID


class KSSLocation(Location):
    game = "Kirby Super Star"


green_greens_locations = {
    location_names.sb_whispy: BASE_ID + 0,
}

float_islands_locations = {
    location_names.sb_lololo: BASE_ID + 1,
}

bubbly_clouds_locations = {
    location_names.sb_kracko: BASE_ID + 2,
}

mt_dedede_locations = {
    location_names.sb_dedede: BASE_ID + 3,
    location_names.sb_complete: None,
}

spring_breeze_locations = {
    **green_greens_locations,
    **float_islands_locations,
    **bubbly_clouds_locations,
    **mt_dedede_locations,
}

peanut_plains_locations = {
    location_names.db_stage_1: BASE_ID + 4,
}

mallow_castle_locations = {
    location_names.db_stage_2: BASE_ID + 5,
    location_names.db_switch_1: BASE_ID + 9,
}

cocoa_cave_locations = {
    location_names.db_stage_3: BASE_ID + 6,
    location_names.db_iron_mam: BASE_ID + 11,
}

candy_mountain_locations = {
    location_names.db_stage_4: BASE_ID + 7,
    location_names.db_switch_2: BASE_ID + 10,
}

dyna_blade_nest_locations = {
    location_names.db_stage_5: BASE_ID + 8,
    location_names.db_complete: None,
}

dyna_blade_locations = {
    **peanut_plains_locations,
    **mallow_castle_locations,
    **cocoa_cave_locations,
    **candy_mountain_locations,
    **dyna_blade_nest_locations,
}

gourmet_race_locations = {
    location_names.gr_stage_1: BASE_ID + 12,
    location_names.gr_stage_2: BASE_ID + 13,
    location_names.gr_stage_3: BASE_ID + 14,
    location_names.gr_complete: None,
}

subtree_locations = {
    location_names.tgco_fatty_whale: BASE_ID + 15,
    location_names.tgco_treasure_1: BASE_ID + 19,
    location_names.tgco_treasure_2: BASE_ID + 20,
    location_names.tgco_treasure_3: BASE_ID + 21,
    location_names.tgco_treasure_4: BASE_ID + 22,
    location_names.tgco_treasure_5: BASE_ID + 23,
    location_names.tgco_treasure_6: BASE_ID + 24,
    location_names.tgco_treasure_7: BASE_ID + 25,
    location_names.tgco_treasure_8: BASE_ID + 26,
    location_names.tgco_treasure_9: BASE_ID + 27,
    location_names.tgco_treasure_10: BASE_ID + 28,
    location_names.tgco_treasure_11: BASE_ID + 29,
    location_names.tgco_treasure_12: BASE_ID + 30,
    location_names.tgco_treasure_13: BASE_ID + 31,
}

crystal_locations = {
    location_names.tgco_virus: BASE_ID + 16,
    location_names.tgco_treasure_14: BASE_ID + 32,
    location_names.tgco_treasure_15: BASE_ID + 33,
    location_names.tgco_treasure_16: BASE_ID + 34,
    location_names.tgco_treasure_17: BASE_ID + 35,
    location_names.tgco_treasure_18: BASE_ID + 36,
    location_names.tgco_treasure_19: BASE_ID + 37,
    location_names.tgco_treasure_20: BASE_ID + 38,
    location_names.tgco_treasure_21: BASE_ID + 39,
    location_names.tgco_treasure_22: BASE_ID + 40,
    location_names.tgco_treasure_23: BASE_ID + 41,
    location_names.tgco_treasure_24: BASE_ID + 42,
    location_names.tgco_treasure_25: BASE_ID + 43,
    location_names.tgco_treasure_26: BASE_ID + 44,
    location_names.tgco_treasure_27: BASE_ID + 45,
    location_names.tgco_treasure_28: BASE_ID + 46,
    location_names.tgco_treasure_29: BASE_ID + 47,
}

old_tower_locations = {
    location_names.tgco_chameleon: BASE_ID + 17,
    location_names.tgco_treasure_30: BASE_ID + 48,
    location_names.tgco_treasure_31: BASE_ID + 49,
    location_names.tgco_treasure_32: BASE_ID + 50,
    location_names.tgco_treasure_33: BASE_ID + 51,
    location_names.tgco_treasure_34: BASE_ID + 52,
    location_names.tgco_treasure_35: BASE_ID + 53,
    location_names.tgco_treasure_36: BASE_ID + 54,
    location_names.tgco_treasure_37: BASE_ID + 55,
    location_names.tgco_treasure_38: BASE_ID + 56,
    location_names.tgco_treasure_39: BASE_ID + 57,
    location_names.tgco_treasure_40: BASE_ID + 58,
    location_names.tgco_treasure_41: BASE_ID + 59,
    location_names.tgco_treasure_42: BASE_ID + 60,
    location_names.tgco_treasure_43: BASE_ID + 61,
    location_names.tgco_treasure_44: BASE_ID + 62,
    location_names.tgco_treasure_45: BASE_ID + 63,
}

garden_locations = {
    location_names.tgco_wham_bam: BASE_ID + 18,
    location_names.tgco_complete: None,
    location_names.tgco_treasure_46: BASE_ID + 64,
    location_names.tgco_treasure_47: BASE_ID + 65,
    location_names.tgco_treasure_48: BASE_ID + 66,
    location_names.tgco_treasure_49: BASE_ID + 67,
    location_names.tgco_treasure_50: BASE_ID + 68,
    location_names.tgco_treasure_51: BASE_ID + 69,
    location_names.tgco_treasure_52: BASE_ID + 70,
    location_names.tgco_treasure_53: BASE_ID + 71,
    location_names.tgco_treasure_54: BASE_ID + 72,
    location_names.tgco_treasure_55: BASE_ID + 73,
    location_names.tgco_treasure_56: BASE_ID + 74,
    location_names.tgco_treasure_57: BASE_ID + 75,
    location_names.tgco_treasure_58: BASE_ID + 76,
    location_names.tgco_treasure_59: BASE_ID + 77,
    location_names.tgco_treasure_60: BASE_ID + 78,
}

tgco_locations = {
    **subtree_locations,
    **crystal_locations,
    **old_tower_locations,
    **garden_locations,
}

romk_chapter_1_locations = {
    location_names.romk_chapter_1: BASE_ID + 79,
}

romk_chapter_2_locations = {
    location_names.romk_chapter_2: BASE_ID + 80,
}

romk_chapter_3_locations = {
    location_names.romk_chapter_3: BASE_ID + 81,
}

romk_chapter_4_locations = {
    location_names.romk_chapter_4: BASE_ID + 82,
}

romk_chapter_5_locations = {
    location_names.romk_chapter_5: BASE_ID + 83,
}

romk_chapter_6_locations = {
    location_names.romk_chapter_6: BASE_ID + 84,
}

romk_chapter_7_locations = {
    location_names.romk_chapter_7: BASE_ID + 85,
    location_names.romk_complete: None,
}

revenge_of_meta_knight_locations = {
    **romk_chapter_1_locations,
    **romk_chapter_2_locations,
    **romk_chapter_3_locations,
    **romk_chapter_4_locations,
    **romk_chapter_5_locations,
    **romk_chapter_6_locations,
    **romk_chapter_7_locations,
}

floria_locations = {
    location_names.mww_floria: BASE_ID + 87,
    location_names.mww_cutter: BASE_ID + 88,
    location_names.mww_fighter: BASE_ID + 89,
    location_names.mww_ice: BASE_ID + 90,
}

aqualiss_locations = {
    location_names.mww_aqualiss: BASE_ID + 91,
    location_names.mww_beam: BASE_ID + 92,
    location_names.mww_parasol: BASE_ID + 93,
    location_names.mww_sword: BASE_ID + 94,
}

skyhigh_locations = {
    location_names.mww_skyhigh: BASE_ID + 95,
    location_names.mww_jet: BASE_ID + 96,
    location_names.mww_wheel: BASE_ID + 97,
    location_names.mww_wing: BASE_ID + 98,
}

hotbeat_locations = {
    location_names.mww_hotbeat: BASE_ID + 99,
    location_names.mww_fire: BASE_ID + 100,
    location_names.mww_suplex: BASE_ID + 101,
}

cavios_locations = {
    location_names.mww_cavios: BASE_ID + 102,
    location_names.mww_bomb: BASE_ID + 103,
    location_names.mww_hammer: BASE_ID + 104,
    location_names.mww_stone: BASE_ID + 105,
}

mecheye_locations = {
    location_names.mww_mecheye: BASE_ID + 106,
    location_names.mww_plasma: BASE_ID + 107,
    location_names.mww_yoyo: BASE_ID + 108,
}

halfmoon_locations = {
    location_names.mww_halfmoon: BASE_ID + 109,
    location_names.mww_mirror: BASE_ID + 110,
    location_names.mww_ninja: BASE_ID + 111,
}

copy_planet_locations = {
    location_names.mww_copy: BASE_ID + 112
}

space_locations = {
    location_names.mww_complete: None
}

milky_way_wishes_locations = {
    **floria_locations,
    **aqualiss_locations,
    **skyhigh_locations,
    **hotbeat_locations,
    **cavios_locations,
    **mecheye_locations,
    **halfmoon_locations,
    **copy_planet_locations,
    **space_locations
}

the_arena_locations = {
    location_names.arena_1: BASE_ID + 113,
    location_names.arena_2: BASE_ID + 114,
    location_names.arena_3: BASE_ID + 115,
    location_names.arena_4: BASE_ID + 116,
    location_names.arena_5: BASE_ID + 117,
    location_names.arena_6: BASE_ID + 118,
    location_names.arena_7: BASE_ID + 119,
    location_names.arena_8: BASE_ID + 120,
    location_names.arena_9: BASE_ID + 121,
    location_names.arena_10: BASE_ID + 122,
    location_names.arena_11: BASE_ID + 123,
    location_names.arena_12: BASE_ID + 124,
    location_names.arena_13: BASE_ID + 125,
    location_names.arena_14: BASE_ID + 126,
    location_names.arena_15: BASE_ID + 127,
    location_names.arena_16: BASE_ID + 128,
    location_names.arena_17: BASE_ID + 129,
    location_names.arena_18: BASE_ID + 130,
    location_names.arena_19: BASE_ID + 131,
    location_names.arena_complete: None,
}

location_table = {
    **spring_breeze_locations,
    **dyna_blade_locations,
    **gourmet_race_locations,
    **tgco_locations,
    **revenge_of_meta_knight_locations,
    **milky_way_wishes_locations,
    **the_arena_locations
}