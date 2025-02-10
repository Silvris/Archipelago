from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MonsterHunter4UltimateArchipelagoOptions:
    monster_hunter_4_ultimate_aged_text_monsters: MonsterHunter4UltimateIncludeAgedTextMonsters
    monster_hunter_4_ultimate_include_apex: MonsterHunter4UltimateIncludeApexMonsters
    monster_hunter_4_ultimate_include_dlcs: MonsterHunter4UltimateIncludeDLC


class MonsterHunter4UltimateGame(Game):
    name = "Monster Hunter 4 Ultimate"
    platform = KeymastersKeepGamePlatforms._3DS

    is_adult_only_or_unrated = False

    options_cls = MonsterHunter4UltimateArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Use an element, or status, that the monster resists",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Hunt as an Guild Quest (if applicable)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Clear 2 Subgoals",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Only run 8 or fewer Decorations",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Run a full set of MONSTER Armor",
                data={
                    "MONSTER": (self.monsters, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Run a MONSTER Weapon (if possible)",
                data={
                    "MONSTER": (self.monsters, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Your weapon type must be rarity level 4 or lower",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't use Wystones",
                data=dict()
            )
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Slay MONSTER",
                data={
                    "MONSTER": (self.monsters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Slay MONSTER using the following weapon: WEAPON",
                data={
                    "MONSTER": (self.monsters, 1),
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Hunt MONSTER with its own Weapon",
                data={
                    "MONSTER": (self.monsters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Hunt MONSTER within TIMER",
                data={
                    "MONSTER": (self.monsters, 1),
                    "TIMER": (self.timers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Capture MONSTER",
                data={
                    "MONSTER": (self.capturable, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Capture MONSTER using the following weapon: WEAPON",
                data={
                    "MONSTER": (self.capturable, 1),
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Carve the following Tail: TAIL",
                data={
                    "TAIL": (self.tails, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Break 2 MONSTER parts",
                data={
                    "MONSTER": (self.monsters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Hunt 2 STAGE monsters",
                data={
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Hunt 3 STAGE monsters",
                data={
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Hunt 3 VARIANT monsters",
                data={
                    "VARIANT": (self.variants, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2
            ),
            GameObjectiveTemplate(
                label="Hunt MONSTER without dying",
                data={
                    "MONSTER": (self.monsters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Wielding the WEAPON, obtain the following Drop: DROP",
                data={
                    "WEAPON": (self.weapons, 1),
                    "DROP": (self.drops, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Obtain the following Drops as Broken Part Rewards (when possible): DROPS",
                data={
                    "DROPS": (self.drops, 2),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a Level 140 MONSTER Guild Quest",
                data={
                    "MONSTER": (self.monsters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

        return templates

    @property
    def include_rank_dependent_monsters(self) -> bool:
        return bool(self.archipelago_options.monster_hunter_4_ultimate_include_rank_dependent_monsters.value)

    @property
    def include_apex_monsters(self):
        return bool(self.archipelago_options.monster_hunter_4_ultimate_include_apex.value)

    @property
    def include_dlc(self):
        return bool(self.archipelago_options.monster_hunter_4_ultimate_include_dlc.value)

    def monsters_base(self) -> List[str]:
        monsters = [
            "Ash Kecha Wacha",
            "Azure Rathalos",
            "Basarios",
            "Berserk Tetsucabra",
            "Black Diablos",
            "Black Gravios",
            "Blue Yian Kut-Ku",
            "Brachydios",
            "Brute Tigrex",
            "Cephadrome",
            "Congalala",
            "Daimyo Hermitaur",
            "Desert Seltas",
            "Desert Seltas Queen",
            "Deviljho",
            "Diablos",
            "Emerald Congalala",
            "Furious Rajang",
            "Gendrome",
            "Gogmazios",
            "Gore Magala",  # Needs a GQ
            "Gravios",
            "Great Jaggi",  # Very funny, only monster that requires a high rank quest
            "Gypceros",
            "Iodrome",
            "Kecha Wacha",
            "Khezu",
            "Kirin",  # you need a GQ for this, but otherwise pretty accessible
            "Kushala Daora",
            "Lagombi",
            "Monoblos",  # Solo only
            "Najarala",
            "Nerscylla",
            "Pink Rathian",
            "Plum Daimyo Hermitaur",
            "Purple Gypceros",
            "Rajang",
            "Rathalos",
            "Rathian",
            "Red Khezu",
            "Ruby Basarios",  # Requires a GQ
            "Rusted Kushala Daora",
            "Seltas",
            "Seltas Queen",
            "Seregios",
            "Shagaru Magala",
            "Shouded Nerscylla",
            "Stygian Zinogre",
            "Teostra",
            "Tetsucabra",
            "Tidal Najarala",
            "Tigerstripe Zamtrios",
            "Tigrex",
            "Ukanlos",
            "Velocidrome",
            "White Monoblos",  # Solo only
            "Yian Garuga",
            "Yian Kut-Ku",
            "Zamtrios",
            "Zinogre",
        ]

        if self.include_apex_monsters:
            monsters.extend(["Apex Gravios", "Apex Diablos", "Apex Tidal Najarala", "Apex Tigrex", "Apex Zinogre"])

        return monsters

    def monsters_rank(self) -> List[str]:
        monsters = [
            "Molten Tigrex",
            "Akantor",
            "Chaotic Gore Magala",
            "Shah Dalamadur",
            "Raging Brachydios",
            "Crimson Fatalis",
        ]

        if self.include_apex_monsters:
            monsters.extend(["Apex Seregios", "Apex Seregios"])

        return monsters

    def monsters_g_dlc(self) -> List[str]:
        monsters = [
            "Silver Rathalos",
            "Gold Rathian",
            "Savage Deviljho",
            "Dah'ren Mohran",
            "Oroshi Kirin",
            "Dalamadur",
            "Fatalis",
            "Old Fatalis",
        ]
        if self.include_apex_monsters:
            monsters.append("Apex Deviljho")

        return monsters

    def monsters(self) -> List[str]:
        monsters: List[str] = self.monsters_base[:]

        if self.include_rank_dependent_monsters:
            monsters.extend(self.monsters_rank())

        if self.include_dlc:
            monsters.extend(self.monsters_g_dlc())

        return sorted(monsters)

    def capturable(self) -> List[str]:
        monsters = self.monsters()

        non_capture = [
            "Kirin",
            "Oroshi Kirin",
            "Shagaru Magala",
            "Dah'ren Mohran",
            "Kushala Daora",
            "Rusted Kushala Daora",
            "Teostra",
            "Chameleos",
            "Dalamadur",
            "Shah Dalamadur",
            "Gogmazios",
            "Fatalis",
            "Crimson Fatalis",
            "Old Fatalis"
        ]

        return sorted(set(monsters).difference(non_capture))

    def variants(self) -> List[str]:
        variants = [
            "Subspecies",
            "Rare Species",
            "Variant Species",
            "Frenzied",
        ]

        if self.include_apex_monsters:
            variants.append("Apex")

        return variants

    @staticmethod
    def weapons() -> List[str]:
        return [
            "Great Sword",
            "Long Sword",
            "Sword and Shield",
            "Dual Blades",
            "Hammer",
            "Hunting Horn",
            "Lance",
            "Gunlance",
            "Switch Axe",
            "Charge Blade",
            "Insect Glaive",
            "Light Bowgun",
            "Heavy Bowgun",
            "Bow",
        ]

    @functools.cached_property
    def stages_base(self) -> List[str]:
        return [
            "Ancestral Steppe",
            "Sunken Hollow",
            "Primal Forest",
            "Frozen Seaway",
            "Volcanic Hollow",
            "Heaven's Mount",
            "Dunes (Day)",
            "Dunes (Night)",
            "Sanctuary",
            "Ingle Isle",
            "Polar Field",
            "Battlequarters",
            "Tower Summit",
            "Everwood"
        ]

    def stages(self) -> List[str]:
        stages: List[str] = self.stages_base[:]

        if self.include_dlc:
            stages.append("Castle Schrade")

        return sorted(stages)

    @functools.cached_property
    def drops_base(self) -> List[str]:
        return [
            "Bird Wyvern Gem",
            "Fey Wyvern Gem",
            "Beast Gem",
            "Wyvern Gem",
            "Lrg Wyvern Gem",
            "Elder Dragon Gem",
            "Lrg Elder Dragon Gem",
            "Rathian Mantle",
            "Rathalos Mantle",
            "Rajang Heart",
            "Ghoulish Gold Gorer",
            "Zinogre Skymerald",
            "S. Zinogre Skymerald",
            "Brach Pallium",
            "Gravios Pallium",
            "B. Gravios Pallium",
            "Tigrex Mantle",
            "S. Magala Mantle",
            "Seregios Lens",
            "Deviljho Crook",
            "Silverpeak Corona",
            "Ukanlos Stone",
            "Wartorn Dragonsphire",
            "Ghoulish Gold Horn",
            "Najarala Medulla",
            "Rathian Ruby",
            "Rathalos Ruby",
            "Zinogre Jasper",
            "S. Zinogre Jasper",
            "Brach Gem",
            "Gravios Medulla",
            "Tigrex Jaw",
            "Pulsating Blastheart",
            "Gore Magala Nyctgem",
            "S. Magala Phosgem",
            "Seregios Dissenter",
            "Deviljho Gem",
            "Daora Gem",
            "Teostra Gem",
            "Akantor Gem",
            "Skyblade Gem",
            "Chameleos Gem",
            "Najarala Marrow",
            "Chilling Beak",
            "Rathian Plate",
            "Rathalos Plate",
            "Rath Marrow",
            "Zinogre Plate",
            "Brach Marrow",
            "Gore Magala Plate",
            "S. Magala Plate",
            "Earth Dragongem",

        ]

    @functools.cached_property
    def drops_rank_base(self) -> List[str]:
        return [
            "Immortal Reactor",
            "Dire Blastheart",
            "Gore Magala Mantle",
            "Conquest Sphere",
            "Skyblade Drgnsphire",
        ]

    @functools.cached_property
    def drops_g_dlc(self) -> List[str]:
        return [
            "Earth Dragonsphire",
        ]

    def drops(self) -> List[str]:
        drops: List[str] = self.drops_base[:]

        if self.include_rank_dependent_monsters:
            drops.extend(self.drops_rank_base)

        if self.include_dlc:
            drops.extend(self.drops_g_dlc)

        return sorted(drops)

    @functools.cached_property
    def tails_base(self) -> List[str]:
        return [
            "Garuga Tail",
            "Garuga Lash",
            "Brach Tail",
            "Brach Lash",
            "Deviljho Tail",
            "Deviljho Flail",
            # no basarios
            # no gravios
            # no rathian?
            "Rathalos Tail",
            "Rathalos Lash",
            "A. Rathalos Tail",
            "A. Rathalos Lash",
            "S. Rathalos Tail",
            "Tigrex Tail",
            "Tigrex Lash",
            "M. Tigrex Tail",
            "Diablos Tailcase+",
            "Seregios Impaler",
            "Seregios Impaler+",
            "Gore Magala Tail",
            "Gore Magala Lash",
            "Akantor Tail",
            "Ukanlos Tail",
            "Ukanlos Flail",
            "Zinogre Tail",
            "Zinogre Lash",
            "S. Zinogre Tail",
            "S. Zinogre Lash",
            "S. Magala Tail",
            "S. Magala Lash",
            "Daora Tail",
            "Daora Lash",
            "Teostra Tail",
            "Teostra Lash",
            "Chameleos Lash",
            "Gogmazios Briartail",
        ]

    @functools.cached_property
    def tails_rank_base(self) -> List[str]:
        return [
            "M. Tigrex Lash",
            "Akantor Flail",
        ]

    @functools.cached_property
    def tails_g_dlc(self) -> List[str]:
        return [
            "S. Rathalos Lash"
        ]

    def tails(self) -> List[str]:
        tails: List[str] = self.tails_base[:]

        if self.include_rank_dependent_monsters:
            tails.extend(self.tails_rank_base)

        if self.include_dlc:
            tails.extend(self.tails_g_dlc)

        return sorted(tails)

    @staticmethod
    def timers() -> List[str]:
        return [
            "30 Minutes",
            "25 Minutes",
            "20 Minutes",
        ]


class MonsterHunter4UltimateIncludeAgedTextMonsters(DefaultOnToggle):
    """
    Indicates whether to include Monster Hunter 4 Ultimate Aged Text monsters when generating objectives.
    """

    display_name = "Monster Hunter 4 Ultimate Include Aged Text Monsters"


class MonsterHunter4UltimateIncludeApexMonsters(DefaultOnToggle):
    """
    Indicates whether to include Monster Hunter 4 Ultimate rank-dependent monsters when generating objectives.
    """

    display_name = "Monster Hunter 4 Ultimate Include Apex Monsters"


class MonsterHunter4UltimateIncludeDLC(DefaultOnToggle):
    """
    Indicates whether to include Monster Hunter 4 Ultimate DLC-exclusive monsters when generating objectives.
    Only G-Rank DLC-exclusive monsters are considered.
    """

    display_name = "Monster Hunter 4 Ultimate Include DLC Monsters"
