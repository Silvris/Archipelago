from Options import Choice, Toggle, Range, TextChoice, OptionDict, DeathLinkMixin, PerGameCommonOptions, Visibility
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


class RequiredWeapons(Range):
    """
    Number of weapons required to be received in order to unlock Wily's Castle.
    Note that at least one of the Super Arm or Elec Beam will always be required, alongside the Magnet Beam.
    """
    display_name = "Required Weapon Count"
    range_start = 1
    range_end = 6
    default = 3


class Consumables(Toggle):
    """
    Whether in-stage consumable pickups should be randomized. This includes the Yashichi.
    """
    display_name = "Consumables"
    visibility = Visibility.none


class EnergyLink(Toggle):
    """
    Enables EnergyLink support.
    When enabled, pickups dropped from enemies are sent to the EnergyLink pool, and healing/weapon energy/1-Ups can
    be requested from the EnergyLink pool.
    Some of the energy sent to the pool will be lost on transfer.
    """
    display_name = "EnergyLink"
    visibility = Visibility.none


@dataclass
class MM1Options(PerGameCommonOptions, DeathLinkMixin):
    starting_robot_master: StartingRobotMaster
    required_weapons: RequiredWeapons
    consumables: Consumables
    energy_link: EnergyLink
