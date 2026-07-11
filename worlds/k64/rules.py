from worlds.AutoWorld import LogicMixin
from BaseClasses import MultiWorld, CollectionState
from copy import deepcopy
from dataclasses import dataclass
from rule_builder.rules import Rule, Has, HasAll, Or
from .items import copy_ability_table, power_combo_map
from .names import LocationName, ItemName

from NetUtils import JSONMessagePart
import typing
from typing_extensions import override

if typing.TYPE_CHECKING:
    from . import K64World

burn_levels = [
    "Pop Star 1",
    "Pop Star 2",
    "Pop Star 3",
    "Rock Star 1",
    "Rock Star 2",
    "Rock Star 3",
    "Aqua Star 1",
    "Aqua Star 2",
    "Neo Star 1",
    "Neo Star 3",
    "Neo Star 4",
    "Shiver Star 1",
    "Shiver Star 4",
    "Ripple Star 1",
    "Ripple Star 3",
]

needle_levels = [
    "Pop Star 1",
    "Pop Star 2",
    "Pop Star 3",
    "Rock Star 1",
    "Rock Star 2",
    "Aqua Star 1",
    "Neo Star 3",
    "Shiver Star 1",
    "Shiver Star 2",
    "Shiver Star 3",
    "Ripple Star 1",
    "Ripple Star 3",
]

bomb_levels = [
    "Pop Star 1",
    "Pop Star 2",
    "Pop Star 3",
    "Rock Star 4",
    "Aqua Star 1",
    "Aqua Star 2",
    "Aqua Star 3",
    "Aqua Star 4",
    "Shiver Star 1",
    "Shiver Star 2",
    "Shiver Star 3",
    "Shiver Star 4",
    "Ripple Star 1",
    "Ripple Star 3",
]

spark_levels = [
    "Pop Star 2",
    "Rock Star 2",
    "Rock Star 4",
    "Aqua Star 1",
    "Aqua Star 2",
    "Aqua Star 4",
    "Shiver Star 2",
    "Shiver Star 3",
    "Ripple Star 1",
    "Ripple Star 3",
]

cutter_levels = [
    "Pop Star 1",
    "Pop Star 2",
    "Pop Star 3",
    "Rock Star 2",
    "Rock Star 3",
    "Aqua Star 1",
    "Aqua Star 3",
    "Aqua Star 4",
    "Neo Star 1",
    "Neo Star 3",
    "Shiver Star 2",
    "Shiver Star 3",
    "Shiver Star 4",
    "Ripple Star 2",
    "Ripple Star 3",
]

stone_levels = [
    "Pop Star 2",
    "Rock Star 1",
    "Rock Star 2",
    "Aqua Star 1",
    "Aqua Star 2",
    "Aqua Star 3",
    "Neo Star 1",
    "Neo Star 3",
    "Neo Star 4",
    "Shiver Star 1",
    "Shiver Star 2",
    "Shiver Star 3",
    "Shiver Star 4",
    "Ripple Star 1",
    "Ripple Star 3",
]

ice_levels = [
    "Pop Star 2",
    "Rock Star 2",
    "Rock Star 3",
    "Aqua Star 1",
    "Aqua Star 2",
    "Neo Star 3",
    "Shiver Star 1",
    "Shiver Star 2",
    "Shiver Star 3",
    "Ripple Star 1",
    "Ripple Star 3",
]

waddle_copy_levels = {
    "Spark Ability": [
        "Rock Star 1",
        "Neo Star 2"
    ],
    "Cutter Ability": [
        "Aqua Star 2",
        "Neo Star 2",
        "Shiver Star 1"
    ]
}

dedede_copy_levels = {
    "Burning Ability": [
        "Aqua Star 3"
    ],
    "Needle Ability": [
        "Neo Star 4",
        "Ripple Star 2",
    ],
    "Bomb Ability": [
        "Neo Star 4",
    ],
    "Spark Ability": [
        "Neo Star 4",
        "Shiver Star 4",
    ],
    "Cutter Ability": [
        "Neo Star 4",
    ]
}


class K64LogicMixin(LogicMixin):
    game: str = "Kirby 64 - The Crystal Shards"
    k64_stale: dict[int, bool]
    k64_level_state: dict[int, list[bool]]

    def init_mixin(self, multiworld: MultiWorld):
        k64_players = multiworld.get_game_players(self.game)
        self.k64_stale = {player: True for player in k64_players}
        self.k64_level_state = {player: [False, False, False, False, False, False] for player in k64_players}

    def copy_mixin(self, other: "K64LogicMixin"):
        other.k64_stale = self.k64_stale.copy()
        other.k64_level_state = deepcopy(self.k64_level_state)
        return other


