from BaseClasses import Region, Location, MultiWorld
from logging import getLogger
from math import floor
from typing import TYPE_CHECKING, Callable
from .data.pokemon import habitats, egg_by_board, special_encounters, bonus_catches, evolutions
from .items import PinballRSItem
from .names import *
from .options import StartingBoard, ShopPrices
if TYPE_CHECKING:
    from . import PokemonPinballRSWorld

logger = getLogger("Pokemon Pinball Ruby & Sapphire")


class PinballRSRegion(Region):
    game = "Pokemon Pinball Ruby & Sapphire"


class PinballRSLocation(Location):
    game = "Pokemon Pinball Ruby & Sapphire"
    cost: int = 0

    def __init__(self, player: int, name: str, address: int, parent: PinballRSRegion, cost: int = 0) -> None:
        super().__init__(player, name, address, parent)
        self.cost = cost


shops_by_board: dict[int, list[str]] = {
    1: [
        SHOP_RED,
        SHOP_GOLD,
        SHOP_DIAMOND,
        SHOP_WHITE,
        SHOP_VIOLET,
    ],
    2: [
        SHOP_GREEN,
        SHOP_SILVER,
        SHOP_PEARL,
        SHOP_BLACK,
        SHOP_SCARLET,
    ]
}

price_functions: dict[int, Callable[[int], int]] = {
    1: lambda x: min(x*5, 99),
    2: lambda x: min(floor((x+2) ** 1.65), 99),
    3: lambda x: min(x*10, 99),
}

roulettes: dict[int, str] = {
    1: ROULETTE_RUBY,
    2: ROULETTE_SAPPHIRE
}

location_lookup: dict[str, int] = {
    **{f"Pokédex - {mon}": idx + 1 for mon, idx in POKEDEX.items()},
    **{stage: 0x100 + idx for idx, stage in BONUS_STAGES.items()},
    **{f"{board} - Bonus Multiplier {i}": 0x200 + (j*100) + i
       for j, board in enumerate((RUBY_BOARD, SAPPHIRE_BOARD))
       for i in range(1, 100)},
    **{f"{board} - Ball Upgrade {i}": 0x300 + (j*100) + i
       for j, board in enumerate((RUBY_BOARD, SAPPHIRE_BOARD))
       for i in range(1, 100)},
    **{f"Ruby Board - Makuhita Ball Upgrade {i}": 0x400 + i
       for i in range(1, 100)},
    **{f"{shop} {k}": 0x500 + (j*15) + (i*75) + k
       for i in range(2)
       for j, shop in enumerate(shops_by_board[i+1])
       for k in range(1, 16)},
    **{f"{roulette} {k}": 0x600 + ((i-1) * 40) + k for i, roulette in roulettes.items() for k in range(1, 41)}
}

location_groups: dict[str, set[str]] = {
    "Pokedex": {f"Pokédex - {mon}" for mon in POKEDEX.keys()},
    "Bonus Stages": {*BONUS_STAGES.values()},
    "Bonus Multipliers": {f"{board} - Bonus Multiplier {i}"
                          for board in (RUBY_BOARD, SAPPHIRE_BOARD)
                          for i in range(1, 100)},
    "Ball Upgrades": {*[f"{board} - Ball Upgrade {i}"
                        for board in (RUBY_BOARD, SAPPHIRE_BOARD)
                        for i in range(1, 100)],
                      *[f"Ruby Board - Makuhita Ball Upgrade {i}" for i in range(1, 100)]},
    "Roulettes": {*[f"{roulette} {k}" for roulette in roulettes.values() for k in range(1, 41)]},
    "Red Shop": {f"{SHOP_RED} {k}" for k in range(1, 16)},
    "Green Shop": {f"{SHOP_GREEN} {k}" for k in range(1, 16)},
    "Gold Shop": {f"{SHOP_GOLD} {k}" for k in range(1, 16)},
    "Silver Shop": {f"{SHOP_SILVER} {k}" for k in range(1, 16)},
    "Diamond Shop": {f"{SHOP_DIAMOND} {k}" for k in range(1, 16)},
    "Pearl Shop": {f"{SHOP_PEARL} {k}" for k in range(1, 16)},
    "Black Shop": {f"{SHOP_BLACK} {k}" for k in range(1, 16)},
    "White Shop": {f"{SHOP_WHITE} {k}" for k in range(1, 16)},
    "Scarlet Shop": {f"{SHOP_SCARLET} {k}" for k in range(1, 16)},
    "Violet Shop": {f"{SHOP_VIOLET} {k}" for k in range(1, 16)},
}


