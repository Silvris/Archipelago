from dataclasses import dataclass
from Options import Toggle, DeathLink, Range, Choice, OptionDict, PerGameCommonOptions

class RequiredArtifacts(Range):
    """How many Artifacts are required to finish"""
    display_name = "Required Artifacts"
    range_start = 0
    range_end = 45
    default = 25

class ComputerChecks(Toggle):
    """If enabled, places checks on the Computer data locations"""
    display_name = "Computer Checks"

class CityShuffle(Toggle):
    """Shuffles which doors lead to which cities"""
    display_name = "City Shuffle"

class IrresponsibleLuigi(Toggle):
    """Causes Luigi to become irresponsible, able to talk to people from behind and cross the street without being on a sidewalk."""
    display_name = "Irresponsible Luigi"

class CommQuestions(Toggle):
    """Replaces all trivia questions in the game with randomly selected Archipelago trivia questions submitted by the community!"""
    display_name = "Community Questions"

class ShowKoopaLoot(Toggle):
    """If enabled, Koopas currently holding treasure will blink on the city map."""
    display_name = "Show Koopa Loot"

class GameQuestions(Choice):
    """If Community Questions is enabled, this option controls specific game-related questions.
       None: All selected questions will only be relevant to Archipelago as a whole.
       Only Relevant: Game specific questions can appear, but only for games currently being played in the multiworld. This option may select questions for 'Unsupported' games.
       All: Game specific questions can appear, regardless of if that game is present in the multiworld or not. This will only pick questions from 'Supported' games."""
    display_name = "Game Specific Questions"
    option_none = 0
    option_only_relevant = 1
    option_all = 2
    default = 0

class ShirtColor(OptionDict):
    """Define a custom color for Luigi's green shirt. Color values are in HTML hex."""
    default = {
      "bright": "#005221",
      "base": "#00C65A",
      "dark": "#00FF7B"
    }

class PantsColor(OptionDict):
    """Define a custom color for Luigi's blue pants. Color values are in HTML hex."""
    default = {
      "bright": "#6B007B",
      "base": "#7329FF",
      "dark": "#9C6BFF"
    }


@dataclass
class MarioisMissingOptions(PerGameCommonOptions):
    required_artifacts: RequiredArtifacts
    computer_sanity: ComputerChecks
    city_shuffle: CityShuffle
    irresponsible_luigi: IrresponsibleLuigi
    show_koopa_loot: ShowKoopaLoot
    community_questions: CommQuestions
    game_specific_questions: GameQuestions
    shirt_color: ShirtColor
    pants_color: PantsColor
    death_link: DeathLink
