from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing_extensions import override
from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from . import names
from .boss import bosses, damage_type_to_weapons, weapon_to_main_damage, DamageType, cost_per_damage_type
from .locations import get_boss_locations, mm11_regions
from .options import SpeedPlatforming
from rule_builder.rules import CanReachLocation, HasAll, HasAny, Has, AtLeast, Rule, True_, OptionFilter, And

if TYPE_CHECKING:
    from . import MM11World

weapons_to_name: dict[int, str] = {
    1: names.block_dropper,
    2: names.acid_barrier,
    3: names.pile_driver,
    4: names.bounce_ball,
    5: names.scramble_thunder,
    6: names.tundra_storm,
    7: names.blazing_torch,
    8: names.chain_blast,
    9: names.charge_buster,
    10: names.power_gear
}

robot_masters: dict[int, str] = {
    0: "Block Man Defeated",
    1: "Acid Man Defeated",
    2: "Impact Man Defeated",
    3: "Bounce Man Defeated",
    4: "Fuse Man Defeated",
    5: "Tundra Man Defeated",
    6: "Torch Man Defeated",
    7: "Blast Man Defeated"
}


@dataclass
class CanDefeatEnoughRBMs(Rule["MM11World"], game="Mega Man 11"):
    @override
    def _instantiate(self, world: "MM11World") -> Rule.Resolved:
        return self.Resolved(tuple([(key, tuple(val)) for key, val in sorted(world.wily_3_weapons.items())]),
                             world.options.wily_3_requirement.value,
                             player=world.player, caching_enabled=getattr(world, "caching_enabled", False))

    class Resolved(Rule.Resolved):
        boss_requirements: tuple[tuple[int, tuple[int, ...]], ...]
        required: int

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                weapons_to_name[x]: {id(self)} for boss, weapons in self.boss_requirements for x in weapons
            }

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            explain_strs = self.explain_str(state).splitlines()
            messages: list[JSONMessagePart] = [{"type": "text", "text": explain_strs[0]}]
            for rbm in explain_strs[1:]:
                color = "salmon" if "Cannot" in rbm else "green"
                messages.append({"type": "color", "text": rbm, "color": color})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            explain_str = f"Required RBMs: {self.required}"
            for boss, reqs in self.boss_requirements:
                if boss in robot_masters:
                    verb = "Can Defeat" if state.has_all(map(lambda x: weapons_to_name[x], reqs), self.player) \
                        else "Cannot Defeat"
                    explain_str += f"\n{robot_masters[boss][:-9]}: {verb}"
            return explain_str

        @override
        def _evaluate(self, state: "CollectionState") -> bool:
            can_defeat = 0
            for boss, reqs in self.boss_requirements:
                if boss in robot_masters:
                    boss_weapons = []
                    for req in reqs:
                        boss_weapons.extend(damage_type_to_weapons[req])
                    if 0 in boss_weapons:
                        return True
                    if state.has_all(map(lambda x: weapons_to_name[x], boss_weapons), self.player):
                        can_defeat += 1
                        if can_defeat >= self.required:
                            return True
            return False


HasPile = Has(names.pile_driver)
HasRushCoil = Has(names.rush_coil)
HasRushJet = Has(names.rush_jet)
HasVertical = HasRushJet | HasRushCoil
HasSpeed = Has(names.speed_gear)
GearlessPlatforming = HasSpeed | OptionFilter(SpeedPlatforming, value=False)

