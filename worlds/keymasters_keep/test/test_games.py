from . import KMKTestBase
from ..game import AutoGameRegister


class TestGames(KMKTestBase):
    def run_default_tests(self) -> bool:
        return False

    def test_game_implementations(self):
        for name, game_cls in AutoGameRegister.games.items():
            random = self.multiworld.worlds[1].random
            with self.subTest(game=name):
                game = game_cls(random, True, True, self.multiworld.worlds[1].options)

                optional_objectives = game.optional_game_constraint_templates()
                for objective in optional_objectives:
                    assert isinstance(objective.generate_game_objective(random), str)

                game_objectives = game.game_objective_templates()

                for objective in game_objectives:
                    assert isinstance(objective.generate_game_objective(random), str)
