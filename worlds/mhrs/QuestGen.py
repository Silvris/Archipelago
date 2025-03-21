import orjson
import json
import os
import zipfile
from pkgutil import get_data
from random import Random
from typing import TYPE_CHECKING

from worlds.Files import APContainer
from .Locations import get_quest_table

if TYPE_CHECKING:
    from . import MHRSWorld
stage_choices = [
    1,  # Shrine Ruins
    2,  # Sandy Plains
    3,  # Flooded Forest
    4,  # Frost Islands
    5,  # Lava Caverns
    9,  # Infernal Springs
    10,  # Arena
    11,  # Coral Palace
    12,  # Jungle
    13,  # Citadel
    14,  # Forlorn Arena
    15  # Yawning Abyss
]

arena_choices = [
    9,  # Infernal Springs
    10,  # Arena
    11,  # Coral Palace
    14,  # Forlorn Arena
    15  # Yawning Abyss
]

stage_set_max = {
    1: 13,
    2: 12,
    3: 14,
    4: 12,
    5: 14,
    9: 1,
    10: 1,
    11: 1,
    # 2 valid areas, however there exists no transition between the two tmk (and I'm unsure how to set between the two)
    12: 11,
    13: 14,
    14: 1,
    15: 1  # 2 valid areas, however monsters likely don't transition to the second area other than Gaisma
}

stage_zako = {
    1: 35,  # Shrine Ruins
    2: 37,  # Sandy Plains
    3: 39,  # Flooded Forest
    4: 15,  # Frost Islands
    5: 43,  # Lava Caverns
    9: 0,  # Infernal Springs
    10: 0,  # Arena
    11: 0,  # Coral Palace
    12: 46,  # Jungle
    13: 49,  # Citadel
    14: 0,  # Forlorn Arena
    15: 0  # Yawning Abyss
}

monster_choices = [
    # Monsters that are always an option for generation
    # Rathian
    # Rathalos
    3,  # Khezu
    4,  # Basarios
    # Diablos
    19,  # Daimyo Hermitaur
    20,  # Shogun Ceanataur
    23,  # Rajang
    # skip Kushala, Teostra, and Chameleos
    32,  # Tigrex
    37,  # Nargacuga
    42,  # Barioth
    44,  # Barroth
    47,  # Royal Ludroth
    54,  # Great Baggi
    # Zinogre
    58,  # Amatsu
    59,  # Great Wroggi
    # Arzuros
    61,  # Lagombi
    62,  # Volvidon
    71,  # Gore Magala
    # Shagaru Magala
    77,  # Seregios
    81,  # Astalos
    # Mizutsune
    89,  # Magnamalo
    90,  # Bishaten
    91,  # Aknosom
    92,  # Tetranadon
    93,  # Somnacanth
    94,  # Rakna-Kadaki
    95,  # Almudron
    96,  # Wind Serpent Ibushi
    97,  # Goss Harag
    98,  # Great Izuchi
    # Thunder Serpent Narwa is invalid, HR only
    100,  # Anjanath
    102,  # Pukei-Pukei
    107,  # Kulu-Ya-Ku
    108,  # Jyuratodus
    109,  # Tobi-Kadachi
    118,  # Bazelgeuse
    124,  # Velkhana
    132,  # Malzeno
    133,  # Lunagaron
    134,  # Garangolm
    135,  # Gaismagorm
    136,  # Espinas
    346,  # Blood Orange Bishaten
    349,  # Aurora Somnacanth
    350,  # Pyre Rakna-Kadaki
    351,  # Magma Almudron
    392,  # Flaming Espinas
    513,  # Gold Rathian
    514,  # Silver Rathalos
    549,  # Lucent Nargacuga
    594,  # Violet Mizutsune
    1303,  # Furious Rajang
    1351,  # Chaotic Gore Magala
    # Crimson Glow Valstrax
    1369,  # Scorned Magnamalo
    1379,  # Narwa the Allmother
    1398,  # Seething Bazelgeuse
    1412   # Primordial Malzeno
]

