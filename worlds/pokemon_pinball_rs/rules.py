from rule_builder.rules import Rule, True_, Has, HasAll, HasFromListUnique, HasAllCounts
from typing import TYPE_CHECKING

from .data.pokemon import special_encounters, rare_encounters, habitats, bonus_catches, evolutions
from .names import (POKEDEX, POKEDEX_INVERSE, AREAS, RUBY_BOARD, SAPPHIRE_BOARD, EXTRA_STARTING_LIFE, STARTING_COINS,
                    PICHU_UPGRADE, SPECIES_RAYQUAZA, SPECIAL_GUESTS, ENCOUNTER_RATE_UP,
                    HATCH_MODE, GET_ARROW, EVO_ARROW, CHIKORITA_DEX, CYNDAQUIL_DEX, TOTODILE_DEX, AERODACTYL_DEX,
                    SPECIES_LATIOS, SPECIES_LATIAS, SPECIES_CHIKORITA, SPECIES_CYNDAQUIL, SPECIES_TOTODILE,
                    SPECIES_AERODACTYL, SPECIES_PICHU)

if TYPE_CHECKING:
    from . import PokemonPinballRSWorld

CanPlayBasicPinball = HasAllCounts({
    EXTRA_STARTING_LIFE: 2,
    STARTING_COINS: 1,
})
CanPlayModeratePinball = HasAllCounts({
    EXTRA_STARTING_LIFE: 3,
    STARTING_COINS: 3,
})
CanPlayLongPinball = HasAllCounts({
    EXTRA_STARTING_LIFE: 5,
    STARTING_COINS: 4,
    PICHU_UPGRADE: 1,
})

SPECIAL_ENCOUNTER_RULES: dict[str, Rule] = {
    SPECIES_LATIOS: CanPlayLongPinball & (Has(SPECIES_RAYQUAZA) | Has(ENCOUNTER_RATE_UP)),
    SPECIES_LATIAS: CanPlayLongPinball & (Has(SPECIES_RAYQUAZA) | Has(ENCOUNTER_RATE_UP)),
    SPECIES_PICHU: Has(HATCH_MODE) & CanPlayLongPinball & (Has(SPECIES_RAYQUAZA) | Has(ENCOUNTER_RATE_UP)),
    SPECIES_CHIKORITA: (CanPlayLongPinball & (Has(SPECIES_RAYQUAZA) | Has(ENCOUNTER_RATE_UP))
                        & Has(CHIKORITA_DEX)) | Has(SPECIAL_GUESTS),
    SPECIES_CYNDAQUIL: (CanPlayLongPinball & (Has(SPECIES_RAYQUAZA) | Has(ENCOUNTER_RATE_UP))
                        & Has(CYNDAQUIL_DEX)) | Has(SPECIAL_GUESTS),
    SPECIES_TOTODILE: (CanPlayLongPinball & (Has(SPECIES_RAYQUAZA) | Has(ENCOUNTER_RATE_UP))
                        & Has(TOTODILE_DEX)) | Has(SPECIAL_GUESTS),
    SPECIES_AERODACTYL: (CanPlayLongPinball & (Has(SPECIES_RAYQUAZA) | Has(ENCOUNTER_RATE_UP))
                        & Has(AERODACTYL_DEX)) | Has(SPECIAL_GUESTS),
}


def set_rules(world: "PokemonPinballRSWorld"):
    # first set rules for the boards
    world.set_rule(world.get_entrance("To Ruby Board"), Has(RUBY_BOARD))
    world.set_rule(world.get_entrance("To Sapphire Board"), Has(SAPPHIRE_BOARD))

    # now for each board, set the rules for areas
    for i, area in AREAS.items():
        world.set_rule(world.get_entrance(f"To {area}"), Has(area))

        for mon, arrows in habitats[i].items():
            rule = True_()
            if arrows > 2:
                rule &= Has(GET_ARROW)
            if mon in rare_encounters:
                rule &= Has(ENCOUNTER_RATE_UP)
            world.set_rule(world.get_location(f"{area} - {POKEDEX_INVERSE[mon]}"), rule)

    for i, board in enumerate((RUBY_BOARD, SAPPHIRE_BOARD)):
        world.set_rule(world.get_entrance(f"To Hatch Eggs ({board})"), Has(HATCH_MODE) & CanPlayBasicPinball)

        for mon in special_encounters:
            world.set_rule(world.get_location(f"{board} - {POKEDEX_INVERSE[mon]}"),
                           SPECIAL_ENCOUNTER_RULES.get(POKEDEX_INVERSE[mon]))

        for mon in bonus_catches[i]:
            if mon == 199:
                rule = CanPlayLongPinball
            else:
                rule = CanPlayBasicPinball
            world.set_rule(world.get_location(f"{board} - {POKEDEX_INVERSE[mon]}"), rule)

    world.set_rule(world.get_entrance("To Evolutions"), Has(EVO_ARROW, count=3) & CanPlayModeratePinball)
    for mon, prevo in evolutions.items():
        # Special case for Vileplume and Bellossom
        if mon == 89:
            board_rule = Has(RUBY_BOARD)
        elif mon == 90:
            board_rule = Has(SAPPHIRE_BOARD)
        else:
            board_rule = True_()
        world.set_rule(world.get_location(f"Evolve - {POKEDEX_INVERSE[prevo]} -> {POKEDEX_INVERSE[mon]}"),
                       Has(POKEDEX_INVERSE[prevo]) & board_rule)

    # Now have every Pokemon location check its event item for accessibility
    for mon in POKEDEX:
        world.set_rule(world.get_location(f"Pokédex - {mon}"), Has(mon))

    goal = True_()

    if "Pokedex" in world.options.goal:
        goal &= HasFromListUnique(*POKEDEX.keys(), count=world.options.pokedex_requirement.value)

    if "Score" in world.options.goal:
        score = world.options.score_requirement.value
        if score < 50000000:
            rule = True_()
        elif score < 250000000:
            rule = CanPlayBasicPinball
        elif score < 750000000:
            rule = CanPlayModeratePinball
        else:
            rule = CanPlayLongPinball
        goal &= rule

    if "Targets" in world.options.goal:
        goal &= HasAll(*world.options.pokemon_targets.value)

    world.multiworld.completion_condition[world.player] = goal.resolve(world)