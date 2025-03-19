from typing import TYPE_CHECKING
from .names import locations, items
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from BaseClasses import CollectionState
    from . import DMC5World


def can_access_nero(state: "CollectionState", player: int):
    return state.has_any([locations.prologue, locations.chapter1, locations.chapter2, locations.chapter3,
                          locations.chapter6, items.chapter7, locations.chapter8, items.chapter13, locations.chapter15],
                         player)


def can_access_v(state: "CollectionState", player: int):
    return state.has_any([locations.chapter4, locations.chapter5, locations.chapter17, locations.chapter9,
                          items.chapter13, locations.chapter14], player)


def can_access_dante(state: "CollectionState", player: int):
    return state.has_any([locations.chapter10, locations.chapter11, locations.chapter12,
                          items.chapter13, locations.chapter16, locations.chapter17, locations.chapter18,
                          locations.chapter19], player)


def can_access_vergil(state: "CollectionState", player: int):
    return state.has_group("Vergil Chapters", player)


def set_rules(world: "DMC5World"):
    # Goal Completion
    if True:  # self.options.mode == GameMode.option_classic:
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory against Vergil",
                                                                                      world.player)
    elif False:  # self.options.mode == GameMode.vergil:
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory against Dante",
                                                                                      world.player)
    else:
        world.multiworld.completion_condition[world.player] = lambda state: state.has_all(["Victory against Vergil",
                                                                                           "Victory against Dante"],
                                                                                          world.player)
    if True:  # self.options.mode in [GameMode.option_classic, GameMode.option_all]:
        set_rule(world.get_location(locations.chapter20), lambda state: state.has_group_unique("Chapters", world.player,
                                                                                               20))
    if False:  # self.options.mode in [GameMode.option_vergil, GameMode.option_all]:
        set_rule(world.get_location(locations.chapter19v), lambda state: state.has_group_unique("Vergil Chapters",
                                                                                               world.player, 19))
