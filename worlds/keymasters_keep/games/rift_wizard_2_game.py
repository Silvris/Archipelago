from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class RiftWizard2ArchipelagoOptions:
    pass


class RiftWizard2Game(Game):
    name = "Rift Wizard 2"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = RiftWizard2ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play the Improviser trial",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="You YODA buy perks that cost X",
                data={
                    "YODA": (self.perkcosts, 1),
                    "X": (self.perkcosts, 1),
                },
            ),
            GameObjectiveTemplate(
                label="The majority of the skills you purchase must have the SPELLTYPE tag",
                data={
                    "SPELLTYPE": (self.spelltype, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Buy exactly X spells",
                data={
                    "X": (self.spellnum, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Once you preview a rift, you must enter it",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run using a majority of SPELLTYPE spells",
                data={
                    "SPELLTYPE": (self.spelltype, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
        ]

    @staticmethod
    def spelltype() -> List[str]:
        return [
            "Fire",
            "Lightning",
            "Ice",
            "Nature",
            "Arcane",
            "Dark",
            "Holy",
            "Sorcery",
            "Conjuration",
            "Enchantment",
            "Metallic",
            "Blood",
        ]

    @staticmethod
    def spellnum() -> range:
        return range(3, 12)

    @staticmethod
    def perkcosts() -> range:
        return range(4, 7)

    @staticmethod
    def yoda() -> List[str]:
        return [
            "can only",
            "cannot",
        ]

# Archipelago Options
# ...