STATIC_LOCATION_RULES: dict[str, Rule] = {
    names.block_man: GearlessPlatforming,
    names.get_block_dropper: GearlessPlatforming,
    names.light_gift_1: AtLeast(2, CanReachLocation(names.block_man), CanReachLocation(names.acid_man),
                                CanReachLocation(names.impact_man), CanReachLocation(names.bounce_man),
                                CanReachLocation(names.fuse_man), CanReachLocation(names.tundra_man),
                                CanReachLocation(names.torch_man), CanReachLocation(names.blast_man)),
    names.get_rush_jet: AtLeast(4, CanReachLocation(names.block_man), CanReachLocation(names.acid_man),
                                CanReachLocation(names.impact_man), CanReachLocation(names.bounce_man),
                                CanReachLocation(names.fuse_man), CanReachLocation(names.tundra_man),
                                CanReachLocation(names.torch_man), CanReachLocation(names.blast_man)),
    names.light_gift_2: AtLeast(6, CanReachLocation(names.block_man), CanReachLocation(names.acid_man),
                                CanReachLocation(names.impact_man), CanReachLocation(names.bounce_man),
                                CanReachLocation(names.fuse_man), CanReachLocation(names.tundra_man),
                                CanReachLocation(names.torch_man), CanReachLocation(names.blast_man)),
    names.light_gift_3: And(CanReachLocation(names.block_man), CanReachLocation(names.acid_man),
                            CanReachLocation(names.impact_man), CanReachLocation(names.bounce_man),
                            CanReachLocation(names.fuse_man), CanReachLocation(names.tundra_man),
                            CanReachLocation(names.torch_man), CanReachLocation(names.blast_man)),
    names.wily_2_boss: GearlessPlatforming,
}

STATIC_ENTRANCE_RULES: dict[str, Rule] = {
    "To Torch Man Stage": GearlessPlatforming,
    "To Wily Stage 4": CanDefeatEnoughRBMs(),
}

STATIC_1UP_RULES: dict[str, Rule] = {
    names.block_man_c9: HasSpeed | HasVertical,
    names.impact_man_c25: HasPile | HasVertical,
    names.bounce_man_c1: HasPile,
    names.bounce_man_c14: HasPile | HasRushJet,
    names.tundra_man_c24: HasSpeed & (HasPile | Has(names.spike_boots)),
    names.torch_man_c15: HasPile | HasRushJet,
    names.blast_man_c3: HasRushJet,
    names.blast_man_c8: HasRushJet | Has(names.blazing_torch),
    names.blast_man_c18: HasRushJet,
    names.wily_1_c5: HasRushCoil,
}

STATIC_ENERGY_RULES: dict[str, Rule] = {
    names.block_man_c12: GearlessPlatforming,
    names.impact_man_c2: HasPile | HasRushJet,  # not really but it's like the Metal Man E-Tank
    names.tundra_man_c10: HasPile | HasVertical,
    names.torch_man_c20: HasVertical,
    names.wily_1_c4: HasRushJet,
    names.wily_1_c6: HasRushJet | (HasSpeed & HasRushCoil),
    names.wily_1_c7: HasRushJet | (HasSpeed & HasRushCoil),
    names.wily_1_c8: HasRushJet | (HasSpeed & HasRushCoil),
    names.wily_2_c12: GearlessPlatforming,
    names.wily_2_c13: GearlessPlatforming,
}


def wily_validate(world: "MM11World", boss_list: list[int]) -> dict[int, list[DamageType]]:
    # Wily validation
    weapon_energy = {idx: 56 for idx in range(1, 9)}
    wily_flexibility: list[tuple[int, float]] = sorted({idx: world.bosses[idx].get_flexibility()
                                                          for idx in boss_list}.items(), key=lambda x: x[1])
    wily_weapons = {boss: [] for boss in boss_list}
    while wily_flexibility:
        idx, _ = wily_flexibility.pop(0)
        defeated, used = world.bosses[idx].can_defeat(weapon_energy)
        if not defeated:
            # catastrophe, find what they used most and incrementally increase its damage
            wily_flexibility.insert(0, (idx, 0))
            if not used:
                # We have no weapons used, check if we have any weapons at all
                available = [weapon for weapon, energy in weapon_energy.items() if energy > 0]
                if available:
                    world.bosses[idx].damage[weapon_to_main_damage[world.random.choice(available)]] = 8
                else:
                    # Buster time
                    world.bosses[idx].damage[DamageType.BusterLv0] = 1
            else:
                top, uses = max(used.items(), key=lambda x: x[1])
                world.bosses[idx].damage[top] += 1
        else:
            for d_type in used:
                for weapon in damage_type_to_weapons[d_type]:
                    if weapon in weapon_energy:
                        # don't have consider buster/gear energy
                        weapon_energy[weapon] -= (used[d_type] * cost_per_damage_type[d_type])
            wily_weapons[idx].extend(x for x in used.keys())
    return wily_weapons


