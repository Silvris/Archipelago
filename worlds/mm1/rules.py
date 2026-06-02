from math import ceil
from typing import TYPE_CHECKING
from rule_builder.rules import Rule, True_, Has, HasAll, CanReachLocation, HasGroupUnique, HasAny
from rule_builder.field_resolvers import FromOption, FromWorldAttr
from .options import RandomWeaknesses, RequiredWeapons, weapons_to_id, bosses

if TYPE_CHECKING:
    from . import MM1World

weapon_damage: dict[int, list[int]] = {
    0: [3,  1,  2,  2,  1,  2,  2,  1,  2,  1,  1],  # Mega Buster
    1: [1,  2,  2,  2,  10, 1,  2,  1,  2,  1,  1],  # Rolling Cutter
    2: [0,  0,  0,  4,  0,  0,  0,  0,  0,  1,  0],  # Ice Slasher
    3: [2,  4,  1,  1,  2,  10, 0,  2,  7,  0,  0],  # Hyper Bomb
    4: [3,  1,  4,  1,  1,  2,  2,  2,  2,  4,  1],  # Fire Storm
    5: [1,  10, 2,  1,  1,  1,  4,  2,  4,  1,  1],  # Thunder Beam
    6: [14, -1, -1, -1, 4,  1,  -1, -1, 20, -1, -1],  # Super Arm
}

weapons_to_name = {
    value: key for key, value in weapons_to_id.items()
}

minimum_weakness_requirement: dict[int, int] = {
    0: 1,  # Mega Buster is free
    1: 1,  # they didn't really try balancing this
    2: 1,
    3: 1,
    4: 1,
    5: 1,
    6: 14,  # Super Arm is...difficult
}

weapon_costs = {
    0: 1,
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 1,
    6: 29, # purposefully excluded from validation logic
    # Super Arm isn't available in any refight, so we have to confirm it's beatable without it
}

class ValidationException(Exception):
    pass

