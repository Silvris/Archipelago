from typing import TYPE_CHECKING
from .names import location_names, item_names
from worlds.generic.Rules import set_rule
if TYPE_CHECKING:
    from . import KSSWorld
    from BaseClasses import CollectionState


def can_burn(state: "CollectionState", player: int):
    return state.has_any([item_names.fire, item_names.jet, item_names.hammer, item_names.bomb], player)


def can_cut_rope(state: "CollectionState", player: int):
    return state.has_any([item_names.sword, item_names.cutter, item_names.ninja, item_names.wing], player)


def can_pound_stakes(state: "CollectionState", player: int):
    return state.has_any([item_names.hammer, item_names.stone], player)


def can_pierce_walls(state: "CollectionState", player: int):
    return state.has_any([item_names.sword, item_names.wing, item_names.jet, item_names.ice, item_names.fire,
                          item_names.mirror, item_names.yoyo, item_names.beam, item_names.fighter, item_names.plasma,],
                         player)


def can_pierce_floors(state: "CollectionState", player: int):
    return state.has_any([item_names.mirror, item_names.beam], player)
    #TODO: test Jet, Yoyo, Plasma


def can_fight_wind(state: "CollectionState", player: int):
    return state.has_any([item_names.wing, item_names.jet, item_names.ninja], player)


def set_rules(world: "KSSWorld"):
    # Revenge of Meta Knight
    set_rule(world.get_entrance("Chapter 3 -> Chapter 4"), lambda state: can_burn(state, world.player))

    # Great Cave Offensive
    set_rule(world.get_location(location_names.tgco_treasure_13), lambda state: can_cut_rope(state, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_18), lambda state: can_pierce_walls(state, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_36), lambda state: can_pierce_floors(state, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_42), lambda state: state.has(item_names.stone, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_43), lambda state: can_cut_rope(state, world.player)
                                                                                and can_pound_stakes(state, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_45), lambda state: can_burn(state, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_47), lambda state: can_fight_wind(state, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_49), lambda state: can_burn(state, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_53), lambda state: state.has(item_names.wheel, world.player))
    set_rule(world.get_location(location_names.tgco_treasure_58), lambda state: state.has(item_names.beam, world.player))

