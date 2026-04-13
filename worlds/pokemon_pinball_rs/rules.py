from rule_builder.rules import Rule, True_, Has, HasAll, HasFromListUnique, HasAllCounts, HasAny, OptionFilter
from typing import TYPE_CHECKING

from .data.pokemon import (special_encounters, rare_encounters, habitats, bonus_catches, evolutions, eggs, egg_groups,
                           species_info)
from .names import (POKEDEX, POKEDEX_INVERSE, AREAS, RUBY_BOARD, SAPPHIRE_BOARD, EXTRA_STARTING_LIFE, STARTING_COINS,
                    PICHU_UPGRADE, SPECIES_RAYQUAZA, SPECIAL_GUESTS, ENCOUNTER_RATE_UP,
                    GET_ARROW, EVO_ARROW, CHIKORITA_DEX, CYNDAQUIL_DEX, TOTODILE_DEX, AERODACTYL_DEX,
                    SPECIES_LATIOS, SPECIES_LATIAS, SPECIES_CHIKORITA, SPECIES_CYNDAQUIL, SPECIES_TOTODILE,
                    SPECIES_AERODACTYL, SPECIES_PICHU, EGG_BUNCH_1, EGG_BUNCH_2, EGG_BUNCH_3, EGG_BUNCH_4,
                    EGG_BUNCH_RUBY, EGG_BUNCH_SAPPHIRE, RUINS_RUBY, RUINS_SAPPHIRE, RUINS_AREA_CARD, BONUS_DUSCLOPS,
                    BONUS_KECLEON, BONUS_KYOGRE, BONUS_GROUDON, BONUS_RAYQUAZA, BONUS_SPHEAL_1, BONUS_SPHEAL_2,
                    BONUS_SPHEAL_3, EVOLUTION_METHODS, EVOLUTION_SPECIAL, HELPER_WHISCASH, HELPER_PELIPPER,
                    HELPER_MAKUHITA)
from .options import Difficulty

if TYPE_CHECKING:
    from . import PokemonPinballRSWorld

EGG_GROUP_ITEMS: dict[int, str] = {
    1: EGG_BUNCH_1,
    2: EGG_BUNCH_2,
    3: EGG_BUNCH_3,
    4: EGG_BUNCH_4,
    5: EGG_BUNCH_RUBY,
    6: EGG_BUNCH_SAPPHIRE,
}

CanPlayBasicPinball = HasAllCounts({
    EXTRA_STARTING_LIFE: 2,
    STARTING_COINS: 1,
}) | OptionFilter(Difficulty, Difficulty.option_hard, "ge")
CanPlayModeratePinball = HasAllCounts({
    EXTRA_STARTING_LIFE: 3,
    STARTING_COINS: 3,
})| OptionFilter(Difficulty, Difficulty.option_expert, "ge")
CanPlayLongPinball = HasAllCounts({
    EXTRA_STARTING_LIFE: 5,
    STARTING_COINS: 4,
    PICHU_UPGRADE: 1,
})| OptionFilter(Difficulty, Difficulty.option_master, "ge")

CanCatchSpecialEncounter = (CanPlayLongPinball & (Has(SPECIES_RAYQUAZA) | Has(ENCOUNTER_RATE_UP)) &
                            HasFromListUnique(*POKEDEX.keys(), count=100))

SPECIAL_ENCOUNTER_RULES: dict[str, Rule] = {
    # Pichu does not require 100 caught, he's just rare
    SPECIES_LATIOS: CanCatchSpecialEncounter,
    SPECIES_LATIAS: CanCatchSpecialEncounter,
    SPECIES_PICHU: HasAny(EGG_BUNCH_RUBY, EGG_BUNCH_SAPPHIRE, EGG_BUNCH_1, EGG_BUNCH_2, EGG_BUNCH_3,
                          EGG_BUNCH_4) & CanPlayLongPinball & (Has(SPECIES_RAYQUAZA) | Has(ENCOUNTER_RATE_UP)),
    SPECIES_CHIKORITA: (CanCatchSpecialEncounter & Has(CHIKORITA_DEX)) | Has(SPECIAL_GUESTS),
    SPECIES_CYNDAQUIL: (CanCatchSpecialEncounter & Has(CYNDAQUIL_DEX)) | Has(SPECIAL_GUESTS),
    SPECIES_TOTODILE: (CanCatchSpecialEncounter & Has(TOTODILE_DEX)) | Has(SPECIAL_GUESTS),
    SPECIES_AERODACTYL: (CanCatchSpecialEncounter & Has(AERODACTYL_DEX)) | Has(SPECIAL_GUESTS),
}


def get_evo_rule(pre: str, post: str) -> Rule:
    species = species_info.get(pre, {})
    if not species or species.evolutionTarget is None:
        return True_()
    if species.evolutionMethod == 11:
        # special cases
        return Has(EVOLUTION_SPECIAL[pre](post))
    else:
        return Has(EVOLUTION_METHODS[species.evolutionMethod])


