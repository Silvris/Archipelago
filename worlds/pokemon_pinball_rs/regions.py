from BaseClasses import Region, Location
from logging import getLogger
from typing import TYPE_CHECKING
from .data.pokemon import habitats, egg_by_board, special_encounters, bonus_catches, evolutions
from .items import PinballRSItem
from .names import *
from .options import StartingBoard
if TYPE_CHECKING:
    from . import PokemonPinballRSWorld

logger = getLogger("Pokemon Pinball Ruby & Sapphire")

class PinballRSRegion(Region):
    game = "Pokemon Pinball Ruby & Sapphire"


class PinballRSLocation(Location):
    game = "Pokemon Pinball Ruby & Sapphire"


location_lookup: dict[str, int] = {
    **{f"Pokédex - {mon}": idx + 1 for mon, idx in POKEDEX.items()},
    **{stage: 0x100 + idx for idx, stage in BONUS_STAGES.items()},
    **{f"{board} - Bonus Multiplier {i}": 0x200 + (j*100) + i
       for j, board in enumerate((RUBY_BOARD, SAPPHIRE_BOARD))
       for i in range(1, 100)},
    **{f"Ball Upgrade {i}": 0x300 + i for i in range(1, 100)},
}


def create_regions(world: "PokemonPinballRSWorld") -> None:
    menu = PinballRSRegion("Menu", world.player, world.multiworld)
    ruby = PinballRSRegion(RUBY_BOARD, world.player, world.multiworld)
    sapphire = PinballRSRegion(SAPPHIRE_BOARD, world.player, world.multiworld)
    pokedex = PinballRSRegion("Pokédex", world.player, world.multiworld)
    evos = PinballRSRegion("Evolutions", world.player, world.multiworld)
    bonuses = PinballRSRegion("Bonus Stages", world.player, world.multiworld)

    boards = {}

    if world.options.single_board:
        if world.options.starting_board.value == StartingBoard.option_ruby:
            boards[1] = ruby
        else:
            boards[2] = sapphire
    else:
        boards.update({1: ruby, 2: sapphire})

    for i, board in boards.items():
        menu.connect(board, f"To {board.name}")

    menu.connect(pokedex, f"To {pokedex.name}")
    menu.connect(evos, f"To {evos.name}")
    menu.connect(bonuses, f"To {bonuses.name}")

    world.multiworld.regions.extend([*(boards.values()), pokedex, menu, bonuses])

    possible_mons = set()

    # Create board locations
    for i, board in boards.items():
        for j in range(7):
            # Make the area regions
            idx = ((i - 1)*7)+j
            area = AREAS[idx]
            area_region = PinballRSRegion(area, world.player, world.multiworld)
            board.connect(area_region, f"To {area_region.name}")
            world.multiworld.regions.append(area_region)
            for mon in habitats[idx]:
                possible_mons.add(mon)
                area_region.add_event(f"{area_region.name} - {POKEDEX_INVERSE[mon]}", POKEDEX_INVERSE[mon],
                                      location_type=PinballRSLocation,
                                      item_type=PinballRSItem, show_in_spoiler=False)
        eggs = PinballRSRegion(f"Hatch Eggs ({board.name})", world.player, world.multiworld)
        board.connect(eggs, f"To {eggs.name}")
        world.multiworld.regions.append(eggs)
        for mon in egg_by_board[i]:
            possible_mons.add(mon)
            eggs.add_event(f"Eggs ({board.name.split(' ')[0]}) - {POKEDEX_INVERSE[mon]}", POKEDEX_INVERSE[mon],
                           location_type=PinballRSLocation,
                           item_type=PinballRSItem, show_in_spoiler=False)

        for mon in bonus_catches[i]:
            possible_mons.add(mon)
            board.add_event(f"{board.name} - {POKEDEX_INVERSE[mon]}", POKEDEX_INVERSE[mon],
                            location_type=PinballRSLocation,
                            item_type=PinballRSItem, show_in_spoiler=False)

        for mon in special_encounters:
            if (i == 1 and mon == 195) or (i == 2 and mon == 196):
                continue
            possible_mons.add(mon)
            board.add_event(f"{board.name} - {POKEDEX_INVERSE[mon]}", POKEDEX_INVERSE[mon],
                            location_type=PinballRSLocation,
                            item_type=PinballRSItem, show_in_spoiler=False)

        board.add_locations({f"{board.name} - Bonus Multiplier {j}": 0x200 + (i * 100) + j
                             for j in range(1, world.options.bonus_multiplier_checks.value + 1)})
    menu.add_locations({f"Ball Upgrade {i}": 0x300 + i for i in range(1, world.options.ball_upgrade_checks.value + 1)})

    # Now create evolution events
    for mon, prevo in evolutions.items():
        if prevo in possible_mons:
            # special case, gloom evo is board-locked
            if world.options.single_board and mon in (89, 90):
                if mon == 89 and world.options.starting_board == StartingBoard.option_sapphire:
                    continue
                elif mon == 90 and world.options.starting_board == StartingBoard.option_ruby:
                    continue
            possible_mons.add(mon)
            evos.add_event(f"Evolve - {POKEDEX_INVERSE[prevo]} -> {POKEDEX_INVERSE[mon]}", POKEDEX_INVERSE[mon],
                           location_type=PinballRSLocation,
                           item_type=PinballRSItem, show_in_spoiler=False)

    world.possible_mons = possible_mons

    # Create the Pokédex, real checks
    pokedex.add_locations({f"Pokédex - {mon}": idx + 1 for mon, idx in POKEDEX.items() if idx in possible_mons})

    num_mons = len(possible_mons)
    if "Pokedex" in world.options.goal and num_mons < world.options.pokedex_requirement:
        # relatively late shifting, but respect their wish by requiring max possible dex
        logger.warning(f"Pokémon Pinball Ruby & Sapphire ({world.player_name}): Pokédex requirement greater than "
                       f"number of Pokémon available, reducing to {num_mons}.")
        world.options.pokedex_requirement.value = num_mons

    # Bonus Stages
    bonus_stages = [4, 5, 6, 7]
    if not world.options.single_board or world.options.starting_board == StartingBoard.option_ruby:
        bonus_stages.extend([1, 3])
    if not world.options.single_board or world.options.starting_board == StartingBoard.option_sapphire:
        bonus_stages.extend([0, 2])

    bonuses.add_locations({stage: 0x100 + idx for idx, stage in BONUS_STAGES.items() if idx in bonus_stages})