monster_icons = {
    1: 0,  # Rathian
    2: 1,  # Rathalos
    3: 2,  # Khezu
    4: 3,  # Basarios
    7: 4,  # Diablos
    19: 43,  # Daimyo Hermitaur
    20: 44,  # Shogun Ceanataur
    23: 5,  # Rajang
    24: 6,  # Kushala Daora
    25: 7,  # Chameleos
    27: 8,  # Teostra
    32: 9,  # Tigrex
    37: 10,  # Nargacuga
    42: 11,  # Barioth
    44: 12,  # Barroth
    47: 13,  # Royal Ludroth
    54: 14,  # Great Baggi
    57: 15,  # Zinogre
    58: 66,  # Amatsu
    59: 16,  # Great Wroggi
    60: 17,  # Arzuros
    61: 18,  # Lagombi
    62: 19,  # Volvidon
    71: 47,  # Gore Magala
    72: 48,  # Shagaru Magala, may have to remove in the future
    77: 49,  # Seregios
    81: 50,  # Astalos
    82: 20,  # Mizutsune
    89: 22,  # Magnamalo
    90: 23,  # Bishaten
    91: 24,  # Aknosom
    92: 25,  # Tetranadon
    93: 26,  # Somnacanth
    94: 27,  # Rakna-Kadaki
    95: 28,  # Almudron
    96: 29,  # Wind Serpent Ibushi
    97: 30,  # Goss Harag
    98: 31,  # Great Izuchi
    # Thunder Serpent Narwa is invalid, HR only
    100: 33,  # Anjanath
    102: 34,  # Pukei-Pukei
    107: 35,  # Kulu-Ya-Ku
    108: 36,  # Jyuratodus
    109: 37,  # Tobi-Kadachi
    118: 38,  # Bazelgeuse
    124: 65,  # Velkhana
    132: 58,  # Malzeno
    133: 59,  # Lunagaron
    134: 60,  # Garangolm
    135: 61,  # Gaismagorm
    136: 62,  # Espinas
    346: 53,  # Blood Orange Bishaten
    349: 54,  # Aurora Somnacanth
    350: 55,  # Pyre Rakna-Kadaki
    351: 56,  # Magma Almudron
    392: 63,  # Flaming Espinas
    513: 41,  # Gold Rathian
    514: 42,  # Silver Rathalos
    549: 46,  # Lucent Nargacuga
    594: 51,  # Violet Mizutsune
    1303: 45,  # Furious Rajang
    1351: 64,  # Chaotic Gore Magala
    1366: 21,  # Crimson Glow Valstrax
    1369: 52,  # Scorned Magnamalo
    1379: 40,  # Narwa the Allmother
    1398: 57,  # Seething Bazelgeuse
    1412: 67,  # Primordial Malzeno
    1793: 69,  # Apex Rathian
    1794: 70,  # Apex Rathalos
    1799: 71,  # Apex Diablos
    1849: 72,  # Apex Zinogre
    1852: 73,  # Apex Arzuros
    1874: 74,  # Apex Mizutsune
    2072: 6,   # Risen Kushala uses regular Kushala
    2073: 7,   # Risen Chameleos uses regular Chameleos
    2075: 8,   # Risen Teostra uses regular Teostra
    2120: 48,  # Risen Shagaru uses regular Shagaru
    2134: 21   # Risen Valstrax uses Crimson Glow Valstrax
}

final_boss_remap = {
    2: 135,
    3: 24,
    4: 25,
    5: 27,
    6: 1369,
    7: 132,
    8: 72,
    9: 1366,
    10: 96,
    11: 1379,
    12: 513,
    13: 514,
    14: 549,
    15: 392,
    16: 594,
    17: 1303,
    18: 1351,
    19: 124,
    20: 58,
    21: 1412,
    22: 0
}


def random_normal_integer(slot_random: Random, mu: int, sigma: int, lower: int, upper: int) -> int:
    num = int(slot_random.normalvariate(mu, sigma))
    return max(lower, min(upper, num))


def can_afflict(monster: int):
    if monster in {24, 25, 27, 58, 72, 96, 124, 132, 135, 549, 594, 1379, 1366, 1412, 2072, 2073, 2075, 2134, 1793, 1794,
                   1799, 1849, 1852, 1874}:
        return False
    else:
        return True


def is_elder_dragon(monster: int):
    if monster in {24, 25, 27, 58, 72, 96, 124, 132, 135, 1366, 1379, 1412, 2072, 2073, 2075, 2134}:
        return True
    else:
        return False


def is_apex(monster: int):
    if (monster & 1792) > 0:
        return True  # this is true because each monster's id consists of two values: the main index (lowest 8 bits)
        # and the sub index (upper 8/24 bits). For apex, sub index is 07
    else:
        return False


def is_risen(monster: int):
    if (monster & 2048) > 0:
        return True  # this is true because each monster's id consists of two values: the main index (lowest 8 bits)
        # and the sub index (upper 8/24 bits). For risen, sub index is 08
    else:
        return False


def get_quest_type(targets: list):
    for target in targets:
        if is_elder_dragon(target) or is_apex(target):
            # since elders and apex cannot be captured, we it to slay
            quest_type = 1
            break
    else:
        quest_type = 2
    return quest_type


def get_quest_goal(targets: list) -> list:
    goals = list()
    for target in targets:
        if is_elder_dragon(target) or is_apex(target):
            goals.append(2)
        else:
            goals.append(3)
    return goals


