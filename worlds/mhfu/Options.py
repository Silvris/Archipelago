from Options import DeathLink, Choice, Toggle, DefaultOnToggle, PerGameCommonOptions, Range, NamedRange
from dataclasses import dataclass


class Goal(Choice):
    """
    Village Low: Complete the Village Elder Urgent Quest "A State of Crisis!"
    Village High: Complete the Nekoht Quest "Rise to the Summit"
    Monster Hunter: Complete the Nekoht Quest "Monster Hunter"
    Low Rank: Complete the Low->High Urgent Quest "The Approaching Gaoren"
    High Rank: Complete the High Rank Urgent Quest "Rise to the Summit"
    G Rank: Complete the G Rank Urgent Quest "Absolute Zero"
    Fatalis: Complete the G Rank Special Quest "Legendary Black Dragon"
    Crimson Fatalis: Complete the G Rank Special Quest "The End Times"
    White Fatalis: Complete the G Rank Special Quest "Ancestral Dragon"
    """
    display_name = "Goal"
    option_village_low = 0
    option_village_high = 1
    option_monster_hunter = 2
    option_low_rank = 3
    option_high_rank = 4
    option_g_rank = 5
    option_fatalis = 6
    option_crimson_fatalis = 7
    option_white_fatalis = 8
    default = 4


class GuildQuestDepth(Choice):
    """
    What ranks to consider as checks. All ranks prior to the selected rank will be added.
    Unranked is considered to be a part of Low Rank.
    """
    display_name = "Guild Quest Depth"
    option_none = 0
    option_low_rank = 1
    option_high_rank = 2
    option_g_rank = 3
    default = 2


class VillageQuestDepth(Choice):
    """
    What Village ranks to consider as checks. All ranks prior to the selected rank will be added.
    """
    display_name = "Village Quest Depth"
    option_none = 0
    option_low_rank = 1
    option_high_rank = 2
    default = 1


class TrainingQuests(DefaultOnToggle):
    """
    Enables checks for successfully clearing a Training quest.
    """
    display_name = "Training Quests"


class TreasureQuests(DefaultOnToggle):
    """
    Enables checks for reaching specific thresholds within the Treasure quests provided by Treshi.
    """
    display_name = "Treasure Quests"


class TotalKeyQuests(Range):
    """
    Maximum number of key quests to include in the pool of items.
    This number may not be exact depending on other settings.
    """
    display_name = "Total Key Quests"
    range_start = 25  # set to 25 because we don't want it too low
    range_end = 250  # this is mostly a guess tbh
    default = 100


class RequiredKeyQuests(Range):
    """
    Percentage of key quests required to unlock the final urgent quest.
    """
    display_name = "Required Key Quests"
    range_start = 1
    range_end = 100
    default = 50


class FillerPercentage(Range):
    """
    Percentage of non-required Key Quests to be converted to filler items (random weapons/armor/decorations).
    """
    display_name = "Filler Percentage"
    range_start = 0
    range_end = 100
    default = 50


class TrapPercentage(Range):
    """
    Percentage of filler items to be converted to trap items.
    """
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 50


class Weapons(Choice):
    """
    Individual: Each individual weapon tree rank can be received separately, not in sequence.
    Progressive: Each individual weapon tree rank is received in sequence from 1 to 10.
    Consolidated: All weapon trees are consolidated into a single item for each rank.
    Progressive Consolidated: All weapon trees are consolidated into a single item, received in sequence.
    """
    display_name = "Weapon Tree"
    option_individual = 0
    option_progressive = 1
    option_consolidated = 2
    option_progressive_consolidated = 3
    default = 1


class ProgressiveArmor(Toggle):
    """
    When enabled, armor will be received progressively starting from rarity 1 to rarity 10.
    """
    display_name = "Progressive Armor"


class QuestRandomization(Toggle):
    """
    When enabled, quest targets and requirements will be randomized.
    """
    display_name = "Quest Randomization"


class QuestDifficulty(NamedRange):
    """
    Multiplier applied to large monster stats, lower being easier and higher being harder.
    """
    range_start = 0
    range_end = 500
    default = 100
    special_range_names = {
        "vanilla": 100,
        "half": 50,
        "quarter": 25,
        "double": 200
    }


class CashOnly(Toggle):
    """When enabled, equipment no longer requires items for crafting/upgrading."""
    display_name = "Cash-Only Equipment"


@dataclass
class MHFUOptions(PerGameCommonOptions):
    death_link: DeathLink
    goal: Goal
    guild_depth: GuildQuestDepth
    village_depth: VillageQuestDepth
    training_quests: TrainingQuests
    treasure_quests: TreasureQuests
    total_keys: TotalKeyQuests
    required_keys: RequiredKeyQuests
    filler_percentage: FillerPercentage
    #trap_percentage: TrapPercentage
    weapons: Weapons
    progressive_armor: ProgressiveArmor
    quest_randomization: QuestRandomization
    quest_difficulty_multiplier: QuestDifficulty
    cash_only_equipment: CashOnly
