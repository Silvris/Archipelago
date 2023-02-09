import typing

from Options import Option, DeathLink, Choice, Range, Toggle, DefaultOnToggle, TextChoice, SpecialRange


class NumericGoal(Range):
    """
    Determines the number of "Proof of a Hero" required to gain access to the final quest.
    """
    display_name = "Required Proofs"
    range_start = 1
    range_end = 7
    default = 3


class Goal(Choice):
    """
    Determines the monster present within the final urgent quest.
    <monster>: This monster will be the singular target of the quest
    Hunting Road: A 5-monster endurance quest
    Random All: Includes all individual monsters as well as the Hunting Road.
    Random Single: Includes all individual monsters.
    """
    display_name = "Final Quest Target"
    option_random_all = 0
    option_random_single = 1
    option_gaismagorm = 2
    option_kushala_daora = 3
    option_chameleos = 4
    option_teostra = 5
    option_scorned_magnamalo = 6
    option_malzeno = 7
    option_shagaru_magala = 8
    option_crimson_glow_valstrax = 9
    option_wind_serpent_ibushi = 10
    option_narwa_the_allmother = 11
    option_gold_rathian = 12
    option_silver_rathalos = 13
    option_lucent_nargacuga = 14
    option_flaming_espinas = 15
    option_violet_mizutsune = 16
    option_furious_rajang = 17
    option_chaotic_gore_magala = 18
    # option_velkhana = 19
    # option_amatsu = 20 #future-proofing :>
    option_hunting_road = 21


class Apexes(Choice):
    """
    Enable: Adds the Apexes into the regular pool and final boss pool (no effect for specific boss seeds)
    Enforce: Replaces all Arzuros, Rathian, Mizutsune, Rathalos, Zinogre, and Diablos with their Apex equivalents,
    and adds them to the final boss pool.
    Disable: Apexes cannot be generated for quests.
    """
    display_name = "Include Apexes"
    option_enable = 0
    option_enforce = 1
    option_disable = 2
    default = 0


class Risens(Choice):
    """
    Enable: Adds the Risen into the regular pool and final boss pool (no effect for specific boss seeds).
    Enforce: Replaces all Chameleos, Teostra, and Kushala Daora with their Risen equivalents.
    Disable: Risen cannot be generated for quests.
    """
    display_name = "Include Risen"
    option_enable = 0
    option_enforce = 1
    option_disable = 2
    default = 0


class EnableAfflicted(DefaultOnToggle):
    """
    Allow monsters to be Afflicted if they support it.
    """
    display_name = "Enable Affliction"


class MasterRankGoal(Range):
    """
    What Master Rank must be reached to reach the final urgent quest.
    Ex. When set to 3, the urgent quest will be a 3★ quest and will require finishing the 1★ and 2★ urgents.
    """
    display_name = "Master Rank Requirement"
    range_start = 1
    range_end = 6
    default = 3


class AverageMonsterDifficulty(SpecialRange):
    """
    The average difficulty of the generated monsters. This will be further scaled by the quest's MR.
    """
    display_name = "Average Monster Difficulty"
    range_start = 0
    range_end = 172
    default = 62
    special_range_names = {
        "easy": 36,
        "normal": 62,
        "hard": 107
    }


class MonsterDifficultyDeviation(Range):
    """
    The general amount difficulty should be allowed to deviate from the average.
    """
    display_name = "Monster Difficulty Deviation"
    range_start = 1
    range_end = 100
    default = 25


class ProgressiveWeapons(DefaultOnToggle):
    """
    Weapon group unlocks will be given progressively, from R1-3 to R4-5 to R6-7 to R8-9 to R10.
    """
    display_name = "Progressive Weapon Unlocks"


class ConsolidateWeapons(Toggle):
    """
    Weapon unlocks will be consolidated to unlock all weapon types at the same time, instead of individually.
    """
    display_name = "Consolidate Weapon Unlocks"


class ProgressiveArmor(Toggle):
    """
    Armor unlocks will be given progressively, from R1 to R10.
    """
    display_name = "Progressive Armor"


class EnableFollowers(Choice):
    """
    Randomized: Followers are added to the item pool and are unlocked as they are received.
    Enabled: All Followers are unlocked and can be used.
    Disabled: All Followers are locked and cannot be used.
    """
    display_name = "Followers"
    option_randomized = 0
    option_enabled = 1
    option_disabled = 2
    default = 0


class FollowerStrength(Range):
    """
    The strength of followers. By default, they do 14% of their theoretical damage.
    """
    display_name = "Follower Strength"
    range_start = 1
    range_end = 100
    default = 14


class GiveKhezuMusic(Toggle):
    """
    Poor Khezu has been denied a theme for years, but now you can finally give him the music he deserves.
    """
    display_name = "Give Khezu Music"
    # this gives him a random monster's music, including the small monster music


class DisableMultiplayerScaling(Toggle):
    """
    Disabling Multiplayer Scaling will keep the monster with constant stats no matter the number of players present in
    the quest.
    """
    display_name = "Disable Multiplayer Scaling"


class MultiplayerGroup(TextChoice):
    """
    An identifier for groups that would like to play multiplayer.
    For groups that would like to play multiplayer, this and the following options must be identical for all players:
    Master Rank Requirement
    Enable Affliction
    Include Apex
    Include Risen
    Average Monster Difficulty
    Disable Multiplayer Scaling
    """
    display_name = "Multiplayer Group"
    # this gets passed to a dict that stores generated quest seeds,
    # so quests (but not items) can be sync'd across players
    option_group_1 = 1
    option_group_2 = 2
    option_group_3 = 3
    option_group_4 = 4


mhrs_options: typing.Dict[str, type(Option)] = {
    "death_link": DeathLink,
    "required_proofs": NumericGoal,
    "final_quest_target": Goal,
    "master_rank_requirement": MasterRankGoal,
    "enable_affliction": EnableAfflicted,
    "include_apex": Apexes,
    "include_risen": Risens,
    "progressive_weapons": ProgressiveWeapons,
    "consolidate_weapons": ConsolidateWeapons,
    "progressive_armor": ProgressiveArmor,
    "average_monster_difficulty": AverageMonsterDifficulty,
    "monster_difficulty_deviation": MonsterDifficultyDeviation,
    "enable_followers": EnableFollowers,
    "disable_multiplayer_scaling": DisableMultiplayerScaling,
    "multiplayer_group": MultiplayerGroup,
    "give_khezu_music": GiveKhezuMusic
}
