from worlds.AutoWorld import World, WebWorld
from BaseClasses import ItemClassification
from Options import OptionError
from .items import MM1Item, all_items, item_lookup, stage_access, weapons
from .locations import location_lookup, MM1Location, MM1Region, mm1_regions
from .options import MM1Options


class MM1WebWorld(WebWorld):
    theme = "partyTime"


class MM1World(World):
    game = "Mega Man"
    item_name_to_id = item_lookup
    location_name_to_id = location_lookup
    options: MM1Options
    options_dataclass = MM1Options
    web = MM1WebWorld()

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

    def create_regions(self):
        menu = MM1Region(self.origin_region_name, self.player, self.multiworld)
        regions = [menu]
        for region in mm1_regions:
            stage = MM1Region(region.name, self.player, self.multiworld)
            stage.add_locations({name: data.location_id for name, data in region.locations.items()}, MM1Location)
            for name, data in region.locations.items():
                if not data.location_id:
                    self.get_location(name).place_locked_item(MM1Item(name, ItemClassification.progression,
                                                                      None, self.player))
            regions.append(stage)
        self.multiworld.regions.extend(regions)
        for region in mm1_regions:
            if region.parent:
                parent_region = self.get_region(region.parent)
            else:
                parent_region = menu
            parent_region.connect(self.get_region(region.name))

    def create_items(self):
        # Define our local itempool
        itempool = []
        starting_robot_master = "Cut Man Access Codes"
        self.multiworld.push_precollected(self.create_item(starting_robot_master))
        itempool.extend([self.create_item(name) for name in stage_access.keys()
                         if name != starting_robot_master])
        itempool.extend([self.create_item(name) for name in weapons.keys()])
        itempool.append(self.create_item("Magnet Beam"))
        filler_count = len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool)
        itempool.extend(self.create_item(item)
                        for item in self.random.choices(["1-Up", "Health Energy (L)", "Weapon Energy (L)"],
                                                        k=filler_count))
        self.multiworld.itempool.extend(itempool)