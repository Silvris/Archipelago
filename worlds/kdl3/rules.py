from BaseClasses import ItemClassification
from rule_builder.rules import HasAll, Has, CanReachLocation, OptionFilter, Rule, True_
from .items import KDL3Item
from .locations import location_table
from .names import location_name, enemy_abilities, animal_friend_spawns
from .options import GoalSpeed
import typing

if typing.TYPE_CHECKING:
    from . import KDL3World
    from BaseClasses import CollectionState


def CanReachBoss(level: int, open_world: int, ow_boss_req: int, player_levels: dict[int, list[int]]) -> Rule:
    if open_world:
        return Has(f"{location_name.level_names_inverse[level]} - Stage Completion", count=ow_boss_req)
    else:
        return CanReachLocation(location_table[player_levels[level][5]])


CanReachRick = HasAll("Rick", "Rick Spawn")
CanReachKine = HasAll("Kine", "Kine Spawn")
CanReachCoo = HasAll("Coo", "Coo Spawn")
CanReachNago = HasAll("Nago", "Nago Spawn")
CanReachChuChu = HasAll("ChuChu", "ChuChu Spawn")
CanReachPitch = HasAll("Pitch", "Pitch Spawn")
CanReachAnyAnimalOtherThanKine = CanReachRick | CanReachCoo | CanReachNago | CanReachChuChu | CanReachPitch

CanReachBurning = HasAll("Burning", "Burning Ability")
CanReachStone = HasAll("Stone", "Stone Ability")
CanReachIce = HasAll("Ice", "Ice Ability")
CanReachNeedle = HasAll("Needle", "Needle Ability")
CanReachClean = HasAll("Clean", "Clean Ability")
CanReachParasol = HasAll("Parasol", "Parasol Ability")
CanReachSpark = HasAll("Spark", "Spark Ability")
CanReachCutter = HasAll("Cutter", "Cutter Ability")


def can_reach_regions(state: "CollectionState", player: int, regions: typing.List[str]):
    for region in regions:
        if not state.can_reach_region(region, player):
            return False
    return True


ability_map: dict[str, Rule] = {
    "No Ability": True_,
    "Burning Ability": CanReachBurning,
    "Stone Ability": CanReachStone,
    "Ice Ability": CanReachIce,
    "Needle Ability": CanReachNeedle,
    "Clean Ability": CanReachClean,
    "Parasol Ability": CanReachParasol,
    "Spark Ability": CanReachSpark,
    "Cutter Ability": CanReachCutter,
}

STATIC_LOCATION_RULES: dict[str, Rule] = {
    # Level 1
    location_name.grass_land_muchi: CanReachChuChu,
    location_name.grass_land_chao: Has("Goku"),
    location_name.grass_land_mine: CanReachKine,
    # Level 2
    # Ripple Field 5 rules are applied on entrances instead
    location_name.ripple_field_kamuribana: CanReachPitch & CanReachClean,
    location_name.ripple_field_bakasa: CanReachKine & CanReachParasol,
    location_name.ripple_field_toad: Has("Little Toad"),
    location_name.ripple_field_4_little_toad: CanReachNeedle,
    location_name.ripple_field_5_wall: CanReachBurning & CanReachStone,
    location_name.ripple_field_mama_pitch: CanReachPitch,  # Rest are on entrances/fixup
    # Level 3
    location_name.sand_canyon_auntie: CanReachClean,
    location_name.sand_canyon_nyupun: CanReachChuChu,  # Cutter handled on entrance
    location_name.sand_canyon_rob: HasAll("ROB Base", "ROB Torso", "ROB Left Arm",
                                          "ROB Right Arm", "ROB Head"),
    location_name.sand_canyon_6_rob_left: CanReachKine,  # edge case
    location_name.sand_canyon_6_rob_right: CanReachCoo,  # edge case
    # Level 4
    location_name.cloudy_park_hibanamodoki: (CanReachRick | CanReachCoo) & CanReachClean,
    location_name.cloudy_park_piyokeko: CanReachNeedle,
    location_name.cloudy_park_mikarin: Has("Mikarin"),
    location_name.cloudy_park_4_mikarin: CanReachCoo,
    location_name.cloudy_park_pick: CanReachRick,
    # Level 5
    location_name.iceberg_kogoesou: CanReachBurning,
    location_name.iceberg_samus: CanReachIce,
    location_name.iceberg_name: Has("Shell"),  # Handled through entrances
    location_name.iceberg_shiro: CanReachNago,
    location_name.iceberg_angel: Has("Angel Feather", count=8)

}

