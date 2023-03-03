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
    "Master Rank 1": ItemData(315901, True),
    "Master Rank 2": ItemData(315902, True),
    "Master Rank 3": ItemData(315903, True),
    "Master Rank 4": ItemData(315904, True),
    "Master Rank 5": ItemData(315905, True),
    "Master Rank 6": ItemData(315906, True),
    "Victory's Flame": ItemData(315907, True),   # Item showing completion of final quest

    # Base Weapon Unlocks
    "Great Sword Rarity 8": ItemData(315200, True),
    "Great Sword Rarity 9": ItemData(315201, True),
    "Great Sword Rarity 10": ItemData(315202, True),

    "Long Sword Rarity 8": ItemData(315204, False),
    "Long Sword Rarity 9": ItemData(315205, False),
    "Long Sword Rarity 10": ItemData(315206, False),

    "Sword and Shield Rarity 8": ItemData(315208, False),
    "Sword and Shield Rarity 9": ItemData(315209, False),
    "Sword and Shield Rarity 10": ItemData(315210, False),

    "Dual Blades Rarity 8": ItemData(315212, False),
    "Dual Blades Rarity 9": ItemData(315213, False),
    "Dual Blades Rarity 10": ItemData(315214, False),

    "Hammer Rarity 8": ItemData(315216, False),
    "Hammer Rarity 9": ItemData(315217, False),
    "Hammer Rarity 10": ItemData(315218, False),

    "Hunting Horn Rarity 8": ItemData(315220, False),
    "Hunting Horn Rarity 9": ItemData(315221, False),
    "Hunting Horn Rarity 10": ItemData(315222, False),

    "Lance Rarity 8": ItemData(315224, False),
    "Lance Rarity 9": ItemData(315225, False),
    "Lance Rarity 10": ItemData(315226, False),

    "Gunlance Rarity 8": ItemData(315228, False),
    "Gunlance Rarity 9": ItemData(315229, False),
    "Gunlance Rarity 10": ItemData(315230, False),

    "Switch Axe Rarity 8": ItemData(315232, False),
    "Switch Axe Rarity 9": ItemData(315233, False),
    "Switch Axe Rarity 10": ItemData(315234, False),

    "Charge Blade Rarity 8": ItemData(315236, False),
    "Charge Blade Rarity 9": ItemData(315237, False),
    "Charge Blade Rarity 10": ItemData(315238, False),

    "Insect Glaive Rarity 8": ItemData(315240, False),
    "Insect Glaive Rarity 9": ItemData(315241, False),
    "Insect Glaive Rarity 10": ItemData(315242, False),

    "Light Bowgun Rarity 8": ItemData(315244, False),
    "Light Bowgun Rarity 9": ItemData(315245, False),
    "Light Bowgun Rarity 10": ItemData(315246, False),

    "Heavy Bowgun Rarity 8": ItemData(315248, False),
    "Heavy Bowgun Rarity 9": ItemData(315249, False),
    "Heavy Bowgun Rarity 10": ItemData(315250, False),

    "Bow Rarity 8": ItemData(315252, False),
    "Bow Rarity 9": ItemData(315253, False),
    "Bow Rarity 10": ItemData(315254, False),

    # Consolidated Rarity Upgrades
    "Weapon Rarity 8": ItemData(315256, False),
    "Weapon Rarity 9": ItemData(315257, False),
    "Weapon Rarity 10": ItemData(315258, False),

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
    "Armor Rarity 8": ItemData(315275, False),
    "Armor Rarity 9": ItemData(315276, False),
    "Armor Rarity 10": ItemData(315277, False),

    #Progressive Armor
    "Progressive Armor Rarity": ItemData(315278, False)
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
    **filler_item_table,
    **follower_table,
}

item_names = {
    "follower": {name for name in follower_table.keys()}
}

lookup_name_to_id: typing.Dict[str, int] = {item_name: data.code for item_name, data in item_table.items() if data.code}
