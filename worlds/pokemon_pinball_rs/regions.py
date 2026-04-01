from BaseClasses import Region, Location
from typing import TYPE_CHECKING
from .data.pokemon import habitats, egg_by_board, special_encounters, bonus_catches, evolutions
from .items import PinballRSItem
from .names import *
if TYPE_CHECKING:
    from . import PokemonPinballRSWorld


class PinballRSRegion(Region):
    game = "Pokemon Pinball Ruby & Sapphire"


class PinballRSLocation(Location):
    game = "Pokemon Pinball Ruby & Sapphire"


location_lookup: dict[str, int] = {
    **{f"Pokédex - {mon}": idx + 1 for mon, idx in POKEDEX.items()},
    **{stage: 0x100 + idx for idx, stage in BONUS_STAGES.items()},
}


def create_regions(world: "PokemonPinballRSWorld") -> None:
    menu = PinballRSRegion("Menu", world.player, world.multiworld)
    ruby = PinballRSRegion(RUBY_BOARD, world.player, world.multiworld)
    sapphire = PinballRSRegion(SAPPHIRE_BOARD, world.player, world.multiworld)
    pokedex = PinballRSRegion("Pokédex", world.player, world.multiworld)
    evos = PinballRSRegion("Evolutions", world.player, world.multiworld)
    bonuses = PinballRSRegion("Bonus Stages", world.player, world.multiworld)

    menu.connect(ruby, f"To {ruby.name}")
    menu.connect(sapphire, f"To {sapphire.name}")
    menu.connect(pokedex, f"To {pokedex.name}")
    menu.connect(evos, f"To {evos.name}")
    menu.connect(bonuses, f"To {bonuses.name}")

    world.multiworld.regions.extend([ruby, sapphire, pokedex, menu, bonuses])

    # Create the Pokédex, real checks
    pokedex.add_locations({f"Pokédex - {mon}": idx + 1 for mon, idx in POKEDEX.items()})

    # Create board locations
    for i, board in enumerate((ruby, sapphire)):
        for j in range(7):
            # Make the area regions
            idx = (i*7)+j
            area = AREAS[idx]
            area_region = PinballRSRegion(area, world.player, world.multiworld)
            board.connect(area_region, f"To {area_region.name}")
            world.multiworld.regions.append(area_region)
            for mon in habitats[idx]:
                area_region.add_event(f"{area_region.name} - {POKEDEX_INVERSE[mon]}", POKEDEX_INVERSE[mon],
                                      location_type=PinballRSLocation,
                                      item_type=PinballRSItem, show_in_spoiler=False)
        eggs = PinballRSRegion(f"Hatch Eggs ({board.name})", world.player, world.multiworld)
        board.connect(eggs, f"To {eggs.name}")
        world.multiworld.regions.append(eggs)
        for mon in egg_by_board[i]:
            eggs.add_event(f"Eggs ({board.name.split(' ')[0]}) - {POKEDEX_INVERSE[mon]}", POKEDEX_INVERSE[mon],
                           location_type=PinballRSLocation,
                           item_type=PinballRSItem, show_in_spoiler=False)

        for mon in bonus_catches[i]:
            board.add_event(f"{board.name} - {POKEDEX_INVERSE[mon]}", POKEDEX_INVERSE[mon],
                            location_type=PinballRSLocation,
                            item_type=PinballRSItem, show_in_spoiler=False)

        for mon in special_encounters:
            if (i == 0 and mon == 196) or (i == 1 and mon == 195):
                continue
            board.add_event(f"{board.name} - {POKEDEX_INVERSE[mon]}", POKEDEX_INVERSE[mon],
                            location_type=PinballRSLocation,
                            item_type=PinballRSItem, show_in_spoiler=False)

    # Now create evolution events
    for mon, prevo in evolutions.items():
        evos.add_event(f"Evolve - {POKEDEX_INVERSE[prevo]} -> {POKEDEX_INVERSE[mon]}", POKEDEX_INVERSE[mon],
                       location_type=PinballRSLocation,
                       item_type=PinballRSItem, show_in_spoiler=False)

    # Bonus Stages
    bonuses.add_locations({stage: 0x100 + idx for idx, stage in BONUS_STAGES.items()})