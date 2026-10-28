from dataclasses import dataclass
from math import ceil
from typing import TYPE_CHECKING, Sequence
from typing_extensions import override
from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from . import names
from .locations import get_boss_locations, mm11_regions
from .options import weapons_to_id, bosses, SpeedPlatforming
from rule_builder.rules import CanReachLocation, HasAll, HasAny, Has, AtLeast, Rule, True_, OptionFilter

if TYPE_CHECKING:
    from . import MM11World

# this will need rewritten entirely, but use this so I can test connection before rewriting the logic
# numbers will assume no power gear for now
weapon_damage: dict[int, list[int]] = {
    0: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],  # Mega Buster
    1: [1, 5, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, ],  # Block Dropper
    2: [1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 5, 3, ],  # Acid Barrier
    3: [2, 2, 1, 4, 2, 2, 2, 2, 2, 3, 2, 2, ],  # Pile Driver
    4: [1, 1, 1, 1, 4, 1, 1, 1, 1, 3, 1, 1, ],  # Bounce Ball
    5: [1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 3, ],  # Scramble Thunder
    6: [4, 4, 4, 4, 1, 1, 6, 4, 1, 1, 1, 1, ],  # Tundra Storm
    7: [2, 2, 2, 2, 2, 2, 1, 6, 1, 1, 1, 1, ],  # Blazing Torch
    8: [4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, ],  # Chain Blast
}

weapons_to_name: dict[int, str] = {
    1: names.block_dropper,
    2: names.acid_barrier,
    3: names.pile_driver,
    4: names.bounce_ball,
    5: names.scramble_thunder,
    6: names.tundra_storm,
    7: names.blazing_torch,
    8: names.chain_blast,
}