def create_regions(world: "PokemonPinballRSWorld") -> None:
    menu = PinballRSRegion("Menu", world.player, world.multiworld)
    ruby = PinballRSRegion(RUBY_BOARD, world.player, world.multiworld)
    sapphire = PinballRSRegion(SAPPHIRE_BOARD, world.player, world.multiworld)
    pokedex = PinballRSRegion("Pokédex", world.player, world.multiworld)
    evos = PinballRSRegion("Evolutions", world.player, world.multiworld)
    bonuses = PinballRSRegion("Bonus Stages", world.player, world.multiworld)
    ruby_shop = PinballRSRegion("Ruby Shop", world.player, world.multiworld)
    sapphire_shop = PinballRSRegion("Sapphire Shop", world.player, world.multiworld)

    boards = {}
    shops = {1: ruby_shop, 2: sapphire_shop}

    if world.options.single_board:
        if world.options.starting_board.value == StartingBoard.option_ruby:
            boards[1] = ruby
        else:
            boards[2] = sapphire
    else:
        boards.update({1: ruby, 2: sapphire})

    for i, board in boards.items():
        menu.connect(board, f"To {board.name}")
        board.connect(shops[i], f"To {shops[i].name}")

    menu.connect(pokedex, f"To {pokedex.name}")
    menu.connect(evos, f"To {evos.name}")
    menu.connect(bonuses, f"To {bonuses.name}")

    world.multiworld.regions.extend([*(boards.values()), pokedex, menu, bonuses, *[shops[board] for board in boards]])

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

        board.add_locations({f"{board.name} - Bonus Multiplier {j}": 0x200 + ((i - 1) * 100) + j
                             for j in range(1, world.options.bonus_multiplier_checks.value + 1)}, PinballRSLocation)
        board.add_locations({f"{board.name} - Ball Upgrade {j}": 0x300 + ((i - 1) * 100) + j
                             for j in range(1, world.options.ball_upgrade_checks.value + 1)}, PinballRSLocation)

        if i == 1:
            board.add_locations({f"{board.name} - Makuhita Ball Upgrade {j}": 0x400 + j
                                 for j in range(1, world.options.ball_upgrade_checks.value + 1)}, PinballRSLocation)

        board.add_locations({f"{roulettes[i]} {k}": 0x600 + ((i-1) * 40) + k
                             for k in range(1, world.options.roulette_prizes.value + 1)}, PinballRSLocation)

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
    pokedex.add_locations({f"Pokédex - {mon}": idx + 1 for mon, idx in POKEDEX.items() if idx in possible_mons},
                          PinballRSLocation)

    num_mons = len(possible_mons)
    if "Pokedex" in world.options.goal and num_mons < world.options.pokedex_requirement:
        # relatively late shifting, but respect their wish by requiring max possible dex
        logger.warning(f"Pokémon Pinball Ruby & Sapphire ({world.player_name}): Pokédex requirement greater than "
                       f"number of Pokémon available, reducing to {num_mons}.")
        world.options.pokedex_requirement.value = num_mons

    if "Targets" in world.options.goal:
        # need to check that we can find at least one target, and filter out any that we can't find
        for target in sorted(world.options.pokemon_targets.value):
            # this acts as a copy, so we can just immediately remove
            if POKEDEX[target] not in possible_mons:
                logger.warning(f"Pokémon Pinball Ruby & Sapphire ({world.player_name}): {target} cannot be "
                               f"found in the multiworld. Removing...")
                world.options.pokemon_targets.value.remove(target)
        if not world.options.pokemon_targets.value:
            # for now, we'll just add Jirachi in the edge case
            # its guaranteed on both boards, and functionally very accessible (also interesting logically)
            logger.warning(f"Pokémon Pinball Ruby & Sapphire ({world.player_name}): No valid targets remain. Adding "
                           f"Jirachi as a target...")
            world.options.pokemon_targets.value.add(SPECIES_JIRACHI)

    # Bonus Stages
    bonus_stages = [4, 5, 6, 7]
    if not world.options.single_board or world.options.starting_board == StartingBoard.option_ruby:
        bonus_stages.extend([1, 3])
    if not world.options.single_board or world.options.starting_board == StartingBoard.option_sapphire:
        bonus_stages.extend([0, 2])

    bonuses.add_locations({stage: 0x100 + idx for idx, stage in BONUS_STAGES.items() if idx in bonus_stages},
                          PinballRSLocation)

    # Handle shops here
    if world.options.shop_tracks.value:
        shop_func = price_functions[world.options.shop_prices.value]
        for i in boards:
            shop = shops[i]
            for k, item in enumerate(shops_by_board[i]):
                if k >= world.options.shop_tracks.value:
                    continue
                for j in range(1, world.options.shop_track_length.value + 1):
                    loc_name = f"{item} {j}"
                    shop_loc = PinballRSLocation(world.player, loc_name, location_lookup[loc_name],
                                                 shop, cost=shop_func(j))
                    shop.locations.append(shop_loc)

