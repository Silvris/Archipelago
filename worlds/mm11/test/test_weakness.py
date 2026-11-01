import typing
from math import ceil

from .bases import MM11TestBase
from ..rules import bosses


# Need to figure out how this test should work
def validate_wily(base: MM11TestBase, boss_list: list[int]) -> None:
    # Wily validation
    weapon_energy = {idx: 56 for idx in range(1, 9)}
    wily_flexibility: list[tuple[int, float]] = sorted({idx: base.world.bosses[idx].get_flexibility()
                                                          for idx in boss_list}.items(), key=lambda x: x[1])
    wily_weapons = {}
    while wily_flexibility:
        idx, _ = wily_flexibility.pop(0)
        defeated, used = base.world.bosses[idx].can_defeat(weapon_energy)
        if not defeated:
            # we are out of weapons that can actually damage the boss
            base.fail(f"Ran out of weapon energy to damage "
                      f"{base.world.bosses[idx].name}\n"
                      f"Seed: {base.multiworld.seed}\n"
                      f"Damage Table: {base.world.bosses[idx].damage}")
        wily_weapons[idx].extend(x for x in used.keys() if x != 0)


class WeaknessTests(MM11TestBase):
    def test_that_every_boss_has_a_weakness(self) -> None:
        world = self.multiworld.worlds[self.player]
        for boss in world.bosses:
            self.assertTrue(boss.get_weakness())

    def test_wily_3(self) -> None:
        validate_wily(self, list(range(8)))

    def test_wily_4(self) -> None:
        validate_wily(self, [10, 11])


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