STATIC_CONSUMABLE_RULES: dict[str, Rule] = {
    location_name.grass_land_1_u1: CanReachParasol,
    location_name.grass_land_1_m1: CanReachSpark,
    location_name.grass_land_2_u1: CanReachNeedle,
    location_name.ripple_field_2_u1: CanReachKine,
    location_name.ripple_field_2_m1: CanReachKine,
    location_name.ripple_field_3_u1: CanReachCutter | CanReachSpark,
    location_name.ripple_field_4_u1: CanReachStone,
    location_name.ripple_field_4_m2: CanReachStone,
    location_name.ripple_field_5_m1: CanReachKine,
    location_name.ripple_field_5_u1: CanReachKine,  # Wall applied in fixup
    location_name.ripple_field_5_m2: CanReachKine,
    location_name.sand_canyon_4_u1: CanReachClean,
    location_name.sand_canyon_4_m2: CanReachNeedle,
    location_name.sand_canyon_5_u2: CanReachIce & CanReachAnyAnimalOtherThanKine,
    location_name.sand_canyon_5_u3: CanReachIce & CanReachAnyAnimalOtherThanKine,
    location_name.sand_canyon_5_u4: CanReachIce & CanReachAnyAnimalOtherThanKine,
    location_name.cloudy_park_6_u1: CanReachCutter,
}

STATIC_STAR_RULES: dict[tuple[str, tuple[int, ...]], Rule] = {
    ("Grass Land 1", (*range(7, 11),)) : CanReachCutter,
    ("Grass Land 1", (*range(11, 14),)) : CanReachParasol,
    ("Grass Land 2", (1, 3, 4, 9, 10)): CanReachStone,
    ("Grass Land 2", (2,)): CanReachBurning,
    ("Ripple Field 2", (17,)): CanReachKine,
    ("Ripple Field 5", (41, 42)): CanReachKine,
    ("Ripple Field 5", (*range(46, 50),)): CanReachBurning & CanReachStone,  # These are the stars in the ability blocks
    ("Sand Canyon 5", (*range(12, 18),)): CanReachIce & CanReachAnyAnimalOtherThanKine,
    ("Sand Canyon 5", (21, 22)): CanReachChuChu,
    ("Sand Canyon 5", (19, 20, *range(23, 31),)): CanReachClean,
    ("Sand Canyon 5", (*range(31, 41),)): CanReachBurning,
    ("Cloudy Park 4", (*range(1, 31), *range(44, 51),)): CanReachCoo,
    ("Cloudy Park 6", (18, *range(20, 25),)): CanReachIce,
    ("Cloudy Park 6", (19, *range(25, 30),)): CanReachBurning,
    ("Iceberg 4", (1, 2, 3)): CanReachBurning
}

STATIC_ABILITY_ANIMAL_RULES: dict[str, Rule] = {
    enemy_abilities.Ripple_Field_2_E3: CanReachKine | CanReachChuChu,
    enemy_abilities.Ripple_Field_3_E6: CanReachKine | CanReachChuChu,
    enemy_abilities.Ripple_Field_4_E5: CanReachKine | CanReachChuChu,
    enemy_abilities.Ripple_Field_4_E7: CanReachKine | CanReachChuChu,
    enemy_abilities.Ripple_Field_4_E8: CanReachKine | CanReachChuChu,
    enemy_abilities.Ripple_Field_5_E1: CanReachKine | CanReachChuChu,
    enemy_abilities.Ripple_Field_5_E2: CanReachKine | CanReachChuChu,
    enemy_abilities.Ripple_Field_5_E3: CanReachKine | CanReachChuChu,
    enemy_abilities.Ripple_Field_5_E4: CanReachKine | CanReachChuChu,
    enemy_abilities.Sand_Canyon_4_E7: CanReachKine | CanReachChuChu,
    enemy_abilities.Sand_Canyon_4_E8: CanReachKine | CanReachChuChu,
    enemy_abilities.Sand_Canyon_4_E9: CanReachKine | CanReachChuChu,
    enemy_abilities.Sand_Canyon_4_E10: CanReachKine | CanReachChuChu,

    animal_friend_spawns.iceberg_4_a2: CanReachChuChu & CanReachBurning,
    animal_friend_spawns.iceberg_4_a3: CanReachChuChu & CanReachBurning,
}

