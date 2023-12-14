from Options import DeathLink, Choice, Toggle, DefaultOnToggle, PerGameCommonOptions
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
    Unranked is considered alongside Low Rank.
    """
    display_name = "Guild Quest Depth"
    option_none = -1
    option_low_rank = 0
    option_high_rank = 1
    option_g_rank = 2
    default = 1


class VillageQuestDepth(Choice):
    """
    What Village ranks to consider as checks. All ranks prior to the selected rank will be added.
    """
    display_name = "Village Quest Depth"
    option_none = -1
    option_low_rank = 0
    option_high_rank = 1
    default = 0


class TrainingQuests(DefaultOnToggle):
    """
    Enables checks for successfully clearing a Training quest.
    """
    display_name = "Training Quests"


class TreasureQuests(DefaultOnToggle):
    """
    Enables checks for reaching specific thresholds within the Treasure quests provided by Treshi.
    """
    display_name = "Training Quests"


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


@dataclass
class MHFUOptions(PerGameCommonOptions):
    death_link: DeathLink
    goal: Goal
    guild_depth: GuildQuestDepth
    village_depth: VillageQuestDepth
    training_quests: TrainingQuests
    treasure_quests: TreasureQuests
    weapons: Weapons
