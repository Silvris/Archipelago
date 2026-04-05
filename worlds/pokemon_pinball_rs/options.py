from dataclasses import dataclass
from Options import Choice, OptionSet, Range, PerGameCommonOptions
from .names import POKEDEX, SPECIES_GROUDON, SPECIES_KYOGRE, SPECIES_RAYQUAZA, SPECIES_JIRACHI


class Difficulty(Choice):
    """Whether logic should apply additional restrictions on locations
    Normal: All locations other than catching have additional requirements"""
    option_normal = 0
    option_hard = 1
    option_expert = 2
    option_master = 3


class Goal(OptionSet):
    """What is considered the goal for Pokemon Pinball:
    Including multiple options will require all to have been met
    Pokédex: a required number of Pokémon are registered within the Pokédex
    Score: a certain target score is reached on either the Ruby or Sapphire board (must be registered to the high scores)
    Targets: certain specific target Pokémon have been captured
    """
    display_name = "Goal"
    default = frozenset({"Pokedex"})
    valid_keys = frozenset({"Pokedex", "Score", "Targets"})


class StartingBoard(Choice):
    """The first unlocked board"""
    display_name = "Starting Board"
    default = "random"
    option_ruby = 0
    option_sapphire = 1


class PokedexRequirement(Range):
    """On Pokédex goal, the amount of Pokémon registered required to goal."""
    display_name = "Pokédex Requirement"
    default = 125
    range_start = 1
    range_end = 205


class ScoreRequirement(Range):
    """On Score goal, the required score for goal."""
    display_name = "Score Requirement"
    default = 0
    range_start = 0
    range_end = 100000000000  # you can technically go more than this, but this is 10 rayquaza


class PokemonTargets(OptionSet):
    """On Targets goal, what specific Pokémon are required for goal."""
    display_name = "Pokémon Targets"
    default = frozenset({SPECIES_GROUDON, SPECIES_KYOGRE, SPECIES_RAYQUAZA, SPECIES_JIRACHI})
    valid_keys = frozenset(POKEDEX.keys())


@dataclass
class PokemonPinballRSOptions(PerGameCommonOptions):
    goal: Goal
    difficulty: Difficulty
    starting_board: StartingBoard
    pokedex_requirement: PokedexRequirement
    score_requirement: ScoreRequirement
    pokemon_targets: PokemonTargets
