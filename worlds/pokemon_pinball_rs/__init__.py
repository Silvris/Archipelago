from worlds.AutoWorld import World, WebWorld
from BaseClasses import Item, ItemClassification, MultiWorld, Tutorial
from Options import OptionError
from settings import Group, UserFilePath
from typing import ClassVar

from .items import PinballRSItem, ALL_ITEMS, item_lookup
from .regions import create_regions, location_lookup


class PokemonPinballRSSettings(Group):
    class RomFile(UserFilePath):
        """File name of the Pokemon Pinball RS EN rom"""
        description = "Pokemon Pinball Ruby & Sapphire ROM File"
        copy_to: str | None = "Pokemon Pinball RS.gba"
        md5s = []

    rom_file: RomFile = RomFile(RomFile.copy_to)


class PokemonPinballRSWebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [

        Tutorial(
           "Multiworld Setup Guide",
           "A guide to setting up the Pokemon Pinball Ruby & Sapphire randomizer connected to an Archipelago Multiworld.",
           "English",
           "setup_en.md",
           "setup/en",
           ["Silvris"]
        )
    ]


class PokemonPinballRSWorld(World):
    """
    Pinball
    """

    game = "Pokemon Pinball Ruby & Sapphire"
    settings: ClassVar[PokemonPinballRSSettings]
    #options_dataclass = PokemonPinballRSOptions
    #options: PokemonPinballRSOptions
    item_name_to_id = item_lookup
    location_name_to_id = location_lookup

    create_regions = create_regions

    def create_item(self, name: str) -> "Item":
        data = ALL_ITEMS.get(name, None)
        if data is None:
            raise OptionError(f"{name} is not a valid item for Pokemon Pinball Ruby & Sapphire")
        return PinballRSItem(name, data.classification, data.idx, self.player)

    def create_items(self) -> None:
        itempool = [self.create_item(name) for name, data in ALL_ITEMS.items() for _ in range(data.count)]
        unfilled = len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool)
        itempool += [Item("Nothing", ItemClassification.filler, -1, self.player) for _ in range(unfilled)]

        self.multiworld.itempool += itempool