def generate_valid_monster(stage: int, allowed_monsters: list, slot_random: Random) -> int:
    monster = slot_random.choice(allowed_monsters)
    if monster == 135 and stage != 15:
        return generate_valid_monster(stage, allowed_monsters, slot_random)
    if monster == 1379 and stage != 11:
        return generate_valid_monster(stage, allowed_monsters, slot_random)
    return monster


def randomize_quest(world: "MHRSWorld", allowed_monsters: list,
                    quest_id: int, quest_targets=None, is_hunting_road=False) -> str:
    if quest_targets is None or is_hunting_road:
        quest_targets = []  # clean the quest targets for Hunting Road
    json_data = get_data(__package__, f"quests/q{quest_id}.json")
    quest_data = orjson.loads(json_data)
    if not quest_data:
        raise FileNotFoundError(f"quests/q{quest_id}.json could not be found!")

    if not quest_data["QuestData"] or not quest_data["EnemyData"]:
        raise FileNotFoundError(f"quests/q{quest_id}.json is destroyed!")

    normal = quest_data["QuestData"]
    enemy = quest_data["EnemyData"]

    if 135 in quest_targets:
        stage = 15  # gaismagorm can only spawn in the Yawning Abyss
    elif 1379 in quest_targets:
        stage = 11  # allmother can only spawn in the Coral Palace
    elif is_hunting_road or world.options.arena_only:
        stage = world.random.choice(arena_choices)
    else:
        stage = world.random.choice(stage_choices)
    if len(quest_targets) > 0:
        mon_num = len(quest_targets)
    elif is_hunting_road:
        mon_num = 5
    else:
        mon_num = world.random.randint(1, 5)
    monsters = list()
    for i in range(0, 5):
        if i < len(quest_targets):
            monsters.append(quest_targets[i])
        else:
            monster = 0 if stage in arena_choices and i >= mon_num else \
                generate_valid_monster(stage, allowed_monsters, world.random)
            monsters.append(monster)
            if i < mon_num:
                quest_targets.append(monster)
    if mon_num > 2:
        normal["QuestType"] = 8
        normal["TargetTypes"] = [5, 0]
        normal["TargetAmounts"] = [mon_num, 0]
    else:
        capture = world.random.randint(1, 10)
        quest_type = get_quest_type(quest_targets)
        quest_goals = get_quest_goal(quest_targets)
        if capture > 7 and quest_type == 3:
            quest_type = 4
            for i in range(len(quest_goals)):
                if quest_goals[i] == 2:
                    quest_goals[i] = 4
        normal["QuestType"] = quest_type
        normal["TargetTypes"] = [quest_goals[0], quest_goals[1] if mon_num > 1 else 0]
        normal["TargetMonsters"] = [quest_targets[0], quest_targets[1] if mon_num > 1 else 0]
        normal["TargetAmounts"] = [1, 1 if mon_num > 1 else 0]
    normal["Map"] = stage
    normal["Carts"] = world.random.choices([1, 3, 5], [5, 85, 10])[0]

    for i in range(5):
        normal["Monsters"][i]["Id"] = monsters[i]
        normal["Monsters"][i]["SpawnCondition"] = 1 if i < min(mon_num, 3) else 14
        normal["Monsters"][i]["SpawnParam"] = 100

    for i in range(5):
        if i < mon_num:
            normal["Icons"][i] = monster_icons[quest_targets[i]]
        else:
            normal["Icons"][i] = 999

    # edge cases
    if quest_id == 315100:
        normal["QuestConditions"] = [0, 0]

    if stage == 10:
        normal["ArenaParam"]["FenceDefaultActive"] = False
        normal["ArenaParam"]["FenceUptime"] = world.random.randint(15, 120)
        normal["ArenaParam"]["FenceInitialDelay"] = world.random.randint(15, 600)
        normal["ArenaParam"]["FenceCooldown"] = world.random.randint(15, 240)
        normal["ArenaParam"]["Pillars"] = [
            bool(world.random.randint(0, 1)),
            bool(world.random.randint(0, 1)),
            bool(world.random.randint(0, 1))
        ]
    # vanity
    normal["BaseTime"] = world.random.randint(0, 23)
    battle_bgm = world.random.randint(0, 50)
    if battle_bgm == 1 and stage not in {9, 10, 14}:
        battle_bgm = 6
    if battle_bgm == 4 and stage not in {9, 10, 14}:
        battle_bgm = 7
    normal["BattleBGMType"] = battle_bgm
    clear_bgm = world.random.randint(0, 9)
    if clear_bgm > 1:
        clear_bgm = 0
    normal["ClearBGMType"] = clear_bgm

    # small monster stats
    enemy["SmallMonsters"]["SpawnType"] = stage_zako[stage]
    enemy["SmallMonsters"]["HealthTable"] = world.random.randint(0, 255)
    enemy["SmallMonsters"]["AttackTable"] = world.random.randint(0, 255)
    enemy["SmallMonsters"]["PartTable"] = world.random.randint(0, 255)
    enemy["SmallMonsters"]["OtherTable"] = world.random.randint(0, 255)

    for i in range(5):
        enemy["Monsters"][i][
            "SetName"] = f"AP_Custom_{world.random.randint(1, stage_set_max[stage])}"
        enemy["Monsters"][i]["HealthTable"] = random_normal_integer(
            world.random,
            world.options.average_monster_difficulty.value,
            world.options.monster_difficulty_deviation.value,
            0,
            173
        )
        enemy["Monsters"][i]["AttackTable"] = random_normal_integer(
            world.random,
            world.options.average_monster_difficulty.value,
            world.options.monster_difficulty_deviation.value,
            0,
            172
        )
        enemy["Monsters"][i]["OtherTable"] = random_normal_integer(
            world.random,
            world.options.average_monster_difficulty.value,
            world.options.monster_difficulty_deviation.value,
            0,
            161
        )
        enemy["Monsters"][i]["PartTable"] = random_normal_integer(
            world.random,
            world.options.average_monster_difficulty.value,
            world.options.monster_difficulty_deviation.value,
            0,
            178
        )
        enemy["Monsters"][i]["StaminaTable"] = random_normal_integer(
            world.random,
            world.options.average_monster_difficulty.value,
            world.options.monster_difficulty_deviation.value,
            0,
            255
        )
        enemy["Monsters"][i]["Size"] = random_normal_integer(
            world.random,
            world.options.average_monster_difficulty.value,
            world.options.monster_difficulty_deviation.value,
            0,
            255
        )
        enemy["Monsters"][i]["SizeTable"] = world.random.randint(0, 41)
        enemy["Monsters"][i]["Difficulty"] = world.random.randint(0, 2)
        if world.options.disable_multiplayer_scaling.value:
            enemy["Monsters"][i]["MultiTable"] = 0
        else:
            enemy["Monsters"][i]["MultiTable"] = world.random.randint(0, 25)

        afflicted = world.options.enable_affliction.value
        if can_afflict(monsters[i]) and afflicted in [0, 1]:
            if afflicted == 1 or (afflicted == 0 and world.random.randint(0, 9) > 6):
                # add affliction
                enemy["Monsters"][i]["IndividualType"] = 1
        elif monsters[i] in [2072, 2073, 2075, 2134]:
            # this is a risen monster, rng it's level
            enemy["Monsters"][i]["IndividualType"] = world.random\
                .choices([2, 3, 4, 5], weights=[7, 1, 1, 1])

        if monsters[i] in [392, 549, 594] and world.random.randint(0, 9) == 9:
            # Hazard monsters, give a 1 in 10 chance for a hazard to spawn
            enemy["Monsters"][i]["SubType"] = 3 if monsters[i] == 392 else 1

        elif monsters[i] in [136, 392]:
            # edge case, Espinas and Flaming Espinas should be sleeping when they spawn
            enemy["Monsters"][i]["SubType"] = 1

    return json.dumps(quest_data)


