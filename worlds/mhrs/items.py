from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    quantity: int = 1
    follower: bool = False
    # trap: bool = False


class MHRSItem(Item):
    game: str = "Monster Hunter Rise Sunbreak"


progression_item_table = {
    "Key Quest": ItemData(315900, True),  # Item to access final quest
    "Master Rank 1": ItemData(None, True),
    "Master Rank 2": ItemData(None, True),
    "Master Rank 3": ItemData(None, True),
    "Master Rank 4": ItemData(None, True),
    "Master Rank 5": ItemData(None, True),
    "Master Rank 6": ItemData(None, True),
    "Victory's Flame": ItemData(None, True),   # Item showing completion of final quest
}

weapon_item_table = {
    # Base Weapon Unlocks
    "Great Sword Rarity 8": ItemData(315200, False),
    "Great Sword Rarity 9": ItemData(315201, False),
    "Great Sword Rarity 10": ItemData(315202, False),

    "Long Sword Rarity 8": ItemData(315203, False),
    "Long Sword Rarity 9": ItemData(315204, False),
    "Long Sword Rarity 10": ItemData(315205, False),

    "Sword and Shield Rarity 8": ItemData(315206, False),
    "Sword and Shield Rarity 9": ItemData(315207, False),
    "Sword and Shield Rarity 10": ItemData(315208, False),

    "Dual Blades Rarity 8": ItemData(315209, False),
    "Dual Blades Rarity 9": ItemData(315210, False),
    "Dual Blades Rarity 10": ItemData(315211, False),

    "Hammer Rarity 8": ItemData(315212, False),
    "Hammer Rarity 9": ItemData(315213, False),
    "Hammer Rarity 10": ItemData(315214, False),

    "Hunting Horn Rarity 8": ItemData(315215, False),
    "Hunting Horn Rarity 9": ItemData(315216, False),
    "Hunting Horn Rarity 10": ItemData(315217, False),

    "Lance Rarity 8": ItemData(315218, False),
    "Lance Rarity 9": ItemData(315219, False),
    "Lance Rarity 10": ItemData(315220, False),

    "Gunlance Rarity 8": ItemData(315221, False),
    "Gunlance Rarity 9": ItemData(315222, False),
    "Gunlance Rarity 10": ItemData(315223, False),

    "Switch Axe Rarity 8": ItemData(315224, False),
    "Switch Axe Rarity 9": ItemData(315225, False),
    "Switch Axe Rarity 10": ItemData(315226, False),

    "Charge Blade Rarity 8": ItemData(315227, False),
    "Charge Blade Rarity 9": ItemData(315228, False),
    "Charge Blade Rarity 10": ItemData(315229, False),

    "Insect Glaive Rarity 8": ItemData(315230, False),
    "Insect Glaive Rarity 9": ItemData(315231, False),
    "Insect Glaive Rarity 10": ItemData(315232, False),

    "Light Bowgun Rarity 8": ItemData(315233, False),
    "Light Bowgun Rarity 9": ItemData(315234, False),
    "Light Bowgun Rarity 10": ItemData(315235, False),

    "Heavy Bowgun Rarity 8": ItemData(315236, False),
    "Heavy Bowgun Rarity 9": ItemData(315237, False),
    "Heavy Bowgun Rarity 10": ItemData(315238, False),

    "Bow Rarity 8": ItemData(315239, False),
    "Bow Rarity 9": ItemData(315240, False),
    "Bow Rarity 10": ItemData(315241, False),

    # Consolidated Rarity Upgrades
    "Weapon Rarity 8": ItemData(315242, False),
    "Weapon Rarity 9": ItemData(315243, False),
    "Weapon Rarity 10": ItemData(315244, False),

    # Progressive Rarity Upgrades
    "Progressive Great Sword": ItemData(315245, False),
    "Progressive Long Sword": ItemData(315246, False),
    "Progressive Sword and Shield": ItemData(315247, False),
    "Progressive Dual Blades": ItemData(315248, False),
    "Progressive Hammer": ItemData(315249, False),
    "Progressive Hunting Horn": ItemData(315250, False),
    "Progressive Lance": ItemData(315251, False),
    "Progressive Gunlance": ItemData(315252, False),
    "Progressive Switch Axe": ItemData(315253, False),
    "Progressive Charge Blade": ItemData(315254, False),
    "Progressive Insect Glaive": ItemData(315255, False),
    "Progressive Light Bowgun": ItemData(315256, False),
    "Progressive Heavy Bowgun": ItemData(315257, False),
    "Progressive Bow": ItemData(315258, False),

    # Progressive Consolidated
    "Progressive Weapon": ItemData(315259, False),
}

