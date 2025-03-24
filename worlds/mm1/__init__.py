from worlds.AutoWorld import World, WebWorld
from BaseClasses import ItemClassification
from Options import OptionError
from .items import MM1Item, all_items, item_lookup


class MM1WebWorld(WebWorld):
    theme = "partyTime"


class MM1World(World):
    game = "Mega Man"
    item_name_to_id = item_lookup

    def create_item(self, name: str) -> MM1Item:
        if name not in all_items:
            raise OptionError(f"{name} is not a valid item name for Mega Man.")
        item_data = all_items.get(name)
        classification = ItemClassification.filler
        if item_data.progression:
            classification |= ItemClassification.progression
        if item_data.useful:
            classification |= ItemClassification.useful
        return MM1Item(name, classification, item_data.item_id, self.player)
