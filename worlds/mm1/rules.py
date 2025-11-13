from math import ceil
from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule, set_rule
from .options import RandomWeaknesses, weapons_to_id, bosses

if TYPE_CHECKING:
    from . import MM1World

weapon_damage: dict[int, list[int]] = {
    0: [3,  1,  2,  2,  1,  2,  2,  1,  2,  1],  # Mega Buster
    1: [1,  2,  2,  2,  10, 1,  2,  1,  2,  1],  # Rolling Cutter
    2: [0,  0,  0,  4,  0,  0,  0,  0,  0,  1],  # Ice Slasher
    3: [2,  4,  1,  1,  2,  10, 0,  2,  7,  0],  # Hyper Bomb
    4: [3,  1,  4,  1,  1,  2,  2,  2,  2,  4],  # Fire Storm
    5: [1,  10, 2,  1,  1,  1,  4,  2,  4,  1],  # Thunder Beam
    6: [14, -1, -1, -1, 4,  1,  -1, -1, 20, -1],  # Super Arm
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


def validate_fights(world: "MM1World", fights: tuple[int, ...]):
    boss_health = {boss: 0x1C if boss != 9 else 0x1C * 2 for boss in fights}

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
    flexibility = sorted(flexibility, key=flexibility.get)  # Fast way to sort dict by value
    used_weapons = {i: set() for i in fights}
    for boss in flexibility:
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
                max_uses, wp = max((weapon_energy[weapon] // weapon_costs[weapon], weapon)
                                   for weapon in weapon_weight
                                   if weapon != 0)
                world.weapon_damage[wp][boss] = minimum_weakness_requirement[wp]
                used = min(int(weapon_energy[wp] // weapon_costs[wp]),
                           ceil(boss_health[boss] / minimum_weakness_requirement[wp]))
                weapon_energy[wp] -= weapon_costs[wp] * used
                boss_health[boss] -= int(used * minimum_weakness_requirement[wp])
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
}


def set_rules(world: "MM1World"):
    # most rules are set on region, so we only worry about rules required within stage access
    # or rules variable on settings
    if (hasattr(world.multiworld, "re_gen_passthrough")
            and "Mega Man" in getattr(world.multiworld, "re_gen_passthrough")):
        slot_data = getattr(world.multiworld, "re_gen_passthrough")["Mega Man 2"]
        world.weapon_damage = slot_data["weapon_damage"]
        world.wily_weapons = slot_data["wily_weapons"]
    else:
        if world.options.random_weakness == RandomWeaknesses.option_shuffled:
            weapon_tables = [table.copy() for weapon, table in weapon_damage.items() if weapon not in (0, 6)]
            world.random.shuffle(weapon_tables)
            for i in range(1, 6):
                world.weapon_damage[i] = weapon_tables.pop()
            for boss in (0, 4, 5, 8):
                # valid Super Arm damage
                world.weapon_damage[6][boss] = min(14, max(-1, int(world.random.normalvariate(3, 3))))
        elif world.options.random_weakness == RandomWeaknesses.option_randomized:
            world.weapon_damage = {i: [] for i in range(7)}
            for boss in range(10):
                for weapon in world.weapon_damage:
                    if boss not in (0, 4, 5, 8) and weapon == 6:
                        world.weapon_damage[weapon].append(-1)
                    else:
                        world.weapon_damage[weapon].append(min(14, max(-1, int(world.random.normalvariate(3, 3)))))
                if not any([world.weapon_damage[weapon][boss] >= max(4, minimum_weakness_requirement[weapon])
                            for weapon in range(1, 6)]):
                    # failsafe, there should be at least one defined non-Buster, non-Super Arm weakness
                    weapon = world.random.randint(1, 5)
                    world.weapon_damage[weapon][boss] = world.random.randint(
                        max(4, minimum_weakness_requirement[weapon]), 14)  # Force weakness


        if world.options.strict_weakness:
            for weapon in weapon_damage:
                for i in range(10):
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
            boss = bosses[p_boss]
            for p_weapon in world.options.plando_weakness[p_boss]:
                weapon = weapons_to_id[p_weapon]
                if world.options.plando_weakness[p_boss][p_weapon] < minimum_weakness_requirement[weapon] \
                        and not any(w != weapon
                                    and world.weapon_damage[w][boss] >= minimum_weakness_requirement[w]
                                    for w in world.weapon_damage):
                    # we need to replace this weakness
                    weakness = world.random.choice([key for key in world.weapon_damage if key != weapon])
                    world.weapon_damage[weakness][boss] = minimum_weakness_requirement[weakness]
                world.weapon_damage[weapon][boss] = world.options.plando_weakness[p_boss][p_weapon]

        # handle special cases
        for boss in (0, 4, 5, 8):
            if (world.weapon_damage[6][boss] >= minimum_weakness_requirement[6] and
                    not any(world.weapon_damage[i][boss] >= minimum_weakness_requirement[i]
                            for i in range(6))):
                # Super Arm cannot be the only weakness
                weakness = world.random.choice(range(1, 6))
                world.weapon_damage[weakness][boss] = minimum_weakness_requirement[weakness]

        if (world.weapon_damage[2][9] >= minimum_weakness_requirement[1] and
                not any(world.weapon_damage[i][9] >= minimum_weakness_requirement[i]
                        for i in range(6) if i != 2)):
            # Hyper Bomb cannot be Wily's only weakness
            world.weapon_damage[1][9] = 0
            weakness = world.random.choice((1, 3, 4, 5))
            world.weapon_damage[weakness][9] = minimum_weakness_requirement[weakness]

        if world.weapon_damage[0][world.options.starting_robot_master.value] < 1:
            world.weapon_damage[0][world.options.starting_robot_master.value] = \
                weapon_damage[0][world.options.starting_robot_master.value]


        world.wily_weapons = validate_fights(world, (1, 2, 3, 5, 9))

    #static rules
    for boss, locations in boss_locations.items():
        if world.weapon_damage[0][boss] > 0:
            continue  # this can always be in logic
        weapons = []
        for weapon in range(1, 7):
            if world.weapon_damage[weapon][boss] > 0:
                if world.weapon_damage[weapon][boss] < minimum_weakness_requirement[weapon]:
                    continue
                weapons.append(weapons_to_name[weapon])
        if not weapons:
            raise Exception(f"Attempted to have boss {boss} with no weakness! Seed: {world.multiworld.seed}")
        for location in locations:
            if "Wily" in location and boss != 8:
                # Special case: Super Arm cannot be logical for any Wily locations
                add_rule(world.get_location(location), lambda state, weps=tuple(weapons): state.has_any([wep for wep in weps if wep != "Super Arm"], world.player))
            else:
                add_rule(world.get_location(location), lambda state, weps=tuple(weapons): state.has_any(weps, world.player))

    # magnet beam
    set_rule(world.get_location("Elec Man Stage - Magnet Beam"),
             lambda state: state.has_any(["Thunder Beam", "Super Arm"], world.player))

    # handle the wily rule
    set_rule(world.get_entrance(f"To Wily Stage 1"),
             lambda state: state.has("Magnet Beam", world.player) and
             state.has_any(["Thunder Beam", "Super Arm"], world.player)
             and state.has_group_unique("Weapons", world.player, world.options.required_weapons.value))

    # boss refight chaining
    add_rule(world.get_location("Wily Stage 2 - Elec Man Rematch"),
             lambda state: state.can_reach_location("Wily Stage 2 - Cut Man Rematch", world.player))
    add_rule(world.get_location("Copy Robot - Defeated"),
             lambda state: state.can_reach_location("Wily Stage 2 - Elec Man Rematch", world.player))
    add_rule(world.get_location("Wily Stage 2 - Complete"),
             lambda state: state.can_reach_location("Wily Stage 2 - Elec Man Rematch", world.player))

    add_rule(world.get_location("Wily Stage 4 - Bomb Man Rematch"),
             lambda state: state.has_all([weapons_to_name[wep] for wep in sorted(world.wily_weapons[2])], world.player))
    add_rule(world.get_location("Wily Stage 4 - Fire Man Rematch"),
             lambda state: state.can_reach_location("Wily Stage 4 - Bomb Man Rematch", world.player) and
             state.has_all([weapons_to_name[wep] for wep in sorted(world.wily_weapons[3])], world.player))
    add_rule(world.get_location("Wily Stage 4 - Ice Man Rematch"),
             lambda state: state.can_reach_location("Wily Stage 4 - Fire Man Rematch", world.player) and
             state.has_all([weapons_to_name[wep] for wep in sorted(world.wily_weapons[1])], world.player))
    add_rule(world.get_location("Wily Stage 4 - Guts Man Rematch"),
             lambda state: state.can_reach_location("Wily Stage 4 - Ice Man Rematch", world.player) and
             state.has_all([weapons_to_name[wep] for wep in sorted(world.wily_weapons[5])], world.player))
    add_rule(world.get_location("Wily Machine - Defeated"),
             lambda state: state.can_reach_location("Wily Stage 4 - Guts Man Rematch", world.player) and
             state.has_all([weapons_to_name[wep] for wep in sorted(world.wily_weapons[9])], world.player))

    world.multiworld.completion_condition[world.player] = lambda state: state.has("Wily Machine - Defeated",
                                                                                  world.player)
