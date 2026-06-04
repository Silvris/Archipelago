import typing

from .bases import MMTestBase
from ..rules import minimum_weakness_requirement, validate_fights


class WeaknessTests(MMTestBase):
    def test_that_every_boss_has_a_weakness(self) -> None:
        world = self.multiworld.worlds[self.player]
        weapon_damage = world.weapon_damage
        min_weakness = minimum_weakness_requirement.copy()
        if world.options.enhanced_super_arm:
            min_weakness[6] = 2
        for boss in range(11):
            if not any(weapon_damage[weapon][boss] >= minimum_weakness_requirement[weapon] for weapon in range(7)):
                self.fail(f"Boss {boss} generated without weakness! Seed: {self.multiworld.seed}")

    def test_wily_4(self) -> None:
        validate_fights(self.multiworld.worlds[self.player], (1, 2, 3, 5, 9, 10), True)


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

    def world_setup(self, seed: typing.Optional[int] = None) -> None:
        super().world_setup(48191693440614706382)


class ShuffledStrictWeaknessTests(WeaknessTests):
    options = {
        "strict_weakness": True,
        "random_weakness": "shuffled",
    }

    def world_setup(self, seed: typing.Optional[int] = None) -> None:
        super().world_setup(8198841857882385550)

class StrictWeaknessTestsSuperArm(WeaknessTests):
    options = {
        "strict_weakness": True,
        "enhanced_super_arm": True,
    }


class RandomWeaknessTestsSuperArm(WeaknessTests):
    options = {
        "random_weakness": "randomized",
        "enhanced_super_arm": True,
    }


class ShuffledWeaknessTestsSuperArm(WeaknessTests):
    options = {
        "random_weakness": "shuffled",
        "enhanced_super_arm": True,
    }


class RandomStrictWeaknessTestsSuperArm(WeaknessTests):
    options = {
        "strict_weakness": True,
        "random_weakness": "randomized",
        "enhanced_super_arm": True,
    }

    def world_setup(self, seed: typing.Optional[int] = None) -> None:
        super().world_setup(37505858307061695899)


class ShuffledStrictWeaknessTestsSuperArm(WeaknessTests):
    options = {
        "strict_weakness": True,
        "random_weakness": "shuffled",
        "enhanced_super_arm": True,
    }
