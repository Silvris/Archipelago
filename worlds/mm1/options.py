from Options import Choice, Toggle, Range, TextChoice, OptionDict, DeathLinkMixin, PerGameCommonOptions
from dataclasses import dataclass


class StartingRobotMaster(Choice):
    """
    The initial stage unlocked at the start.
    """
    display_name = "Starting Robot Master"
    option_cut_man = 0
    option_ice_man = 1
    option_bomb_man = 2
    option_fire_man = 3
    option_elec_man = 4
    option_guts_man = 5
    default = "random"


@dataclass
class MM1Options(PerGameCommonOptions, DeathLinkMixin):
    starting_robot_master: StartingRobotMaster