def randomize_quests(world: "MHRSWorld", final_boss: int) -> dict:
    quest_data = dict()
    allowed_monsters = monster_choices.copy()

    if world.options.include_apex.value in [0, 2]:
        allowed_monsters.extend([1, 2, 7, 57, 60, 82])

    if world.options.include_apex.value in [0, 1]:
        allowed_monsters.extend([1793, 1794, 1799, 1849, 1852, 1874])

    if world.options.include_risen.value in [0, 2]:
        allowed_monsters.extend([24, 25, 27, 72, 1366])

    if world.options.include_risen.value in [0, 1]:
        allowed_monsters.extend([2072, 2073, 2075, 2120, 2134])

    for quest in get_quest_table(world.options.master_rank_requirement.value):
        quest_data[quest] = randomize_quest(world, allowed_monsters, quest, None)

    quest_data[315618] = randomize_quest(world, allowed_monsters, 315618, [final_boss_remap[final_boss]],
                                         True if final_boss == 22 else False)

    return quest_data


class MHRSZipFile(APContainer):
    def __init__(self, quest_data: dict, base_path: str, output_directory: str,
                 player=None, player_name: str = "", server: str = ""):
        self.quest_data = quest_data
        container_path = os.path.join(output_directory, base_path + ".zip")
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        for qid in self.quest_data:
            opened_zipfile.writestr(f"reframework/quests/q{qid}.json", self.quest_data[qid])
        super().write_contents(opened_zipfile)


def generate_quests(world: "MHRSWorld", output_directory: str):

    file_dir = world.multiworld.get_out_file_name_base(world.player)
    apmhrs = MHRSZipFile(
        randomize_quests(world, world.get_final_boss()),
        file_dir,
        output_directory,
        world.player,
        world.multiworld.get_player_name(world.player)
    )
    apmhrs.write()
