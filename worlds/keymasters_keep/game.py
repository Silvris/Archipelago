from __future__ import annotations

import abc

from random import Random
from typing import Any, Dict, List, Optional, Tuple, Type

from .enums import KeymastersKeepGamePlatforms

from .game_objective_template import GameObjectiveTemplate


class AutoGameRegister(type):
    games: Dict[str, Type[Game]] = dict()
    metagames: Dict[str, Type[Game]] = dict()
    modded_games: Dict[str, Type[Game]] = dict()

    def __new__(mcs, name: str, bases: Tuple[type, ...], dict_: Dict[str, Any]) -> AutoGameRegister:
        new_class: Type[Game] = super().__new__(mcs, name, bases, dict_)

        if name != "Game" and new_class.should_autoregister:
            game_name: str = new_class.game_name_with_platforms()

            if "is_metagame" in dict_ and dict_["is_metagame"]:
                mcs.metagames[game_name] = new_class
            elif "is_modded_game" in dict_ and dict_["is_modded_game"]:
                mcs.modded_games[game_name] = new_class
            else:
                mcs.games[game_name] = new_class

        return new_class


class Game(metaclass=AutoGameRegister):
    name: str  # Official name of the game. Use a resource like IGDB to get the correct name
    platform: KeymastersKeepGamePlatforms  # Platform that the game integration was developed with and tested on

    # Other available platforms the game integration might work with
    platforms_other: Optional[List[KeymastersKeepGamePlatforms]] = None

    is_metagame: bool = False  # Whether the game should be considered a metagame for grouping purposes
    is_modded_game: bool = False  # Whether the game is a modded version of a base game. For grouping purposes

    is_adult_only_or_unrated: bool = True  # ESRB AO / PEGI 18 / USK 18 / Unrated? Used for filtering

    should_autoregister: bool = True  # Development flag. Used to prevent AutoGameRegister from registering the game

    archipelago_options: Any  # Archipelago options dataclass (for access)

    random: Random  # Random instance

    options_cls: Type = None  # Archipelago options type

    def __init__(self, random: Random = None, archipelago_options: Any = None) -> None:
        self.random = random or Random()
        self.archipelago_options = archipelago_options

    @property
    def only_has_difficult_objectives(self) -> bool:
        template: GameObjectiveTemplate
        for template in self.game_objective_templates():
            if not template.is_difficult:
                return False

        return True

    @property
    def only_has_time_consuming_objectives(self) -> bool:
        template: GameObjectiveTemplate
        for template in self.game_objective_templates():
            if not template.is_time_consuming:
                return False

        return True

    @abc.abstractmethod
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    @abc.abstractmethod
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        ...

    def filter_game_objective_templates(
        self,
        include_difficult: bool = False,
        include_time_consuming: bool = False,
    ) -> List[GameObjectiveTemplate]:
        filtered_objectives: List[GameObjectiveTemplate] = list()

        template: GameObjectiveTemplate
        for template in self.game_objective_templates():
            if not include_difficult and template.is_difficult:
                continue

            if not include_time_consuming and template.is_time_consuming:
                continue

            filtered_objectives.append(template)

        return filtered_objectives

    def generate_objectives(
        self,
        count: int = 1,
        include_difficult: bool = False,
        include_time_consuming: bool = False,
    ) -> Tuple[List[str], List[str]]:
        optional_constraints: List[str] = list()
        optional_constraint_templates: List[GameObjectiveTemplate] = self.optional_game_constraint_templates()

        if len(optional_constraint_templates):
            template: GameObjectiveTemplate = self.random.choice(self.optional_game_constraint_templates())
            optional_constraints.append(template.generate_game_objective(self.random))

        filtered_objectives: List[GameObjectiveTemplate] = self.filter_game_objective_templates(
            include_difficult=include_difficult,
            include_time_consuming=include_time_consuming,
        )

        weights: List[int] = [template.weight for template in filtered_objectives]

        selected_objectives: List[GameObjectiveTemplate] = self.random.choices(
            filtered_objectives, weights=weights, k=count
        )

        objectives: List[str] = list()

        for template in selected_objectives:
            passes: int = 0

            while True:
                passes += 1
                objective: str = template.generate_game_objective(self.random)

                if objective not in objectives or passes > 10:
                    objectives.append(objective)
                    break

        return optional_constraints, objectives

    @classmethod
    def game_name_with_platforms(cls) -> str:
        game_name = f"{cls.name} ({cls.platform.value}"

        if cls.platforms_other:
            game_name += " + "
            game_name += f"{', '.join(platform.value for platform in cls.platforms_other)}"

        game_name += ")"

        return game_name