def set_rules(world: "PokemonPinballRSWorld") -> None:
    # first set rules for the boards
    world.set_rule(world.get_entrance("To Ruby Board"), Has(RUBY_BOARD))
    world.set_rule(world.get_entrance("To Sapphire Board"), Has(SAPPHIRE_BOARD))

    # now for each board, set the rules for areas
    for i, area in AREAS.items():
        area_rule = Has(area)
        if area in (RUINS_RUBY, RUINS_SAPPHIRE):
            area_rule &= (Has(RUINS_AREA_CARD) | CanPlayModeratePinball)
        world.set_rule(world.get_entrance(f"To {area}"), area_rule)

        for mon, arrows in habitats[i].items():
            rule: Rule = True_()
            if arrows > 2:
                rule &= Has(GET_ARROW)
            if mon in rare_encounters:
                rule &= Has(ENCOUNTER_RATE_UP)
            world.set_rule(world.get_location(f"{area} - {POKEDEX_INVERSE[mon]}"), rule)

    for i, board in enumerate((RUBY_BOARD, SAPPHIRE_BOARD)):
        world.set_rule(world.get_entrance(f"To Hatch Eggs ({board})"), HasAny(EGG_BUNCH_RUBY,
                                                                               EGG_BUNCH_SAPPHIRE,
                                                                               EGG_BUNCH_1,
                                                                               EGG_BUNCH_2,
                                                                               EGG_BUNCH_3,
                                                                               EGG_BUNCH_4) & CanPlayBasicPinball)

        for idx, group in egg_groups.items():
            if (i == 0 and idx == 6) or (i == 1 and idx == 5):
                continue
            for mon in group:
                world.set_rule(world.get_location(f"Eggs ({board.split(' ')[0]}) - {POKEDEX_INVERSE[eggs[mon]]}"),
                               Has(EGG_GROUP_ITEMS[idx]))

        for mon in special_encounters:
            if (i == 0 and mon == 195) or (i == 1 and mon == 196):
                continue
            world.set_rule(world.get_location(f"{board} - {POKEDEX_INVERSE[mon]}"),
                           SPECIAL_ENCOUNTER_RULES.get(POKEDEX_INVERSE[mon]))

        for mon in bonus_catches[i]:
            if mon == 199:
                rule = CanPlayLongPinball | (CanPlayModeratePinball & Has(RUINS_AREA_CARD))
            else:
                rule = CanPlayModeratePinball
            world.set_rule(world.get_location(f"{board} - {POKEDEX_INVERSE[mon]}"), rule)

    world.set_rule(world.get_entrance("To Evolutions"), Has(EVO_ARROW, count=3) & CanPlayBasicPinball)
    for mon, prevo in evolutions.items():
        # Special case for Vileplume and Bellossom
        if mon == 89:
            board_rule: Rule = Has(RUBY_BOARD)
        elif mon == 90:
            board_rule: Rule = Has(SAPPHIRE_BOARD)
        else:
            board_rule: Rule = True_()
        evo_rule = get_evo_rule(POKEDEX_INVERSE[prevo], POKEDEX_INVERSE[mon])
        world.set_rule(world.get_location(f"Evolve - {POKEDEX_INVERSE[prevo]} -> {POKEDEX_INVERSE[mon]}"),
                       Has(POKEDEX_INVERSE[prevo]) & board_rule & evo_rule)

    # Now have every Pokemon location check its event item for accessibility
    for mon in POKEDEX:
        world.set_rule(world.get_location(f"Pokédex - {mon}"), Has(mon))

    # Bonus Stages
    world.set_rule(world.get_location(BONUS_DUSCLOPS), Has(SAPPHIRE_BOARD))
    world.set_rule(world.get_location(BONUS_KECLEON), Has(RUBY_BOARD))
    world.set_rule(world.get_location(BONUS_KYOGRE), Has(SAPPHIRE_BOARD) & CanPlayBasicPinball)
    world.set_rule(world.get_location(BONUS_GROUDON), Has(RUBY_BOARD) & CanPlayBasicPinball)
    world.set_rule(world.get_location(BONUS_RAYQUAZA), CanPlayModeratePinball |
                   (CanPlayBasicPinball & Has(RUINS_AREA_CARD)))
    for spheal in (BONUS_SPHEAL_1, BONUS_SPHEAL_2, BONUS_SPHEAL_3):
        world.set_rule(world.get_location(spheal),
                       HasAll(RUBY_BOARD, HELPER_WHISCASH) |
                       HasAll(SAPPHIRE_BOARD, HELPER_PELIPPER))

    # Bumpers
    for board in (RUBY_BOARD, SAPPHIRE_BOARD):
        for j in range(1, world.options.bonus_multiplier_checks.value + 1):
            if j >= 75:
                rule = CanPlayLongPinball
            elif j >= 25:
                rule = CanPlayModeratePinball
            elif j >= 10:
                rule = CanPlayBasicPinball
            else:
                rule = True_()
            world.set_rule(world.get_location(f"{board} - Bonus Multiplier {j}"), rule)

    for i in range(1, world.options.ball_upgrade_checks.value + 1):
        if i >= 75:
            rule = CanPlayLongPinball | (CanPlayModeratePinball & HasAll(RUBY_BOARD, HELPER_MAKUHITA))
        elif i >= 25:
            rule = CanPlayModeratePinball | (CanPlayBasicPinball & HasAll(RUBY_BOARD, HELPER_MAKUHITA))
        elif i >= 10:
            rule = CanPlayBasicPinball | HasAll(RUBY_BOARD, HELPER_MAKUHITA)
        else:
            rule = True_()
        world.set_rule(world.get_location(f"Ball Upgrade {i}"), rule)

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
