from Options import PerGameCommonOptions, Range, Choice
from dataclasses import dataclass

class RequiredSubgames(Range):
    """
    How many subgames must be completed for the game to be considered complete.
    """
    display_name = "Required Sub-Games"
    range_start = 1
    range_end = 7
    default = 6

class StartingSubgame(Choice):
    """
    The subgame that will be unlocked by default.
    """
    display_name = "Starting Subgame"
    option_spring_breeze = 0
    option_dyna_blade = 1
    option_gourmet_race = 2
    option_the_great_cave_offensive = 3
    option_revenge_of_meta_knight = 4
    option_milky_way_wishes = 5
    option_the_arena = 6
    default = 0

@dataclass
class KSSOptions(PerGameCommonOptions):
    required_subgames: RequiredSubgames
    starting_subgame: StartingSubgame