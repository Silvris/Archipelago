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
    "MR2 Urgent": ItemData(315900, True),
    "MR3 Urgent": ItemData(315901, True),
    "MR4 Urgent": ItemData(315902, True),
    "MR5 Urgent": ItemData(315903, True),
    "MR6 Urgent": ItemData(315904, True),
    "Victory's Flame": ItemData(315905, True)
}

useful_item_table = {
    # Base Weapon Unlocks
    "Great Sword Rarities 1-3": ItemData(315200, False),
    "Great Sword Rarities 4-5": ItemData(315201, False),
    "Great Sword Rarities 6-7": ItemData(315202, False),
    "Great Sword Rarities 8-10": ItemData(315203, False),

    "Long Sword Rarities 1-3": ItemData(315204, False),
    "Long Sword Rarities 4-5": ItemData(315205, False),
    "Long Sword Rarities 6-7": ItemData(315206, False),
    "Long Sword Rarities 8-10": ItemData(315207, False),

    "Sword and Shield Rarities 1-3": ItemData(315208, False),
    "Sword and Shield Rarities 4-5": ItemData(315209, False),
    "Sword and Shield Rarities 6-7": ItemData(315210, False),
    "Sword and Shield Rarities 8-10": ItemData(315211, False),

    "Dual Blades Rarities 1-3": ItemData(315212, False),
    "Dual Blades Rarities 4-5": ItemData(315213, False),
    "Dual Blades Rarities 6-7": ItemData(315214, False),
    "Dual Blades Rarities 8-10": ItemData(315215, False),

    "Hammer Rarities 1-3": ItemData(315216, False),
    "Hammer Rarities 4-5": ItemData(315217, False),
    "Hammer Rarities 6-7": ItemData(315218, False),
    "Hammer Rarities 8-10": ItemData(315219, False),

    "Hunting Horn Rarities 1-3": ItemData(315220, False),
    "Hunting Horn Rarities 4-5": ItemData(315221, False),
    "Hunting Horn Rarities 6-7": ItemData(315222, False),
    "Hunting Horn Rarities 8-10": ItemData(315223, False),

    "Lance Rarities 1-3": ItemData(315224, False),
    "Lance Rarities 4-5": ItemData(315225, False),
    "Lance Rarities 6-7": ItemData(315226, False),
    "Lance Rarities 8-10": ItemData(315227, False),

    "Gunlance Rarities 1-3": ItemData(315228, False),
    "Gunlance Rarities 4-5": ItemData(315229, False),
    "Gunlance Rarities 6-7": ItemData(315230, False),
    "Gunlance Rarities 8-10": ItemData(315231, False),

    "Switch Axe Rarities 1-3": ItemData(315232, False),
    "Switch Axe Rarities 4-5": ItemData(315233, False),
    "Switch Axe Rarities 6-7": ItemData(315234, False),
    "Switch Axe Rarities 8-10": ItemData(315235, False),

    "Charge Blade Rarities 1-3": ItemData(315236, False),
    "Charge Blade Rarities 4-5": ItemData(315237, False),
    "Charge Blade Rarities 6-7": ItemData(315238, False),
    "Charge Blade Rarities 8-10": ItemData(315239, False),

    "Insect Glaive Rarities 1-3": ItemData(315240, False),
    "Insect Glaive Rarities 4-5": ItemData(315241, False),
    "Insect Glaive Rarities 6-7": ItemData(315242, False),
    "Insect Glaive Rarities 8-10": ItemData(315243, False),

    "Light Bowgun Rarities 1-3": ItemData(315244, False),
    "Light Bowgun Rarities 4-5": ItemData(315245, False),
    "Light Bowgun Rarities 6-7": ItemData(315246, False),
    "Light Bowgun Rarities 8-10": ItemData(315247, False),

    "Heavy Bowgun Rarities 1-3": ItemData(315248, False),
    "Heavy Bowgun Rarities 4-5": ItemData(315249, False),
    "Heavy Bowgun Rarities 6-7": ItemData(315250, False),
    "Heavy Bowgun Rarities 8-10": ItemData(315251, False),

    "Bow Rarities 1-3": ItemData(315252, False),
    "Bow Rarities 4-5": ItemData(315253, False),
    "Bow Rarities 6-7": ItemData(315254, False),
    "Bow Rarities 8-10": ItemData(315255, False),

    # Consolidated Rarity Upgrades
    "Weapon Rarities 1-3": ItemData(315256, False),
    "Weapon Rarities 4-5": ItemData(315257, False),
    "Weapon Rarities 6-7": ItemData(315258, False),
    "Weapon Rarities 8-10": ItemData(315259, False),

    # Progressive Rarity Upgrades
    "Progressive Great Sword": ItemData(315260, False),
    "Progressive Long Sword": ItemData(315261, False),
    "Progressive Sword and Shield": ItemData(315262, False),
    "Progressive Dual Blades": ItemData(315263, False),
    "Progressive Hammer": ItemData(315264, False),
    "Progressive Hunting Horn": ItemData(315265, False),
    "Progressive Lance": ItemData(315266, False),
    "Progressive Gunlance": ItemData(315267, False),
    "Progressive Switch Axe": ItemData(315268, False),
    "Progressive Charge Blade": ItemData(315269, False),
    "Progressive Insect Glaive": ItemData(315270, False),
    "Progressive Light Bowgun": ItemData(315271, False),
    "Progressive Heavy Bowgun": ItemData(315272, False),
    "Progressive Bow": ItemData(315273, False),

    # Progressive Consolidated
    "Progressive Weapon": ItemData(315274, False),

    # Armor
    "Armor Rarity 1": ItemData(315275, False),
    "Armor Rarity 2": ItemData(315276, False),
    "Armor Rarity 3": ItemData(315277, False),
    "Armor Rarity 4": ItemData(315278, False),
    "Armor Rarity 5": ItemData(315279, False),
    "Armor Rarity 6": ItemData(315280, False),
    "Armor Rarity 7": ItemData(315281, False),
    "Armor Rarity 8": ItemData(315282, False),
    "Armor Rarity 9": ItemData(315283, False),
    "Armor Rarity 10": ItemData(315284, False),

    #Progressive Armor
    "Progressive Armor Rarity": ItemData(315285, False)
}

filler_item_table = {
    "Random Weapon": ItemData(315100, False),
    "Random Armor": ItemData(315101, False),
    "Decoration Gift": ItemData(315102, False, 5),
    "Item Gift": ItemData(315103, False, 20),
    "Garbage": ItemData(315104, False)
}

filler_weights = {
    "Random Weapon": 4,
    "Random Armor": 4,
    "Decoration Gift": 2,
    "Item Gift": 2,
    "Garbage": 1
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

item_table = {
    **progression_item_table,
    **useful_item_table,
    **filler_item_table,
    **follower_table,
}

item_names = {
    "follower": {name for name in follower_table.keys()}
}

lookup_name_to_id: typing.Dict[str, int] = {item_name: data.code for item_name, data in item_table.items() if data.code}