def set_rules(world: "KDL3World") -> None:
    goal = world.options.goal.value
    goal_location = world.get_location(location_name.goals[goal])
    goal_location.place_locked_item(KDL3Item("Love-Love Rod", ItemClassification.progression, None, world.player))
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Love-Love Rod", world.player)

    for location, rule in STATIC_LOCATION_RULES.items():
        world.set_rule(world.get_location(location), rule)

    if not world.options.door_shuffle:
        angel_requirements = [
            world.copy_abilities["Sparky"],
            world.copy_abilities["Blocky"],
            world.copy_abilities["Jumper Shoot"],
            world.copy_abilities["Yuki"],
            world.copy_abilities["Sir Kibble"],
            world.copy_abilities["Haboki"],
            world.copy_abilities["Boboo"],
            world.copy_abilities["Captain Stitch"],
        ]
    else:
        angel_requirements = [
            "Spark Ability",
            "Stone Ability",
            "Parasol Ability",
            "Ice Ability",
            "Cutter Ability",
            "Clean Ability",
            "Burning Ability",
            "Needle Ability"
        ]
    for i, req in enumerate(angel_requirements):
        angel_rule = ability_map[req]
        world.set_rule(world.get_location(f"Iceberg 6 - Feather {i+1}"), angel_rule)

    # Consumables
    if world.options.consumables:
        for location, rule in STATIC_CONSUMABLE_RULES.items():
            world.set_rule(world.get_location(location), rule)

    if world.options.starsanity:
        # ranges are our friend
        for loc_info, rule in STATIC_STAR_RULES.items():
            level, stars = loc_info
            for i in stars:
                world.set_rule(world.get_location(f"{level} - Star {i}"), rule)

    # copy ability access edge cases
    # Kirby cannot eat enemies fully submerged in water. Vast majority of cases, the enemy can be brought to the surface
    # and eaten by inhaling while falling on top of them
    for location, rule in STATIC_ABILITY_ANIMAL_RULES.items():
        world.set_rule(world.get_location(location), rule)

    for boss_flag, purification, i in zip(["Level 1 Boss - Purified", "Level 2 Boss - Purified",
                                           "Level 3 Boss - Purified", "Level 4 Boss - Purified",
                                           "Level 5 Boss - Purified"],
                                          [location_name.grass_land_whispy, location_name.ripple_field_acro,
                                           location_name.sand_canyon_poncon, location_name.cloudy_park_ado,
                                           location_name.iceberg_dedede],
                                          range(1, 6)):
        rule = Has("Heart Star", count=world.boss_requirements[i - 1]) \
                                     & CanReachBoss(i,
                                                        world.options.open_world.value,
                                                        world.options.ow_boss_requirement.value,
                                                        world.player_levels)
        world.set_rule(world.get_location(boss_flag), rule)
        world.set_rule(world.get_location(purification), rule)

    if world.options.open_world:
        for boss_flag, level in zip(["Level 1 Boss - Defeated", "Level 2 Boss - Defeated", "Level 3 Boss - Defeated",
                                     "Level 4 Boss - Defeated", "Level 5 Boss - Defeated"],
                                    location_name.level_names.keys()):
            world.set_rule(world.get_location(boss_flag), Has(f"{level} - Stage Completion",
                                                              count=world.options.ow_boss_requirement.value))

    hyper_zone_rule = Has("Heart Star", count=world.required_heart_stars)
    if world.options.goal_speed == GoalSpeed.option_normal:
        hyper_zone_rule &= HasAll("Level 1 Boss Purified", "Level 2 Boss Purified", "Level 3 Boss Purified",
                                              "Level 4 Boss Purified", "Level 5 Boss Purified")
    world.set_rule(world.get_entrance("To Level 6"), hyper_zone_rule)

    for level in range(2, 6):
        rule = Has(f"Level {level - 1} Boss Defeated")
        if world.options.strict_bosses:
            rule &= Has(f"Level {level - 1} Boss Purified")
        world.set_rule(world.get_entrance(f"To Level {level}"), rule)
