import typing
from BaseClasses import Item
from .Quests import base_id


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

weapon_item_table = {f"Progressive {weapon}": ItemData(base_id + (idx * 11), True)
                     for idx, weapon in enumerate([*weapons, "Weapons"])}

for idx, weapon in enumerate([*weapons, "Weapons"]):
    weapon_item_table.update({f"{weapon} Rarity {x}": ItemData(base_id + (idx * 11) + x, True) for x in range(1, 11)})

weapon_max = max([weapon_item_table[weapon].code for weapon in weapon_item_table])

progression_item_table = {
    "Key Quest": ItemData(weapon_max + 1, True, True),
    "Victory": ItemData(weapon_max + 2, True)
}

filler_item_table = {
    "Random Weapon": ItemData(weapon_max + 3, False),
    "Random Armor": ItemData(weapon_max + 4, False),
    "Decoration Gift": ItemData(weapon_max + 5, False),
    "Item Gift": ItemData(weapon_max + 6, False),
}

filler_weights = {
    "Random Weapon": 4,
    "Random Armor": 4,
    "Decoration Gift": 2,
    "Item Gift": 2,
}

item_table = {
    **weapon_item_table,
    **progression_item_table,
    **filler_item_table
}

item_name_to_id = {name: item_table[name].code for name in item_table}