ABILITY_ACCESS_TABLE: dict[str, str] = {
    ItemName.burn: ItemName.burn_event,
    ItemName.stone: ItemName.stone_event,
    ItemName.ice: ItemName.ice_event,
    ItemName.needle: ItemName.needle_event,
    ItemName.bomb: ItemName.bomb_event,
    ItemName.spark: ItemName.spark_event,
    ItemName.cutter: ItemName.cutter_event,
}


@dataclass
class PowerCombo(Rule["K64World"], game="Kirby 64 - The Crystal Shards"):
    ability_a: str
    ability_b: str

    def __init__(self, ability_a: str, ability_b: str):
        super().__init__()
        self.ability_a = ability_a
        self.ability_b = ability_b

    @override
    def _instantiate(self, world: "K64World") -> Rule.Resolved:
        if world.options.split_power_combos:
            return self.SplitResolved(ability_a=self.ability_a, ability_b=self.ability_b, player=world.player)
        else:
            return self.NonSplitResolved(ability_a=self.ability_a, ability_b=self.ability_b, player=world.player)

    class SplitResolved(Rule.Resolved):
        ability_a: str
        ability_b: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            key = sorted([copy_ability_table[self.ability_a].code, copy_ability_table[self.ability_b].code])
            combo = power_combo_map[tuple(key)]
            if state.has(combo, self.player):
                if state.has_any([self.ability_a, self.ability_b], self.player):
                    # now check for the access
                    return state.has_all([ABILITY_ACCESS_TABLE[self.ability_a],
                                          ABILITY_ACCESS_TABLE[self.ability_b]], self.player)
            return False

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            key = sorted([copy_ability_table[self.ability_a].code, copy_ability_table[self.ability_b].code])
            combo = power_combo_map[tuple(key)]
            s = (f"{combo}: {'Have' if state.has(combo, self.player) else 'Don\'t Have'}\n"
                 f"{self.ability_a}: {'Have' if state.has(self.ability_a, self.player) else 'Don\'t Have'}\n"
                 f"Can Reach {self.ability_a}: {state.has(ABILITY_ACCESS_TABLE[self.ability_a], self.player)}\n"
                 f"{self.ability_b}: {'Have' if state.has(self.ability_b, self.player) else 'Don\'t Have'}\n"
                 f"Can Reach {self.ability_b}: {state.has(ABILITY_ACCESS_TABLE[self.ability_b], self.player)}")
            return s

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            explain_strs = self.explain_str(state).splitlines()
            messages: list[JSONMessagePart] = [{"type": "text", "text": explain_strs[0]}]
            return messages

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            key = sorted([copy_ability_table[self.ability_a].code, copy_ability_table[self.ability_b].code])
            combo = power_combo_map[tuple(key)]
            return {
                x: {id(self)} for x in [combo, self.ability_a, self.ability_b,
                                        ABILITY_ACCESS_TABLE[self.ability_a], ABILITY_ACCESS_TABLE[self.ability_b]]
            }

    class NonSplitResolved(Rule.Resolved):
        ability_a: str
        ability_b: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            if state.has_all([self.ability_a, self.ability_b], self.player):
                # now check for the access
                return state.has_all([ABILITY_ACCESS_TABLE[self.ability_a],
                                      ABILITY_ACCESS_TABLE[self.ability_b]], self.player)
            return False

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            s = (f"{self.ability_a}: {'Have' if state.has(self.ability_a, self.player) else 'Don\'t Have'}\n"
                 f"Can Reach {self.ability_a}: {state.has(ABILITY_ACCESS_TABLE[self.ability_a], self.player)}\n"
                 f"{self.ability_b}: {'Have' if state.has(self.ability_b, self.player) else 'Don\'t Have'}\n"
                 f"Can Reach {self.ability_b}: {state.has(ABILITY_ACCESS_TABLE[self.ability_b], self.player)}")
            return s

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            explain_strs = self.explain_str(state).splitlines()
            messages: list[JSONMessagePart] = [{"type": "text", "text": explain_strs[0]}]
            return messages

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                x: {id(self)} for x in [self.ability_a, self.ability_b,
                                        ABILITY_ACCESS_TABLE[self.ability_a], ABILITY_ACCESS_TABLE[self.ability_b]]
            }


HasBasicBurning = HasAll(ItemName.burn, ItemName.burn_event)
HasBasicStone = HasAll(ItemName.stone, ItemName.stone_event)
HasBasicIce = HasAll(ItemName.ice, ItemName.ice_event)
HasBasicNeedle = HasAll(ItemName.needle, ItemName.needle_event)
HasBasicBomb = HasAll(ItemName.bomb, ItemName.bomb_event)
HasBasicSpark = HasAll(ItemName.spark, ItemName.spark_event)
HasBasicCutter = HasAll(ItemName.cutter, ItemName.cutter_event)


