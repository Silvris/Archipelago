from math import ceil
from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule, set_rule
from .locations import mm1_regions

if TYPE_CHECKING:
    from . import MM1World

weapon_damage: dict[int, list[int]] = {
    0: [3, 1, 2, 2, 1, 2, 2, 1, 1, 1],  # Mega Buster
    1: [1, 2, 2, 2, 10, 1, 2, 1, 1, 1],  # Rolling Cutter
    2: [0, 0, 0, 4, 0, 0, 0, 0, 1, 0],  # Ice Slasher
    3: [2, 4, 1, 1, 2, 10, 0, 2, 0, 0],  # Hyper Bomb
    4: [3, 1, 4, 1, 1, 2, 2, 2, 4, 1],  # Fire Storm
    5: [1, 10, 2, 1, 1, 1, 4, 2, 1, 1],  # Thunder Beam
    6: [14, -1, -1, -1, 4, 1, -1, -1, -1, -1],  # Super Arm
}

weapons_to_name: dict[int, str] = {
    1: "Rolling Cutter",
    2: "Ice Slasher",
    3: "Hyper Bomb",
    4: "Fire Storm",
    5: "Thunder Beam",
    6: "Super Arm",
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
    # 6: 2, purposefully excluded from validation logic
    # Super Arm isn't available in any refight, so we have to confirm it's beatable without it
}


def validate_fights(world: "MM1World", fights: list[int]):
    boss_health = {boss: 0x1C if boss != 12 else 0x1C * 2 for boss in [*range(8), 12]}

    weapon_energy = {key: float(0x1C) for key in weapon_costs}
    weapon_boss = {boss: {weapon: world.weapon_damage[weapon][boss] for weapon in world.weapon_damage}
                   for boss in fights}
    flexibility = {
        boss: (
                sum(damage_value > 0 for damage_value in
                    weapon_damages.values())  # Amount of weapons that hit this boss
                * sum(weapon_damages.values())  # Overall damage that those weapons do
        )
        for boss, weapon_damages in weapon_boss.items() if boss != 12
    }
    flexibility = sorted(flexibility, key=flexibility.get)  # Fast way to sort dict by value
    used_weapons = {i: set() for i in fights}
    for boss in [*flexibility, 12]:
        boss_damage = weapon_boss[boss]
        weapon_weight = {weapon: (weapon_energy[weapon] / damage) if damage else 0 for weapon, damage in
                         boss_damage.items() if weapon_energy[weapon] > 0}
        if boss_damage[8]:
            boss_damage[8] = 1.75 * boss_damage[8]
        if any(boss_damage[i] > 0 for i in range(8)) and 8 in weapon_weight:
            # We get exactly one use of Time Stopper during the rush
            # So we want to make sure that use is absolutely needed
            weapon_weight[8] = min(weapon_weight[8], 0.001)
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
    # worry about randomization later

    #static rules
    for boss, locations in boss_locations.items():
        if world.weapon_damage[0][boss] > 0:
            continue  # this can always be in logic
        weapons = []
        for weapon in range(1, 6):
            if world.weapon_damage[weapon][boss] > 0:
                if world.weapon_damage[weapon][boss] < minimum_weakness_requirement[weapon]:
                    continue  # Atomic Fire can only be considered logical for bosses it can kill in 2 hits
                weapons.append(weapons_to_name[weapon])
        if not weapons:
            raise Exception(f"Attempted to have boss {boss} with no weakness! Seed: {world.multiworld.seed}")
        for location in locations:
            add_rule(world.get_location(location), lambda state, weps=tuple(weapons): state.has_any(weps, world.player))

    # handle the wily rule
    set_rule(world.get_entrance(f"To Wily Stage 1"),
             lambda state: state.has("Magnet Beam", world.player) and
             state.has_any(["Thunder Beam", "Super Arm"], world.player)
             and state.has_group_unique("Weapons", world.options.required_weapons.value, world.player))

    # boss refight chaining
    add_rule(world.get_location("Wily Stage 2 - Elec Man Rematch"),
             lambda state: state.can_reach_location("Wily Stage 2 - Cut Man Rematch", world.player))
    add_rule(world.get_location("Copy Robot - Defeated"),
             lambda state: state.can_reach_location("Wily Stage 2 - Elec Man Rematch", world.player))
    add_rule(world.get_location("Wily Stage 2 - Complete"),
             lambda state: state.can_reach_location("Wily Stage 2 - Elec Man Rematch", world.player))

    add_rule(world.get_location("Wily Stage 4 - Fire Man Rematch"),
             lambda state: state.can_reach_location("Wily Stage 4 - Bomb Man Rematch", world.player))
    add_rule(world.get_location("Wily Stage 4 - Ice Man Rematch"),
             lambda state: state.can_reach_location("Wily Stage 4 - Fire Man Rematch", world.player))
    add_rule(world.get_location("Wily Stage 4 - Guts Man Rematch"),
             lambda state: state.can_reach_location("Wily Stage 4 - Ice Man Rematch", world.player))
    add_rule(world.get_location("Wily Machine - Defeated"),
             lambda state: state.can_reach_location("Wily Stage 4 - Guts Man Rematch", world.player))

