from dataclasses import dataclass
from Options import Choice, Toggle, Range, TextChoice, OptionDict, DeathLinkMixin, PerGameCommonOptions, Visibility
from schema import Schema, And, Use, Optional


robot_masters = {
    0: "Cut Man",
    1: "Ice Man",
    2: "Bomb Man",
    3: "Fire Man",
    4: "Elec Man",
    5: "Guts Man",
}

bosses = {
    **{value: key for key, value in robot_masters.items()},
    "Yellow Devil": 6,
    "Copy Robot": 7,
    "CWU-01P": 8,
    "Wily Machine": 9,
}

weapons_to_id: dict[str, int] = {
    "Rolling Cutter": 1,
    "Ice Slasher": 2,
    "Hyper Bomb": 3,
    "Fire Storm": 4,
    "Thunder Beam": 5,
    "Super Arm": 6,
}

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

class EnemyWeaknesses(Toggle):
    """
    Randomizes the damage dealt to enemies by weapons.
    """
    display_name = "Random Enemy Weaknesses"
    visibility = Visibility.none


class StrictWeaknesses(Toggle):
    """
    Only your starting Robot Master will take damage from the Mega Buster, the rest must be defeated with weapons.
    Weapons that only do 1-3 damage to bosses no longer deal damage (aside from Alien).
    """
    display_name = "Strict Boss Weaknesses"


class RandomWeaknesses(Choice):
    """
    None: Bosses will have their regular weaknesses.
    Shuffled: Weapon damage will be shuffled amongst the weapons, so Elec Beam may do Rolling Cutter damage.
    Super Arm will do a random amount of damage to susceptible bosses.
    Randomized: Weapon damage will be fully randomized.
    """
    display_name = "Random Boss Weaknesses"
    option_none = 0
    option_shuffled = 1
    option_randomized = 2
    alias_false = 0
    alias_true = 2


class WeaknessPlando(OptionDict):
    """
    Specify specific damage numbers for boss damage. Can be used even without strict/random weaknesses.
    plando_weakness:
        Robot Master:
            Weapon: Damage
    """
    display_name = "Plando Weaknesses"
    schema = Schema({
        Optional(And(str, Use(str.title), lambda s: s in bosses)): {
            And(str, Use(str.title), lambda s: s in weapons_to_id): And(int, lambda i: i in range(-1, 15))
        }
    })
    default = {}


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
    strict_weakness: StrictWeaknesses
    random_weakness: RandomWeaknesses
    plando_weakness: WeaknessPlando
    consumables: Consumables
    energy_link: EnergyLink
