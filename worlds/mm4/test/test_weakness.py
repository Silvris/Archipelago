import typing
from math import ceil

from .bases import MM4TestBase
from ..rules import minimum_weakness_requirement, bosses


# Need to figure out how this test should work
def validate_wily_3(base: MM4TestBase) -> None:
    world = base.multiworld.worlds[base.player]
    weapon_damage = world.weapon_damage
    weapon_costs = {
        0: 0,
        1: 4,
        2: 4,
        3: 1,
        4: 2,
        5: 1,
        6: 1,
        7: 1,
        8: 2,
    }
    boss_health = {boss: 0x1C for boss in (*range(8), 14, 15)}
    weapon_energy = {key: float(0x1C) for key in weapon_costs if key not in (9, 10) or world.options.random_rush}
    weapon_boss = {boss: {weapon: world.weapon_damage[weapon][boss] for weapon in world.weapon_damage
                          if weapon not in (9, 10) or world.options.random_rush}
                   for boss in (*range(8), 14, 15)}
    flexibility = {
        boss: (
                sum(damage_value > 0 for damage_value in
                    weapon_damages.values())  # Amount of weapons that hit this boss
                * sum(weapon_damages.values())  # Overall damage that those weapons do
        )
        for boss, weapon_damages in weapon_boss.items() if boss not in (14, 15)
    }
    boss_flexibility = sorted(flexibility, key=flexibility.get)  # Fast way to sort dict by value
    used_weapons: dict[int, set[int]] = {i: set() for i in (*range(8), 14, 15)}
    for boss in [*boss_flexibility, 14, 15]:
        boss_damage = weapon_boss[boss]
        weapon_weight = {weapon: (weapon_energy[weapon] / damage) if damage else 0 for weapon, damage in
                         boss_damage.items() if weapon_energy[weapon] > 0}
        while boss_health[boss] > 0:
            if boss_damage[0] > 0:
                boss_health[boss] = 0  # if we can buster, we should buster
                continue
            highest, wp = max(zip(weapon_weight.values(), weapon_weight.keys()))
            uses = weapon_energy[wp] // weapon_costs[wp]
            used_weapons[boss].add(wp)
            if int(uses * boss_damage[wp]) > boss_health[boss]:
                used = ceil(boss_health[boss] / boss_damage[wp])
                weapon_energy[wp] -= weapon_costs[wp] * used
                boss_health[boss] = 0
            elif highest <= 0:
                # we are out of weapons that can actually damage the boss
                base.fail(f"Ran out of weapon energy to damage "
                          f"{next(name for name in bosses if bosses[name] == boss)}\n"
                          f"Seed: {base.multiworld.seed}\n"
                          f"Damage Table: {weapon_damage}")
            else:
                # drain the weapon and continue
                boss_health[boss] -= int(uses * boss_damage[wp])
                weapon_energy[wp] -= weapon_costs[wp] * uses
                weapon_weight.pop(wp)


class WeaknessTests(MM4TestBase):
    def test_that_every_boss_has_a_weakness(self) -> None:
        world = self.multiworld.worlds[self.player]
        weapon_damage = world.weapon_damage
        for boss in range(17):
            if not any(weapon_damage[weapon][boss] >= minimum_weakness_requirement[weapon] for weapon in range(9)):
                self.fail(f"Boss {boss} generated without weakness! Seed: {self.multiworld.seed}")

    def test_wily_3(self) -> None:
        validate_wily_3(self)


class StrictWeaknessTests(WeaknessTests):
    options = {
        "strict_weakness": True,
    }


class RandomWeaknessTests(WeaknessTests):
    options = {
        "random_weakness": "randomized"
    }


class ShuffledWeaknessTests(WeaknessTests):
    options = {
        "random_weakness": "shuffled"
    }


class RandomStrictWeaknessTests(WeaknessTests):
    options = {
        "strict_weakness": True,
        "random_weakness": "randomized",
    }


class ShuffledStrictWeaknessTests(WeaknessTests):
    options = {
        "strict_weakness": True,
        "random_weakness": "shuffled"
    }

    def world_setup(self, seed: typing.Optional[int] = None) -> None:
        super().world_setup(28108592829562768234)
