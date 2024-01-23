from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule, add_rule

if TYPE_CHECKING:
    from . import PokemonBW2World


def set_rules(world: "PokemonBW2World"):

    if "Route 20 Hiker" not in world.options.remove_roadblocks:
        set_rule(world.multiworld.get_entrance("Route 20 -> Virbank City", world.player),
                 lambda state: state.has("Basic Badge", world.player))

    set_rule(world.multiworld.get_entrance("Route 20 -> Cave of Being", world.player),
             lambda state: state.has("HM03 Surf", world.player))

    set_rule(world.multiworld.get_entrance("Virbank City -> Pokestar Studios", world.player),
             lambda state: state.has("Toxic Badge", world.player))

    if world.options.extra_key_items:
        set_rule(world.multiworld.get_entrance("Virbank City -> Castelia City", world.player),
                 lambda state: state.has("Ferry Pass", world.player))

    set_rule(world.multiworld.get_entrance("Castelia City -> Castelia Sewers", world.player),
             lambda state: state.has("Insect Badge", world.player))

    if "Castelia City Clowns" not in world.options.remove_roadblocks:
        set_rule(world.multiworld.get_entrance("Castelia City -> Route 4", world.player),
                 lambda state: state.has("Insect Badge", world.player))

    set_rule(world.multiworld.get_entrance("Castelia Sewers -> Castelia Back Alley", world.player),
             lambda state: state.has_all(["HM03 Surf", "Season Machine"], world.player))

    set_rule(world.multiworld.get_entrance("Castelia Sewers -> Castelia Park", world.player),
             lambda state: state.has_all(["HM03 Surf", "Season Machine"], world.player))

    set_rule(world.multiworld.get_entrance("Route 14 -> Abundant Shrine", world.player),
             lambda state: state.has("HM03 Surf", world.player))

    set_rule(world.multiworld.get_entrance("Undella Town -> Undella Bay", world.player),
             lambda state: state.has("HM03 Surf", world.player))

    set_rule(world.multiworld.get_entrance("Undella Bay -> Seaside Cave", world.player),
             lambda state: state.has("HM03 Surf", world.player))

    set_rule(world.multiworld.get_entrance("Undella Bay -> Abyssal Ruins", world.player),
             lambda state: state.has_all(["HM03 Surf", "HM06 Dive"], world.player))

    set_rule(world.multiworld.get_entrance("Seaside Cave -> Plasma Frigate (Route 21)", world.player),
             lambda state: state.has_all(["Colress MCHN", "HM03 Surf"], world.player))

    set_rule(world.multiworld.get_location("Giant Chasm - DNA Splicers", world.player),
             lambda state: state.has_all(["HM03 Surf", "HM04 Strength"], world.player))

    # Elite 4 condition
    set_rule(world.multiworld.get_entrance("Victory Road -> Pokemon League", world.player),
             lambda state: state.count_group("Badges", world.player) >= 8
                           and state.has_all(["HM03 Surf", "HM04 Strength"], world.player))

    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
