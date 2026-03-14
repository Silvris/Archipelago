from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions


class StartingBoard(Choice):
    """The first unlocked board"""
    display_name = "Starting Board"
    default = "random"
    option_ruby = 0
    option_sapphire = 1


@dataclass
class PokemonPinballRSOptions(PerGameCommonOptions):
    starting_board: StartingBoard
