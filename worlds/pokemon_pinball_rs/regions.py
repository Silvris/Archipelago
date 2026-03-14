from BaseClasses import Region, Location
from typing import TYPE_CHECKING
from .data.pokemon import habitats, egg_by_board, special_encounters
from .items import PinballRSItem
from .names import *
if TYPE_CHECKING:
    from . import PokemonPinballRSWorld


class PinballRSRegion(Region):
    game = "Pokemon Pinball Ruby & Sapphire"


class PinballRSLocation(Location):
    game = "Pokemon Pinball Ruby & Sapphire"


location_lookup: dict[str, int] = {
    **POKEDEX,
}


def create_regions(world: "PokemonPinballRSWorld") -> None:
    menu = PinballRSRegion("Menu", world.player, world.multiworld)
    ruby = PinballRSRegion(RUBY_BOARD, world.player, world.multiworld)
    sapphire = PinballRSRegion(SAPPHIRE_BOARD, world.player, world.multiworld)
    pokedex = PinballRSRegion("Pokédex", world.player, world.multiworld)

    menu.connect(ruby)
    menu.connect(sapphire)
    menu.connect(pokedex)

    world.multiworld.regions.extend([ruby, sapphire, pokedex, menu])

    # Create the Pokédex, real checks
    pokedex.add_locations({f"Pokédex - {mon}": idx for mon, idx in POKEDEX.items()})

    for i, board in enumerate((ruby, sapphire)):
        for j in range(7):
            # Make the area regions
            idx = (i*7)+j
            area = AREAS[idx]
            area_region = PinballRSRegion(area, world.player, world.multiworld)
            board.connect(area_region)
            world.multiworld.regions.append(area_region)
            for mon in habitats[idx]:
                area_region.add_event(f"{area_region.name} - {POKEDEX_INVERSE[mon]}", POKEDEX_INVERSE[mon],
                                      location_type=PinballRSLocation,
                                      item_type=PinballRSItem, show_in_spoiler=False)
        eggs = PinballRSRegion(f"Hatch Eggs ({board.name})", world.player, world.multiworld)
        board.connect(eggs)
        world.multiworld.regions.append(eggs)
        for mon in egg_by_board[i]:
            eggs.add_event(f"Eggs ({board.name.split(' ')[0]}) - {POKEDEX_INVERSE[mon]}", POKEDEX_INVERSE[mon],
                           location_type=PinballRSLocation,
                           item_type=PinballRSItem, show_in_spoiler=False)

        for mon in special_encounters:
            board.add_event(f"{board.name} - {POKEDEX_INVERSE[mon]}", POKEDEX_INVERSE[mon],
                            location_type=PinballRSLocation,
                            item_type=PinballRSItem, show_in_spoiler=False)
