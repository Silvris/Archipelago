import typing

from Options import Choice, Range, Toggle, DefaultOnToggle, NamedRange, PerGameCommonOptions
from dataclasses import dataclass


class MHRSDeathLink(Choice):
    """
    When you die, everyone dies. Of course the reverse is true too.
    Cart: Deathlinks are sent when the player carts, receiving a deathlink will cart the player.
    Quest: Deathlinks are sent when the player fails a quest, receiving a deathlink will fail the current quest.
    """
    display_name = "Death Link"
    option_none = 0
    option_cart = 1
    option_quest = 2
    default = 0


class RequiredKeys(Range):
    """
    Determines the percentage of "Key Quest" required to gain access to the final quest.
    """
    display_name = "Max Required Keys"
    range_start = 1
    range_end = 100
    default = 45


class TotalKeys(Range):
    """
    The max amount of key quests to add to the item pool. Fewer key quests may exist in the pool should the total be higher than
    the amount of available quests.
    """
    display_name = "Total Keys"
    range_start = 1
    range_end = 80
    default = 30


class FillerWeight(Range):
    """
    Replace a given percentage of non-required key quests with filler items.
    """
    display_name = "Filler Percentage"
    range_start = 0
    range_end = 100
    default = 25


class FinalBoss(Choice):
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
    option_velkhana = 19
    option_amatsu = 20
    option_primordial_malzeno = 21
    option_hunting_road = 22


class Apexes(Choice):
    """
    Enable: Adds the Apexes into the regular pool and final boss pool (no effect for specific boss settings)
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
    Enable: Adds the Risen into the regular pool and final boss pool (no effect for specific boss settings).
    Enforce: Replaces all Chameleos, Teostra, Kushala Daora, Valstrax, and Shagaru Magala with their Risen equivalents,
    and adds them to the final boss pool.
    Disable: Risen cannot be generated for quests.
    """
    display_name = "Include Risen"
    option_enable = 0
    option_enforce = 1
    option_disable = 2
    default = 0


class EnableAfflicted(Choice):
    """
    Enable: If a monster can be afflicted, it has a 50% chance of being afflicted.
    Enforce: All monsters that can be afflicted will be afflicted.
    Disable: Monsters cannot be afflicted.
    """
    display_name = "Enable Affliction"
    option_enable = 0
    option_enforce = 1
    option_disable = 2
    default = 0


class MasterRankGoal(Range):
    """
    What Master Rank must be reached to reach the final urgent quest.
    Ex. When set to 3, the urgent quest will be a 3★ quest and will require finishing the 1★ and 2★ urgents.
    """
    display_name = "Master Rank Requirement"
    range_start = 1
    range_end = 6
    default = 3


class AverageMonsterDifficulty(NamedRange):
    """
    The base difficulty of the generated monsters. This will be further scaled by the quest's MR.
    """
    display_name = "Base Monster Difficulty"
    range_start = 0
    range_end = 173
    default = 62
    special_range_names = {
        "easy": 36,
        "normal": 62,
        "hard": 107,
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
    Weapon group unlocks will be given progressively, from R8 to R9 to R10.
    """
    display_name = "Progressive Weapon Unlocks"


class ConsolidateWeapons(Toggle):
    """
    Weapon unlocks will be consolidated to unlock all weapon types at the same time, instead of individually.
    """
    display_name = "Consolidate Weapon Unlocks"


class ProgressiveArmor(Toggle):
    """
    Armor unlocks will be given progressively, from R8 to R10.
    """
    display_name = "Progressive Armor"


class ArenaOnly(Toggle):
    """
    Quests will only be generated in the following maps:
    Arena, Infernal Springs, Coral Palace, Yawning Abyss, Forlorn Arena
    """
    display_name = "Oops! All Arenas"


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


class FollowerStrength(NamedRange):
    """
    The strength of followers. By default, they do 14% of their theoretical damage.
    """
    display_name = "Follower Strength"
    range_start = 1
    range_end = 100
    default = 14
    special_range_names = {
        "default": 14,
        "double": 28,
        "quadruple": 56,
        "hunter": 100,
    }


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


@dataclass
class MHRSOptions(PerGameCommonOptions):
    death_link: MHRSDeathLink
    required_keys: RequiredKeys
    total_keys: TotalKeys
    filler_percentage: FillerWeight
    final_quest_target: FinalBoss
    master_rank_requirement: MasterRankGoal
    enable_affliction: EnableAfflicted
    include_apex: Apexes
    include_risen: Risens
    progressive_weapons: ProgressiveWeapons
    consolidate_weapons: ConsolidateWeapons
    progressive_armor: ProgressiveArmor
    arena_only: ArenaOnly
    average_monster_difficulty: AverageMonsterDifficulty
    monster_difficulty_deviation: MonsterDifficultyDeviation
    enable_followers: EnableFollowers
    follower_strength: FollowerStrength
    disable_multiplayer_scaling: DisableMultiplayerScaling
    give_khezu_music: GiveKhezuMusic
