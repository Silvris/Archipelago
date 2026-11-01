from dataclasses import dataclass

from Options import Choice, Toggle, DeathLink, TextChoice, Range, OptionDict, PerGameCommonOptions, Visibility
from schema import Schema, And, Use, Optional
from . import names
from .boss import DamageType, boss_names


class EnergyLink(Toggle):
    """
    Enables EnergyLink support.
    When enabled, pickups dropped from enemies are sent to the EnergyLink pool, and healing/weapon energy/1-Ups can
    be requested from the EnergyLink pool.
    Some of the energy sent to the pool will be lost on transfer.
    """
    display_name = "EnergyLink"


class StartingRobotMaster(Choice):
    """
    The initial stage unlocked at the start.
    """
    display_name = "Starting Robot Master"
    option_block_man = 0
    option_acid_man = 1
    option_impact_man = 2
    option_bounce_man = 3
    option_fuse_man = 4
    option_tundra_man = 5
    option_torch_man = 6
    option_blast_man = 7
    default = "random"


class Consumables(Choice):
    """
    When enabled, e-tanks/1-ups/health/weapon energy will be added to the pool of items and included as checks.
    """
    display_name = "Consumables"
    option_none = 0
    option_1up_etank = 1
    option_weapon_health = 2
    option_all = 3
    default = 1
    alias_true = 3
    alias_false = 0

    @classmethod
    def get_option_name(cls, value: int) -> str:
        if value == 1:
            return "1-Ups/E-Tanks"
        elif value == 2:
            return "Weapon/Health Energy"
        return super().get_option_name(value)


class SpeedPlatforming(Toggle):
    """
    When enabled, Torch Man's stage, the end of Block Man's stage, and Wily 2 will logically require you to have
    Speed Gear to complete them.
    """
    display_name = "Gearless Platforming"


class PaletteShuffle(TextChoice):
    """
    Change the color of Mega Man and the Robot Masters.
    None: The palettes are unchanged.
    Shuffled: Palette colors are shuffled amongst the robot masters.
    Randomized: Random (usually good) palettes are generated for each robot master.
    Singularity: one palette is generated and used for all robot masters.
    Supports custom palettes using HTML named colors in the
    following format: Mega Buster-Lavender|Violet;randomized
    The first value is the character whose palette you'd like to define, then separated by - is a set of 2 colors for
    that character. separate every color with a pipe, and separate every character as well as the remaining shuffle with
    a semicolon.
    """
    display_name = "Palette Shuffle"
    option_none = 0
    option_shuffled = 1
    option_randomized = 2
    option_singularity = 3


class EnemyWeaknesses(Toggle):
    """
    Randomizes the damage dealt to enemies by weapons. Certain enemies will always take damage from the buster.
    """
    display_name = "Random Enemy Weaknesses"
    visibility = Visibility.none


class StrictWeaknesses(Choice):
    """
    Only your starting Robot Master will take damage from the Mega Buster, the rest must be defeated with weapons.
    Weapons that only do 1-3 damage to bosses no longer deal damage.
    Include Charge: the Charge Buster is considered a weapon separate from the Mega Buster and may deal damage.
    """
    display_name = "Strict Boss Weaknesses"
    option_disabled = 0
    option_include_charge = 1
    option_enabled = 2
    alias_false = 0
    alias_true = 2


class RandomWeaknesses(Choice):
    """
    None: Bosses will have their regular weaknesses.
    Shuffled: Weapon damage will be shuffled amongst the weapons, so Shadow Blade may do Top Spin damage.
    Randomized: Weapon damage will be fully randomized.
    """
    display_name = "Random Boss Weaknesses"
    option_none = 0
    option_shuffled = 1
    option_randomized = 2
    alias_false = 0
    alias_true = 2


class Wily3Requirement(Range):
    """
    Change the amount of Robot Masters that are required to be defeated for
    the door to the Wily Machine to open.
    """
    display_name = "Wily 3 Requirement"
    default = 8
    range_start = 1
    range_end = 8


class WeaknessPlando(OptionDict):
    """
    Specify specific damage numbers for boss damage. Can be used even without strict/random weaknesses.
    plando_weakness:
        Robot Master:
            Weapon: Damage
    """
    display_name = "Plando Weaknesses"
    schema = Schema({
        Optional(And(str, Use(str.title), lambda s: s in boss_names)): {
            And(str, Use(str.title), lambda s: getattr(DamageType, s, None) is not None): And(int, lambda i: i in range(0, 20))
        }
    })
    default = {}


class MusicShuffle(Choice):
    """
    Shuffle the music that plays in every stage
    """
    display_name = "Music Shuffle"
    option_none = 0
    option_shuffled = 1
    option_randomized = 2
    option_no_music = 3
    default = 0


@dataclass
class MM11Options(PerGameCommonOptions):
    death_link: DeathLink
    energy_link: EnergyLink
    starting_robot_master: StartingRobotMaster
    consumables: Consumables
    speed_platforming: SpeedPlatforming
    enemy_weakness: EnemyWeaknesses
    strict_weakness: StrictWeaknesses
    random_weakness: RandomWeaknesses
    plando_weakness: WeaknessPlando
    wily_3_requirement: Wily3Requirement
    # palette_shuffle: PaletteShuffle
    music_shuffle: MusicShuffle
