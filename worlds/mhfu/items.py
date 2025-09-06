import typing
from BaseClasses import Item


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    skip_balancing: bool = False
    trap: bool = False


class MHFUItem(Item):
    game = "Monster Hunter Freedom Unite"


weapons = [
    "Great Sword/Long Sword",
    "Hammer/Hunting Horn",
    "Sword and Shield/Dual Blades",
    "Lance/Gunlance",
    "Bowgun/Bow"
]

weapon_item_table = {'Progressive Great Sword/Long Sword': ItemData(24700000, True),
                     'Great Sword/Long Sword Rarity 1': ItemData(24700001, True),
                     'Great Sword/Long Sword Rarity 2': ItemData(24700002, True),
                     'Great Sword/Long Sword Rarity 3': ItemData(24700003, True),
                     'Great Sword/Long Sword Rarity 4': ItemData(24700004, True),
                     'Great Sword/Long Sword Rarity 5': ItemData(24700005, True),
                     'Great Sword/Long Sword Rarity 6': ItemData(24700006, True),
                     'Great Sword/Long Sword Rarity 7': ItemData(24700007, True),
                     'Great Sword/Long Sword Rarity 8': ItemData(24700008, True),
                     'Great Sword/Long Sword Rarity 9': ItemData(24700009, True),
                     'Great Sword/Long Sword Rarity 10': ItemData(24700010, True),
                     'Progressive Hammer/Hunting Horn': ItemData(24700011, True),
                     'Hammer/Hunting Horn Rarity 1': ItemData(24700012, True),
                     'Hammer/Hunting Horn Rarity 2': ItemData(24700013, True),
                     'Hammer/Hunting Horn Rarity 3': ItemData(24700014, True),
                     'Hammer/Hunting Horn Rarity 4': ItemData(24700015, True),
                     'Hammer/Hunting Horn Rarity 5': ItemData(24700016, True),
                     'Hammer/Hunting Horn Rarity 6': ItemData(24700017, True),
                     'Hammer/Hunting Horn Rarity 7': ItemData(24700018, True),
                     'Hammer/Hunting Horn Rarity 8': ItemData(24700019, True),
                     'Hammer/Hunting Horn Rarity 9': ItemData(24700020, True),
                     'Hammer/Hunting Horn Rarity 10': ItemData(24700021, True),
                     'Progressive Sword and Shield/Dual Blades': ItemData(24700022, True),
                     'Sword and Shield/Dual Blades Rarity 1': ItemData(24700023, True),
                     'Sword and Shield/Dual Blades Rarity 2': ItemData(24700024, True),
                     'Sword and Shield/Dual Blades Rarity 3': ItemData(24700025, True),
                     'Sword and Shield/Dual Blades Rarity 4': ItemData(24700026, True),
                     'Sword and Shield/Dual Blades Rarity 5': ItemData(24700027, True),
                     'Sword and Shield/Dual Blades Rarity 6': ItemData(24700028, True),
                     'Sword and Shield/Dual Blades Rarity 7': ItemData(24700029, True),
                     'Sword and Shield/Dual Blades Rarity 8': ItemData(24700030, True),
                     'Sword and Shield/Dual Blades Rarity 9': ItemData(24700031, True),
                     'Sword and Shield/Dual Blades Rarity 10': ItemData(24700032, True),
                     'Progressive Lance/Gunlance': ItemData(24700033, True),
                     'Lance/Gunlance Rarity 1': ItemData(24700034, True),
                     'Lance/Gunlance Rarity 2': ItemData(24700035, True),
                     'Lance/Gunlance Rarity 3': ItemData(24700036, True),
                     'Lance/Gunlance Rarity 4': ItemData(24700037, True),
                     'Lance/Gunlance Rarity 5': ItemData(24700038, True),
                     'Lance/Gunlance Rarity 6': ItemData(24700039, True),
                     'Lance/Gunlance Rarity 7': ItemData(24700040, True),
                     'Lance/Gunlance Rarity 8': ItemData(24700041, True),
                     'Lance/Gunlance Rarity 9': ItemData(24700042, True),
                     'Lance/Gunlance Rarity 10': ItemData(24700043, True),
                     'Progressive Bowgun/Bow': ItemData(24700044, True),
                     'Bowgun/Bow Rarity 1': ItemData(24700045, True),
                     'Bowgun/Bow Rarity 2': ItemData(24700046, True),
                     'Bowgun/Bow Rarity 3': ItemData(24700047, True),
                     'Bowgun/Bow Rarity 4': ItemData(24700048, True),
                     'Bowgun/Bow Rarity 5': ItemData(24700049, True),
                     'Bowgun/Bow Rarity 6': ItemData(24700050, True),
                     'Bowgun/Bow Rarity 7': ItemData(24700051, True),
                     'Bowgun/Bow Rarity 8': ItemData(24700052, True),
                     'Bowgun/Bow Rarity 9': ItemData(24700053, True),
                     'Bowgun/Bow Rarity 10': ItemData(24700054, True),
                     'Progressive Weapons': ItemData(24700055, True),
                     'Weapons Rarity 1': ItemData(24700056, True),
                     'Weapons Rarity 2': ItemData(24700057, True),
                     'Weapons Rarity 3': ItemData(24700058, True),
                     'Weapons Rarity 4': ItemData(24700059, True),
                     'Weapons Rarity 5': ItemData(24700060, True),
                     'Weapons Rarity 6': ItemData(24700061, True),
                     'Weapons Rarity 7': ItemData(24700062, True),
                     'Weapons Rarity 8': ItemData(24700063, True),
                     'Weapons Rarity 9': ItemData(24700064, True),
                     'Weapons Rarity 10': ItemData(24700065, True)}

