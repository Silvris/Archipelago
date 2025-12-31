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

enemy_indexes: dict[str, int] = {
    "Bunby Heli": 0x00,
    "Metall": 0x01,
    "Kamadoma": 0x02,
    "Gabyoall": 0x03,
    "Adhering Suzy (Vertical)": 0x04,
    "Screw Driver": 0x05,
    "Peng": 0x07,
    "Killer Bomb": 0x08,
    "Big Eye": 0x09,
    "Mambu": 0x0A,
    "Blaster": 0x0B,
    "Super Cutter": 0x11,
    "Sniper Joe": 0x12,
    "Pickelman": 0x15,
    "Screw Driver (Upside Down)": 0x16,
    "Crazy Razy (Head)": 0x1D,
    "Crazy Razy (Body)": 0x1E,
    "Crazy Razy (Separate Head)": 0x1F,
    "Adhering Suzy (Horizontal)": 0x21,
    "Watcher": 0x2A,
    "Changkey": 0x31,
    "CWU-001": 0x3A,
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
        Optional(And(str, Use(str.title), lambda s: s in bosses or s in enemy_indexes)): {
            And(str, Use(str.title), lambda s: s in weapons_to_id): And(int, lambda i: i in range(-1, 15))
        }
    })
    default = {}


class Consumables(Toggle):
    """
    Whether in-stage consumable pickups should be randomized. This includes the Yashichi.
    """
    display_name = "Consumables"


class EnergyLink(Toggle):
    """
    Enables EnergyLink support.
    When enabled, pickups dropped from enemies are sent to the EnergyLink pool, and healing/weapon energy/1-Ups can
    be requested from the EnergyLink pool.
    Some of the energy sent to the pool will be lost on transfer.
    """
    display_name = "EnergyLink"
    visibility = Visibility.none


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


class RandomMusic(Choice):
    """
    Vanilla: music is unchanged
    Shuffled: stage and certain menu music is shuffled.
    Randomized: stage and certain menu music is randomly selected
    None: no music will play
    """
    display_name = "Random Music"
    option_vanilla = 0
    option_shuffled = 1
    option_randomized = 2
    option_none = 3


@dataclass
class MM1Options(PerGameCommonOptions, DeathLinkMixin):
    starting_robot_master: StartingRobotMaster
    required_weapons: RequiredWeapons
    strict_weakness: StrictWeaknesses
    random_weakness: RandomWeaknesses
    plando_weakness: WeaknessPlando
    enemy_weakness: EnemyWeaknesses
    consumables: Consumables
    energy_link: EnergyLink
    palette_shuffle: PaletteShuffle
    random_music: RandomMusic
