from dataclasses import dataclass
from Options import Choice, OptionSet, Range, Toggle, PerGameCommonOptions, DeathLinkMixin
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
    Medals: receiving a certain number of Pokédex Medals from the multiworld
    """
    display_name = "Goal"
    default = frozenset({"Pokedex"})
    valid_keys = frozenset({"Pokedex", "Score", "Targets", "Medals"})


class StartingBoard(Choice):
    """The first unlocked board"""
    display_name = "Starting Board"
    default = "random"
    option_ruby = 0
    option_sapphire = 1


class SingleBoard(Toggle):
    """If enabled, only items/locations associated with your starting board will be created."""
    display_name = "Single Board Mode"


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


class TotalMedals(Range):
    """On Medals goal, maximum number of medals to include in the pool of items.
    The exact number may be less depending on settings.
    """
    display_name = "Max Medal Count"
    range_start = 1
    range_end = 255  # not storing this in more than a byte
    default = 75


class RequiredMedals(Range):
    """Percentage of Pokédex Medals required to goal."""
    display_name = "Required Medal Count"
    range_start = 1
    range_end = 100
    default = 66


class GoalTrigger(Choice):
    """Defines what triggers goal once all targets have been reached.
    Ball: goal is triggered at the end of the current ball.
    Groudon/Kyogre: goal is triggered when Groudon or Kyogre are defeated while all goal targets have been met.
    Rayquaza: goal is triggered when Rayquaza is defeated while all goal targets have been met.
    """
    display_name = "Goal Trigger"
    option_ball = 0
    option_groudon_kyogre = 1
    option_rayquaza = 2
    default = 0

    @classmethod
    def get_option_name(cls, value: int) -> str:
        if value == 1:
            return "Groudon/Kyogre"
        return super().get_option_name(value)


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


class ShopTracks(Range):
    """Number of available shop tracks available per board."""
    display_name = "Shop Tracks"
    range_start = 0
    range_end = 5
    default = 3


class ShopTrackLength(Range):
    """Number of available locations per shop track."""
    display_name = "Shop Track Length"
    range_start = 1
    range_end = 15
    default = 10


class ShopPrices(Choice):
    """
    Low: Shop prices linearly increase by 5.
    Medium: Shop prices follow an exponential curve of 1.65.
    High: Shop prices linearly increase by 10.
    """
    display_name = "Shop Prices"
    option_low = 1
    option_medium = 2
    option_high = 3
    default = 1


class RouletteChecks(Range):
    """Number of checks locked behind roulette prizes per board.
    Note that Zigzagoon is not considered in logic for these locations."""
    display_name = "Roulette Locations"
    range_start = 0
    range_end = 40
    default = 5


class EvoMode(Choice):
    """Evo Mode Behavior
    Arrows: Each arrow of Evo mode is split up and added to the pool.
    Full: All arrows are condensed into a single item and added to the pool.
    Start With: Evo Mode is placed within your starting inventory.
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


class RingLink(Toggle):
    """Links coin gain/loss with other players."""
    display_name = "RingLink"


@dataclass
class PokemonPinballRSOptions(PerGameCommonOptions, DeathLinkMixin):
    goal: Goal
    difficulty: Difficulty
    starting_board: StartingBoard
    single_board: SingleBoard
    pokedex_requirement: PokedexRequirement
    score_requirement: ScoreRequirement
    pokemon_targets: PokemonTargets
    total_medals: TotalMedals
    medal_requirement: RequiredMedals
    goal_trigger: GoalTrigger
    bonus_multiplier_checks: BonusMultChecks
    ball_upgrade_checks: BallUpgradeChecks
    shop_tracks: ShopTracks
    shop_track_length: ShopTrackLength
    shop_prices: ShopPrices
    roulette_prizes: RouletteChecks
    evo_mode: EvoMode
    collect_pokedex: CollectPokedex
    ringlink: RingLink
