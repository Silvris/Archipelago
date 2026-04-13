from dataclasses import dataclass
from Options import Choice, OptionSet, Range, Toggle, PerGameCommonOptions
from .names import POKEDEX, SPECIES_GROUDON, SPECIES_KYOGRE, SPECIES_RAYQUAZA, SPECIES_JIRACHI


class Difficulty(Choice):
    """Whether logic should apply additional restrictions on locations
    Normal: All locations other than catching have additional requirements
    Hard: Simple board tasks such as hatching and evolutions have no additional requirements
    Expert: Longer board tasks such as 25+ multiplier bumper hits and catching Groudon/Kyogre have no additional requirements
    Master: No locations have additional requirements other than what is strictly required"""
    display_name = "Difficulty"
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


class BonusMultChecks(Range):
    """Number of bonus multiplier hits to include as checks per-board"""
    display_name = "Bonus Multiplier Checks"
    default = 0
    range_start = 0
    range_end = 99


class BallUpgradeChecks(Range):
    """Number of ball upgrades to include as checks. This includes both the ball upgrades """
    display_name = "Ball Upgrade Checks"
    default = 0
    range_start = 0
    range_end = 99


class EvoMode(Choice):
    """Evo Mode Behavior
    Arrows: Each arrow of Evo mode is split up and added to the pool.
    Full: All arrows are condensed into a single item and added to the pool.
    Start With: Start with Evo Mode.
    """
    display_name = "Evo Mode"
    default = 0
    option_arrows = 0
    option_full = 1
    option_start_with = 2


class CollectPokedex(Toggle):
    """Whether server collects should apply to Pokédex locations. This can cause goaling if all goals are tied to
    Pokédex locations."""
    display_name = "Collect Pokédex"


@dataclass
class PokemonPinballRSOptions(PerGameCommonOptions):
    goal: Goal
    difficulty: Difficulty
    starting_board: StartingBoard
    pokedex_requirement: PokedexRequirement
    score_requirement: ScoreRequirement
    pokemon_targets: PokemonTargets
    bonus_multiplier_checks: BonusMultChecks
    ball_upgrade_checks: BallUpgradeChecks
    evo_mode: EvoMode
    collect_pokedex: CollectPokedex
