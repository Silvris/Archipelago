from Options import PerGameCommonOptions, Range, Choice, OptionSet
from dataclasses import dataclass


subgame_mapping = {
        0: "Spring Breeze",
        1: "Dyna Blade",
        2: "Gourmet Race",
        3: "The Great Cave Offensive",
        4: "Revenge of Meta Knight",
        5: "Milky Way Wishes",
        6: "The Arena"
}


class RequiredSubgameCompletions(Range):
    """
    How many subgames must be completed for the game to be considered complete.
    """
    display_name = "Required Sub-Games"
    range_start = 1
    range_end = 7
    default = 6


class RequiredSubgames(OptionSet):
    """
    Which subgames are required to be completed for the game to be considered complete.
    """
    display_name = "Included Subgames"
    valid_keys = {
        "Spring Breeze",
        "Dyna Blade",
        "Gourmet Race",
        "The Great Cave Offensive",
        "Revenge of Meta Knight",
        "Milky Way Wishes",
        "The Arena"
    }
    default = ("Milky Way Wishes", )


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


class IncludedSubgames(OptionSet):
    """
    Which subgames should be included as locations.
    """
    display_name = "Included Subgames"
    valid_keys = {
        "Spring Breeze",
        "Dyna Blade",
        "Gourmet Race",
        "The Great Cave Offensive",
        "Revenge of Meta Knight",
        "Milky Way Wishes",
        "The Arena"
    }
    default = valid_keys


class MilkyWayWishesMode(Choice):
    """
    Determines how Marx is unlocked in Milky Way Wishes.
    Local: Marx is unlocked after completing the 7 main planets
    (Floria, Aqualiss, Skyhigh, Hotbeat, Cavios, Mecheye, Halfmoon)
    Multiworld: Marx is unlocked after receiving 7 Rainbow Stars scattered across the multiworld
    """
    display_name = "Milky Way Wishes Mode"
    option_local = 0
    option_multiworld = 1
    default = 0


@dataclass
class KSSOptions(PerGameCommonOptions):
    required_subgame_completions: RequiredSubgameCompletions
    required_subgames: RequiredSubgames
    starting_subgame: StartingSubgame
    included_subgames: IncludedSubgames
    milky_way_wishes_mode: MilkyWayWishesMode