armor_item_table = {
    # Armor
    "Armor Rarity 8": ItemData(315260, False),
    "Armor Rarity 9": ItemData(315261, False),
    "Armor Rarity 10": ItemData(315262, False),

    #Progressive Armor
    "Progressive Armor Rarity": ItemData(315263, False)
}

filler_item_table = {
    "Random Weapon": ItemData(315100, False),
    "Random Armor": ItemData(315101, False),
    "Decoration Gift": ItemData(315102, False, 5),
    "Item Gift": ItemData(315103, False, 20),
}

filler_weights = {
    "Random Weapon": 4,
    "Random Armor": 4,
    "Decoration Gift": 2,
    "Item Gift": 2,
}

follower_table = {
    "Fiorayne": ItemData(315700, False, 1, True),
    "Luchika": ItemData(315701, False, 1, True),
    "Jae": ItemData(315702, False, 1, True),
    "Arlow": ItemData(315703, False, 1, True),
    "Rondine": ItemData(315704, False, 1, True),
    "Hinoa": ItemData(315705, False, 1, True),
    "Minoto": ItemData(315706, False, 1, True),
    "Utsushi": ItemData(315707, False, 1, True),
    "Fugen": ItemData(315708, False, 1, True),
    "Galleus": ItemData(315709, False, 1, True)
}

useful_item_table = {
    **weapon_item_table,
    **armor_item_table,
    **follower_table
}

item_table = {
    **progression_item_table,
    **weapon_item_table,
    **armor_item_table,
    **filler_item_table,
    **follower_table,
}

item_name_groups = {
    "Follower": {name for name in follower_table.keys()},
    "Weapons": {name for name in weapon_item_table.keys()},
    "Great Sword": ["Great Sword Rarity 8", "Great Sword Rarity 9", "Great Sword Rarity 10", "Progressive Great Sword"],
    "Long Sword": ["Long Sword Rarity 8", "Long Sword Rarity 9", "Long Sword Rarity 10", "Progressive Long Sword"],
    "Sword and Shield": ["Sword and Shield Rarity 8", "Sword and Shield Rarity 9",
                         "Sword and Shield Rarity 10", "Progressive Sword and Shield"],
    "Dual Blades": ["Dual Blades Rarity 8", "Dual Blades Rarity 9", "Dual Blades Rarity 10", "Progressive Dual Blades"],
    "Hammer": ["Hammer Rarity 8", "Hammer Rarity 9", "Hammer Rarity 10", "Progressive Hammer"],
    "Hunting Horn": ["Hunting Horn Rarity 8", "Hunting Horn Rarity 9",
                     "Hunting Horn Rarity 10", "Progressive Hunting Horn"],
    "Lance": ["Lance Rarity 8", "Lance Rarity 9", "Lance Rarity 10", "Progressive Lance"],
    "Gunlance": ["Gunlance Rarity 8", "Gunlance Rarity 9", "Gunlance Rarity 10", "Progressive Gunlance"],
    "Switch Axe": ["Switch Axe Rarity 8", "Switch Axe Rarity 9", "Switch Axe Rarity 10", "Progressive Switch Axe"],
    "Insect Glaive": ["Insect Glaive Rarity 8", "Insect Glaive Rarity 9",
                      "Insect Glaive Rarity 10", "Progressive Insect Glaive"],
    "Charge Blade": ["Charge Blade Rarity 8", "Charge Blade Rarity 9",
                     "Charge Blade Rarity 10", "Progressive Charge Blade"],
    "Light Bowgun": ["Light Bowgun Rarity 8", "Light Bowgun Rarity 9",
                     "Light Bowgun Rarity 10", "Progressive Light Bowgun"],
    "Heavy Bowgun": ["Heavy Bowgun Rarity 8", "Heavy Bowgun Rarity 9",
                     "Heavy Bowgun Rarity 10", "Progressive Heavy Bowgun"],
    "Bow": ["Bow Rarity 8", "Bow Rarity 9", "Bow Rarity 10", "Progressive Bow"],
}

lookup_name_to_id: typing.Dict[str, int] = {item_name: data.code for item_name, data in item_table.items() if data.code}
