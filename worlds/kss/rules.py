from typing import TYPE_CHECKING
from .names import location_names, item_names
from .items import sub_game_completion
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import KSSWorld
    from BaseClasses import CollectionState


def can_fight_wind(state: "CollectionState", player: int):
    return state.has_any([item_names.wing, item_names.jet, item_names.ninja], player)


def set_rules(world: "KSSWorld"):
    if "Dyna Blade" in world.options.included_subgames:
        # Dyna Blade
        set_rule(world.get_location(location_names.db_switch_1), lambda state: state.has(item_names.mirror,
                                                                                         world.player))

    if "Revenge of Meta Knight" in world.options.included_subgames:
        # Revenge of Meta Knight
        set_rule(world.get_entrance("RoMK - Chapter 3 -> RoMK - Chapter 4"),
                 lambda state: state.has(item_names.fire, world.player))
        set_rule(world.get_entrance("RoMK - Chapter 4 -> RoMK - Chapter 5"),
                 lambda state: state.has_any([item_names.beam,
                                              item_names.yoyo,
                                              item_names.jet,
                                              item_names.bomb],
                                             world.player))
        set_rule(world.get_entrance("RoMK - Chapter 5 -> RoMK - Chapter 6"),
                 lambda state: state.has_any([item_names.wing,
                                              item_names.suplex],
                                             world.player))
    if "The Great Cave Offensive" in world.options.included_subgames:
        # Delay setting these rules until we know for sure
        if world.treasure_value:
            set_rule(world.get_entrance("Sub-Tree -> Crystal"), lambda state: state.has("Gold", world.player,
                                                                                        world.treasure_value[0]))
            set_rule(world.get_entrance("Crystal -> Old Tower"), lambda state: state.has("Gold", world.player,
                                                                                         world.treasure_value[1]))
            set_rule(world.get_entrance("Old Tower -> Garden"), lambda state: state.has("Gold", world.player,
                                                                                        world.treasure_value[2]))
            set_rule(world.get_location(location_names.tgco_complete), lambda state: state.has("Gold", world.player,
                                                                                               world.treasure_value[3]))
        # Great Cave Offensive
        set_rule(world.get_location(location_names.tgco_treasure_4),
                 lambda state: state.has_any([item_names.wing, item_names.plasma], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_7),
                 lambda state: state.has_any([item_names.beam, item_names.wing, item_names.plasma], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_13),
                 lambda state: state.has_any([item_names.cutter, item_names.sword, item_names.wing], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_18),
                 lambda state: state.has_any([item_names.crash, item_names.yoyo,
                                              item_names.bomb, item_names.beam], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_19),
                 lambda state: state.has_any([item_names.crash, item_names.yoyo,
                                              item_names.bomb, item_names.beam], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_20),
                 lambda state: state.has_any([item_names.crash, item_names.yoyo,
                                              item_names.bomb, item_names.beam], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_21),
                 lambda state: state.has_any([item_names.crash, item_names.yoyo,
                                              item_names.bomb, item_names.beam], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_22),
                 lambda state: state.has_any([item_names.crash, item_names.yoyo,
                                              item_names.bomb, item_names.beam], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_28),
                 lambda state: state.has_any([item_names.crash, item_names.yoyo,
                                              item_names.beam, item_names.beam], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_31),
                 lambda state: state.has_any([item_names.hammer, item_names.stone], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_32),
                 lambda state: state.has_any([item_names.hammer, item_names.stone], world.player)
                               and state.has(item_names.fire, world.player))
        set_rule(world.get_location(location_names.tgco_treasure_33),
                 lambda state: state.has_any([item_names.hammer, item_names.stone], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_34),
                 lambda state: state.has_any([item_names.cutter, item_names.beam, item_names.beam, item_names.hammer,
                                              item_names.bomb, item_names.jet, item_names.wing, item_names.stone,
                                              item_names.plasma], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_36),
                 lambda state: state.has_any([item_names.beam, item_names.yoyo, item_names.plasma], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_37),
                 lambda state: state.has_any([item_names.parasol, item_names.yoyo, item_names.beam, item_names.plasma,
                                              item_names.hammer, item_names.stone, item_names.bomb], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_42),
                 lambda state: state.has(item_names.stone, world.player))
        set_rule(world.get_location(location_names.tgco_treasure_43),
                 lambda state: state.has_any([item_names.ninja, item_names.sword, item_names.wing], world.player)
                               and state.has(item_names.stone, world.player))
        set_rule(world.get_location(location_names.tgco_treasure_45),
                 lambda state: state.has_any([item_names.jet, item_names.fire], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_47),
                 lambda state: can_fight_wind(state, world.player))
        set_rule(world.get_location(location_names.tgco_treasure_49),
                 lambda state: state.has(item_names.jet, world.player))
        set_rule(world.get_location(location_names.tgco_treasure_52),
                 lambda state: state.has_any([item_names.parasol, item_names.wing, item_names.plasma], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_53),
                 lambda state: state.has(item_names.wheel, world.player))
        set_rule(world.get_location(location_names.tgco_treasure_58),
                 lambda state: state.has_any([item_names.beam, item_names.crash], world.player))
        set_rule(world.get_location(location_names.tgco_treasure_59),
                 lambda state: state.has_any([item_names.ninja, item_names.sword, item_names.wing, item_names.cutter],
                                             world.player))

    if "Milky Way Wishes" in world.options.included_subgames:
        if world.options.milky_way_wishes_mode == "local":
            set_rule(world.get_location(location_names.mww_complete),
                     lambda state: state.has_all([item_names.floria, item_names.aqualiss,
                                                  item_names.skyhigh, item_names.hotbeat,
                                                  item_names.cavios, item_names.mecheye,
                                                  item_names.halfmoon], world.player))
        else:
            set_rule(world.get_location(location_names.mww_complete),
                     lambda state: state.has(item_names.rainbow_star, world.player, 7))

        set_rule(world.get_location(location_names.mww_sword),
                 lambda state: state.has_any([item_names.beam, item_names.bomb, item_names.cutter, item_names.fire,
                                              item_names.hammer, item_names.jet, item_names.mirror, item_names.parasol,
                                              item_names.plasma, item_names.stone, item_names.wing, item_names.yoyo],
                                             world.player))

        set_rule(world.get_location(location_names.mww_wheel),
                 lambda state: state.has_any([item_names.fire, item_names.jet], world.player))

        set_rule(world.get_location(location_names.mww_suplex),
                 lambda state: state.has_any([item_names.fighter, item_names.yoyo], world.player))

        set_rule(world.get_location(location_names.mww_ninja),
                 lambda state: state.has_any([item_names.beam, item_names.cutter, item_names.fire, item_names.hammer,
                                              item_names.jet, item_names.mirror, item_names.parasol, item_names.plasma,
                                              item_names.stone, item_names.sword, item_names.wing, item_names.yoyo],
                                             world.player))

    if "The Arena" in world.options.included_subgames:
        for i in range(10, 21):
            set_rule(world.get_location(f"The Arena - {i} Straight Wins"),
                     lambda state: state.has_group_unique("Copy Ability", world.player, 5))

    sub_game_complete = list(sub_game_completion.keys())
    sub_game_required = []
    for sub_game in sub_game_completion.keys():
        if sub_game.rsplit(" - ")[0] in world.options.required_subgames:
            sub_game_required.append(sub_game)

    world.multiworld.completion_condition[world.player] = lambda state: \
        state.has_all(sub_game_required, world.player) and state.has_from_list(
        sub_game_complete, world.player, world.options.required_subgame_completions)
