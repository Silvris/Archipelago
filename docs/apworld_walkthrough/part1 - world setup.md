# APWorld Creation Process

This guide is a supplement to existing Archipelago documentation designed to walk users
through the process of setting up and creating a brand new APWorld. This guide assumes users
have basic understanding of Python, classes, and inheritance. While it isn't expressly required, we recommend the use of
version control software such as Git and GitHub for backing up your code. This guide assumes that you have forked the
main Archipelago repository, and are working within the forked repo.

For the sake of this example, we will be creating an APWorld for Mega Man on the NES, a logically simple game
that lets us explore many aspects of creating an APWorld.

## Creating the Initial World

To start, we create a new folder within the `worlds` directory named after our game, in this case `mm1`. In our new 
folder, we create the file `__init__.py`. This is the main file of our APWorld, and will house the actual world definition.
This is also the only required file that needs to be created, any further files are purely for organizational purposes.

In `__init__.py`, we'll first import `World` and `WebWorld` from `worlds.AutoWorld`. 

`WebWorld` handles certain WebHost-parameters such as linking to tutorials, page theme, option presets, and option groups.

`World` is the core of the APWorld, as Archipelago creates an instance of your World for every player that is playing that
particular game. Every World is required to define the following members:
* `__doc__` - The docstring, immediately following the def, used to describe the World on the WebHost
* `game` - The name of the game (used directly in the options file)
* `item_name_to_id` - The mapping of item names to their ids, more on this later
* `location_name_to_id` - The mapping of location names to their ids, more on this later
* `def create_item(name: str) -> Item:` - A function to create an item intended for this game, given the name of the item

You should have an `__init__.py` that looks somewhat like this. 
```python
from worlds.AutoWorld import World, WebWorld


class MM1WebWorld(WebWorld):
    theme = "partyTime"


class MM1World(World):
    game = "Mega Man"
```

Further information about the World class can be found in the [apworld specification document](../apworld%20specification.md),
and much of it will be discussed in later parts of this guide.

From here, we'll create an additional two files - `locations.py` and `items.py` to contain information about locations 
and items respectively.

## Items

There are many ways to define information about items, but one of the most common is to create a data structure to hold
information about your items. This is typically done by defining a NamedTuple with the fields you need.

```python
from typing import NamedTuple


class ItemData(NamedTuple):
    item_id: int
    progression: bool
    useful: bool = False
```

Additionally, many worlds will subclass the base Item class in order to set the `game` field automatically. This isn't necessary,
but may be useful for debugging purposes.

### Item Information

We then define information about each individual item. Item parameters such as classification are defined upon the creation of the
individual item object, but we can use the ItemData to define defaults for each given item name. Items are expected to have a unique
name that matches to a unique ID within the world. You can have an item named the same and with the same ID as another world,
but you cannot have two items with the same name or same ID within your own world.

```python
weapons: dict[str, ItemData] = {
    "Rolling Cutter": ItemData(0x1, True),
    "Ice Slasher": ItemData(0x2, True),
    "Hyper Bomb": ItemData(0x3, True),
    "Fire Storm": ItemData(0x4, True),
    "Thunder Beam": ItemData(0x5, True),
    "Super Arm": ItemData(0x6, True),
}
```

`World` has two required attributes related to items: `item_name_to_id` and `create_item`. We can create the former using
our data structure with a comprehension.
```python
# items.py
# Combine all of our item data into one single dict
all_items: dict[str, ItemData] = {
    **weapons,
    **stage_access,
    **misc_items,
}

# Then filter them down to a lookup of item name to item id, leaving out events
item_lookup: dict[str, int] = {item: data.item_id for item, data in all_items.items() if data.item_id}

# __init__.py
...
from .items import item_lookup

...
class MM1World(World):
    game = "Mega Man"
    item_name_to_id = item_lookup
```

`create_item` is where the actual Item instance is created, and can be called by itself without any other generation steps 
having been ran. `create_item` can also be called with any arbitrary string as the item name, and worlds are expected to return
a proper exception if they cannot handle the item name. We can use our ItemData table to create our items.

```python
from BaseClasses import ItemClassification
from Options import OptionError
from .items import item_lookup, all_items, MM1Item
...
class MM1World(World):
    ...
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
```

### Item Classifications
`ItemClassification` refers to the type of item being created, and an item can have multiple different classifications
* Filler items are considered logically irrelevant and are typically not particularly useful. Think health pickups, 
money, ammo. They are the only type of item allowed to be placed on an excluded location.
* Useful items are also considered logically irrelevant, but are generally considered good by the playerbase. 
Think armor upgrades or a damage increase. They are not allowed to be placed on excluded locations.
* **Progression items are the only items able to be considered by logic.** They are any item that can logically unlock a 
location, no matter how many locations. They are the only type of item allowed to be placed on a priority location.
* `skip_balancing` is an additional flag used to tell AP's progression balancing that it should skip this item. 
This is typically used for items that by themselves can unlock very little if anything by themselves, such as Power Stars 
or HK's Dreamers.


### Event Items and Locations

Within discussions about APWorlds, you may see mention of "event items". An event item is an item with an ID of `None`,
and are the only items that are allowed to share IDs. Event items are excluded from the final output, and cannot be sent
or received by clients.

