from BaseClasses import Tutorial, MultiWorld, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .items import item_lookup, all_items, chapter_items, DMC5Item, filler_item_weights, item_groups
from .regions import create_regions, location_lookup, all_locations
from .rules import set_rules
from .names import items
from Options import OptionError


class DMC5WebWorld(WebWorld):
    theme = "stone"


class DMC5World(World):
    game = "Devil May Cry 5"
    # options_dataclass: DMC5Options
    # options: DMC5Options
    web = DMC5WebWorld()
    item_name_to_id = item_lookup
    location_name_to_id = location_lookup
    item_name_groups = item_groups

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
            first_chapter = self.random.choice(list(chapter_items.keys()))
            itempool.extend(self.create_item(name) for name in chapter_items if name != first_chapter and
                            (name not in all_locations or not all_locations[name].event_item))
            self.multiworld.push_precollected(self.create_item(first_chapter))
        filler_items = len(list(self.multiworld.get_unfilled_locations(self.player))) - len(itempool)
        itempool.extend(self.create_item(name) for name in self.random.choices(list(filler_item_weights.keys()),
                                                                               list(filler_item_weights.values()),
                                                                               k=filler_items))
        self.multiworld.itempool.extend(itempool)

    create_regions = create_regions
    set_rules = set_rules