def validate_fights(world: "MM1World", fights: tuple[int, ...], error: bool = False) -> dict[int, set[int]]:
    boss_health = {boss: 0x1C if boss != 9 else 0x1C * 2 for boss in fights}
    costs = weapon_costs.copy()
    min_weakness = minimum_weakness_requirement.copy()
    if world.options.enhanced_super_arm:
        costs[6] = 2
        min_weakness[6] = 2

    weapon_energy = {key: float(0x1C) for key in weapon_costs}
    weapon_boss = {boss: {weapon: world.weapon_damage[weapon][boss] for weapon in world.weapon_damage}
                   for boss in fights}
    flexibility = {
        boss: (
                sum(damage_value > 0 for damage_value in
                    weapon_damages.values())  # Amount of weapons that hit this boss
                * sum(weapon_damages.values())  # Overall damage that those weapons do
        )
        for boss, weapon_damages in weapon_boss.items() if boss != 9
    }
    flex = sorted(flexibility, key=flexibility.get)  # Fast way to sort dict by value
    used_weapons: dict[int, set[int]] = {i: set() for i in fights}
    for boss in flex:
        boss_damage = weapon_boss[boss]
        weapon_weight = {weapon: (weapon_energy[weapon] / damage) if damage else 0 for weapon, damage in
                         boss_damage.items() if weapon != 6 and weapon_energy[weapon] > 0}
        while boss_health[boss] > 0:
            if boss_damage[0] > 0:
                boss_health[boss] = 0  # if we can buster, we should buster
                continue
            highest, wp = max(zip(weapon_weight.values(), weapon_weight.keys()))
            uses = weapon_energy[wp] // weapon_costs[wp]
            if int(uses * boss_damage[wp]) >= boss_health[boss]:
                used = ceil(boss_health[boss] / boss_damage[wp])
                weapon_energy[wp] -= weapon_costs[wp] * used
                boss_health[boss] = 0
                used_weapons[boss].add(wp)
            elif highest <= 0:
                # we are out of weapons that can actually damage the boss
                # so find the weapon that has the most uses, and apply that as an additional weakness
                # it should be impossible to be out of energy
                if error:
                    # we should throw an exception, as we are in a testing environment
                    raise ValidationException(f"Ran out of weapon energy to damage "
                          f"{next(name for name in bosses if bosses[name] == boss)}\n"
                          f"Seed: {world.multiworld.seed}\n"
                          f"Damage Table: {weapon_damage}")
                max_uses, wp = max((weapon_energy[weapon] // weapon_costs[weapon], weapon)
                                   for weapon in weapon_weight
                                   if weapon != 0)
                world.weapon_damage[wp][boss] = min_weakness[wp]
                used = min(int(weapon_energy[wp] // weapon_costs[wp]),
                           ceil(boss_health[boss] / min_weakness[wp]))
                weapon_energy[wp] -= weapon_costs[wp] * used
                boss_health[boss] -= int(used * min_weakness[wp])
                weapon_weight.pop(wp)
                used_weapons[boss].add(wp)
            else:
                # drain the weapon and continue
                boss_health[boss] -= int(uses * boss_damage[wp])
                weapon_energy[wp] -= weapon_costs[wp] * uses
                weapon_weight.pop(wp)
                used_weapons[boss].add(wp)
    return used_weapons


boss_locations = {
    0: ["Cut Man - Defeated", "Rolling Cutter - Received", "Wily Stage 2 - Cut Man Rematch"],
    1: ["Ice Man - Defeated", "Ice Slasher - Received", "Wily Stage 4 - Ice Man Rematch"],
    2: ["Bomb Man - Defeated", "Hyper Bomb - Received", "Wily Stage 4 - Bomb Man Rematch"],
    3: ["Fire Man - Defeated", "Fire Storm - Received", "Wily Stage 4 - Fire Man Rematch"],
    4: ["Elec Man - Defeated", "Thunder Beam - Received", "Wily Stage 2 - Elec Man Rematch"],
    5: ["Guts Man - Defeated", "Super Arm - Received", "Wily Stage 4 - Guts Man Rematch"],
    6: ["Yellow Devil - Defeated", "Wily Stage 1 - Complete"],
    7: ["Copy Robot - Defeated", "Wily Stage 2 - Complete"],
    8: ["CWU-01P - Defeated", "Wily Stage 3 - Complete"],
    9: ["Wily Machine - Defeated"],
    10: ["Wily Machine - Defeated"],
}

STATIC_LOCATION_RULES: dict[str, Rule] = {
    "Elec Man Stage - Magnet Beam": HasAny("Super Arm", "Thunder Beam"),
    "Wily Stage 2 - Elec Man Rematch": CanReachLocation("Wily Stage 2 - Cut Man Rematch"),
    "Copy Robot - Defeated": CanReachLocation("Wily Stage 2 - Elec Man Rematch"),
    "Wily Stage 2 - Complete": CanReachLocation("Wily Stage 2 - Elec Man Rematch"),
    "Wily Stage 4 - Fire Man Rematch": CanReachLocation("Wily Stage 4 - Bomb Man Rematch"),
    "Wily Stage 4 - Ice Man Rematch": CanReachLocation("Wily Stage 4 - Fire Man Rematch"),
    "Wily Stage 4 - Guts Man Rematch": CanReachLocation("Wily Stage 4 - Ice Man Rematch"),
    "Wily Machine Defeated": CanReachLocation("Wily Stage 4 - Guts Man Rematch"),
    "Fire Man Stage - Weapon Energy 1": HasAny("Magnet Beam", "Ice Slasher"),
    "Fire Man Stage - Weapon Energy 2": HasAny("Magnet Beam", "Ice Slasher"),
    "Wily Stage 2 - Health Energy 2": CanReachLocation("Wily Stage 2 - Cut Man Rematch"),
    "Wily Stage 2 - Weapon Energy 3": CanReachLocation("Wily Stage 2 - Cut Man Rematch"),
    "Wily Stage 2 - Weapon Energy 4": CanReachLocation("Wily Stage 2 - Cut Man Rematch"),
    "Wily Stage 2 - Weapon Energy 5": CanReachLocation("Wily Stage 2 - Elec Man Rematch"),
    "Wily Stage 2 - Weapon Energy 6": CanReachLocation("Wily Stage 2 - Elec Man Rematch"),
    "Wily Stage 2 - Weapon Energy 7": CanReachLocation("Wily Stage 2 - Elec Man Rematch"),
    "Wily Stage 2 - 1-Up": CanReachLocation("Wily Stage 2 - Elec Man Rematch"),
    "Wily Stage 4 - Weapon Energy 2": CanReachLocation("Wily Stage 4 - Guts Man Rematch"),

}

STATIC_ENTRANCE_RULES: dict[str, Rule] = {
    "To Wily Stage 1": Has("Magnet Beam") & HasAny("Super Arm", "Thunder Beam")
                       & HasGroupUnique("Weapons",count=FromOption(RequiredWeapons)),

}

def set_rules(world: "MM1World"):
    # most rules are set on region, so we only worry about rules required within stage access
    # or rules variable on settings
    min_weakness = minimum_weakness_requirement.copy()
    if (hasattr(world.multiworld, "re_gen_passthrough")
            and "Mega Man" in getattr(world.multiworld, "re_gen_passthrough")):
        slot_data = getattr(world.multiworld, "re_gen_passthrough")["Mega Man"]
        world.weapon_damage = slot_data["weapon_damage"]
        world.wily_weapons = slot_data["wily_weapons"]
    else:
        if world.options.enhanced_super_arm:
            min_weakness[6] = 2

        if world.options.random_weakness == RandomWeaknesses.option_shuffled:
            weapon_tables = [table.copy() for weapon, table in weapon_damage.items() if weapon not in (0, 6)]
            world.random.shuffle(weapon_tables)
            for i in range(1, 6 if not world.options.enhanced_super_arm else 7):
                world.weapon_damage[i] = weapon_tables.pop()
            if not world.options.enhanced_super_arm:
                for boss in (0, 4, 5, 8):
                    # valid Super Arm damage
                    world.weapon_damage[6][boss] = min(14, max(-1, int(world.random.normalvariate(9, 3))))
        elif world.options.random_weakness == RandomWeaknesses.option_randomized:
            world.weapon_damage = {i: [] for i in range(7)}
            for boss in range(11):
                for weapon in world.weapon_damage:
                    if not world.options.enhanced_super_arm and boss not in (0, 4, 5, 8) and weapon == 6:
                        # Bosses cannot take Super Arm damage
                        world.weapon_damage[weapon].append(-1)
                    elif not world.options.enhanced_hyper_bomb and boss in (6, 9, 10) and weapon == 3:
                        # Bosses cannot take Hyper Bomb damage
                        world.weapon_damage[weapon].append(-1)
                    else:
                        world.weapon_damage[weapon].append(min(14, max(-1, int(world.random.normalvariate(3, 3)))))
                if not any([world.weapon_damage[weapon][boss] >= max(4, min_weakness[weapon])
                            for weapon in range(1, 6)]):
                    # failsafe, there should be at least one defined non-Buster, non-Super Arm weakness
                    weapons = [1, 2, 4, 5]
                    if boss not in (6, 8):
                        weapons.append(3)
                    weapon = world.random.choice(weapons)
                    world.weapon_damage[weapon][boss] = world.random.randint(
                        max(4, min_weakness[weapon]), 14)  # Force weakness


        if world.options.strict_weakness:
            for weapon in weapon_damage:
                for i in range(11):
                    if weapon == 0:
                        world.weapon_damage[weapon][i] = 0
                    elif i == 7 and not world.options.random_weakness:
                        continue
                        # Wily Machine needs all weaknesses present, so allow
                    elif i in (0, 7):
                        if 2 > world.weapon_damage[weapon][i] > 0:
                            world.weapon_damage[weapon][i] = 0
                    elif 4 > world.weapon_damage[weapon][i] > 0:
                        world.weapon_damage[weapon][i] = 0

        for p_boss in world.options.plando_weakness:
            if p_boss in bosses:
                boss = bosses[p_boss]
                for p_weapon in world.options.plando_weakness[p_boss]:
                    weapon = min(14, weapons_to_id[p_weapon])
                    if world.options.plando_weakness[p_boss][p_weapon] < min_weakness[weapon] \
                            and not any(w != weapon
                                        and world.weapon_damage[w][boss] >= min_weakness[w]
                                        for w in world.weapon_damage):
                        # we need to replace this weakness
                        weakness = world.random.choice([key for key in world.weapon_damage if key != weapon])
                        world.weapon_damage[weakness][boss] = min_weakness[weakness]
                    world.weapon_damage[weapon][boss] = world.options.plando_weakness[p_boss][p_weapon]

        # handle special cases
        if not world.options.enhanced_super_arm:
            for boss in range(11):
                if boss in (0, 4, 5, 8):
                    if (world.weapon_damage[6][boss] >= min_weakness[6] and
                            not any(world.weapon_damage[i][boss] >= min_weakness[i]
                                    for i in range(6))):
                        # Super Arm cannot be the only weakness
                        weakness = world.random.choice(range(1, 6))
                        world.weapon_damage[weakness][boss] = min_weakness[weakness]
                else:
                    # enforce 0 damage from super arm
                    world.weapon_damage[6][boss] = 0

        if not world.options.enhanced_hyper_bomb:
            for boss in range(11):
                if boss in (6, 9, 10):
                    if (world.weapon_damage[3][boss] >= min_weakness[1] and
                            not any(world.weapon_damage[i][boss] >= min_weakness[i]
                                    for i in range(6) if i != 3)):
                        # Hyper Bomb cannot be Wily or Yellow Devil's only weakness
                        world.weapon_damage[3][boss] = 0
                        weakness = world.random.choice((1, 2, 4, 5))
                        world.weapon_damage[weakness][boss] = min_weakness[weakness]
                else:
                    # enforce 0 damage from hyper bomb
                    world.weapon_damage[3][boss] = 0

        if world.weapon_damage[0][world.options.starting_robot_master.value] < 1:
            world.weapon_damage[0][world.options.starting_robot_master.value] = \
                weapon_damage[0][world.options.starting_robot_master.value]


        world.wily_weapons = validate_fights(world, (1, 2, 3, 5, 9, 10))

    #static rules
    location_rules: dict[str, Rule] = {}
    entrance_rules: dict[str, Rule] = {}

    for boss, locations in boss_locations.items():
        if world.weapon_damage[0][boss] > 0:
            continue  # this can always be in logic
        boss_weapons: list[str] = []
        for weapon in range(1, 7):
            if world.weapon_damage[weapon][boss] > 0:
                if world.weapon_damage[weapon][boss] < min_weakness[weapon]:
                    continue
                boss_weapons.append(weapons_to_name[weapon])
        if not boss_weapons:
            raise Exception(f"Attempted to have boss {boss} with no weakness! Seed: {world.multiworld.seed}")
        for location in locations:
            if "Wily" in location and not world.options.enhanced_super_arm:
                # Special case: Super Arm cannot be logical for any Wily locations
                # This includes CWU-001, since there aren't enough guts blocks without cloning
                # Side note: I think cloning can be consistent? But absolutely not worth being in logic
                rule = HasAny(*[w for w in boss_weapons if w != "Super Arm"])
            else:
                rule = HasAny(*boss_weapons)
            if location in location_rules:
                location_rules[location] &= rule
            else:
                location_rules[location] = rule

    # wily weapon rules
    location_rules["Wily Stage 4 - Bomb Man Rematch"] = HasAll(*[weapons_to_name[wep] for wep in sorted(world.wily_weapons[2])])
    location_rules["Wily Stage 4 - Fire Man Rematch"] = HasAll(*[weapons_to_name[wep] for wep in sorted(world.wily_weapons[3])])
    location_rules["Wily Stage 4 - Ice Man Rematch"] = HasAll(*[weapons_to_name[wep] for wep in sorted(world.wily_weapons[1])])
    location_rules["Wily Stage 4 - Guts Man Rematch"] = HasAll(*[weapons_to_name[wep] for wep in sorted(world.wily_weapons[5])])
    location_rules["Wily Machine - Defeated"] = HasAll(*[weapons_to_name[wep] for wep in sorted(world.wily_weapons[9])])

    # apply static rules
    for location in STATIC_LOCATION_RULES:
        if location in location_rules:
            location_rules[location] &= STATIC_LOCATION_RULES[location]
        else:
            location_rules[location] = STATIC_LOCATION_RULES[location]

    for entrance in STATIC_ENTRANCE_RULES:
        if entrance in entrance_rules:
            entrance_rules[entrance] &= STATIC_ENTRANCE_RULES[entrance]
        else:
            entrance_rules[entrance] = STATIC_ENTRANCE_RULES[entrance]

    for location in world.get_locations():
        if location.name in location_rules:
            world.set_rule(location, location_rules[location.name])

    for entrance in world.get_entrances():
        if entrance.name in entrance_rules:
            world.set_rule(entrance, entrance_rules[entrance.name])


    world.multiworld.completion_condition[world.player] = Has("Wily Machine - Defeated").resolve(world)
