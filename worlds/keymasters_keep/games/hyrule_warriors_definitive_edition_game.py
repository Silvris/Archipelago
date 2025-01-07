from __future__ import annotations

from typing import List

from dataclasses import dataclass


from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class HyruleWarriorsDefinitiveEditionArchipelagoOptions:
    pass


class HyruleWarriorsDefinitiveEditionGame(Game):
    name = "Hyrule Warriors: Definitive Edition"
    platform = KeymastersKeepGamePlatforms.SW

    platforms_other = [
        KeymastersKeepGamePlatforms._3DS,
    ]

    is_adult_only_or_unrated = False

    options_cls = HyruleWarriorsDefinitiveEditionArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play on Stage Difficulty DIFFICULTY",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Get Challenge Rank RANK or higher",
                data={
                    "RANK": (self.ranks, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete STAGE with CHARACTER",
                data={
                    "STAGE": (self.stages, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat the Battle Challenge BATTLE CHALLENGE with CHARACTER",
                data={
                    "BATTLE CHALLENGE": (self.battle_challenges, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat the Boss Challenge BOSS CHALLENGE with CHARACTER",
                data={
                    "BOSS CHALLENGE": (self.boss_challenges, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat the Ganon's Fury Mission GANON'S FURY with CHARACTER",
                data={
                    "GANON'S FURY": (self.ganons_fury, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Unlock the following Character: CHARACTER",
                data={
                    "CHARACTER": (self.characters_unlockable, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Unlock the following Weapon: WEAPON",
                data={
                    "WEAPON": (self.weapons_unlockable, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach at least 5% Completion on ADVENTURE_MODE",
                data={
                    "ADVENTURE_MODE": (self.adventure_mode_maps, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Reach at least 10% Completion on ADVENTURE_MODE",
                data={
                    "ADVENTURE_MODE": (self.adventure_mode_maps, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Reach at least 25% Completion on ADVENTURE_MODE",
                data={
                    "ADVENTURE_MODE": (self.adventure_mode_maps, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach at least 50% Completion on ADVENTURE_MODE",
                data={
                    "ADVENTURE_MODE": (self.adventure_mode_maps, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Easy",
            "Normal",
            "Hard",
            "Hero",
        ]

    @staticmethod
    def ranks() -> List[str]:
        return [
            "A Rank",
            "B Rank",
            "C Rank",
        ]

    @staticmethod
    def characters() -> List[str]:
        return [
            "Link",
            "Impa",
            "Sheik",
            "Lana",
            "Darunia",
            "Zelda",
            "Ganondorf",
            "Ruto",
            "Agitha",
            "Midna",
            "Zant",
            "Fi",
            "Ghirahim",
            "Cia",
            "Volga",
            "Wizzro",
            "Twili Midna",
            "Young Link",
            "Tingle",
            "Linkle",
            "Skull Kid",
            "Toon Link",
            "Tetra",
            "King Daphnes",
            "Medli",
            "Marin",
            "Toon Zelda",
            "Ravio",
            "Yuga",
        ]

    @staticmethod
    def characters_unlockable() -> List[str]:
        return [
            "Twili Midna",
            "Young Link",
            "Tingle",
            "Skull Kid",
            "Toon Link",
            "Tetra",
            "King Daphnes",
            "Medli",
            "Marin",
            "Toon Zelda",
            "Ravio",
            "Yuga",
        ]

    @staticmethod
    def weapons_unlockable() -> List[str]:
        return [
            "Magic Rod",
            "Great Fairy",
            "Gauntlets",
            "Master Sword",
            "Horse",
            "Spinner",
            "Niginata",
            "Summoning Gate",
            "Baton",
            "Dominion Rod",
            "Trident",
            "Boots",
            "Sand Wand",
        ]

    @staticmethod
    def stages() -> List[str]:
        return [
            "The Dragon of the Caves",
            "The Invasion Begins",
            "The Armies of Ruin",
            "The Shiekah Tribesman",
            "The Sorceress of the Woods",
            "The Girl in the Green Tunic",
            "The Sorceress of the Valley",
            "The Demon Lord's Plan",
            "The Demon Lord",
            "Land in the Sky",
            "Sealed Ambition",
            "Land of Myth",
            "The Water Temple",
            "Powers Collide",
            "The Usurper King",
            "Land of Twilight",
            "The Shadow King",
            "The Sacred Sword",
            "Her True Self",
            "A War of Spirit",
            "Darkness Falls",
            "Shining Beacon",
            "Ganondorf's Return",
            "March of the Demon King",
            "Battle of the Triforce",
            "Enduring Resolve",
            "Liberation of the Triforce",
            "The Other Hero",
            "A New Disturbance",
            "The Search for Cia",
            "Reclaiming the Darkness",
            "Watchers of the Triforce",
        ]

    @staticmethod
    def adventure_mode_maps() -> List[str]:
        return [
            "Adventure Map",
            "Great Sea Map",
            "Master Quest Map",
            "Master Wind Waker Map",
            "Twilight Map",
            "Termina Map",
            "Koholint Island Map",
            "Grand Travels Map",
            "Lorule Map",
        ]

    @staticmethod
    def battle_challenges() -> List[str]:
        return [
            "Running Battle in Faron Woods",
            "Rush Battle",
            "Defeat 800 Enemies",
        ]

    @staticmethod
    def boss_challenges() -> List[str]:
        return [
            "Defeat 1,000 Enemies",
            "Defeat 1,500 Enemies",
            "Defeat 2,000 Enemies",
            "Brave Battle LV.1",
            "Brave Battle LV.2",
            "Brave Battle LV.3",
            "Survival Battle LV.1",
            "Survival Battle LV.2",
            "Survival Battle LV.3",
            "Survival Battle LV.4",
        ]

    @staticmethod
    def ganons_fury() -> List[str]:
        return [
            "Defeat 5,000 Enemies",
            "Defeat 7,000 Enemies",
            "Defeat 9,999 Enemies",
            "Giant Battle LV.1",
            "Giant Battle LV.2",
            "Giant Battle LV.3",
            "Survival Battle LV.1",
            "Survival Battle LV.2",
            "Survival Battle LV.3",
            "Survival Battle LV.4",
        ]

# Archipelago Options
# ...