minimum_weakness_requirement: dict[int, int] = {
    0: 1,  # Mega Buster is free
    1: 2,  # 14 shots of Block Dropper
    2: 1,  # 7 activations of Acid Barrier, this one is a skill issue more than anything
    3: 3,  # 10 uses of Pile Driver
    4: 1,  # 28 shots of Bounce Ball
    5: 2,  # 14 shots of Scramble Thunder
    6: 4,  # 7 uses of Tundra Storm
    7: 2,  # 14 shots of Blazing Torch
    8: 1,  # 28 shots of Chain Blast
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

weapon_costs = {
    0: 0,
    1: 2,
    2: 4,
    3: 3,
    4: 1,
    5: 2,
    6: 4,
    7: 2,
    8: 1,
}


@dataclass
class CanDefeatEnoughRBMs(Rule["MM11World"], game="Mega Man 11"):
    @override
    def _instantiate(self, world: "MM11World") -> Rule.Resolved:
        return self.Resolved(tuple([(key, tuple(val)) for key, val in sorted(world.wily_3_weapons.items())]),
                             world.options.wily_3_requirement.value,
                             player=world.player, caching_enabled=False)

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
                    if state.has_all(map(lambda x: weapons_to_name[x], reqs), self.player):
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


def set_rules(world: "MM11World") -> None:
    from .options import RandomWeaknesses
    # most rules are set on region, so we only worry about rules required within stage access
    # or rules variable on settings
    if hasattr(world.multiworld, "re_gen_passthrough"):
        slot_data = getattr(world.multiworld, "re_gen_passthrough")["Mega Man 11"]
        world.weapon_damage = slot_data["weapon_damage"]
    else:
        if world.options.random_weakness == world.options.random_weakness.option_shuffled:
            weapon_tables = [table.copy() for weapon, table in weapon_damage.items() if weapon != 0]
            world.random.shuffle(weapon_tables)
            for i in range(1, 9):
                world.weapon_damage[i] = weapon_tables.pop()
        elif world.options.random_weakness == world.options.random_weakness.option_randomized:
            world.weapon_damage = {i: [] for i in range(9)}
            for boss in range(11):
                for weapon in world.weapon_damage:
                    world.weapon_damage[weapon].append(min(14, max(0, int(world.random.normalvariate(3, 3)))))
                if not any([world.weapon_damage[weapon][boss] >= 4
                            for weapon in range(1, 9)]):
                    # failsafe, there should be at least one defined non-Buster weakness
                    weapon = world.random.randint(1, 7)
                    world.weapon_damage[weapon][boss] = world.random.randint(4, 14)  # Force weakness
            # handle Wily Capsule
            boss = 11
            for weapon in world.weapon_damage:
                world.weapon_damage[weapon].append(0)
            weapon = world.random.choice(list(world.weapon_damage.keys()))
            world.weapon_damage[weapon][boss] = minimum_weakness_requirement[weapon]

        if world.options.strict_weakness:
            for weapon in weapon_damage:
                for i in range(12):
                    if weapon == 0:
                        world.weapon_damage[weapon][i] = 0
                    elif i in (9, 11):
                        if 3 > world.weapon_damage[weapon][i] > 0:
                            world.weapon_damage[weapon][i] = 0
                    elif i == 8:
                        if 2 > world.weapon_damage[weapon][i] > 0:
                            world.weapon_damage[weapon][i] = 0
                    elif 4 > world.weapon_damage[weapon][i] > 0:
                        world.weapon_damage[weapon][i] = 0

        for p_boss in world.options.plando_weakness:
            for p_weapon in world.options.plando_weakness[p_boss]:
                if not any(w for w in world.weapon_damage
                           if w != weapons_to_id[p_weapon]
                           and world.weapon_damage[w][bosses[p_boss]] > minimum_weakness_requirement[w]):
                    # we need to replace this weakness
                    weakness = world.random.choice([key for key in world.weapon_damage
                                                    if key != weapons_to_id[p_weapon]])
                    world.weapon_damage[weakness][bosses[p_boss]] = minimum_weakness_requirement[weakness]
                world.weapon_damage[weapons_to_id[p_weapon]][bosses[p_boss]] \
                    = world.options.plando_weakness[p_boss][p_weapon]

        # handle special cases
        for boss in range(12):
            for weapon in range(1, 9):
                if (0 < world.weapon_damage[weapon][boss] < minimum_weakness_requirement[weapon] and
                        not any(world.weapon_damage[i][boss] >= minimum_weakness_requirement[i]
                                for i in range(1, 9) if i != weapon)):
                    world.weapon_damage[weapon][boss] = minimum_weakness_requirement[weapon]

        if world.weapon_damage[0][world.options.starting_robot_master.value] < 1:
            world.weapon_damage[0][world.options.starting_robot_master.value] = 1

        # weakness validation, it is better to confirm a completable seed than respect plando
        boss_health = {boss: 0x1C for boss in range(8)}

        weapon_energy = {key: float(0x1C) for key in weapon_costs}
        weapon_boss = {boss: {weapon: world.weapon_damage[weapon][boss] for weapon in world.weapon_damage}
                       for boss in range(8)}
        flexibility = {
            boss: (
                    sum(damage_value > 0 for damage_value in
                        weapon_damages.values())  # Amount of weapons that hit this boss
                    * sum(weapon_damages.values())  # Overall damage that those weapons do
            )
            for boss, weapon_damages in weapon_boss.items()
        }
        boss_flexibility = sorted(flexibility, key=flexibility.get)  # Fast way to sort dict by value
        used_weapons: dict[int, set[int]] = {i: set() for i in range(8)}
        for boss in boss_flexibility:
            boss_damage = weapon_boss[boss]
            weapon_weight = {weapon: (weapon_energy[weapon] / damage) if damage else 0 for weapon, damage in
                             boss_damage.items() if weapon_energy[weapon] > 0 and weapon != 0}
            while boss_health[boss] > 0:
                if boss_damage[0] > 0:
                    boss_health[boss] = 0  # if we can buster, we should buster
                    continue
                if not weapon_weight:
                    # no choice, we have to apply a buster weakness to any remaining bosses
                    for boss, health in boss_health.items():
                        if health > 0:
                            world.weapon_damage[0][boss] = 1
                    break
                highest, wp = max(zip(weapon_weight.values(), weapon_weight.keys()))
                uses = weapon_energy[wp] // weapon_costs[wp]
                if int(uses * boss_damage[wp]) >= boss_health[boss]:
                    used = ceil(boss_health[boss] / boss_damage[wp])
                    weapon_energy[wp] -= weapon_costs[wp] * used
                    boss_health[boss] = 0
                    used_weapons[boss].add(wp)
                elif highest <= 0:
                    # we are out of weapons that can actually damage the boss
                    # so find the weapon that has the most uses, and apply that as an additional weakness
                    max_uses, wp = max((weapon_energy[weapon] // weapon_costs[weapon], weapon)
                                       for weapon in weapon_weight
                                       if weapon != 0)
                    world.weapon_damage[wp][boss] = minimum_weakness_requirement[wp]
                    used = min(int(weapon_energy[wp] // weapon_costs[wp]),
                               ceil(boss_health[boss] / minimum_weakness_requirement[wp]))
                    weapon_energy[wp] -= weapon_costs[wp] * used
                    boss_health[boss] -= int(used * minimum_weakness_requirement[wp])
                    weapon_weight.pop(wp)
                    used_weapons[boss].add(wp)
                    if not weapon_weight:
                        # DANGER: we are out of weapons!!
                        if not all(health <= 0 for health in boss_health.values()):
                            # this boss still has HP, add 1 to the damage for this boss until it dies
                            # if there's still another boss remaining, we've entered a catastrophic failure state
                            while boss_health[boss] > 0:
                                world.weapon_damage[wp][boss] += 1
                                boss_health[boss] -= int(used)
                        # if the boss doesn't have HP, it'll harmlessly break out of the while
                else:
                    # drain the weapon and continue
                    boss_health[boss] -= int(uses * boss_damage[wp])
                    weapon_energy[wp] -= weapon_costs[wp] * uses
                    weapon_weight.pop(wp)
                    used_weapons[boss].add(wp)

            world.wily_3_weapons = {boss: sorted(weapons) for boss, weapons in used_weapons.items()}

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
        if world.weapon_damage[0][i] > 0:
            continue  # this can always be in logic
        weapons = []
        for weapon in range(1, 9):
            if world.weapon_damage[weapon][i] > 0:
                if world.weapon_damage[weapon][i] < minimum_weakness_requirement[weapon]:
                    continue
                weapons.append(weapons_to_name[weapon])
            if i == 10:
                if world.weapon_damage[weapon][i+1] > 0:
                    if world.weapon_damage[weapon][i+1] < minimum_weakness_requirement[weapon]:
                        continue
                    weapons.append(weapons_to_name[weapon])
        if not weapons:
            raise Exception(f"Attempted to have boss {i} with no weakness! Seed: {world.multiworld.seed}")
        for location in boss_locations:
            static_rule = STATIC_LOCATION_RULES.get(location, True_())
            if i == 10:
                # multi-phase fight, get all potential weaknesses
                # we should probably do this smarter, but this works for now
                location_rules[location] = static_rule & HasAll(*weapons)
            else:
                location_rules[location] = static_rule & HasAny(*weapons)

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
