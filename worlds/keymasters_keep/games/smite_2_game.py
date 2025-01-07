from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class Smite2ArchipelagoOptions:
    pass


class Smite2Game(Game):
    name = "Smite 2"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = Smite2ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Cannot use these Gods: GODS",
                data={
                    "GODS": (self.gods, 5),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot equip these Items: STRENGTH",
                data={
                    "STRENGTH": (self.strength, 3),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot equip these Items: INTELLIGENCE",
                data={
                    "INTELLIGENCE": (self.intelligence, 3),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot equip these Items: HYBRID",
                data={
                    "HYBRID": (self.hybrid, 3),
                },
            ),
            GameObjectiveTemplate(
                label="Must build this Item: ITEMS",
                data={
                    "ITEMS": (self.items, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Can only play this Game Mode: GAMEMODE",
                data={
                    "GAMEMODE": (self.gamemode, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot equip these Relics: RELIC",
                data={
                    "RELIC": (self.relics, 2),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a game using GOD",
                data={"GOD": (self.gods, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Win a game in the ROLE role",
                data={"ROLE": (self.roles, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Win a game in the ROLE role while using a OTHER god",
                data={
                    "ROLE": (self.roles, 1),
                    "OTHER": (self.roles, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD, having built ITEM",
                data={
                    "GOD": (self.gods, 1),
                    "ITEM": (self.items, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD while only using Strength Items",
                data={
                    "GOD": (self.gods, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD while only using Intelligence Items",
                data={
                    "GOD": (self.gods, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD, having built HYBRID",
                data={
                    "GOD": (self.gods, 1),
                    "HYBRID": (self.hybrid, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Win a game, having built all of STRENGTH, INTELLIGENCE and HYBRID",
                data={
                    "STRENGTH": (self.strength, 1),
                    "INTELLIGENCE": (self.intelligence, 1),
                    "HYBRID": (self.hybrid, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="In a Conquest game, kill the Gold Fury 3 times to receive the Gold Fury Soul",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In a Conquest game, kill the Enhanced Fire Giant one time",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In a GAMEMODE game, deal 30,000 player damage using GOD",
                data={
                    "GAMEMODE": (self.gamemode, 1),
                    "GOD": (self.gods, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="In a GAMEMODE game, mitigate 30,000 player damage using GOD",
                data={
                    "GAMEMODE": (self.gamemode, 1),
                    "GOD": (self.gods, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="In a GAMEMODE game, get First Blood",
                data={
                    "GAMEMODE": (self.gamemode, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="In a Conquest game, upgrade your designated buff to Level 4 in a single match",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def roles() -> List[str]:
        return [
            "ADC",
            "Support",
            "Mid",
            "Solo",
            "Jungle",
        ]

    @staticmethod
    def relics() -> List[str]:
        return [
            "Beads",
            "Blink",
            "Aegis",
            "Shell",
            "Sunder",
        ]

    @staticmethod
    def strength() -> List[str]:
        return [
            "Brawler's Ruin",
            "Avenging Blade",
            "Hydra's Lament",
            "Devourer's Gauntlet",
            "Transcendence",
            "Jotunns Revenge",
            "Oath Sworn Spear",
            "Sun-Beam Bow",
            "Bloodforge",
            "Titan's Bane",
            "Relic Dagger",
            "Serrated Edge",
            "Bragi's Harp",
            "Qin's Blade",
            "Shield Splitter",
            "The Executioner",
            "The Reaper",
            "Hastened Fatalis",
            "Avatar's Parashu",
            "Tekko-Gaki",
            "Demon Blade",
            "The Crusher",
            "Pendulum Blade",
            "Heartseeker",
            "Death Metal",
            "Deathbringer",
            "Musashi's Dual Swords",
            "Golden Blade",
            "Eye of the Storm",
            "Void Shield",
            "Shifter's Shield",
            "Triton's Conch",
        ]

    @staticmethod
    def intelligence() -> List[str]:
        return [
            "Book of Thoth",
            "Divine Ruin",
            "Chronos Pendant",
            "Obsidian Shard",
            "Lifebinder",
            "Sun-Beam Bow",
            "Polynomicon",
            "Spear of Desolation",
            "Rod of Asclepius",
            "Gem of Isolation",
            "Soul Gem",
            "Blood Bound Book",
            "Jade Sceptor",
            "Bragi's Harp",
            "Bracer of the Abyss",
            "Gem of Focus",
            "The Cosmic Horror",
            "Demonic Grip",
            "Typhon's Fang",
            "Sceptor of Dominion",
            "Dreamer's Idol",
            "Necronomicon",
            "Totem of Death",
            "World Stone",
            "Death Metal",
            "Doom Orb",
            "Staff of Myrddin",
            "Soul Reaver",
            "Rod of Tahuti",
            "Wish-Granting Pearl",
            "Sphere of Negation",
            "Helm of Radiance",
            "Void Stone",
            "Triton's Conch",
            "Helm of Darkness",
        ]

    @staticmethod
    def hybrid() -> List[str]:
        return [
            "Bragi's Harp",
            "Sun-Beam Bow",
            "Golden Blade",
            "Eye of the Storm",
            "Shifter's Shield",
            "Void Shield",
            "Triton's Conch",
            "Wish-Granting Pearl",
            "Sphere of Negation",
            "Helm of Radiance",
            "Void Stone",
            "Helm of Darkness",
        ]

    @staticmethod
    def items() -> List[str]:
        return [
            "Brawler's Ruin",
            "Avenging Blade",
            "Hydra's Lament",
            "Devourer's Gauntlet",
            "Transcendence",
            "Jotunns Revenge",
            "Oath Sworn Spear",
            "Sun-Beam Bow",
            "Bloodforge",
            "Titan's Bane",
            "Relic Dagger",
            "Serrated Edge",
            "Bragi's Harp",
            "Qin's Blade",
            "Shield Splitter",
            "The Executioner",
            "The Reaper",
            "Hastened Fatalis",
            "Avatar's Parashu",
            "Tekko-Gaki",
            "Demon Blade",
            "The Crusher",
            "Pendulum Blade",
            "Heartseeker",
            "Death Metal",
            "Deathbringer",
            "Musashi's Dual Swords",
            "Golden Blade",
            "Eye of the Storm",
            "Void Shield",
            "Shifter's Shield",
            "Triton's Conch",
            "Book of Thoth",
            "Divine Ruin",
            "Chronos Pendant",
            "Obsidian Shard",
            "Lifebinder",
            "Polynomicon",
            "Spear of Desolation",
            "Rod of Asclepius",
            "Gem of Isolation",
            "Soul Gem",
            "Blood Bound Book",
            "Jade Sceptor",
            "Bracer of the Abyss",
            "Gem of Focus",
            "The Cosmic Horror",
            "Demonic Grip",
            "Typhon's Fang",
            "Sceptor of Dominion",
            "Dreamer's Idol",
            "Necronomicon",
            "Totem of Death",
            "World Stone",
            "Death Metal",
            "Doom Orb",
            "Staff of Myrddin",
            "Soul Reaver",
            "Rod of Tahuti",
            "Wish-Granting Pearl",
            "Sphere of Negation",
            "Helm of Radiance",
            "Void Stone",
            "Helm of Darkness",
        ]

    @staticmethod
    def gods() -> List[str]:
        return [
            "Aphrodite",
            "Medusa",
            "Pele",
            "Amaterasu",
            "Anhur",
            "Anubis",
            "Ares",
            "Athena",
            "Bacchus",
            "Baron Samedi",
            "Bellona",
            "Cernnunos",
            "Chaac",
            "Cupid",
            "Danzaburou",
            "Fenrir",
            "Hades",
            "Hecate",
            "Hercules",
            "Izanami",
            "Jing Wei",
            "Khepri",
            "Kukulkan",
            "Loki",
            "Mordred",
            "Neith",
            "Nemesis",
            "Nu Wa",
            "Odin",
            "Poseidon",
            "Ra",
            "Sobek",
            "Sol",
            "Susano",
            "Thanatos",
            "The Morrigan",
            "Thor",
            "Yemoja",
            "Ymir",
            "Zeus",
        ]

    @staticmethod
    def carry() -> List[str]:
        return [
            "Medusa",
            "Anhur",
            "Cernnunos",
            "Cupid",
            "Danzaburou",
            "Izanami",
            "Jing Wei",
            "Neith",
            "Sol",
        ]

    @staticmethod
    def mid() -> List[str]:
        return [
            "Aphrodite",
            "Anubis",
            "Baron Samedi",
            "Hades",
            "Hecate",
            "Kukulkan",
            "Nu Wa",
            "Poseidon",
            "Ra",
            "Sol",
            "The Morrigan",
            "Zeus",
        ]

    @staticmethod
    def support() -> List[str]:
        return [
            "Aphrodite",
            "Ares",
            "Athena",
            "Bacchus",
            "Baron Samedi",
            "Khepri",
            "Sobek",
            "Yemoja",
            "Ymir",
        ]

    @staticmethod
    def solo() -> List[str]:
        return [
            "Amaterasu",
            "Bellona",
            "Chaac",
            "Hades",
            "Hercules",
            "Mordred",
            "Odin",
        ]

    @staticmethod
    def jungle() -> List[str]:
        return [
            "Pele",
            "Fenrir",
            "Loki",
            "Mordred",
            "Nemesis",
            "Susano",
            "Thanatos",
            "The Morrigan",
            "Thor",
        ]

    @staticmethod
    def gamemode() -> List[str]:
        return [
            "Conquest",
            "Arena",
        ]


# Archipelago Options
# ...
