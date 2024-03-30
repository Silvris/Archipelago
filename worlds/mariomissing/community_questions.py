import csv
import os.path
from pkgutil import get_data
from Utils import user_path

answer_addrs = {
    0: 0x0053,
    1: 0x0075,
    2: 0x0097,
    3: 0x00B9
}

supported_categories = ['Adventure', 'Blasphemous', 'Bumper Stickers', 'ChecksFinder'
                        'Clique', 'Dark Souls III', 'DLCQuest', 'Donkey Kong Country 3',
                        'DOOM 1993', 'Factorio', 'Final Fantasy', 'Hollow Knight',
                        'Hylics 2', 'Kingdom Hearts 2', 'The Legend of Zelda', 'A Link to the Past',
                        'Links Awakening DX', 'Lufia II Ancient Cave', 'MegaMan Battle Network 3', 'Meritous',
                        'The Messenger', 'Minecraft', 'Muse Dash', 'Noita',
                        'Ocarina of Time', 'Overcooked! 2', 'Pokemon Red and Blue', 'Raft',
                        'Risk of Rain 2', 'Rogue Legacy', 'Secret of Evermore', 'Slay the Spire',
                        'SMZ3', 'Sonic Adventure 2 Battle', 'Starcraft 2 Wings of Liberty', 'Stardew Valley',
                        'Subnautica', 'Super Mario 64', 'Super Mario World', 'Super Metroid',
                        'Terraria', 'Timespinner', 'Undertale', 'VVVVVV',
                        'Wargroove', 'The Witness', 'Zillion', 'DOOM II',
                        'Final Fantasy Mystic Quest', 'Landstalker - The Treasures of King Nole', 'Lingo', 'Heretic',
                        'Pokemon Emerald', 'Shivers', "TUNIC", "Kirby's Dream Land 3", "Celeste 64",
                        "Zork: Grand Inquisitor", "Castlevania 64", "A Short Hike", "Yoshi's Island"]

default_info = get_data(__name__, "default_questions.csv").decode('utf-8').splitlines()
default_questions = csv.DictReader(default_info, delimiter='|')
question_mapping = {}
for question in default_questions:
    assert isinstance(question, dict)
    if not question_mapping.get(question["Game"]):
        question_mapping[question["Game"]] = []
    question_mapping[question["Game"]].append(question)

custom_questions_path = os.path.join(user_path(), "data", "trivia_questions.csv")
if os.path.exists(custom_questions_path):
    custom_questions = csv.DictReader(open(custom_questions_path, 'r', newline=''), delimiter='|')
    for question in custom_questions:
        assert isinstance(question, dict)
        if not question_mapping.get(question["Game"]):
            question_mapping[question["Game"]] = []
        question_mapping[question["Game"]].append(question)

question_test = []
for category in question_mapping:
    question_test.extend(question_mapping[category])