Event locations are locations with an ID of `None`, and are only capable of holding event items. When put together as a 
pair, they serve as a way to represent logical aspects of gameplay that cannot be handled through standard items. One of
the most common use cases for events is to represent the player completing their game, achieved by creating an event item/location
pair with the logical requirements needed to beat the game.


## Regions and Locations

There are also many ways of handling locations; however, it is recommended for efficiency that you use regions to group 
together locations. Despite their names, regions do not have to correspond to physical in-game regions. Rather, they can
be used to group together any group of locations/connections with a shared access rule. For example, if fast travel is a part of your 
game's randomization, fast travel can be represented as a region that connects to all possible fast travel points.

For this guide, we'll be using a similar approach as we did for items. We define a NamedTuple for locations to hold specific
information about the locations. The same approach is used for regions; however, many games do not need to go to these lengths
for their regions. A game with a small amount of regions can very easily be handled manually.

```python
from BaseClasses import Location, Region
from typing import NamedTuple


class MM1Region(Region):
    game = "Mega Man"

    
class MM1Location(Location):
    game = "Mega Man"


class LocationData(NamedTuple):
    location_id: int | None
    consumable: bool = False

class RegionData(NamedTuple):
    name: str
    locations: dict[str, LocationData]
    parent: str = "" # For a more complex game, this might be swapped for a list[str]. 
    # MM1 only has one connection per region other than the origin, so that is unnecessary
```

Using these, we can begin to define the structure of our world. This is a truncated example of our world's region data:
```python
mm1_regions: list[RegionData] = [
    RegionData("Cut Man Stage", {
        "Cut Man - Defeated": LocationData(0x1),
        "Rolling Cutter - Received": LocationData(0x11),
        "Cut Man Stage - Health Energy 1": LocationData(0x101, True),
    }),
    RegionData("Ice Man Stage", {
        "Ice Man - Defeated": LocationData(0x2),
        "Ice Slasher - Received": LocationData(0x12),
        "Ice Man Stage - Health Energy 1": LocationData(0x102, True),
        "Ice Man Stage - Weapon Energy 1": LocationData(0x103, True),
        "Ice Man Stage - 1-Up": LocationData(0x104, True),
        "Ice Man Stage - Health Energy 2": LocationData(0x105, True),
        "Ice Man Stage - Health Energy 3": LocationData(0x106, True),
        "Ice Man Stage - Health Energy 4": LocationData(0x107, True),
        "Ice Man Stage - Weapon Energy 2": LocationData(0x108, True),
        "Ice Man Stage - Weapon Energy 3": LocationData(0x109, True),
        "Ice Man Stage - Weapon Energy 4": LocationData(0x10A, True),
    }),
    RegionData("Wily Stage 1", {
        "Yellow Devil - Defeated": LocationData(0x7),
        "Wily Stage 1 - Complete": LocationData(None),
        "Wily Stage 1 - Health Energy 1": LocationData(0x125, True),
        "Wily Stage 1 - Health Energy 2": LocationData(0x126, True),
        "Wily Stage 1 - Weapon Energy 1": LocationData(0x127, True),
        "Wily Stage 1 - Weapon Energy 2": LocationData(0x128, True),
    })
]
```

And much like the items, we will need to create a mapping of location names to location ids to give to our world class.

```python
# locations.py
all_locations: dict[str, LocationData] = {key: value for region in mm1_regions 
                                          for key, value in region.locations.items()}

location_lookup: dict[str, int] = {name: data.location_id for name, data in all_locations.items()}

# __init__.py
...
from .locations import location_lookup

...
class MM1World(World):
    game = "Mega Man"
    location_name_to_id = location_lookup
```

With both our items and locations defined, we can finally set up our world with the capability to generate.

## Generation

Archipelago expects every world in a generation to provide an equal number of locations and items for placement. 
For this purpose, we'll define two methods on our world: `create_regions` and `create_items`.

### create_regions

Within `create_regions`, we are expected to create all regions and locations that are to be filled by Archipelago.
On our world class is a value called `origin_region_name` that we can set (defaulted to "Menu"). This region represents 
the start of the game, and Archipelago expects that the player is always able to return to this point from any given region.

Additionally, as we create our locations, it is best practice to fill our event locations as they are created.

```python
from .items import MM1Item
from .locations import MM1Location, MM1Region, mm1_regions

class MM1World(World):
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
```

Note that at this point, our regions exist unconnected from each other. Typically, it is best to connect your regions as
soon as you can. However, you cannot connect them until you have created the region you need to connect to. 

```python
class MM1World(World):
    def create_regions(self):
        ...
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
```

### create_items

Within `create_items`, we are expected to create every item we would like Archipelago to fill for us. We must provide a 
number of items equivalent to the number of locations we created during `create_regions`.

Since `create_items` runs after `create_regions`, we can use `self.multiworld.get_unfilled_locations` to get an accurate count of locations
in the world, regardless of player options. Do note that this does include any unfilled event items, so you may need to 
account for any that have been left unfilled.

Additionally, this is a good time to place any items in the player's starting inventory using `self.multiworld.push_precollected`

```python
from .items import stage_access, weapons

class MM1World(World):
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
```

From this point, Archipelago is able to complete a generation and successfully place all of your items on your locations.
However, this generation may not be completable due to the lack of *logic* for these placements, which is where Part 2 will
pick up.
