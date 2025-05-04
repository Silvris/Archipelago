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
* `game` - The name of the game (used directly in the yaml)
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

Further information about the World class can be found in the [apworld specification document](../docs/apworld%20specification.md),
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
weapons = {
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
all_items = {
    **weapons,
    **stage_access,
    **misc_items,
}

item_lookup = {item: data.item_id for item, data in all_items.items()}

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

### Event Items

Within discussions about APWorlds, you may see mention of "event items". An event item is an item with an ID of `None`,
and are the only items that are allowed to share IDs. Event items are excluded from the final output, and cannot be sent
or received by clients and exist solely for the purpose of logic. 

## Regions and Locations

There are also many ways of handling locations; however, it is recommended for efficiency that you use regions to group 
together locations. Despite their names, regions do not have to correspond to physical in-game regions. Rather, they can
be used to group together any group of locations with a shared access rule.

For this guide, we'll be using a similar approach as we did for items. We define a NamedTuple for locations to hold specific
information about the locations. We could take a similar approach for regions as well, but our connections are simple enough
that we will just handle them manually.

```python
from BaseClasses import Region, Location
from typing import NamedTuple


class MM1Region(Region):
    game = "Mega Man"

    
class MM1Location(Location):
    game = "Mega Man"
```