HasAnyBurning = HasBasicBurning | Or(*[PowerCombo(ItemName.burn, x) for x in [ItemName.burn, ItemName.stone,
                                                                              ItemName.ice, ItemName.needle,
                                                                              ItemName.bomb, ItemName.spark,
                                                                              ItemName.cutter]])
HasAnyStone = HasBasicStone | Or(*[PowerCombo(ItemName.stone, x) for x in [ItemName.burn, ItemName.stone,
                                                                              ItemName.ice, ItemName.needle,
                                                                              ItemName.bomb, ItemName.spark,
                                                                              ItemName.cutter]])
HasAnyIce = HasBasicIce | Or(*[PowerCombo(ItemName.ice, x) for x in [ItemName.burn, ItemName.stone,
                                                                              ItemName.ice, ItemName.needle,
                                                                              ItemName.bomb,
                                                                              ItemName.cutter]])
HasAnyNeedle = HasBasicNeedle | Or(*[PowerCombo(ItemName.needle, x) for x in [ItemName.burn, ItemName.stone,
                                                                              ItemName.ice, ItemName.needle,
                                                                              ItemName.bomb, ItemName.spark,
                                                                              ItemName.cutter]])
HasAnyBomb = HasBasicBomb | Or(*[PowerCombo(ItemName.bomb, x) for x in [ItemName.burn, ItemName.stone,
                                                                              ItemName.ice, ItemName.needle,
                                                                              ItemName.bomb, ItemName.spark,
                                                                              ItemName.cutter]])
HasAnySpark = HasBasicSpark | Or(*[PowerCombo(ItemName.spark, x) for x in [ItemName.burn, ItemName.stone,
                                                                              ItemName.ice, ItemName.needle,
                                                                              ItemName.bomb, ItemName.spark,
                                                                              ItemName.cutter]])
HasAnyCutter = HasBasicCutter | Or(*[PowerCombo(ItemName.cutter, x) for x in [ItemName.burn, ItemName.stone,
                                                                              ItemName.ice, ItemName.needle,
                                                                              ItemName.bomb, ItemName.spark,
                                                                              ItemName.cutter]])

HasGreatCutter = PowerCombo(ItemName.cutter, ItemName.cutter)
HasGeokinesis = PowerCombo(ItemName.stone, ItemName.spark)
HasLightbulb = PowerCombo(ItemName.bomb, ItemName.spark)
HasExplodingSnowman = PowerCombo(ItemName.ice, ItemName.bomb)
HasVolcano = PowerCombo(ItemName.burn, ItemName.stone)
HasShurikens = PowerCombo(ItemName.bomb, ItemName.cutter)
HasStoneFriends = PowerCombo(ItemName.stone, ItemName.cutter)
HasDynamite = PowerCombo(ItemName.stone, ItemName.bomb)
HasLightningRod = PowerCombo(ItemName.needle, ItemName.spark)
HasDrill = PowerCombo(ItemName.stone, ItemName.needle)
HasLightsaber = PowerCombo(ItemName.spark, ItemName.cutter)
HasExplodingGordo = PowerCombo(ItemName.needle, ItemName.bomb)
HasFireArrows = PowerCombo(ItemName.burn, ItemName.needle)

HasWaddleDee = Has(ItemName.waddle_dee)
HasAdeleine = Has(ItemName.adeleine)
HasKingDedede = Has(ItemName.king_dedede)

ONEUP_RULES: dict[str, Rule] = {
    LocationName.neo_star_2_u1: HasWaddleDee,
    LocationName.neo_star_2_u2: HasWaddleDee,
    LocationName.aqua_star_3_u1: HasKingDedede & HasStoneFriends,
    LocationName.neo_star_4_u1: HasKingDedede,
    LocationName.ripple_star_2_u1: HasKingDedede,
    LocationName.ripple_star_2_u2: HasKingDedede & HasAnySpark,
}

