from worlds.AutoWorld import World, WebWorld
from BaseClasses import ItemClassification
from Options import OptionError
from .items import MM1Item, all_items, item_lookup, stage_access, weapons
from .locations import location_lookup, MM1Location, MM1Region, mm1_regions


class MM1WebWorld(WebWorld):
    theme = "partyTime"


class MM1World(World):
    game = "Mega Man"
    item_name_to_id = item_lookup
    location_name_to_id = location_lookup

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
            # Create the region
            stage = MM1Region(region.name, self.player, self.multiworld)
            # Then add its locations
            # Region.add_locations takes a dict[str, int | None] as its first argument,
            # to define the locations themselves
            # The second argument is what class to create the locations as.
            stage.add_locations({name: data.location_id for name, data in region.locations.items()}, MM1Location)
            # Create any event items
            for name, data in region.locations.items():
                if not data.location_id:
                    # place_locked_item ensures that nothing will ever move this item
                    self.get_location(name).place_locked_item(MM1Item(name, ItemClassification.progression,
                                                                      None, self.player))
            # Then we add the region to our list of regions
            regions.append(stage)
        # Finally, we have to submit the regions to the multiworld's list of regions
        self.multiworld.regions.extend(regions)
        # Now we can connect our regions
        for region in mm1_regions:
            if region.parent:
                parent_region = self.get_region(region.parent)
            else:
                parent_region = menu
            # The first argument to Region.connect is the region you'd like to connect to
            # The second argument is a string that is the name of this connection, defaulting to "Parent -> Connected"
            # Additionally, if you already know the access rule by the time of connection, you can pass it in here
            parent_region.connect(self.get_region(region.name))

    def create_items(self):
        # Define our local itempool
        itempool = []
        # In Part 3, we'll change this to use a player-facing option instead
        starting_robot_master = "Cut Man Access Codes"
        self.multiworld.push_precollected(self.create_item(starting_robot_master))
        # Now we can create our access items for all others
        itempool.extend([self.create_item(name) for name in stage_access.keys()
                         if name != starting_robot_master])
        # Create our weapons
        itempool.extend([self.create_item(name) for name in weapons.keys()])
        # Add the Magnet Beam
        itempool.append(self.create_item("Magnet Beam"))
        # Now that we have our static items, we want to fill the item pool with unimportant items
        # until we reach our required amount
        filler_count = len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool)
        itempool.extend(self.create_item(item)
                        for item in self.random.choices(["1-Up", "Health Energy (L)", "Weapon Energy (L)"],
                                                        k=filler_count))
        # Now with our item count correct, we add these to the multiworld itempool
        self.multiworld.itempool.extend(itempool)