from BaseClasses import Tutorial, MultiWorld, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .items import item_lookup, all_items, chapter_items, DMC5Item
from Options import OptionError


class DMC5WebWorld(WebWorld):
    theme = "stone"


class DMC5World(World):
    game = "Devil May Cry 5"
    # options_dataclass: DMC5Options
    # options: DMC5Options
    web = DMC5WebWorld()
    item_name_to_id = item_lookup

    def create_item(self, name: str):
        if name not in all_items:
            raise OptionError(f"{name} is not a valid item name for Devil May Cry 5")
        item = all_items.get(name)
        classification = ItemClassification.filler
        if item.progression:
            classification |= ItemClassification.progression
        if item.useful:
            classification |= ItemClassification.useful
        return DMC5Item(name, classification, item.code, self.player)

    def create_items(self):
        itempool = []
        if True: # self.options.mode in [GameMode.option_classic, GameMode.option_all]:
            itempool.extend(self.create_item(name) for name in chapter_items)
        self.multiworld.itempool.extend(itempool)