def set_rules(world: "MM11World") -> None:
    from .options import RandomWeaknesses
    # most rules are set on region, so we only worry about rules required within stage access
    # or rules variable on settings
    if hasattr(world.multiworld, "re_gen_passthrough"):
        slot_data = getattr(world.multiworld, "re_gen_passthrough")["Mega Man 11"]
    else:
        world.bosses = bosses.copy()
        shuffle_remap = {}
        if world.options.random_weakness == RandomWeaknesses.option_shuffled:
            vals = list(damage_type_to_weapons.keys())
            shuffle_remap = dict(zip(damage_type_to_weapons.keys(), vals))
        for idx, boss in world.bosses.items():
            boss.generate_weakness(world, shuffle_remap)

        # Wily 3
        world.wily_3_weapons = wily_validate(world, list(range(8)))

        # Wily 4
        world.wily_4_weapons = wily_validate(world, [10, 11])

    location_rules: dict[str, Rule] = {}

    for i, boss_locations in zip([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] , [
        get_boss_locations("Block Man Stage"),
        get_boss_locations("Acid Man Stage"),
        get_boss_locations("Impact Man Stage"),
        get_boss_locations("Bounce Man Stage"),
        get_boss_locations("Fuse Man Stage"),
        get_boss_locations("Tundra Man Stage"),
        get_boss_locations("Torch Man Stage"),
        get_boss_locations("Blast Man Stage"),
        get_boss_locations("Wily Stage 1"),
        get_boss_locations("Wily Stage 2"),
        get_boss_locations("Wily Stage 4")
    ]):
        if i == 10:
            weapons = []
            for phase in world.wily_4_weapons.values():
                for d_type in phase:
                    weapons.append(damage_type_to_weapons[d_type])
        else:
            weapons = world.bosses[i].get_vulnerabilities()
        if any(0 in weapon_group for weapon_group in weapons):
            continue  # this can always be in logic
        if not weapons:
            raise Exception(f"Attempted to have {world.bosses[i].name} with no weakness! Seed: {world.multiworld.seed}")
        for location in boss_locations:
            static_rule = STATIC_LOCATION_RULES.get(location, True_())
            for weapon_group in weapons:
                if i == 10:
                    # multi-phase fight, get used weapons for each phase
                    static_rule &= HasAll(*[weapons_to_name[x] for x in weapon_group])
                else:
                    static_rule |= HasAll(*[weapons_to_name[x] for x in weapon_group])
            location_rules[location] = static_rule

    for location in STATIC_LOCATION_RULES:
        if location not in location_rules:
            location_rules[location] = STATIC_LOCATION_RULES[location]

    # Handle entrance rules
    for region, info in mm11_regions.items():
        entrance = world.get_entrance(f"To {region}")
        static_rule = STATIC_ENTRANCE_RULES.get(entrance.name, True_())
        location_rule = True_()
        for location in info.required_locations:
            location_rule &= CanReachLocation(location)
        world.set_rule(entrance, static_rule & location_rule & HasAll(*info.required_items))

    # Consumable rules
    if world.options.consumables in (world.options.consumables.option_1up_etank,
                                     world.options.consumables.option_all):
        for location in STATIC_1UP_RULES:
            location_rules[location] = STATIC_1UP_RULES[location]

    if world.options.consumables in (world.options.consumables.option_weapon_health,
                                     world.options.consumables.option_all):
        for location in STATIC_ENERGY_RULES:
            location_rules[location] = STATIC_ENERGY_RULES[location]

    for location, rule in location_rules.items():
        world.set_rule(world.get_location(location), rule)