armor_item_table = {
    'Progressive Armor': ItemData(24700066, True),
    'Armor Rarity 1': ItemData(24700067, True),
    'Armor Rarity 2': ItemData(24700068, True),
    'Armor Rarity 3': ItemData(24700069, True),
    'Armor Rarity 4': ItemData(24700070, True),
    'Armor Rarity 5': ItemData(24700071, True),
    'Armor Rarity 6': ItemData(24700072, True),
    'Armor Rarity 7': ItemData(24700073, True),
    'Armor Rarity 8': ItemData(24700074, True),
    'Armor Rarity 9': ItemData(24700075, True),
    'Armor Rarity 10': ItemData(24700076, True)
}

progression_item_table = {
    "Key Quest": ItemData(24700077, True, True),
    "Victory": ItemData(None, True)
}

filler_item_table = {
    "Random Weapon": ItemData(24700079, False),
    "Random Armor": ItemData(24700080, False),
    "Decoration Gift": ItemData(24700081, False),
    "Item Gift": ItemData(24700082, False),
    "Zenny Bag": ItemData(24700083, False),
}

filler_weights = {
    "Random Weapon": 1,
    "Random Armor": 2,
    "Decoration Gift": 4,
    "Item Gift": 4,
    "Zenny Bag": 4
}

trap_item_table = {
    "Farcaster": ItemData(24700510, False, trap=True),
    "Paratoad": ItemData(24700511, False, trap=True),
    "Sleeptoad": ItemData(24700512, False, trap=True),
    "Poisontoad": ItemData(24700513, False, trap=True),
    "Blango Artillery": ItemData(24700514, False, trap=True),
    "Puppet Spider": ItemData(24700515, False, trap=True),
    "Blastoad": ItemData(24700516, False, trap=True),
    "Gustcrab": ItemData(24700517, False, trap=True),
    "Wailnard": ItemData(24700518, False, trap=True),
    "Pincercrab": ItemData(24700519, False, trap=True),
    # "Conga Artillery": ItemData(24700520, False, trap=True)
    # "Chameleos Spit": ItemData(24700521, False, trap=True)
}

item_table = {
    **weapon_item_table,
    **armor_item_table,
    **progression_item_table,
    **filler_item_table,
    **trap_item_table
}

item_name_groups = {
    "Weapons": {name for name in weapon_item_table},
    "Armor": {name for name in armor_item_table}
}

item_name_to_id: dict[str, int] = {name: data.code for name, data in item_table.items() if data.code is not None}
item_id_to_name: dict[int, str] = {data.code: name for name, data in item_table.items() if data.code is not None}
