from Options import Choice, Toggle, DefaultOnToggle, Range, PerGameCommonOptions, OptionSet
from dataclasses import dataclass

class GameVersion(Choice):
    """Whether to play Black 2 or White 2"""
    display_name = "Game Version"
    option_black_2 = 0
    option_white_2 = 1
    default = 1


class Goal(Choice):
    """
    Champion: defeat the Unova Pokemon League and become Champion
    Subway Master: defeat Ingo or Emmet in the Battle Subway Super Trains
    Champion's Cup: win in the Champion's Cup at the PWT
    """
    display_name = "Goal"
    option_champion = 0
    option_subway_master = 1
    option_champions_cup = 2
    default = 0


class Badges(Choice):
    """
    Default: each gym leader will have their regular badge
    Shuffled: badges will be shuffled amongst the gym leaders
    Anywhere: badges can be anywhere
    """
    display_name = "Randomize Badges"
    option_default = 0
    option_shuffled = 1
    option_anywhere = 2
    default = 2


class HiddenMachines(DefaultOnToggle):
    """
    When enabled, HMs are shuffled into the item pool. Else, they will be at their vanilla locations.
    """
    display_name = "Hidden Machines"


class KeyItems(DefaultOnToggle):
    """
    When enabled, key items are shuffled into the item pool. Else, they will be at their vanilla locations.
    """
    display_name = "Key Items"


class OverworldItems(DefaultOnToggle):
    """
    When enabled, overworld item balls are shuffled into the item pool. Else, they will contain their vanilla items.
    """
    display_name = "Overworld Items"


class HiddenItems(Toggle):
    """
    When enabled, hidden overworld items are shuffled into the item pool. Else, they will contain their vanilla items.
    """
    display_name = "Hidden Items"


class GiftItems(Toggle):
    """
    When enabled, gift items are shuffled into the item pool. Else, they will contain their vanilla items.
    """
    display_name = "Gift Items"


class ExtraKeyItems(Toggle):
    """
    Adds additional key items to the pool.
    """
    display_name = "Extra Key Items"


class IncludePostgame(Toggle):
    """
    Adds locations that are unlocked by defeating the Champion.
    """
    display_name = "Include Postgame"


class FreeFlyLocation(Choice):
    """
    Grants a free fly location when starting the game. Additionally,
    a second free location can be granted upon receiving the Town Map.
    """
    display_name = "Free Fly Location"
    option_none = 0
    option_enabled = 1
    option_enabled_plus_town_map = 2
    default = 2


class RemoveRoadblocks(OptionSet):
    """
    Removes specific NPCs that normally stand in your way until certain events are completed.

    This can open up the world a bit and make your playthrough less linear, but careful how many you remove;
    it may make too much of your world available all at once.
    """
    display_name = "Remove Roadblocks"
    valid_keys = frozenset([
        "Route 20 Hiker",
        "Castelia City Clowns"
    ])
    default = (
        "Route 20 Hiker"
    )


@dataclass
class PokemonBW2Options(PerGameCommonOptions):
    version: GameVersion
    goal: Goal
    badges: Badges
    hms: HiddenMachines
    key_items: KeyItems
    overworld_items: OverworldItems
    hidden_items: HiddenItems
    gift_items: GiftItems
    extra_key_items: ExtraKeyItems
    include_postgame: IncludePostgame
    free_fly_location: FreeFlyLocation
    remove_roadblocks: RemoveRoadblocks