FOOD_RULES: dict[str, Rule] = {
    LocationName.rock_star_1_f5: HasWaddleDee,
    LocationName.aqua_star_2_f4: HasWaddleDee,
    LocationName.aqua_star_2_f5: HasWaddleDee,
    LocationName.aqua_star_2_f6: HasWaddleDee,
    LocationName.aqua_star_2_f7: HasWaddleDee,
    LocationName.aqua_star_2_f8: HasWaddleDee,
    LocationName.aqua_star_2_f9: HasWaddleDee,
    LocationName.aqua_star_2_f10: HasWaddleDee,
    LocationName.aqua_star_2_f11: HasWaddleDee,
    LocationName.neo_star_2_f2: HasWaddleDee,
    LocationName.neo_star_2_f3: HasWaddleDee,
    LocationName.neo_star_2_f4: HasWaddleDee,
    LocationName.neo_star_2_f5: HasWaddleDee,
    LocationName.neo_star_2_f6: HasWaddleDee,
    LocationName.neo_star_2_f7: HasWaddleDee,
    LocationName.neo_star_2_f8: HasWaddleDee,
    LocationName.neo_star_2_f9: HasWaddleDee,
    LocationName.neo_star_2_f10: HasWaddleDee,
    LocationName.shiver_star_1_f4: HasWaddleDee,
    LocationName.shiver_star_1_f5: HasWaddleDee,
    LocationName.shiver_star_1_f6: HasWaddleDee,
    LocationName.shiver_star_1_f7: HasWaddleDee,
    LocationName.shiver_star_1_f8: HasWaddleDee,
    LocationName.shiver_star_1_f9: HasWaddleDee,
    LocationName.shiver_star_1_f10: HasWaddleDee,
    LocationName.shiver_star_1_f11: HasWaddleDee,
    LocationName.shiver_star_1_f12: HasWaddleDee,
    LocationName.rock_star_2_f7: HasKingDedede,
    LocationName.rock_star_2_f8: HasKingDedede,
    LocationName.rock_star_2_f9: HasKingDedede,
    LocationName.rock_star_2_f10: HasKingDedede,
    LocationName.aqua_star_3_f3: HasKingDedede,
    LocationName.neo_star_4_f3: HasKingDedede,
    LocationName.neo_star_4_f4: HasKingDedede,
    LocationName.neo_star_4_f5: HasKingDedede,
    LocationName.neo_star_4_f6: HasKingDedede,
    LocationName.neo_star_4_f7: HasKingDedede,
    LocationName.neo_star_4_f8: HasKingDedede,
    LocationName.neo_star_4_f9: HasKingDedede,
    LocationName.neo_star_4_f10: HasKingDedede,
    LocationName.neo_star_4_f11: HasKingDedede,
    LocationName.neo_star_4_f12: HasKingDedede,
    LocationName.neo_star_4_f13: HasKingDedede,
    LocationName.neo_star_4_f14: HasKingDedede,
    LocationName.shiver_star_4_f3: HasKingDedede,
    LocationName.shiver_star_4_f4: HasKingDedede,
    LocationName.shiver_star_4_f5: HasKingDedede,
    LocationName.shiver_star_4_f6: HasKingDedede,
    LocationName.shiver_star_4_f7: HasKingDedede,
    LocationName.shiver_star_4_f8: HasKingDedede,
    LocationName.shiver_star_4_f9: HasKingDedede,
    LocationName.shiver_star_4_f10: HasKingDedede,
    LocationName.shiver_star_4_f11: HasKingDedede,
    LocationName.shiver_star_4_f12: HasKingDedede,
    LocationName.shiver_star_4_f13: HasKingDedede,
    LocationName.shiver_star_4_f14: HasKingDedede,
    LocationName.ripple_star_2_f3: HasKingDedede,
    LocationName.ripple_star_2_f4: HasKingDedede,
    LocationName.ripple_star_2_f5: HasKingDedede,
    LocationName.ripple_star_2_f6: HasKingDedede,
    LocationName.ripple_star_2_f7: HasKingDedede,
    LocationName.ripple_star_2_f8: HasKingDedede,
    LocationName.ripple_star_2_f9: HasKingDedede,
    LocationName.ripple_star_2_f10: HasKingDedede & HasAnyIce,
    LocationName.ripple_star_2_f11: HasKingDedede & HasAnyNeedle,
    LocationName.pop_star_3_f3: HasAdeleine,
    LocationName.aqua_star_1_f8: HasAdeleine,
    LocationName.dark_star_adeleine: HasAdeleine,
}

