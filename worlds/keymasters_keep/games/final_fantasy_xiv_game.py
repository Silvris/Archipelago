from __future__ import annotations

import functools
from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class FinalFantasyXIVArchipelagoOptions:
    final_fantasy_xiv_content_types_allowed: FinalFantasyXIVContentTypesAllowed
    final_fantasy_xiv_expansions_accessible: FinalFantasyXIVExpansionsAccessible
    final_fantasy_xiv_playable_jobs: FinalFantasyXIVPlayableJobs


class FinalFantasyXIVGame(Game):
    # Initial implementation by @delcake on Discord

    name = "Final Fantasy XIV"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = FinalFantasyXIVArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete any instanced duty objectives without utilizing the Unrestricted Party option",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Travel without the use of Teleport, Return, or other item-based teleportation methods",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objective_list = list()
        
        # Objectives are determined entirely by what the player opts in to from their
        # configuration file. However, some types will be added as defaults if no valid
        # keys are provided to pick from.
        if "FATEs" in self.content_types_allowed or len(self.content_types_allowed) == 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete COUNT FATEs in ZONE with gold credit as JOB",
                    data={
                        "COUNT": (self.fate_range, 1),
                        "ZONE": (self.zones, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete one FATE with gold credit in each zone as JOB: ZONE",
                    data={
                        "ZONE": (self.zones, 3),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ]

            if "Unreasonable Tasks" in self.content_types_allowed:
                objective_list += [
                    GameObjectiveTemplate(
                        label="Complete World FATE 'NAME' with gold credit as JOB",
                        data={
                            "NAME": (self.world_fates, 1),
                            "JOB": (self.combat_jobs, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                    ),
                ]

        if "Guildhests" in self.content_types_allowed or len(self.content_types_allowed) == 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the Guildhest 'GUILDHEST' as JOB",
                    data={
                        "GUILDHEST": (self.guildhests, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ]

        if "Jumping Puzzles" in self.content_types_allowed or len(self.content_types_allowed) == 0:
            if len(self.jumping_puzzles()) > 0:
                objective_list += [
                    GameObjectiveTemplate(
                        label="Scale the jumping puzzle located at LOC",
                        data={
                            "LOC": (self.jumping_puzzles, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ]
            
            if "Gold Saucer" in self.content_types_allowed:
                objective_list += [
                    GameObjectiveTemplate(
                        label="Complete any 'Leap of Faith' GATE in the Gold Saucer",
                        data=dict(),
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=2,
                    ),
                ]
        
        if "The Hunt" in self.content_types_allowed or len(self.content_types_allowed) == 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Locate and defeat B-rank Hunt mark MARK as JOB",
                    data={
                        "MARK": (self.hunt_b_ranks, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ]

            if "Unreasonable Tasks" in self.content_types_allowed:
                objective_list += [
                    GameObjectiveTemplate(
                        label="Successfully spawn S-rank Hunt mark MARK",
                        data={
                            "MARK": (self.hunt_s_ranks, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                    ),
                ]
        
        if "Dungeons" in self.content_types_allowed or len(self.content_types_allowed) == 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the instance DUTY as JOB",
                    data={
                        "DUTY": (self.dungeons, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                ),
            ]
        
        if "Trials" in self.content_types_allowed or len(self.content_types_allowed) == 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the instance DUTY as JOB",
                    data={
                        "DUTY": (self.trials, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                ),
            ]

        if "Extreme Trials" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the instance DUTY as JOB",
                    data={
                        "DUTY": (self.extreme_trials, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                ),
            ]

        if "Normal Raids" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the instance DUTY as JOB",
                    data={
                        "DUTY": (self.normal_raids, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                ),
            ]

        if "Savage Raids" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the instance DUTY as JOB",
                    data={
                        "DUTY": (self.savage_raids, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                ),
            ]

        if "Alliance Raids" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the instance DUTY as JOB",
                    data={
                        "DUTY": (self.alliance_raids, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                ),
            ]

        if "Chaotic Alliance Raids" in self.content_types_allowed and len(self.chaotic_alliance_raids()) > 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the instance DUTY as JOB",
                    data={
                        "DUTY": (self.chaotic_alliance_raids, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                ),
            ]
        
        if "Deep Dungeons" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete COUNT unique sets of floors in DEEPDUNGEON solo as JOB (prior saves allowed)",
                    data={
                        "COUNT": (self.deep_dungeon_floor_range, 1),
                        "DEEPDUNGEON": (self.deep_dungeons, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Obtain 3 Accursed Hoard from a single set of floors in DEEPDUNGEON solo as JOB (prior saves allowed)",
                    data={
                        "DEEPDUNGEON": (self.deep_dungeons, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete a single set of floors in DEEPDUNGEON solo without triggering any floor traps as JOB (prior saves allowed)",
                    data={
                        "DEEPDUNGEON": (self.deep_dungeons, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ]

        if "Variant Dungeons" in self.content_types_allowed and len(self.variant_dungeon_routes()) > 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the Variant Dungeon route which corresponds to the record entry 'ROUTE' as JOB",
                    data={
                        "ROUTE": (self.variant_dungeon_routes, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ]
        
        if "Limited Jobs" in self.content_types_allowed:
            if "Blue Mage" in self.playable_jobs:
                objective_list += [
                    GameObjectiveTemplate(
                        label="In Masked Carnivale, complete the stage STAGE within the TIME Completion Time",
                        data={
                            "STAGE": (self.masked_carnivale, 1),
                            "TIME": (self.masked_carnivale_completion_times, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="In Masked Carnivale, complete the Weekly DIFF Target stage, satisfying all completion requirements within the TIME Completion Time",
                        data={
                            "DIFF": (self.masked_carnivale_weekly_targets, 1),
                            "TIME": (self.masked_carnivale_completion_times, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ]

        if "Bozja" in self.content_types_allowed and "Shadowbringers" in self.expansions_accessible:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete COUNT critical engagements in AREA",
                    data={"COUNT": ((lambda: list(range(3, 11))), 1), "AREA": (self.bozja_areas, 1)}
                )
            ]

        if "Gathering" in self.content_types_allowed and len(self.gathering_collectables()) > 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Turn in COUNTx ITEM at the highest tier of collectability to a Collectable Appraiser",
                    data={
                        "COUNT": (self.gathering_collectables_count_range, 1),
                        "ITEM": (self.gathering_collectables, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Turn in at least one of each collectable at the highest tier of collectability to a Collectable Appraiser: ITEMS",
                    data={
                        "ITEMS": (self.gathering_collectables, 6),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ]

        if "Fishing" in self.content_types_allowed and len(self.fishing_collectables()) > 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Turn in COUNTx ITEM at the highest tier of collectability to a Collectable Appraiser",
                    data={
                        "COUNT": (self.fishing_collectables_count_range, 1),
                        "ITEM": (self.fishing_collectables, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Turn in at least one of each collectable at the highest tier of collectability to a Collectable Appraiser: ITEMS",
                    data={
                        "ITEMS": (self.fishing_collectables, 6),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ]

            if "Unreasonable Tasks" in self.content_types_allowed:
                objective_list += [
                    GameObjectiveTemplate(
                        label="Catch the Big Fish 'FISH'",
                        data={
                            "FISH": (self.big_fish, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                    ),
                ]

        if "Crafting" in self.content_types_allowed and len(self.crafting_collectables()) > 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Turn in COUNTx ITEM at the highest tier of collectability to a Collectable Appraiser",
                    data={
                        "COUNT": (self.crafting_collectables_count_range, 1),
                        "ITEM": (self.crafting_collectables, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Turn in at least one of each collectable at the highest tier of collectability to a Collectable Appraiser: ITEMS",
                    data={
                        "ITEMS": (self.crafting_collectables, 6),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ]

        if "Crystalline Conflict" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Participate in COUNT Crystalline Conflict matches as JOB",
                    data={
                        "COUNT": (self.crystalline_conflict_match_counts, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win COUNT Crystalline Conflict matches as JOB",
                    data={
                        "COUNT": (self.crystalline_conflict_match_counts, 1),
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
            ]

        if "Frontline" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Participate in a Frontline match as JOB",
                    data={
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win a Frontline match as JOB",
                    data={
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
            ]

        if "Rival Wings" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Participate in a Rival Wings match as JOB",
                    data={
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win a Rival Wings match as JOB",
                    data={
                        "JOB": (self.combat_jobs, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
            ]

        if "Gold Saucer" in self.content_types_allowed or len(self.content_types_allowed) == 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="TASK",
                    data={
                        "TASK": (self.gate_tasks, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Successfully complete COUNT GATEs in the Gold Saucer",
                    data={
                        "COUNT": (self.gate_count, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Claim a Small Item from The Moogle's Paw machine in the Gold Saucer",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Earn a 'BRUTAL!!!' rating on the Cuff-a-Cur machine in the Gold Saucer",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Earn a 'PULVERIZING!!!' rating on the Crystal Tower Striker machine in the Gold Saucer",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Score 5+ points on the Monster Toss machine in the Gold Saucer",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Participate in a Chocobo Race Duty Finder match",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Place 1st in a Chocobo Race Duty Finder match",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
            ]

        if "Triple Triad" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Defeat the following opponents in a Triple Triad match: OPPONENTS",
                    data={
                        "OPPONENTS": (self.triple_triad, 3),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Obtain a RARITY-Star or better Triple Triad card reward from COUNT unique NPC opponents of your choice",
                    data={
                        "RARITY": (self.triple_triad_rarity_range, 1),
                        "COUNT": (self.triple_triad_range, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ]

        if "Minigames" in self.content_types_allowed:
            if "Shadowbringers" in self.expansions_accessible:
                objective_list += [
                    GameObjectiveTemplate(
                        label="Win COUNT consecutive matches of High or Low against Tista-Bie in Eulmore",
                        data={
                            "COUNT": (self.high_low_range, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ]
        
        return objective_list

    @property
    def expansions_accessible(self) -> Set[str]:
        return self.archipelago_options.final_fantasy_xiv_expansions_accessible.value

    def expansions(self) -> List[str]:
        return sorted(self.expansions_accessible)

    @property
    def content_types_allowed(self) -> Set[str]:
        return self.archipelago_options.final_fantasy_xiv_content_types_allowed.value

    @property
    def playable_jobs(self) -> Set[str]:
        return self.archipelago_options.final_fantasy_xiv_playable_jobs.value

    def combat_jobs(self) -> List[str]:
        combat_jobs = [
            "Paladin",
            "Warrior",
            "White Mage",
            "Scholar",
            "Monk",
            "Dragoon",
            "Ninja",
            "Bard",
            "Black Mage",
            "Summoner",
        ]

        heavensward_jobs = [
            "Dark Knight",
            "Astrologian",
            "Machinist",
        ]

        stormblood_jobs = [
            "Samurai",
            "Red Mage",
        ]

        shadowbringers_jobs = [
            "Gunbreaker",
            "Dancer",
        ]

        endwalker_jobs = [
            "Sage",
            "Reaper",
        ]

        dawntrail_jobs = [
            "Viper",
            "Pictomancer",
        ]

        if "Heavensward" in self.expansions_accessible:
            combat_jobs.extend(heavensward_jobs)

        if "Stormblood" in self.expansions_accessible:
            combat_jobs.extend(stormblood_jobs)

        if "Shadowbringers" in self.expansions_accessible:
            combat_jobs.extend(shadowbringers_jobs)

        if "Endwalker" in self.expansions_accessible:
            combat_jobs.extend(endwalker_jobs)

        if "Dawntrail" in self.expansions_accessible:
            combat_jobs.extend(dawntrail_jobs)

        # Remove any jobs that the player has not enabled in their config.
        jobs = [x for x in combat_jobs if x in self.playable_jobs]

        if len(jobs) == 0:
            # The player didn't enable any jobs in their configuration, so
            # instead return all possible jobs.
            jobs = combat_jobs

        return sorted(jobs)

    def limited_jobs(self) -> List[str]:
        limited_jobs = [
            "Blue Mage",
            # "Beastmaster",
        ]

        # Remove any jobs that the player has not enabled in their config.
        jobs = [x for x in limited_jobs if x in self.playable_jobs]

        return sorted(jobs)

    @staticmethod
    def fate_range() -> range:
        return range(1, 6)

    def zones(self) -> List[str]:
        zones = [
            "Middle La Noscea",
            "Lower La Noscea",
            "Eastern La Noscea",
            "Western La Noscea",
            "Upper La Noscea",
            "Outer La Noscea",
            "Central Shroud",
            "East Shroud",
            "South Shroud",
            "North Shroud",
            "Western Thanalan",
            "Central Thanalan",
            "Eastern Thanalan",
            "Southern Thanalan",
            "Northern Thanalan",
            "Coerthas Central Highlands",
            "Mor Dhona",
        ]

        heavensward_zones = [
            "Coerthas Western highlands",
            "The Sea of Clouds",
            "Azys Lla",
            "The Dravanian Forelands",
            "The Dravanian Hinterlands",
            "The Churning Mists",
        ]

        stormblood_zones = [
            "The Fringes",
            "The Peaks",
            "The Lochs",
            "The Ruby Sea",
            "Yanxia",
            "The Azim Steppe",
        ]

        shadowbringers_zones = [
            "Lakeland",
            "Kholusia",
            "Amh Araeng",
            "Il Mheg",
            "The Rak'tika Greatwood",
            "The Tempest",
        ]

        endwalker_zones = [
            "Thavnair",
            "Garlemald",
            "Labyrinthos",
            "Mare Lamentorum",
            "Ultima Thule",
            "Elpis",
        ]

        dawntrail_zones = [
            "Urqopacha",
            "Kozama'uka",
            "Yak T'el",
            "Shaaloani",
            "Heritage Found",
            "Living Memory",
        ]

        if "Heavensward" in self.expansions_accessible:
            zones.extend(heavensward_zones)

        if "Stormblood" in self.expansions_accessible:
            zones.extend(stormblood_zones)

        if "Shadowbringers" in self.expansions_accessible:
            zones.extend(shadowbringers_zones)

        if "Endwalker" in self.expansions_accessible:
            zones.extend(endwalker_zones)

        if "Dawntrail" in self.expansions_accessible:
            zones.extend(dawntrail_zones)

        return sorted(zones)

    def world_fates(self) -> List[str]:
        world_fates = [
            "He Taketh It with His Eyes",
            "Steel Reign",
        ]

        heavensward_world_fates = [
            "Coeurls Chase Boys Chase Coeurls",
            "Prey Online",
        ]

        stormblood_world_fates = [
            "A Horse Outside",
            "Foxy Lady",
        ]

        shadowbringers_world_fates = [
            "A Finale Most Formidable",
            "The Head, the Tail, the Whole Damned Thing",
        ]

        endwalker_world_fates = [
            "Devout Pilgrims vs. Daivadipa",
            "Omicron Recall: Killing Order",
        ]

        dawntrail_world_fates = [
            "The Serpentlord Seethes",
            "Mascot Murder",
        ]

        if "Heavensward" in self.expansions_accessible:
            world_fates.extend(heavensward_world_fates)

        if "Stormblood" in self.expansions_accessible:
            world_fates.extend(stormblood_world_fates)

        if "Shadowbringers" in self.expansions_accessible:
            world_fates.extend(shadowbringers_world_fates)

        if "Endwalker" in self.expansions_accessible:
            world_fates.extend(endwalker_world_fates)

        if "Dawntrail" in self.expansions_accessible:
            world_fates.extend(dawntrail_world_fates)

        return sorted(world_fates)
    
    @staticmethod
    def guildhests() -> List[str]:
        guildests = [
            "Basic Training: Enemy Parties",
            "Under the Armor",
            "Basic Training: Enemy Strongholds",
            "Hero on the Half Shell",
            "Pulling Poison Posies",
            "Stinging Back",
            "All's Well that Ends in the Well",
            "Flicking Sticks and Taking Names",
            "More than a Feeler",
            "Annoy the Void",
            "Shadow and Claw",
            "Long Live the Queen",
            "Ward Up",
            "Solemn Trinity",
        ]

        return sorted(guildests)

    def hunt_b_ranks(self) -> List[str]:
        b_ranks = [
            "Skogs Fru",
            "Barbastelle",
            "Bloody Mary",
            "Dark Helmet",
            "Myradrosh",
            "Vuokho",
            "Sewer Syrup",
            "Ovjang",
            "Gatling",
            "Albin the Ashen",
            "Flame Sergeant Dalvag",
            "White Joker",
            "Stinging Sophie",
            "Monarch Ogrefly",
            "Phecda",
            "Naul",
            "Leech King",
        ]

        heavensward_b_ranks = [
            "Alteci",
            "Kreutzet",
            "Squonk",
            "Sanu Vali of Dancing Wings",
            "Gnath Cometdrone",
            "Thextera",
            "Scitalis",
            "The Scarecrow",
            "Pterygotus",
            "False Gigantopithecus",
            "Lycidas",
            "Omni",
        ]

        stormblood_b_ranks = [
            "Shadow-dweller Yamini",
            "Ouzelum",
            "Gwas-y-neidr",
            "Buccaboo",
            "Gauki Strongblade",
            "Guhuo Niao",
            "Deidar",
            "Gyorai Quickstrike",
            "Kurma",
            "Aswang",
            "Manes",
            "Kiwa",
        ]

        shadowbringers_b_ranks = [
            "La Velue",
            "Itzpapalotl",
            "Coquecigrue",
            "Indomitable",
            "Worm of the Well",
            "Juggler Hecatomb",
            "Domovoi",
            "Vulpangue",
            "Mindmaker",
            "Pachamama",
            "Gilshs Aath Swiftclaw",
            "Deacon",
        ]

        endwalker_b_ranks = [
            "Green Archon",
            "Ü-u-ü-u",
            "Vajrakumara",
            "Iravati",
            "Warmonger",
            "Emperor's Rose",
            "Daphnia Magna",
            "Genesis Rock",
            "Yumcax",
            "Shockmaw",
            "Level Cheater",
            "Oskh Rhei",
        ]

        dawntrail_b_ranks = [
            "Mad Maguey",
            "Chupacabra",
            "The Slammer",
            "Go'ozoabek'be",
            "Leafscourge Hadoll Ja",
            "Xty'iinbek",
            "Nopalitender Fabuloso",
            "Uktena",
            "Gallowsbeak",
            "Gargant",
            "Jewel Bearer",
            "13th Child",
        ]

        if "Heavensward" in self.expansions_accessible:
            b_ranks.extend(heavensward_b_ranks)

        if "Stormblood" in self.expansions_accessible:
            b_ranks.extend(stormblood_b_ranks)

        if "Shadowbringers" in self.expansions_accessible:
            b_ranks.extend(shadowbringers_b_ranks)

        if "Endwalker" in self.expansions_accessible:
            b_ranks.extend(endwalker_b_ranks)

        if "Dawntrail" in self.expansions_accessible:
            b_ranks.extend(dawntrail_b_ranks)

        return sorted(b_ranks)
    
    def hunt_s_ranks(self) -> List[str]:
        s_ranks = [
            # Laideronnette excluded as it isn't spawned by players.
            # The Garlok excluded as it isn't spawned by players.
            "Nunyunuwi",
            "Agrippa the Mighty",
            "Mindflayer",
            "Bonnacon",
            "Safat",
            "Croakadile",
            "Croque-mitaine",
            "Wulgaru",
            "Lampalagua",
            "Brontes",
            "Thousand-cast Theda",
            "Zona Seeker",
            "Nandi",
            "Minhocao",
            "Chernobog",
        ]

        heavensward_s_ranks = [
            "The Pale Rider",
            "Gandarewa",
            "Leucrotta",
            "Senmurv",
            "Kaiser Behemoth",
            "Bird of Paradise",
        ]

        stormblood_s_ranks = [
            "Orghana",
            "Salt and Light",
            "Bone Crawler",
            "Okina",
            "Gamma",
            "Udumbara",
        ]

        shadowbringers_s_ranks = [
            "Aglaope",
            "Tarchia",
            "Tyger",
            "Ixtab",
            "Forgiven Pedantry",
            "Gunitt",
        ]

        endwalker_s_ranks = [
            "Sphatika",
            "Narrow-rift",
            "Ruminator",
            "Ophioneus",
            "Burfurlur the Canny",
            "Armstrong",
        ]

        dawntrail_s_ranks = [
            "Kirlirger the Abhorrent",
            "Neyoozoteel",
            "Inhuxokiy",
            "Atticus the Primogenitor",
            "The Forecaster",
            "Sansheya",
        ]

        if "Heavensward" in self.expansions_accessible:
            s_ranks.extend(heavensward_s_ranks)

        if "Stormblood" in self.expansions_accessible:
            s_ranks.extend(stormblood_s_ranks)

        if "Shadowbringers" in self.expansions_accessible:
            s_ranks.extend(shadowbringers_s_ranks)

        if "Endwalker" in self.expansions_accessible:
            s_ranks.extend(endwalker_s_ranks)

        if "Dawntrail" in self.expansions_accessible:
            s_ranks.extend(dawntrail_s_ranks)

        return sorted(s_ranks)

    def jumping_puzzles(self) -> List[str]:
        jumping_puzzles = list()

        if "Heavensward" in self.expansions_accessible:
            jumping_puzzles += ["The Firmament: Outer Towers"]

        if "Stormblood" in self.expansions_accessible:
            jumping_puzzles += [
                "Kugane: Shiokaze Hostelry",
                "Kugane: Bokairo Inn",
                "Shirogane: Beach Lighthouse",
                "Rhalgr's Reach: Chakra Falls",
            ]
        
        if "Endwalker" in self.expansions_accessible:
            jumping_puzzles += ["Radz-at-Han: Paksa's Path"]
        
        return sorted(jumping_puzzles)
    
    def dungeons(self) -> List[str]:
        dungeons = [
            "Sastasha",
            "The Tam-Tara Deepcroft",
            "Copperbell Mines",
            "Halatali",
            "The Thousand Maws of Toto-Rak",
            "Haukke Manor",
            "Brayflox's Longstop",
            "The Sunken Temple of Qarn",
            "Cutter's Cry",
            "The Stone Vigil",
            "Dzemael Darkhold",
            "The Aurum Vale",
            "The Wanderer's Palace",
            "Castrum Meridianum",
            "The Praetorium",
            "Amdapor Keep",
            "Pharos Sirius",
            "Copperbell Mines (Hard)",
            "Haukke Manor (Hard)",
            "The Lost City of Amdapor",
            "Halatali (Hard)",
            "Brayflox's Longstop (Hard)",
            "Hullbreaker Isle",
            "The Tam-Tara Deepcroft (Hard)",
            "The Stone Vigil (Hard)",
            "Snowcloak",
            "Sastasha (Hard)",
            "The Sunken Temple of Qarn (Hard)",
            "The Keeper of the Lake",
            "The Wanderer's Palace (Hard)",
            "Amdapor Keep (Hard)",
        ]

        heavensward_dungeons = [
            "The Dusk Vigil",
            "Sohm Al",
            "The Aery",
            "The Vault",
            "The Great Gubal Library",
            "The Aetherochemical Research Facility",
            "Neverreap",
            "The Fractal Continuum",
            "Saint Mocianne's Arboretum",
            "Pharos Sirius (Hard)",
            "The Antitower",
            "The Lost City of Amdapor (Hard)",
            "Sohr Khai",
            "Hullbreaker Isle (Hard)",
            "Xelphatol",
            "The Great Gubal Library (Hard)",
            "Baelsar's Wall",
            "Sohm Al (Hard)",
        ]

        stormblood_dungeons = [
            "The Sirensong Sea",
            "Shisui of the Violet Tides",
            "Bardam's Mettle",
            "Doma Castle",
            "Castrum Abania",
            "Ala Mhigo",
            "Kugane Castle",
            "The Temple of the Fist",
            "The Drowned City of Skalla",
            "Hells' Lid",
            "The Fractal Continuum (Hard)",
            "The Swallow's Compass",
            "The Burn",
            "Saint Mocianne's Arboretum (Hard)",
            "The Ghimlyt Dark",
        ]

        shadowbringers_dungeons = [
            "Holminster Switch",
            "Dohn Mheg",
            "The Qitana Ravel",
            "Malikah's Well",
            "Mt. Gulg",
            "Amaurot",
            "The Twinning",
            "Akadaemia Anyder",
            "The Grand Cosmos",
            "Anamnesis Anyder",
            "The Heroes' Gauntlet",
            "Matoya's Relict",
            "Paglth'an",
        ]

        endwalker_dungeons = [
            "The Tower of Zot",
            "The Tower of Babil",
            "Vanaspati",
            "Ktisis Hyperboreia",
            "The Aitiascope",
            "The Dead Ends",
            "Smileton",
            "The Stigma Dreamscape",
            "Alzadaal's Legacy",
            "The Fell Court of Troia",
            "Lapis Manalis",
            "The Aetherfont",
            "The Lunar Subterrane",
        ]

        dawntrail_dungeons = [
            "Ihuykatumu",
            "Worqor Zormor",
            "The Skydeep Cenote",
            "Vanguard",
            "Origenics",
            "Alexandria",
            "Tender Valley",
            "The Strayborough Deadwalk",
            "Yuweyawata Field Station",
        ]

        if "Heavensward" in self.expansions_accessible:
            dungeons.extend(heavensward_dungeons)

        if "Stormblood" in self.expansions_accessible:
            dungeons.extend(stormblood_dungeons)

        if "Shadowbringers" in self.expansions_accessible:
            dungeons.extend(shadowbringers_dungeons)

        if "Endwalker" in self.expansions_accessible:
            dungeons.extend(endwalker_dungeons)

        if "Dawntrail" in self.expansions_accessible:
            dungeons.extend(dawntrail_dungeons)

        return sorted(dungeons)

    def trials(self) -> List[str]:
        trials = [
            "The Bowl of Embers",
            "The Navel",
            "The Howling Eye",
            "The Porta Decumana",
            "The Chrysalis",
            "A Relic Reborn: the Chimera",
            "A Relic Reborn: the Hydra",
            "Battle on the Big Bridge",
            "The Dragon's Neck",
            "Battle in the Big Keep",
            "The Bowl of Embers (Hard)",
            "The Howling Eye (Hard)",
            "The Navel (Hard)",
            "Thornmarch (Hard)",
            "The Whorleater (Hard)",
            "The Striking Tree (Hard)",
            "The Akh Afah Amphitheatre (Hard)",
            "Urth's Fount",
        ]

        heavensward_trials = [
            "Thok ast Thok (Hard)",
            "The Limitless Blue (Hard)",
            "The Singularity Reactor",
            "The Final Steps of Faith",
            "Containment Bay S1T7",
            "Containment Bay P1T6",
            "Containment Bay Z1T9",
        ]

        stormblood_trials = [
            "The Pool of Tribute",
            "Emanation",
            "The Royal Menagerie",
            "Castrum Fluminis",
            "Kugane Ohashi",
            "The Great Hunt",
            "The Jade Stoa",
            "Hells' Kier",
            "The Wreath of Snakes",
        ]

        shadowbringers_trials = [
            "The Dancing Plague",
            "The Crown of the Immaculate",
            "The Dying Gasp",
            "Cinder Drift",
            "The Seat of Sacrifice",
            "Castrum Marinum",
            "The Cloud Deck",
        ]

        endwalker_trials = [
            "The Dark Inside",
            "The Mothercrystal",
            "The Final Day",
            "Storm's Crown",
            "Mount Ordeals",
            "The Voidcast Dais",
            "The Abyssal Fracture",
            "The Gilded Araya",
        ]

        dawntrail_trials = [
            "Worqor Lar Dor",
            "Everkeep",
            "The Interphos",
        ]

        if "Heavensward" in self.expansions_accessible:
            trials.extend(heavensward_trials)

        if "Stormblood" in self.expansions_accessible:
            trials.extend(stormblood_trials)

        if "Shadowbringers" in self.expansions_accessible:
            trials.extend(shadowbringers_trials)

        if "Endwalker" in self.expansions_accessible:
            trials.extend(endwalker_trials)

        if "Dawntrail" in self.expansions_accessible:
            trials.extend(dawntrail_trials)

        return sorted(trials)
    
    def extreme_trials(self) -> List[str]:
        extreme_trials = [
            "The Minstrel's Ballad: Ultima's Bane",
            "The Howling Eye (Extreme)",
            "The Navel (Extreme)",
            "The Bowl of Embers (Extreme)",
            "Thornmarch (Extreme)",
            "The Whorleater (Extreme)",
            "The Striking Tree (Extreme)",
            "The Akh Afah Amphitheatre (Extreme)",
        ]

        heavensward_extreme_trials = [
            "The Limitless Blue (Extreme)",
            "Thok ast Thok (Extreme)",
            "The Minstrel's Ballad: Thordan's Reign",
            "The Minstrel's Ballad: Nidhogg's Rage",
            "Containment Bay S1T7 (Extreme)",
            "Containment Bay P1T6 (Extreme)",
            "Containment Bay Z1T9 (Extreme)",
        ]

        stormblood_extreme_trials = [
            "The Pool of Tribute (Extreme)",
            "Emanation (Extreme)",
            "The Minstrel's Ballad: Shinryu's Domain",
            "The Minstrel's Ballad: Tsukuyomi's Pain",
            "The Great Hunt (Extreme)",
            "The Jade Stoa (Extreme)",
            "Hells' Kier (Extreme)",
            "The Wreath of Snakes (Extreme)",
        ]

        shadowbringers_extreme_trials = [
            "The Dancing Plague (Extreme)",
            "The Crown of the Immaculate (Extreme)",
            "The Minstrel's Ballad: Hades's Elegy",
            "Cinder Drift (Extreme)",
            "Memoria Misera (Extreme)",
            "The Seat of Sacrifice (Extreme)",
            "Castrum Marinum (Extreme)",
            "The Cloud Deck (Extreme)",
        ]

        endwalker_extreme_trials = [
            "The Minstrel's Ballad: Zodiark's Fall",
            "The Minstrel's Ballad: Hydaelyn's Call",
            "The Minstrel's Ballad: Endsinger's Aria",
            "Storm's Crown (Extreme)",
            "Mount Ordeals (Extreme)",
            "The Voidcast Dais (Extreme)",
            "The Abyssal Fracture (Extreme)",
        ]

        dawntrail_extreme_trials = [
            "Worqor Lar Dor (Extreme)",
            "Everkeep (Extreme)",
            "The Minstrel's Ballad: Sphene's Burden",
        ]

        if "Heavensward" in self.expansions_accessible:
            extreme_trials.extend(heavensward_extreme_trials)

        if "Stormblood" in self.expansions_accessible:
            extreme_trials.extend(stormblood_extreme_trials)

        if "Shadowbringers" in self.expansions_accessible:
            extreme_trials.extend(shadowbringers_extreme_trials)

        if "Endwalker" in self.expansions_accessible:
            extreme_trials.extend(endwalker_extreme_trials)

        if "Dawntrail" in self.expansions_accessible:
            extreme_trials.extend(dawntrail_extreme_trials)

        return sorted(extreme_trials)

    def normal_raids(self) -> List[str]:
        normal_raids = [
            "The Binding Coil of Bahamut - Turn 1",
            "The Binding Coil of Bahamut - Turn 2",
            "The Binding Coil of Bahamut - Turn 3",
            "The Binding Coil of Bahamut - Turn 4",
            "The Binding Coil of Bahamut - Turn 5",
            "The Second Coil of Bahamut - Turn 1",
            "The Second Coil of Bahamut - Turn 2",
            "The Second Coil of Bahamut - Turn 3",
            "The Second Coil of Bahamut - Turn 4",
            "The Final Coil of Bahamut - Turn 1",
            "The Final Coil of Bahamut - Turn 2",
            "The Final Coil of Bahamut - Turn 3",
            "The Final Coil of Bahamut - Turn 4",
        ]

        heavensward_normal_raids = [
            "Alexander - The Fist of the Father",
            "Alexander - The Cuff of the Father",
            "Alexander - The Arm of the Father",
            "Alexander - The Burdern of the Father",
            "Alexander - The Fist of the Son",
            "Alexander - The Cuff of the Son",
            "Alexander - The Arm of the Son",
            "Alexander - The Burden of the Son",
            "Alexander - The Eyes of the Creator",
            "Alexander - The Breath of the Creator",
            "Alexander - The Heart of the Creator",
            "Alexander - The Soul of the Creator",
        ]

        stormblood_normal_raids = [
            "Deltascape V1.0",
            "Deltascape V2.0",
            "Deltascape V3.0",
            "Deltascape V4.0",
            "Sigmascape V1.0",
            "Sigmascape V2.0",
            "Sigmascape V3.0",
            "Sigmascape V4.0",
            "Alphascape V1.0",
            "Alphascape V2.0",
            "Alphascape V3.0",
            "Alphascape V4.0",
        ]

        shadowbringers_normal_raids = [
            "Eden's Gate: Resurrection",
            "Eden's Gate: Descent",
            "Eden's Gate: Inundation",
            "Eden's Gate: Sepulture",
            "Eden's Verse: Fulmination",
            "Eden's Verse: Furor",
            "Eden's Verse: Iconoclasm",
            "Eden's Verse: Refulgence",
            "Eden's Promise: Umbra",
            "Eden's Promise: Litany",
            "Eden's Promise: Anamorphosis",
            "Eden's Promise: Eternity",
        ]

        endwalker_normal_raids = [
            "Asphodelos: The First Circle",
            "Asphodelos: The Second Circle",
            "Asphodelos: The Third Circle",
            "Asphodelos: The Fourth Circle",
            "Abyssos: The Fifth Circle",
            "Abyssos: The Sixth Circle",
            "Abyssos: The Seventh Circle",
            "Abyssos: The Eighth Circle",
            "Anabaseios: The Ninth Circle",
            "Anabaseios: The Tenth Circle",
            "Anabaseios: The Eleventh Circle",
            "Anabaseios: The Twelfth Circle",
        ]

        dawntrail_normal_raids = [
            "AAC Light-heavyweight M1",
            "AAC Light-heavyweight M2",
            "AAC Light-heavyweight M3",
            "AAC Light-heavyweight M4",
        ]
        
        if "Heavensward" in self.expansions_accessible:
            normal_raids.extend(heavensward_normal_raids)

        if "Stormblood" in self.expansions_accessible:
            normal_raids.extend(stormblood_normal_raids)

        if "Shadowbringers" in self.expansions_accessible:
            normal_raids.extend(shadowbringers_normal_raids)

        if "Endwalker" in self.expansions_accessible:
            normal_raids.extend(endwalker_normal_raids)

        if "Dawntrail" in self.expansions_accessible:
            normal_raids.extend(dawntrail_normal_raids)

        return sorted(normal_raids)
    
    def savage_raids(self) -> List[str]:
        savage_raids = [
            "The Second Coil of Bahamut (Savage) - Turn 1",
            "The Second Coil of Bahamut (Savage) - Turn 2",
            "The Second Coil of Bahamut (Savage) - Turn 3",
            "The Second Coil of Bahamut (Savage) - Turn 4",
        ]

        heavensward_savage_raids = [
            "Alexander - The Fist of the Father (Savage)",
            "Alexander - The Cuff of the Father (Savage)",
            "Alexander - The Arm of the Father (Savage)",
            "Alexander - The Burdern of the Father (Savage)",
            "Alexander - The Fist of the Son (Savage)",
            "Alexander - The Cuff of the Son (Savage)",
            "Alexander - The Arm of the Son (Savage)",
            "Alexander - The Burden of the Son (Savage)",
            "Alexander - The Eyes of the Creator (Savage)",
            "Alexander - The Breath of the Creator (Savage)",
            "Alexander - The Heart of the Creator (Savage)",
            "Alexander - The Soul of the Creator (Savage)",
        ]

        stormblood_savage_raids = [
            "Deltascape V1.0 (Savage)",
            "Deltascape V2.0 (Savage)",
            "Deltascape V3.0 (Savage)",
            "Deltascape V4.0 (Savage)",
            "Sigmascape V1.0 (Savage)",
            "Sigmascape V2.0 (Savage)",
            "Sigmascape V3.0 (Savage)",
            "Sigmascape V4.0 (Savage)",
            "Alphascape V1.0 (Savage)",
            "Alphascape V2.0 (Savage)",
            "Alphascape V3.0 (Savage)",
            "Alphascape V4.0 (Savage)",
        ]

        shadowbringers_savage_raids = [
            "Eden's Gate: Resurrection (Savage)",
            "Eden's Gate: Descent (Savage)",
            "Eden's Gate: Inundation (Savage)",
            "Eden's Gate: Sepulture (Savage)",
            "Eden's Verse: Fulmination (Savage)",
            "Eden's Verse: Furor (Savage)",
            "Eden's Verse: Iconoclasm (Savage)",
            "Eden's Verse: Refulgence (Savage)",
            "Eden's Promise: Umbra (Savage)",
            "Eden's Promise: Litany (Savage)",
            "Eden's Promise: Anamorphosis (Savage)",
            "Eden's Promise: Eternity (Savage)",
        ]

        endwalker_savage_raids = [
            "Asphodelos: The First Circle (Savage)",
            "Asphodelos: The Second Circle (Savage)",
            "Asphodelos: The Third Circle (Savage)",
            "Asphodelos: The Fourth Circle (Savage)",
            "Abyssos: The Fifth Circle (Savage)",
            "Abyssos: The Sixth Circle (Savage)",
            "Abyssos: The Seventh Circle (Savage)",
            "Abyssos: The Eighth Circle (Savage)",
            "Anabaseios: The Ninth Circle (Savage)",
            "Anabaseios: The Tenth Circle (Savage)",
            "Anabaseios: The Eleventh Circle (Savage)",
            "Anabaseios: The Twelfth Circle (Savage)",
        ]

        dawntrail_savage_raids = [
            "AAC Light-heavyweight M1 (Savage)",
            "AAC Light-heavyweight M2 (Savage)",
            "AAC Light-heavyweight M3 (Savage)",
            "AAC Light-heavyweight M4 (Savage)",
        ]
        
        if "Heavensward" in self.expansions_accessible:
            savage_raids.extend(heavensward_savage_raids)

        if "Stormblood" in self.expansions_accessible:
            savage_raids.extend(stormblood_savage_raids)

        if "Shadowbringers" in self.expansions_accessible:
            savage_raids.extend(shadowbringers_savage_raids)

        if "Endwalker" in self.expansions_accessible:
            savage_raids.extend(endwalker_savage_raids)

        if "Dawntrail" in self.expansions_accessible:
            savage_raids.extend(dawntrail_savage_raids)

        return sorted(savage_raids)

    def alliance_raids(self) -> List[str]:
        alliance_raids = [
            "The Labyrinth of the Ancients",
            "Syrcus Tower",
            "The World of Darkness",
        ]

        heavensward_alliance_raids = [
            "The Void Ark",
            "The Weeping City of Mhach",
            "Dun Scaith",
        ]

        stormblood_alliance_raids = [
            "The Royal City of Rabanastre",
            "The Ridorana Lighthouse",
            "The Orbonne Monastery",
        ]

        shadowbringers_alliance_raids = [
            "The Copied Factory",
            "The Puppets' Bunker",
            "The Tower at Paradigm's Breach",
        ]

        endwalker_alliance_raids = [
            "Aglaia",
            "Euphrosyne",
            "Thaleia",
        ]

        dawntrail_alliance_raids = [
            "Jeuno: The First Walk",
        ]

        if "Heavensward" in self.expansions_accessible:
            alliance_raids.extend(heavensward_alliance_raids)

        if "Stormblood" in self.expansions_accessible:
            alliance_raids.extend(stormblood_alliance_raids)

        if "Shadowbringers" in self.expansions_accessible:
            alliance_raids.extend(shadowbringers_alliance_raids)

        if "Endwalker" in self.expansions_accessible:
            alliance_raids.extend(endwalker_alliance_raids)

        if "Dawntrail" in self.expansions_accessible:
            alliance_raids.extend(dawntrail_alliance_raids)

        return sorted(alliance_raids)

    def chaotic_alliance_raids(self):
        chaotic_alliance_raids = list()

        dawntrail_chaotic_alliance_raids = [
            "The Cloud of Darkness (Chaotic)",
        ]

        if "Dawntrail" in self.expansions_accessible:
            chaotic_alliance_raids.extend(dawntrail_chaotic_alliance_raids)

        return sorted(chaotic_alliance_raids)



    @staticmethod
    def deep_dungeon_floor_range() -> range:
        return range(1,4)

    def deep_dungeons(self) -> List[str]:
        deep_dungeons = ["Palace of the Dead"]

        if "Stormblood" in self.expansions_accessible:
            deep_dungeons += ["Heaven-on-High"]

        if "Endwalker" in self.expansions_accessible:
            deep_dungeons += ["Eureka Orthos"]

        return sorted(deep_dungeons)
    
    def variant_dungeon_routes(self) -> List[str]:
        routes = list()

        if "Endwalker" in self.expansions_accessible:
            routes += [
                "Sil'dihn Subterrane: Whom the Silkie Serves",
                "Sil'dihn Subterrane: Pride and Acceptance",
                "Sil'dihn Subterrane: A Spot in the Sunlight",
                "Sil'dihn Subterrane: A Key Memory",
                "Sil'dihn Subterrane: In Father's Stead",
                "Sil'dihn Subterrane: Ul'dah's Sin to Bear",
                "Sil'dihn Subterrane: To Learn More of Myrrh",
                "Sil'dihn Subterrane: Ul'dah and Sil'dih",
                "Sil'dihn Subterrane: Raising the Flags",
                "Sil'dihn Subterrane: My Mother's Eyes",
                "Sil'dihn Subterrane: The Thorne Legacy",
                "Sil'dihn Subterrane: In Parchment We Trust",
                "Mount Rokkon: Gift of the Onmyoji",
                "Mount Rokkon: The Crimson Sword",
                "Mount Rokkon: A Tale of Dead Men",
                "Mount Rokkon: Forging a Legacy",
                "Mount Rokkon: The Luthier and the Songstress",
                "Mount Rokkon: Lost to Avarice",
                "Mount Rokkon: Beyond the Lanterns' Light",
                "Mount Rokkon: The Common Man's Courage",
                "Mount Rokkon: Sound of the Stone",
                "Mount Rokkon: The Seal of Silence",
                "Mount Rokkon: Seasons of the Fleeting",
                "Mount Rokkon: The Ogiseru's Fate",
                "Aloalo Island: A Not-quite Deserted Island",
                "Aloalo Island: The First Settlers of Aloalo Island",
                "Aloalo Island: God of Heaven and Sea",
                "Aloalo Island: A Noxious Gift",
                "Aloalo Island: The Roots of Arcanima",
                "Aloalo Island: Under the Boughs of the Great Tree",
                "Aloalo Island: A Dear Friend",
                "Aloalo Island: Fish for the Mind",
                "Aloalo Island: A Familiar History",
                "Aloalo Island: The Remnants of Faith",
                "Aloalo Island: A Lalafell or a Fish?",
                "Aloalo Island: Wellspring of Golden Memories",
            ]
        
        return sorted(routes)

    @staticmethod
    def masked_carnivale_range() -> range:
        return range(1,4)
    
    @staticmethod
    def masked_carnivale_weekly_targets() -> List[str]:
        return [
            "Novice",
            "Moderate",
            "Advanced",
        ]

    @staticmethod
    def masked_carnivale_completion_times() -> List[str]:
        return [
            "Standard",
            "Ideal",
        ]

    def masked_carnivale(self) -> List[str]:
        masked_carnivale = [
            "All's Well That Starts Well",
            "Much Ado About Pudding",
            "Waiting for Golem",
            "Gentlemen Prefer Swords",
            "The Threepenny Turtles",
            "Eye Society",
            "A Chorus Slime",
            "Bomb-edy of Errors",
            "To Kill a Mockingslime",
            "A Little Knight Music",
            "Some Like It Excruciatingly Hot",
            "The Plant-om of the Opera",
            "Beauty and a Beast",
            "Blobs in the Woods",
            "The Me Nobody Nodes",
            "Sunset Bull-evard",
            "The Sword of Music",
            "Midsummer Night's Explosion",
            "On a Clear Day You Can Smell Forever",
            "Miss Typhon",
            "Chimera on a Hot Tin Roof",
            "Here Comes the Boom",
            "Behemoths and Broomsticks",
            "Amazing Technicolor Pit Fiends",
            "Dirty Rotten Azulmagia",
        ]

        heavensward_masked_carnivale = [
            "Papa Mia",
            "Lock up Your Snorters",
            "Dangerous When Dead",
            "Red, Fraught, and Blue",
            "The Catch of the Siegfried",
        ]

        stormblood_masked_carnivale = [
            "Anything Gogo's",
        ]

        shadowbringers_masked_carnivale = [
            "A Golden Opportunity",
        ]

        if "Heavensward" in self.expansions_accessible:
            masked_carnivale.extend(heavensward_masked_carnivale)

        if "Stormblood" in self.expansions_accessible:
            masked_carnivale.extend(stormblood_masked_carnivale)

        if "Shadowbringers" in self.expansions_accessible:
            masked_carnivale.extend(shadowbringers_masked_carnivale)

        return sorted(masked_carnivale)

    @functools.cached_property
    def bozja_areas(self):
        return ["the Bozjan Southern Front", "Zadnor"]

    @functools.cached_property
    def bozja_raids(self):
        return ["Castrum Lacus Litore", "The Dalriada", "Delubrum Reginae"]

    @functools.cached_property
    def bozja_critical_engagements(self):
        return [
            "Kill It with Fire",
            "The Baying of the Hound(s)",
            "The Shadow of Death's Hand",
            "Vigil for the Lost",
            "Aces High",
            "Patriot Games",
            "The Final Furlong",
            "The Fires of War",
            "The Hunt for Red Choctober",
            "Beast of Man",
            "Metal Fox Chaos",
            "Rise of the Robots",
            "Trampled under Hoof",
            "Where Strode the Behemoth",
            "And the Flames Went Higher",
        ]

    @staticmethod
    def gathering_collectables_count_range() -> range:
        return range(3,13)
    
    def gathering_collectables(self) -> List[str]:
        gathering_collectables = list()

        heavensward_mining_collectables = [
            "Rarefied Mythrite Sand",
            "Rarefied Pyrite",
            "Rarefied Chalcocite",
            "Rarefied Limonite",
            "Rarefied Abalathian Spring Water",
            "Rarefied Aurum Regis Sand",
        ]

        heavensward_botany_collectables = [
            "Rarefied Rainbow Cotton Boll",
            "Rarefied Dark Chestnut Sap",
            "Rarefied Dark Chestnut Log",
            "Rarefied Dark Chestnut Branch",
            "Rarefied Dark Chestnut",
            "Rarefied Dark Chestnut Resin",
        ]

        stormblood_mining_collectables = [
            "Rarefied Gyr Abanian Mineral Water",
            "Rarefied Raw Triphane",
            "Rarefied Raw Star Spinel",
            "Rarefied Raw Kyanite",
            "Rarefied Raw Azurite",
            "Rarefied Silvergrace Ore",
        ]

        stormblood_botany_collectables = [
            "Rarefied Bloodhemp",
            "Rarefied Larch Log",
            "Rarefied Shiitake Mushroom",
            "Rarefied Larch Sap",
            "Rarefied Pine Resin",
            "Rarefied Pine Log",
        ]

        shadowbringers_mining_collectables = [
            "Rarefied Bluespirit Ore",
            "Rarefied Titancopper Ore",
            "Rarefied Raw Lazurite",
            "Rarefied Raw Petalite",
            "Rarefied Sea Salt",
            "Rarefied Reef Rock",
            "Rarefied Manasilver Sand",
            "Rarefied Raw Onyx",
            "Rarefied Gyr Abanian Alumen",
            "Rarefied Tungsten Ore",
        ]

        shadowbringers_botany_collectables = [
            "Rarefied Bright Flax",
            "Rarefied Pixie Apple",
            "Rarefied White Oak Log",
            "Rarefied Miracle Apple Log",
            "Rarefied Sandteak Log",
            "Rarefied Kelp",
            "Rarefied Night Pepper",
            "Rarefied Amber Cloves",
            "Rarefied Urunday Log",
            "Rarefied Coral",
        ]

        endwalker_mining_collectables = [
            "Rarefied Raw Ametrine",
            "Rarefied High Durium Ore",
            "Rarefied Bismuth Ore",
            "Rarefied Sharlayan Rock Salt",
            "Rarefied Phrygian Gold Ore",
            "Rarefied Blue Zircon",
            "Rarefied Eblan Alumen",
            "Rarefied Chloroschist",
            "Rarefied Pewter Ore",
            "Rarefied Annite",
        ]

        endwalker_botany_collectables = [
            "Rarefied Palm Log",
            "Rarefied Thavnairian Perilla Leaf",
            "Rarefied Red Pine Log",
            "Rarefied Coconut",
            "Rarefied Sykon",
            "Rarefied Dark Rye",
            "Rarefied Elder Nutmeg",
            "Rarefied Ironwood Log",
            "Rarefied AR-Caean Cotton Boll",
            "Rarefied Iceberg Lettuce",
        ]

        dawntrail_mining_collectables = [
            "Rarefied Raw Ihuykanite",
            "Rarefied Raw Dark Amber",
            "Rarefied Titanium Gold Ore",
            "Rarefied White Gold Ore",
            "Rarefied Magnesite Ore",
            "Rarefied Artificial Volcanic Rock",
            "Rarefied Ash Soil",
            "Rarefied Ra'Kaznar Ore",
        ]

        dawntrail_botany_collectables = [
            "Rarefied Kozama'uka Chamomile",
            "Rarefied Mountain Flax",
            "Rarefied Sweet Kukuru Bean",
            "Rarefied Acacia Bark",
            "Rarefied Dark Mahogany Log",
            "Rarefied Wild Agave",
            "Rarefied Windsbalm Bay Leaf",
            "Rarefied Acacia Log",
        ]

        if "Heavensward" in self.expansions_accessible:
            if "Miner" in self.playable_jobs:
                gathering_collectables.extend(heavensward_mining_collectables)

            if "Botanist" in self.playable_jobs:
                gathering_collectables.extend(heavensward_botany_collectables)

        if "Stormblood" in self.expansions_accessible:
            if "Miner" in self.playable_jobs:
                gathering_collectables.extend(stormblood_mining_collectables)

            if "Botanist" in self.playable_jobs:
                gathering_collectables.extend(stormblood_botany_collectables)

        if "Shadowbringers" in self.expansions_accessible:
            if "Miner" in self.playable_jobs:
                gathering_collectables.extend(shadowbringers_mining_collectables)

            if "Botanist" in self.playable_jobs:
                gathering_collectables.extend(shadowbringers_botany_collectables)

        if "Endwalker" in self.expansions_accessible:
            if "Miner" in self.playable_jobs:
                gathering_collectables.extend(endwalker_mining_collectables)

            if "Botanist" in self.playable_jobs:
                gathering_collectables.extend(endwalker_botany_collectables)

        if "Dawntrail" in self.expansions_accessible:
            if "Miner" in self.playable_jobs:
                gathering_collectables.extend(dawntrail_mining_collectables)

            if "Botanist" in self.playable_jobs:
                gathering_collectables.extend(dawntrail_botany_collectables)

        return sorted(gathering_collectables)
    
    @staticmethod
    def fishing_collectables_count_range() -> range:
        return range(3,13)
    
    def fishing_collectables(self) -> List[str]:
        fishing_collectables = list()

        heavensward_fishing_collectables = [
            "Glacier Core",
            "Icepick",
            "Whilom Catfish",
            "Sorcerer Fish",
            "Bubble Eye",
            "Dravanian Squeaker",
            "Warmwater Bichir",
            "Noontide Oscar",
            "Weston Bowfin",
            "Illuminati Perch",
            "Moogle Spirit",
            "Dravanian Smelt",
            "Vampiric Tapestry",
            "Thunderbolt Eel",
            "Tiny Axolotl",
            "Capelin",
            "Loosetongue",
            "Barreleye",
            "Stupendemys",
            "Amber Salamander",
        ]

        stormblood_fishing_collectables = [
            "Velodyna Grass Carp",
            "Butterfly Fish",
            "Yanxian Koi",
            "Killifish",
            "Mitsukuri Shark",
            "Silken Sunfish",
            "Eternal Eye",
            "Cherubfish",
            "Mosasaur",
            "Soul of the Stallion",
            "Fangshi",
            "Thousandfang",
            "Tao Bitterling",
            "Samurai Fish",
            "Daio Squid",
            "Seraphim",
            "Ala Mhigan Ribbon",
            "Wraithfish",
            "Swordfish",
            "Deemster",
            "Silken Koi",
            "Sculptor",
            "Hak Bitterling",
        ]

        shadowbringers_fishing_collectables = [
            "Albino Caiman",
            "Little Bismarck",
            "Bothriolepis",
            "Weedy Seadragon",
            "Golden Lobster",
            "Rak'tika Goby",
            "Elder Pixie",
            "Viis Ear",
            "Blue Mountain Bubble",
            "Diamond Pipira",
            "Eryops",
            "Winged Hatchetfish",
            "Pancake Octopus",
            "Ondo Harpoon",
            "Aapoak",
            "Darkdweller",
            "Toadhead",
            "Thorned Lizard",
            "Henodus",
            "Platinum Guppy",
        ]

        endwalker_fishing_collectables = [
            "Topminnow",
            "Othardian Wrasse",
            "Shogun's Kabuto",
            "Pipefish",
            "Seema Duta",
            "Pantherscale Grouper",
            "Xiphactinus",
            "Kitefin Shark",
            "Tebqeyiq Smelt",
            "Fleeting Brand",
            "Forgeflame",
            "Banana Eel",
            "Echinos",
            "Foun Myhk",
            "Phallaina",
            "Mangar",
            "Lunar Deathworm",
            "Basilosaurus",
            "Red Drum",
            "Labyrinthos Tilapia",
        ]

        dawntrail_fishing_collectables = [
            "Zorlortor",
            "Purussaurus",
            "Piraputanga",
            "Plattershell",
            "Mirror Carp",
            "Glittergill",
            "Moxutural Gar",
            "Toari Sucker",
            "Wivre Cod",
            "Iq Rrax Crab",
            "Goldgrouper",
            "Zorgor Condor",
            "Copper Shark",
            "Hydro Louvar",
            "Cloud Wasp",
            "Chain Shark",
            "Yellow Peacock Bass",
            "Urqofrog",
        ]

        if "Heavensward" in self.expansions_accessible:
            fishing_collectables.extend(heavensward_fishing_collectables)

        if "Stormblood" in self.expansions_accessible:
            fishing_collectables.extend(stormblood_fishing_collectables)

        if "Shadowbringers" in self.expansions_accessible:
            fishing_collectables.extend(shadowbringers_fishing_collectables)

        if "Endwalker" in self.expansions_accessible:
            fishing_collectables.extend(endwalker_fishing_collectables)

        if "Dawntrail" in self.expansions_accessible:
            fishing_collectables.extend(dawntrail_fishing_collectables)

        return sorted(fishing_collectables)

    def big_fish(self) -> List[str]:
        big_fish = [
            "Goldenfin",
            "Octomammoth",
            "Zalera",
            "Beguiler Chub",
            "Great Gudgeon",
            "Gigantshark",
            "High Perch",
            "Crystal Perch",
            "Caterwauler",
            "Oschon's Print",
            "Syldra",
            "Silver Sovereign",
            "Sabertooth Cod",
            "Jacques the Snipper",
            "Faerie Queen",
            "Meteor Survivor",
            "Cupfish",
            "The Greatest Bream in the World",
            "Shark Tuna",
            "Bombardfish",
            "The Old Man in the Sea",
            "The Salter",
            "The Drowned Sniper",
            "The Terpsichorean",
            "Mirrorscale",
            "Imperial Goldfish",
            "Armorer",
            "Junkmonger",
            "Navigator's Brand",
            "The Lone Ripper",
            "Helmsman's Hand",
            "Frilled Shark",
            "The Captain's Chalice",
            "Toramafish",
            "Joan of Trout",
            "Worm of Nym",
            "King of the Spring",
            "Thundergut",
            "Twitchbeard",
            "Stormdancer",
            "Bloody Brewer",
            "Matron Carp",
            "Carp Diem",
            "Chirurgeon",
            "Ghost Carp",
            "Levinlight",
            "Bloodbath",
            "The Green Jester",
            "Dark Ambusher",
            "Moldva",
            "The Assassin",
            "Sylphsbane",
            "Blue Widow",
            "Judgeray",
            "Shadowstreak",
            "Cornelia",
            "Son of Levin",
            "The Gobfather",
            "Vip Viper",
            "Floating Boulder",
            "The Grinner",
            "The Sinker",
            "Sweetnewt",
            "Glimmerscale",
            "Mud Golem",
            "Rivet Oyster",
            "Pirate's Bane",
            "Fingers",
            "Dirty Herry",
            "Dream Goby",
            "Slime King",
            "Old Softie",
            "Dark Knight",
            "Marrow Sucker",
            "Mud Pilgrim",
            "The Warden's Wand",
            "The Thousand-year Itch",
            "Olgoi-Khorkhoi",
            "Magic Carpet",
            "Old Hollow Eyes",
            "Discobolus",
            "Iron Noose",
            "Hannibal",
            "Spearnose",
            "The Matriarch",
            "Anomalocaris",
            "Charon's Lantern",
            "Daniffen's Mark",
            "Dawn Maiden",
            "Starbright",
            "Mahar",
            "Aetherlouse",
            "Void Bass",
            "Ninja Betta",
            "Ignus Horn",
            "Blood Red Bonytongue",
            "Canavan",
            "Namitaro",
            "Endoceras",
            "Helicoprion",
            "Kuno the Killer",
            "Shonisaurus",
            "Nepto Dragon",
        ]

        heavensward_big_fish = [
            "Fat Purse",
            "La Reale",
            "Bishopfish",
            "Hailfinder",
            "Captain Nemo",
            "Flarefish",
            "Merciless",
            "Inkfish",
            "Cirrostratus",
            "Basking Shark",
            "The Second One",
            "Paikiller",
            "Scaleripper",
            "Riddle",
            "The Lord of Lords",
            "Meteortoise",
            "The Dreamweaver",
            "Hraesvelgr's Tear",
            "Twin-tongued Carp",
            "Vidofnir",
            "Moggle Mogpom",
            "The Soul of the Martyr",
            "Dimorphodon",
            "Bloodchaser",
            "Thousand Fin",
            "The Ewer King",
            "Bobgoblin Bass",
            "Madam Butterfly",
            "The Speaker",
            "Augmented High Allagan Helmet",
            "Aetherochemical Compound #666",
            "Aphotic Pirarucu",
            "Ceti",
            "Allagan Bladeshark",
            "Crystal Pigeon",
            "Hundred-eyed Axolotl",
            "Armor Fish",
            "Problematicus",
            "Opabinia",
            "Raimdellopterus",
            "Charibenet",
            "Sea Butterfly",
        ]

        stormblood_big_fish = [
            "Downstream Loach",
            "Sapphire Fan",
            "Corpse Chub",
            "The Archbishop",
            "Hardhead Trout",
            "Hookstealer",
            "Watcher Catfish",
            "Bloodtail Zombie",
            "Bondsplitter",
            "The Last Tear",
            "Lily of the Veil",
            "Hemon",
            "Moksha",
            "The Undecided",
            "Diamond-eye",
            "Rising Dragon",
            "The Gambler",
            "Princess Killifish",
            "Ku'er",
            "The Vegetarian",
            "Pinhead",
            "Argonautica",
            "The Winter Queen",
            "Seven Stars",
            "Rakshasa",
            "Hermit's End",
            "Suiten Ippeki",
            "Hagoromo Koi",
            "The Unraveled Bow",
            "Pomegranate Trout",
            "Glarramundi",
            "Axelrod",
            "Hagoromo Bijin",
            "Banderole",
            "Duskfish",
            "Nhaama's Treasure",
            "Yat Khan",
            "Garden Skipper",
            "The Word of God",
            "Blade Skipper",
            "Drepanaspis",
            "The Unconditional",
            "Warden of the Seven Hues",
            "Xenacanthus",
            "Stethacanthus",
            "The Ruby Dragon",
        ]

        shadowbringers_big_fish = [
            "Loose Pendant",
            "The Sinsteeped",
            "Aster Trivi",
            "Winged Dame",
            "Sweetheart",
            "The Unforgiven",
            "Python Discus",
            "Moonlight Guppy",
            "The Jaws of Undeath",
            "White Ronso",
            "Bronze Sole",
            "Steel Fan",
            "Henodus Grandis",
            "Steel Razor",
            "Shadeshifter",
            "Giant Taimen",
            "The Horned King",
            "Nabaath Saw",
            "Ambling Caltrop",
            "Leannisg",
            "The Sound of Fury",
            "Gold Hammer",
            "Sunken Tome",
            "Fae Rainbow",
            "Dammroen Herring",
            "Celestial",
            "Priest of Yx'Lokwa",
            "Golden Pipira",
            "Recordkiller",
            "Black Jet",
            "Pearl Pipira",
            "Deephaunt",
            "Mora Tecta",
            "Starchaser",
            "The Ondotaker",
            "The Mother of All Pancakes",
            "Ondo Sigh",
            "Opal Shrimp",
            "Maru Crab",
            "Listracanthus",
            "Aquamaton",
            "Cinder Surprise",
            "Ealad Skaan",
            "Greater Serpent of Ronka",
            "Lancetfish",
        ]

        endwalker_big_fish = [
            "Aetherolectric Guitarfish",
            "Greatsword Snook",
            "Catastrophizer",
            "Jumbo Snook",
            "Swampsucker Bowfin",
            "Mossgill Salmon",
            "Earful",
            "Lale Crab",
            "Hippo Frog",
            "Bigcuda",
            "Browned Banana Eel",
            "Vidyutvat Wrasse",
            "Sovereign Shadow",
            "Rimepike",
            "Disappirarucu",
            "Frozen Regotoise",
            "Foun Ahlm",
            "Starscryer",
            "Forbiddingway",
            "Argonauta argo",
            "Cosmic Haze",
            "Planetes",
            "Antheian Dahlia",
            "Basilosaurus Rex",
            "Onyx Knifefish",
            "Eehs Fan",
            "Wakeful Warden",
            "Gilt Dermogenys",
            "Mayaman",
            "Starscale Ephemeris",
            "Chlorophos Deathworm",
            "Durdina Fish",
            "E.B.E.-852738",
            "Circuit Tilapia",
            "Hyphalosaurus",
            "Gharlichthys",
            "Snowy Parexus",
            "Lopoceras Elegans",
            "Furcacauda",
            "Sidereal Whale",
        ]

        dawntrail_big_fish = [
            "Icuvlo's Barter",
            "Moongripper",
            "Cazuela Crab",
            "Ilyon Asoh Cichlid",
            "Stardust Sleeper",
            "Hwittayoanaan Cichlid",
            "Thunderswift Trout",
            "Pixel Loach",
        ]

        return sorted(big_fish)

    @staticmethod
    def crafting_collectables_count_range() -> range:
        return range(3,13)
    
    def crafting_collectables(self) -> List[str]:
        crafting_collectables = list()

        heavensward_carpenter_collectables = [
            "Rarefied Cedar Longbow",
            "Rarefied Cedar Fishing Rod",
            "Rarefied Holy Cedar Spinning Wheel",
            "Rarefied Dark Chestnut Rod",
            "Rarefied Hallowed Chestnut Ring",
            "Rarefied Birch Signum",
        ]

        heavensward_blacksmith_collectables = [
            "Rarefied Mythrite Katzbalger",
            "Rarefied Mythrite Pugiones",
            "Rarefied Mythrite halfheart Saw",
            "Rarefied Titanium Creasing Knife",
            "Rarefied Titanium Mortar",
            "Rarefied Adamantite Bill",
        ]

        heavensward_armorer_collectables = [
            "Rarefied Mythrite Sallet",
            "Rarefied Mythrite Hauberk",
            "Rarefied Mythrite Bladed Lantern Shield",
            "Rarefied Titanium Frypan",
            "Rarefied Titanium Vambraces",
            "Rarefied Adamantite Scutum",
        ]

        heavensward_goldsmith_collectables = [
            "Rarefied Mythrite Goggles",
            "Rarefied Mythrite Bangle",
            "Rarefied Mythrite Needle",
            "Rarefied Hardsilver Monocle",
            "Rarefied Hardsilver Pole",
            "Rarefied Aurum Regis Earrings",
        ]

        heavensward_leatherworker_collectables = [
            "Rarefied Archaeoskin Belt",
            "Rarefied Archaeoskin Cloche",
            "Rarefied Wyvernskin Mask",
            "Rarefied Dhalmelskin Coat",
            "Rarefied Dragonskin Ring",
            "Rarefied Serpentskin Hat",
        ]

        heavensward_weaver_collectables = [
            "Rarefied Rainbow Bolero",
            "Rarefied Rainbow Ribbon",
            "Rarefied Holy Rainbow Hat",
            "Rarefied Ramie Turban",
            "Rarefied Hallowed Ramie Doublet",
            "Rarefied Chimerical Felt Cyclas",
        ]

        heavensward_alchemist_collectables = [
            "Rarefied Archaeoskin Grimoire",
            "Rarefied Archaeoskin Codex",
            "Rarefied Dissolvent",
            "Rarefied Dhalmelskin Codex",
            "Rarefied Max-Potion",
            "Rarefied Book of Aurum Regis",
        ]

        heavensward_culinarian_collectables = [
            "Rarefied Dhalmel Gratin",
            "Rarefied Sohm Al Tart",
            "Rarefied Sauteed Porcini",
            "Rarefied Royal Eggs",
            "Rarefied Peperoncino",
            "Rarefied Marron Glace",
        ]

        stormblood_carpenter_collectables = [
            "Rarefied Beech Composite Bow",
            "Rarefied Larch Necklace",
            "Rarefied Pine Cane",
            "Rarefied Persimmon Bracelets",
            "Rarefied Zelkova Spinning Wheel",
        ]

        stormblood_blacksmith_collectables = [
            "Rarefied High Steel Guillotine",
            "Rarefied High Steel Claw Hammer",
            "Rarefied Doman Iron Uchigatana",
            "Rarefied Doman Steel Patas",
            "Rarefied Molybdenum Pliers",
        ]

        stormblood_armorer_collectables = [
            "Rarefied High Steel Thermal Alembic",
            "Rarefied High Steel Plate Belt",
            "Rarefied Doman Iron Greaves",
            "Rarefied Doman Steel Tabard",
            "Rarefied Molybdenum Headgear",
        ]

        stormblood_goldsmith_collectables = [
            "Rarefied Koppranickel Planisphere",
            "Rarefied Koppranickel Necklace",
            "Rarefied Durium Chaplets",
            "Rarefied Durium Rod",
            "Rarefied Palladium Needle",
        ]

        stormblood_leatherworker_collectables = [
            "Rarefied Gaganaskin Shoes",
            "Rarefied Gyuki Leather Jacket",
            "Rarefied Tigerskin Tricorne",
            "Rarefied Marid Leather Corset",
            "Rarefied Gazelleskin Armguards",
        ]

        stormblood_weaver_collectables = [
            "Rarefied Bloodhempen Skirt",
            "Rarefied Ruby Cotton Gilet",
            "Rarefied Kudzu Hat",
            "Rarefied Serge Hose",
            "Rarefied Twinsilk Apron",
        ]

        stormblood_alchemist_collectables = [
            "Rarefied Koppranickel Index",
            "Rarefied Reisui",
            "Rarefied Tigerskin Grimoire",
            "Rarefied Growth Formula",
            "Rarefied Gazelleskin Codex",
        ]

        stormblood_culinarian_collectables = [
            "Rarefied Baklava",
            "Rarefied Shorlog",
            "Rarefied Tempura Platter",
            "Rarefied Persimmon Pudding",
            "Rarefied Chirashi-zushi",
        ]

        shadowbringers_carpenter_collectables = [
            "Rarefied White Oak Partisan",
            "Rarefied Applewood Staff",
            "Rarefied White Ash Earrings",
            "Rarefied Sandteak Fauchard",
            "Rarefied Lignum Vitae Grinding Wheel",
        ]

        shadowbringers_blacksmith_collectables = [
            "Rarefied Deepgold Anelace",
            "Rarefied Deepgold Culinary Knife",
            "Rarefied Bluespirit Gunblade",
            "Rarefied Titanbronze Pickaxe",
            "Rarefied Mythril Hatchet",
        ]

        shadowbringers_armorer_collectables = [
            "Rarefied Deepgold Cuirass",
            "Rarefied Deepgold Wings",
            "Rarefied Bluespirit Gauntlets",
            "Rarefied Titanbronze Tower Shield",
            "Rarefied Mythril Alembic",
        ]

        shadowbringers_goldsmith_collectables = [
            "Rarefied Stonegold Degen",
            "Rarefied Stonegold Orrery",
            "Rarefied Manasilver Ear Cuffs",
            "Rarefied Titanbronze Headgear",
            "Rarefied Mythril Ring",
        ]

        shadowbringers_leatherworker_collectables = [
            "Rarefied Smilodonskin Trousers",
            "Rarefied Gliderskin Thighboots",
            "Rarefied Atrociraptorskin Cap",
            "Rarefied Zonureskin Fingerless Gloves",
            "Rarefied Swallowskin Coat",
        ]

        shadowbringers_weaver_collectables = [
            "Rarefied Brightlinen Himation",
            "Rarefied Iridescent Top",
            "Rarefied Pixie Cotton Hood",
            "Rarefied Ovim Wool Tunic",
            "Rarefied Dwarven Cotton Beret",
        ]

        shadowbringers_alchemist_collectables = [
            "Rarefied Alkahest",
            "Rarefied Gliderskin Grimoire",
            "Rarefied Bluespirit Codex",
            "Rarefied Syrup",
            "Rarefied Dwarven Mythrile Grimoire",
        ]

        shadowbringers_culinarian_collectables = [
            "Rarefied Grilled Rail",
            "Rarefied Spaghetti al Nero",
            "Rarefied Popotoes au Gratin",
            "Rarefied Espresso con Panna",
            "Rarefied Lemonade",
        ]

        endwalker_carpenter_collectables = [
            "Rarefied Horse Chestnut Kasa",
            "Rarefied Palm Bracelet",
            "Rarefied Red Pine Spinning Wheel",
            "Rarefied Ironwood Grinding Wheel",
            "Rarefied Integral Armillae",
            "Rarefied Integral Fishing Rod",
        ]

        endwalker_blacksmith_collectables = [
            "Rarefied High Durium Pistol",
            "Rarefied High Durium Greatsword",
            "Rarefied Bismuth Sledgehammer",
            "Rarefied Manganese Cross-pein Hammer",
            "Rarefied Chondrite Culinary Knife",
            "Rarefied Chondrite Lapidary Hammer",
        ]

        endwalker_armorer_collectables = [
            "Rarefied High Durium Knuckles",
            "Rarefied High Durium Kite Shield",
            "Rarefied Bismuth Fat Cat Frypan",
            "Rarefied Manganese Armor of the Behemoth King",
            "Rarefied Chondrite Sollerets",
            "Rarefied Chondrite Alembic",
        ]

        endwalker_goldsmith_collectables = [
            "Rarefied High Durium Milpreves",
            "Rarefied Pewter Choker",
            "Rarefied Phrygian Earring",
            "Rarefied Manganese Horn of the Last Unicorn",
            "Rarefied Star Quartz Choker",
            "Rarefied Chondrite Needle",
        ]

        endwalker_leatherworker_collectables = [
            "Rarefied Gajaskin Shoes",
            "Rarefied Luncheon Toadskin Hose",
            "Rarefied Saigaskin Gloves",
            "Rarefied Kumbhiraskin Shoes",
            "Rarefied Ophiotauroskin Top",
            "Rarefied Ophiotauroskin Halfgloves",
        ]

        endwalker_weaver_collectables = [
            "Rarefied Darkhempen Hat",
            "Rarefied Almasty Serge Gloves",
            "Rarefied Snow Linen Doublet",
            "Rarefied Scarlet Moko Wedge Cap",
            "Rarefied AR-Caean Velvet Bottoms",
            "Rarefied AR-Caean Velvet Work Cap",
        ]

        endwalker_alchemist_collectables = [
            "Rarefied Gajaskin Codex",
            "Rarefied Luncheon Toadskin Grimoire",
            "Rarefied Moon Gel",
            "Rarefied Enchanted Manganese Ink",
            "Rarefied Draught",
            "Rarefied Ophiotauroskin Magitek Codex",
        ]

        endwalker_culinarian_collectables = [
            "Rarefied Archon Loaf",
            "Rarefied King Crab Cake",
            "Rarefied Happiness Juice",
            "Rarefied Giant Haddock Dip",
            "Rarefied Giant Popoto Pancakes",
            "Rarefied Sykon Bavarois",
        ]

        dawntrail_carpenter_collectables = [
            "Rarefied Ginseng Earrings",
            "Rarefied Ceiba Spear",
            "Rarefied Dark Mahogany Necklace",
            "Rarefied Acacia Rod",
            "Rarefied Claro Walnut Grinding Wheel",
            "Rarefied Claro Walnut Fishing Rod",
        ]

        dawntrail_blacksmith_collectables = [
            "Rarefied Mountain Chromite Fists",
            "Rarefied Ruthenium War Axe",
            "Rarefied Cobalt Tungsten Scimitars",
            "Rarefied Titanium Gold Mortar",
            "Rarefied Ra'Kaznar War Scythe",
            "Rarefied Ra'Kaznar Round Knife",
        ]

        dawntrail_armorer_collectables = [
            "Rarefied Mountain Chromite Alembic",
            "Rarefied Ruthenium Sabatons",
            "Rarefied Cobalt Tungsten Chocobo Frypan",
            "Rarefied Titanium Gold Thorned Corselet",
            "Rarefied Ra'Kaznar Greaves",
            "Rarefied Ra'Kaznar Ring",
        ]

        dawntrail_goldsmith_collectables = [
            "Rarefied Lar Longbow",
            "Rarefied Ihuykanite Circlet",
            "Rarefied Cobalt Tungsten Tuck",
            "Rarefied White Gold Choker",
            "Rarefied Ra'Kaznar Orrery",
            "Rarefied Black Star Earrings",
        ]

        dawntrail_leatherworker_collectables = [
            "Rarefied Loboskin Fingerless Gloves",
            "Rarefied Crocodileskin Leggings",
            "Rarefied Br'aaxskin Armlets",
            "Rarefied Gomphotherium Brais",
            "Rarefied Gargantuaskin Trousers",
            "Rarefied Gargantuaskin Hat",
        ]

        dawntrail_weaver_collectables = [
            "Rarefied Snow Cotton Beret",
            "Rarefied Mountain Linen Top",
            "Rarefied Sarcenet Kecks",
            "Rarefied Rroneek Serge Hat",
            "Rarefied Thunderyards Silk Gloves",
            "Rarefied Thunderyards Silk Culottes",
        ]

        dawntrail_alchemist_collectables = [
            "Rarefied Loboskin Grimoire",
            "Rarefied Gemsap of Dexterity",
            "Rarefied Br'aaxskin Codex",
            "Rarefied Cunning Craftsman's Tisane",
            "Rarefied Gemdraught of Vitality",
            "Rarefied Claro Walnut Flat Brush",
        ]

        dawntrail_culinarian_collectables = [
            "Rarefied Boiled Alpaca Steak",
            "Rarefied Banana Ponzecake",
            "Rarefied Turali Pineapple Ponzecake",
            "Rarefied Salmon Jerky",
            "Rarefied Stuffed Peppers",
            "Rarefied Tacos de Carne Asada",
        ]

        if "Heavensward" in self.expansions_accessible:
            if "Carpenter" in self.playable_jobs:
                crafting_collectables.extend(heavensward_carpenter_collectables)

            if "Blacksmith" in self.playable_jobs:
                crafting_collectables.extend(heavensward_blacksmith_collectables)

            if "Armorer" in self.playable_jobs:
                crafting_collectables.extend(heavensward_armorer_collectables)

            if "Goldsmith" in self.playable_jobs:
                crafting_collectables.extend(heavensward_goldsmith_collectables)

            if "Leatherworker" in self.playable_jobs:
                crafting_collectables.extend(heavensward_leatherworker_collectables)

            if "Weaver" in self.playable_jobs:
                crafting_collectables.extend(heavensward_weaver_collectables)

            if "Alchemist" in self.playable_jobs:
                crafting_collectables.extend(heavensward_alchemist_collectables)

            if "Culinarian" in self.playable_jobs:
                crafting_collectables.extend(heavensward_culinarian_collectables)

        if "Stormblood" in self.expansions_accessible:
            if "Carpenter" in self.playable_jobs:
                crafting_collectables.extend(stormblood_carpenter_collectables)

            if "Blacksmith" in self.playable_jobs:
                crafting_collectables.extend(stormblood_blacksmith_collectables)

            if "Armorer" in self.playable_jobs:
                crafting_collectables.extend(stormblood_armorer_collectables)

            if "Goldsmith" in self.playable_jobs:
                crafting_collectables.extend(stormblood_goldsmith_collectables)

            if "Leatherworker" in self.playable_jobs:
                crafting_collectables.extend(stormblood_leatherworker_collectables)

            if "Weaver" in self.playable_jobs:
                crafting_collectables.extend(stormblood_weaver_collectables)

            if "Alchemist" in self.playable_jobs:
                crafting_collectables.extend(stormblood_alchemist_collectables)

            if "Culinarian" in self.playable_jobs:
                crafting_collectables.extend(stormblood_culinarian_collectables)

        if "Shadowbringers" in self.expansions_accessible:
            if "Carpenter" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_carpenter_collectables)

            if "Blacksmith" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_blacksmith_collectables)

            if "Armorer" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_armorer_collectables)

            if "Goldsmith" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_goldsmith_collectables)

            if "Leatherworker" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_leatherworker_collectables)

            if "Weaver" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_weaver_collectables)

            if "Alchemist" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_alchemist_collectables)

            if "Culinarian" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_culinarian_collectables)

        if "Endwalker" in self.expansions_accessible:
            if "Carpenter" in self.playable_jobs:
                crafting_collectables.extend(endwalker_carpenter_collectables)

            if "Blacksmith" in self.playable_jobs:
                crafting_collectables.extend(endwalker_blacksmith_collectables)

            if "Armorer" in self.playable_jobs:
                crafting_collectables.extend(endwalker_armorer_collectables)

            if "Goldsmith" in self.playable_jobs:
                crafting_collectables.extend(endwalker_goldsmith_collectables)

            if "Leatherworker" in self.playable_jobs:
                crafting_collectables.extend(endwalker_leatherworker_collectables)

            if "Weaver" in self.playable_jobs:
                crafting_collectables.extend(endwalker_weaver_collectables)

            if "Alchemist" in self.playable_jobs:
                crafting_collectables.extend(endwalker_alchemist_collectables)

            if "Culinarian" in self.playable_jobs:
                crafting_collectables.extend(endwalker_culinarian_collectables)

        if "Dawntrail" in self.expansions_accessible:
            if "Carpenter" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_carpenter_collectables)

            if "Blacksmith" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_blacksmith_collectables)

            if "Armorer" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_armorer_collectables)

            if "Goldsmith" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_goldsmith_collectables)

            if "Leatherworker" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_leatherworker_collectables)

            if "Weaver" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_weaver_collectables)

            if "Alchemist" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_alchemist_collectables)

            if "Culinarian" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_culinarian_collectables)

        return sorted(crafting_collectables)
    
    @staticmethod
    def crystalline_conflict_match_counts() -> range:
        return range(1,6)
    
    @staticmethod
    def gate_count() -> range:
        return range(3,7)

    @staticmethod
    def gate_tasks() -> List[str]:
        gates = [
            "Successfully complete the GATE 'The Slice Is Right'",
            "Record a perfect score in the GATE 'Air Force One'",
            "Obtain all cactuars in the GATE 'Leap of Faith'",
            "Successfully complete the GATE 'Any Way the Wind Blows'",
            "Complete the GATE 'Cliffhanger' without being knocked back by any explosives",
        ]

        return sorted(gates)

    @staticmethod
    def triple_triad_range() -> range:
        return range(2,6)

    @staticmethod
    def triple_triad_rarity_range() -> range:
        return range(1,5)

    def triple_triad(self) -> List[str]:
        triple_triad = [
            "Memeroon",
            "Jonas of the Three Spades",
            "Maisenta",
            "Roger",
            "Guhtwint of the Three Diamonds",
            "Mother Miounne",
            "Wymond",
            "Momodi",
            "F'hobhas",
            "Triple Triad Master",
            "Joellaut",
            "Aurifort of the Three Clubs",
            "Piralnaut",
            "Trachtoum",
            "Mimidoa",
            "Baderon",
            "Fufulupa",
            "Helmhart",
            "Ourdilic",
            "Ruhtwyda of the Three Hearts",
            "Marcette",
            "Buscarron",
            "Sezul Totoloc",
            "Landenel",
            "King Elmer III",
            "Vorsaile Heuloix",
            "Swift",
            "Hab",
            "Indolent Imperial",
            "Rowena",
            "Gegeruju",
            "R'ashaht Rhiki",
            "Lewena",
            "Noes",
            "Yellow Moon",
            "Wawalago",
            "Yayake",
            "Gibrillont",
            "Wyra 'Greenhands' Lyehga",
            "Prideful Stag",
            "Nell Half-full",
            "Flichoirel the Lordling",
            "Hall Overseer",
        ]

        heavensward_triple_triad = [
            "Marcechamp",
            "Marielle",
            "Midnight Dew",
            "Idle Imperial",
            "Mogmill",
            "Dominiac",
            "Linu Vali",
            "Vath Deftarm",
            "Elaisse",
            "Laniaitte",
            "Voracious Vath",
            "Seika",
            "Tapklix",
            "Redbill Storeboy",
            "Klynthota",
            "House Fortemps Manservant",
            "Master Mogzin",
            "O'kalkaya",
            "Mordyn",
        ]

        stormblood_triple_triad = [
            "Ercanbald",
            "Kotokaze",
            "Kaizan",
            "Tsuzura",
            "Gyoei",
            "Nigen",
            "Ogodei",
            "Munglig",
            "Kiuka",
            "Garima",
            "Imperial Deserter",
            "Umber Torrent",
            "Hachinan",
            "Masatsuchi",
            "Isobe",
            "Yusui",
            "Kikimo",
            "Ushiogi",
            "Botan",
            "Mero Roggo",
            "Hokushin",
            "Hetsukaze",
            "Ironworks Hand",
        ]

        shadowbringers_triple_triad = [
            "Glynard",
            "Gyuf Uin",
            "Hargra",
            "Drery",
            "Ibenart",
            "Lamlyn",
            "Saushs Koal",
            "Grewenn",
            "Eo Sigun",
            "Redard",
            "Hanagasa",
            "Cobleva",
            "Furtive Former Imperial",
            "Arsieu",
            "Lewto-Sue",
            "Droyn",
            "Sladkey",
        ]

        endwalker_triple_triad = [
            "Aiglephine",
            "Qetanur",
            "Worldly Imperial",
            "Mehryde",
            "Cheatingway",
            "Celia",
            "Prudence",
            "Ghasa",
            "Kilfufu",
            "Gamingway",
            "Ruissenaud",
            "Tokimori",
            "Ylaire",
            "Maillart",
        ]

        dawntrail_triple_triad = [
            "Nyikweni",
            "Wopli",
            "Warsowok",
            "Br'uk Noq'",
            "Luwyawa",
            "Uataaye",
            "Larisa",
            "Gavoll Ja",
            "Pawkukwe",
            "Miitso",
        ]

        if "Heavensward" in self.expansions_accessible:
            triple_triad.extend(heavensward_triple_triad)

        if "Stormblood" in self.expansions_accessible:
            triple_triad.extend(stormblood_triple_triad)

        if "Shadowbringers" in self.expansions_accessible:
            triple_triad.extend(shadowbringers_triple_triad)

        if "Endwalker" in self.expansions_accessible:
            triple_triad.extend(endwalker_triple_triad)

        if "Dawntrail" in self.expansions_accessible:
            triple_triad.extend(dawntrail_triple_triad)

        return sorted(triple_triad)

    @staticmethod
    def high_low_range() -> range:
        return range(2,6)


# Archipelago Options
class FinalFantasyXIVContentTypesAllowed(OptionSet):
    """
    Indicates what possible Final Fantasy XIV content types the player would like to include.

    Note: Opting in to Unreasonable Tasks adds extra objectives to several different content types, 
    which could potentially take multiple days or weeks to even make an attempt.
    """

    display_name = "Final Fantasy XIV Allowed Content Types"
    valid_keys = [
        # Battle Content
        "FATEs",
        "Guildhests",
        "The Hunt",
        "Dungeons",
        "Trials",
        "Extreme Trials",
        "Normal Raids",
        "Savage Raids",
        "Alliance Raids",
        "Chaotic Alliance Raids"
        "Deep Dungeons",
        "Variant Dungeons",
        "Limited Jobs",
        "Bozja"
        # PvP
        "Crystalline Conflict",
        "Frontline",
        "Rival Wings",
        # Non-combat
        "Gathering",
        "Fishing",
        "Crafting",
        "Jumping Puzzles",
        "Gold Saucer",
        "Triple Triad",
        "Minigames",
        # Special
        "Unreasonable Tasks",
    ]

    default = valid_keys


class FinalFantasyXIVExpansionsAccessible(OptionSet):
    """
    Indicates which Final Fantasy XIV expansions the player has access to.
    """

    display_name = "Final Fantasy XIV Expansions Accessible"
    valid_keys = [
        "Heavensward",
        "Stormblood",
        "Shadowbringers",
        "Endwalker",
        "Dawntrail",
    ]

    default = valid_keys


class FinalFantasyXIVPlayableJobs(OptionSet):
    """
    Indicates what jobs the player has unlocked to be considered for challenges.

    It is recommended to only enable jobs which are of a sufficient level to participate in content of
    the latest expansion that will be allowed, or that can be leveled to that point over the course
    of your game.
    """

    display_name = "Final Fantasy XIV Playable Jobs"
    valid_keys = [
        # Combat
        "Paladin",
        "Warrior",
        "Dark Knight",
        "Gunbreaker",
        "White Mage",
        "Scholar",
        "Astrologian",
        "Sage",
        "Monk",
        "Dragoon",
        "Ninja",
        "Samurai",
        "Reaper",
        "Viper",
        "Bard",
        "Machinist",
        "Dancer",
        "Black Mage",
        "Summoner",
        "Red Mage",
        "Pictomancer",
        # Limited Jobs
        "Blue Mage",
        # "Beastmaster",
        # Crafting
        "Carpenter",
        "Blacksmith",
        "Armorer",
        "Goldsmith",
        "Leatherworker",
        "Weaver",
        "Alchemist",
        "Culinarian",
        # Gathering
        "Miner",
        "Botanist",
        "Fisher",
    ]

    default = valid_keys
