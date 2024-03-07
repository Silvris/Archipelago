from NetUtils import SlotType
from worlds.AutoWorld import World, WebWorld
from BaseClasses import MultiWorld, ItemClassification
from .Items import item_table, BalatroItem
from .Regions import create_regions, location_table


class BalatroWorld(World):
    game = "Balatro"

    item_name_to_id = {card.name: card.code for name, card in item_table.items()}
    location_name_to_id = location_table

    create_regions = create_regions

    def create_item(self, name: str) -> BalatroItem:
        if name in item_table:
            real_name = item_table[name].name
            classification = item_table[name].classification
            code = item_table[name].code
        else:
            real_name = name
            classification = ItemClassification.progression
            code = None
        return BalatroItem(real_name, classification, code, self.player)

    def get_filler_item_name(self) -> str:
        return "Random Consumable"

    def create_items(self) -> None:
        itempool = []
        for item in item_table:
            itempool.append(self.create_item(item))
        itempool.extend([self.create_item(self.get_filler_item_name())
                         for _ in range(len(location_table) - len(itempool) - 1)])
        self.multiworld.itempool += itempool

    def generate_basic(self):
        self.get_location("Ante 8 Boss").place_locked_item(self.create_item("Heads Up!"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Heads Up!", self.player)