STAR_RULES: dict[str, Rule] = {
    LocationName.rock_star_1_t12: HasWaddleDee,
    LocationName.rock_star_1_t13: HasWaddleDee,
    LocationName.rock_star_1_t14: HasWaddleDee,
    LocationName.rock_star_1_t15: HasWaddleDee,
    LocationName.rock_star_1_t16: HasWaddleDee,
    LocationName.rock_star_2_t30: HasKingDedede,
    LocationName.rock_star_2_t31: HasKingDedede,
    LocationName.rock_star_2_t32: HasKingDedede,
    LocationName.rock_star_2_t33: HasKingDedede,
    LocationName.rock_star_2_t34: HasKingDedede,
    LocationName.rock_star_2_t35: HasKingDedede,
    LocationName.rock_star_2_t36: HasKingDedede,
    LocationName.rock_star_2_t37: HasKingDedede,
    LocationName.rock_star_2_t38: HasKingDedede,
    LocationName.aqua_star_1_t35: HasExplodingSnowman,
    LocationName.aqua_star_1_t36: HasExplodingSnowman,
    LocationName.aqua_star_1_t37: HasExplodingSnowman,
    LocationName.aqua_star_1_t38: HasExplodingSnowman,
    LocationName.aqua_star_2_t8: HasWaddleDee,
    LocationName.aqua_star_2_t9: HasWaddleDee,
    LocationName.aqua_star_2_t10: HasWaddleDee,
    LocationName.aqua_star_2_t11: HasWaddleDee,
    LocationName.aqua_star_2_t12: HasWaddleDee,
    LocationName.aqua_star_2_t13: HasWaddleDee,
    LocationName.aqua_star_2_t14: HasWaddleDee,
    LocationName.aqua_star_2_t15: HasWaddleDee,
    LocationName.aqua_star_2_t16: HasWaddleDee,
    LocationName.aqua_star_2_t17: HasWaddleDee,
    LocationName.aqua_star_2_t18: HasWaddleDee,
    LocationName.aqua_star_2_t19: HasWaddleDee,
    LocationName.aqua_star_2_t20: HasWaddleDee,
    LocationName.aqua_star_2_t21: HasWaddleDee,
    LocationName.aqua_star_2_t22: HasWaddleDee,
    LocationName.aqua_star_2_t23: HasWaddleDee,
    LocationName.aqua_star_2_t24: HasWaddleDee,
    LocationName.aqua_star_2_t25: HasWaddleDee,
    LocationName.aqua_star_2_t26: HasWaddleDee,
    LocationName.aqua_star_2_t27: HasWaddleDee,
    LocationName.aqua_star_2_t28: HasWaddleDee,
    LocationName.aqua_star_2_t29: HasWaddleDee,
    LocationName.aqua_star_2_t30: HasWaddleDee,
    LocationName.aqua_star_2_t31: HasWaddleDee,
    LocationName.aqua_star_2_t32: HasWaddleDee,
    LocationName.aqua_star_2_t33: HasWaddleDee,
    LocationName.aqua_star_2_t34: HasWaddleDee,
    LocationName.aqua_star_2_t35: HasWaddleDee,
    LocationName.aqua_star_2_t36: HasWaddleDee,
    LocationName.aqua_star_2_t37: HasWaddleDee,
    LocationName.aqua_star_2_t38: HasWaddleDee,
    LocationName.aqua_star_2_t39: HasWaddleDee,
    LocationName.aqua_star_2_t40: HasWaddleDee,
    LocationName.aqua_star_2_t41: HasWaddleDee,
    LocationName.aqua_star_2_t42: HasWaddleDee,
    LocationName.aqua_star_2_t43: HasWaddleDee,
    LocationName.aqua_star_2_t44: HasWaddleDee,
    LocationName.aqua_star_2_t45: HasWaddleDee,
    LocationName.aqua_star_2_t46: HasWaddleDee,
    LocationName.aqua_star_2_t47: HasWaddleDee,
    LocationName.aqua_star_2_t48: HasWaddleDee,
    LocationName.aqua_star_2_t49: HasWaddleDee,
    LocationName.aqua_star_3_t15: HasKingDedede,
    LocationName.aqua_star_3_t16: HasKingDedede,
    LocationName.aqua_star_3_t17: HasKingDedede,
    LocationName.aqua_star_3_t18: HasKingDedede,
    LocationName.aqua_star_3_t19: HasKingDedede,
    LocationName.aqua_star_3_t20: HasKingDedede,
    LocationName.aqua_star_3_t21: HasKingDedede,
    LocationName.aqua_star_3_t22: HasKingDedede,
    LocationName.aqua_star_3_t23: HasKingDedede,
    LocationName.aqua_star_3_t24: HasKingDedede,
    LocationName.aqua_star_3_t25: HasKingDedede,
    LocationName.aqua_star_3_t26: HasKingDedede,
    LocationName.neo_star_2_t17: HasWaddleDee,
    LocationName.neo_star_2_t18: HasWaddleDee,
    LocationName.neo_star_2_t19: HasWaddleDee,
    LocationName.neo_star_2_t20: HasWaddleDee,
    LocationName.neo_star_2_t21: HasWaddleDee,
    LocationName.neo_star_2_t22: HasWaddleDee,
    LocationName.neo_star_2_t23: HasWaddleDee,
    LocationName.neo_star_2_t24: HasWaddleDee,
    LocationName.neo_star_2_t25: HasWaddleDee,
    LocationName.neo_star_2_t26: HasWaddleDee,
    LocationName.neo_star_2_t27: HasWaddleDee,
    LocationName.neo_star_2_t28: HasWaddleDee,
    LocationName.neo_star_2_t29: HasWaddleDee,
    LocationName.neo_star_2_t30: HasWaddleDee,
    LocationName.neo_star_2_t31: HasWaddleDee,
    LocationName.neo_star_2_t32: HasWaddleDee,
    LocationName.neo_star_2_t33: HasWaddleDee,
    LocationName.neo_star_2_t34: HasWaddleDee,
    LocationName.neo_star_2_t35: HasWaddleDee,
    LocationName.neo_star_2_t36: HasWaddleDee,
    LocationName.neo_star_2_t37: HasWaddleDee,
    LocationName.neo_star_2_t38: HasWaddleDee,
    LocationName.neo_star_2_t39: HasWaddleDee,
    LocationName.neo_star_2_t40: HasWaddleDee,
    LocationName.neo_star_2_t41: HasWaddleDee,
    LocationName.neo_star_2_t42: HasWaddleDee,
    LocationName.neo_star_2_t43: HasWaddleDee,
    LocationName.neo_star_2_t44: HasWaddleDee,
    LocationName.neo_star_2_t45: HasWaddleDee,
    LocationName.neo_star_2_t46: HasWaddleDee,
    LocationName.neo_star_2_t47: HasWaddleDee,
    LocationName.neo_star_2_t48: HasWaddleDee,
    LocationName.neo_star_2_t49: HasWaddleDee,
    LocationName.neo_star_2_t50: HasWaddleDee,
    LocationName.neo_star_2_t51: HasWaddleDee,
    LocationName.neo_star_2_t52: HasWaddleDee,
    LocationName.neo_star_2_t53: HasWaddleDee,
    LocationName.neo_star_2_t54: HasWaddleDee,
    LocationName.neo_star_2_t55: HasWaddleDee,
    LocationName.neo_star_2_t56: HasWaddleDee,
    LocationName.neo_star_2_t57: HasWaddleDee,
    LocationName.neo_star_2_t58: HasWaddleDee,
    LocationName.neo_star_2_t59: HasWaddleDee,
    LocationName.neo_star_2_t60: HasWaddleDee,
    LocationName.neo_star_4_t4: HasKingDedede,
    LocationName.neo_star_4_t5: HasKingDedede,
    LocationName.neo_star_4_t6: HasKingDedede,
    LocationName.neo_star_4_t7: HasKingDedede,
    LocationName.neo_star_4_t8: HasKingDedede,
    LocationName.neo_star_4_t9: HasKingDedede,
    LocationName.neo_star_4_t10: HasKingDedede,
    LocationName.neo_star_4_t11: HasKingDedede,
    LocationName.neo_star_4_t12: HasKingDedede,
    LocationName.neo_star_4_t13: HasKingDedede,
    LocationName.neo_star_4_t14: HasKingDedede,
    LocationName.neo_star_4_t15: HasKingDedede,
    LocationName.neo_star_4_t16: HasKingDedede,
    LocationName.neo_star_4_t17: HasKingDedede,
    LocationName.neo_star_4_t18: HasKingDedede,
    LocationName.neo_star_4_t19: HasKingDedede,
    LocationName.neo_star_4_t20: HasKingDedede,
    LocationName.neo_star_4_t21: HasKingDedede,
    LocationName.neo_star_4_t22: HasKingDedede,
    LocationName.neo_star_4_t23: HasKingDedede,
    LocationName.neo_star_4_t24: HasKingDedede,
    LocationName.neo_star_4_t25: HasKingDedede,
    LocationName.shiver_star_1_t18: HasWaddleDee,
    LocationName.shiver_star_1_t19: HasWaddleDee,
    LocationName.shiver_star_1_t20: HasWaddleDee,
    LocationName.shiver_star_1_t21: HasWaddleDee,
    LocationName.shiver_star_1_t22: HasWaddleDee,
    LocationName.shiver_star_1_t23: HasWaddleDee,
    LocationName.shiver_star_1_t24: HasWaddleDee,
    LocationName.shiver_star_1_t25: HasWaddleDee,
    LocationName.shiver_star_1_t26: HasWaddleDee,
    LocationName.shiver_star_1_t27: HasWaddleDee,
    LocationName.shiver_star_1_t28: HasWaddleDee,
    LocationName.shiver_star_1_t29: HasWaddleDee,
    LocationName.shiver_star_1_t30: HasWaddleDee,
    LocationName.shiver_star_1_t31: HasWaddleDee,
    LocationName.shiver_star_1_t32: HasWaddleDee,
    LocationName.shiver_star_1_t33: HasWaddleDee,
    LocationName.shiver_star_1_t34: HasWaddleDee,
    LocationName.shiver_star_1_t35: HasWaddleDee,
    LocationName.shiver_star_1_t36: HasWaddleDee,
    LocationName.shiver_star_1_t37: HasWaddleDee,
    LocationName.shiver_star_1_t38: HasWaddleDee,
    LocationName.shiver_star_1_t39: HasWaddleDee,
    LocationName.shiver_star_1_t40: HasWaddleDee,
    LocationName.shiver_star_1_t41: HasWaddleDee,
    LocationName.shiver_star_1_t42: HasWaddleDee,
    LocationName.shiver_star_1_t43: HasWaddleDee,
    LocationName.shiver_star_1_t44: HasWaddleDee,
    LocationName.shiver_star_1_t45: HasWaddleDee,
    LocationName.shiver_star_1_t46: HasWaddleDee,
    LocationName.shiver_star_1_t47: HasWaddleDee,
    LocationName.shiver_star_1_t48: HasWaddleDee,
    LocationName.shiver_star_1_t49: HasWaddleDee,
    LocationName.shiver_star_1_t50: HasWaddleDee,
    LocationName.shiver_star_1_t51: HasWaddleDee,
    LocationName.shiver_star_1_t52: HasWaddleDee,
    LocationName.shiver_star_1_t53: HasWaddleDee,
    LocationName.shiver_star_1_t54: HasWaddleDee,
    LocationName.shiver_star_1_t55: HasWaddleDee,
    LocationName.shiver_star_1_t56: HasWaddleDee,
    LocationName.shiver_star_1_t57: HasWaddleDee,
    LocationName.shiver_star_1_t58: HasWaddleDee,
    LocationName.shiver_star_1_t59: HasWaddleDee,
    LocationName.shiver_star_1_t60: HasWaddleDee,
    LocationName.shiver_star_1_t61: HasWaddleDee,
    LocationName.shiver_star_1_t62: HasWaddleDee,
    LocationName.shiver_star_1_t63: HasWaddleDee,
    LocationName.shiver_star_1_t64: HasWaddleDee,
    LocationName.shiver_star_4_t6: HasDrill,
    LocationName.shiver_star_4_t7: HasDrill,
    LocationName.shiver_star_4_t8: HasKingDedede,
    LocationName.shiver_star_4_t9: HasKingDedede,
    LocationName.shiver_star_4_t10: HasKingDedede,
    LocationName.shiver_star_4_t11: HasKingDedede,
    LocationName.shiver_star_4_t12: HasKingDedede,
    LocationName.shiver_star_4_t13: HasKingDedede,
    LocationName.shiver_star_4_t14: HasKingDedede,
    LocationName.shiver_star_4_t15: HasKingDedede,
    LocationName.shiver_star_4_t16: HasKingDedede,
    LocationName.shiver_star_4_t17: HasKingDedede,
    LocationName.shiver_star_4_t18: HasKingDedede,
    LocationName.shiver_star_4_t19: HasKingDedede,
    LocationName.shiver_star_4_t20: HasKingDedede,
    LocationName.shiver_star_4_t21: HasKingDedede,
    LocationName.shiver_star_4_t22: HasKingDedede,
    LocationName.shiver_star_4_t23: HasKingDedede,
    LocationName.shiver_star_4_t24: HasKingDedede,
    LocationName.shiver_star_4_t25: HasKingDedede,
    LocationName.shiver_star_4_t26: HasKingDedede,
    LocationName.shiver_star_4_t27: HasKingDedede,
    LocationName.shiver_star_4_t28: HasKingDedede,
    LocationName.shiver_star_4_t29: HasKingDedede,
    LocationName.shiver_star_4_t30: HasKingDedede,
    LocationName.shiver_star_4_t31: HasKingDedede,
    LocationName.shiver_star_4_t32: HasKingDedede,
    LocationName.shiver_star_4_t33: HasKingDedede,
    LocationName.shiver_star_4_t34: HasKingDedede,
    LocationName.shiver_star_4_t35: HasKingDedede,
    LocationName.shiver_star_4_t36: HasKingDedede,
    LocationName.shiver_star_4_t37: HasKingDedede,
    LocationName.shiver_star_4_t38: HasKingDedede,
    LocationName.shiver_star_4_t39: HasKingDedede,
    LocationName.shiver_star_4_t40: HasKingDedede,
    LocationName.shiver_star_4_t41: HasKingDedede,
    LocationName.shiver_star_4_t42: HasKingDedede,
    LocationName.shiver_star_4_t43: HasKingDedede,
    LocationName.shiver_star_4_t44: HasKingDedede,
    LocationName.shiver_star_4_t45: HasKingDedede,
    LocationName.shiver_star_4_t46: HasKingDedede,
    LocationName.shiver_star_4_t47: HasKingDedede,
    LocationName.shiver_star_4_t48: HasKingDedede,
    LocationName.shiver_star_4_t49: HasKingDedede,
    LocationName.shiver_star_4_t50: HasKingDedede,
    LocationName.shiver_star_4_t51: HasKingDedede,
    LocationName.ripple_star_2_t8: HasKingDedede,
    LocationName.ripple_star_2_t9: HasKingDedede,
    LocationName.ripple_star_2_t10: HasKingDedede,
    LocationName.ripple_star_2_t11: HasKingDedede,
    LocationName.ripple_star_2_t12: HasKingDedede,
    LocationName.ripple_star_2_t13: HasKingDedede,
    LocationName.ripple_star_2_t14: HasKingDedede,
    LocationName.ripple_star_2_t15: HasKingDedede,
    LocationName.ripple_star_2_t16: HasKingDedede,
}

STANDARD_RULES: dict[str, Rule] = {
    LocationName.pop_star_1_s2: HasAnyBomb,
    LocationName.pop_star_3_s1: HasGreatCutter,

    LocationName.rock_star_1: HasWaddleDee,
    LocationName.rock_star_1_s3: HasWaddleDee & HasGeokinesis,
    LocationName.rock_star_2: HasKingDedede,
    LocationName.rock_star_2_s3: HasKingDedede,
    LocationName.rock_star_3_s3: HasAnyStone,
    LocationName.rock_star_4_s2: HasLightbulb,

    LocationName.aqua_star_1_s3: HasExplodingSnowman,
    LocationName.aqua_star_2: HasWaddleDee,
    LocationName.aqua_star_2_s1: HasVolcano,
    LocationName.aqua_star_2_s2: HasWaddleDee,
    LocationName.aqua_star_2_s3: HasWaddleDee,
    LocationName.aqua_star_3: HasKingDedede,
    LocationName.aqua_star_3_s1: HasShurikens,
    LocationName.aqua_star_3_s2: HasKingDedede,
    LocationName.aqua_star_3_s3: HasKingDedede & HasStoneFriends,

    LocationName.neo_star_2: HasWaddleDee,
    LocationName.neo_star_2_s2: HasWaddleDee,
    LocationName.neo_star_2_s3: HasWaddleDee & HasDynamite,
    LocationName.neo_star_3_s1: HasAnyNeedle,
    LocationName.neo_star_3_s2: HasAdeleine,
    LocationName.neo_star_4: HasKingDedede,
    LocationName.neo_star_4_s1: HasKingDedede,
    LocationName.neo_star_4_s2: HasKingDedede & HasAnyIce,
    LocationName.neo_star_4_s3: HasKingDedede,

    LocationName.shiver_star_1: HasWaddleDee,
    LocationName.shiver_star_1_s1: HasWaddleDee,
    LocationName.shiver_star_1_s2: HasWaddleDee & HasAnyBurning,
    LocationName.shiver_star_1_s3: HasWaddleDee,
    LocationName.shiver_star_2_s3: HasLightningRod,
    LocationName.shiver_star_3_s3: HasAdeleine,
    LocationName.shiver_star_4: HasKingDedede,
    LocationName.shiver_star_4_s1: HasDrill,
    LocationName.shiver_star_4_s2: HasKingDedede & HasLightsaber,
    LocationName.shiver_star_4_s3: HasKingDedede,

    LocationName.ripple_star_1_s3: HasExplodingGordo,
    LocationName.ripple_star_2: HasKingDedede,
    LocationName.ripple_star_2_s1: HasAnySpark,
    LocationName.ripple_star_2_s2: HasKingDedede,
    LocationName.ripple_star_2_s3: HasKingDedede & HasAnyCutter,
    LocationName.ripple_star_3_s2: HasFireArrows,
}


def set_rules(world: "K64World") -> None:
    for location, rule in STANDARD_RULES.items():
        world.set_rule(world.get_location(location), rule)

    # Crystal Requirements
    for i, level in zip(range(1, 7), world.boss_requirements):
        rule = Has(ItemName.crystal_shard, count=level)
        if i == 6:
            rule &= (HasKingDedede & HasWaddleDee & HasAdeleine)
        world.set_rule(world.get_entrance(f"To Level {i + 1}"), rule)
        world.set_rule(world.get_location(f"{LocationName.level_names[i]} - Boss Defeated"), rule)

    # Consumables
    if "1-Ups" in world.options.consumables:
        for location, rule in ONEUP_RULES.items():
            world.set_rule(world.get_location(location), rule)
    if "Food" in world.options.consumables:
        for location, rule in FOOD_RULES.items():
            world.set_rule(world.get_location(location), rule)
    if "Stars" in world.options.consumables:
        for location, rule in STAR_RULES.items():
            world.set_rule(world.get_location(location), rule)

    world.multiworld.completion_condition[world.player] = lambda state: state.has(ItemName.ribbons_crystal,
                                                                                  world.player)
