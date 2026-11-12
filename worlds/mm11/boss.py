import math
from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING
from . import names
if TYPE_CHECKING:
    from . import MM11World


class DamageType(IntEnum):
    BusterLv0 = 0
    BusterLv1 = 1
    BusterLv2 = 2
    PowerShot1 = 3
    PowerShot2 = 4
    FinalBuster = 5
    Block = 6
    PowerBlock = 7
    AcidBarrier = 8
    AcidRain = 9
    AcidBuster = 10
    PowerAcidBarrier = 11
    PowerAcidRain = 12
    PowerAcidBuster = 13
    PileDash = 14
    PileBurst = 15
    PowerPileDash = 16
    PowerPileBurst = 17
    BounceBall = 18
    PowerBounceBall = 19
    ThunderShot = 20
    ThunderBulb = 21
    ThunderBurst = 22
    PowerThunderShot = 23
    PowerThunderBulb = 24
    PowerThunderBurst = 25
    TundraStorm = 26
    PowerTundraStorm = 27
    RisingTorch = 28
    TorchShot = 29
    PowerRisingTorch = 30
    PowerTorchShot = 31
    Blast1 = 32
    Blast2 = 33
    Blast3 = 34
    Blast4 = 35
    PowerBlast = 36


weapons_to_id: dict[str, int] = {
    "Mega Buster": 0,
    names.block_dropper: 1,
    names.acid_barrier: 2,
    names.pile_driver: 3,
    names.bounce_ball: 4,
    names.scramble_thunder: 5,
    names.tundra_storm: 6,
    names.blazing_torch: 7,
    names.chain_blast: 8,
    names.charge_buster: 9,
    names.power_gear: 10,
}

boss_names: dict[str, int] = {
    "Block Man": 0,
    "Acid Man": 1,
    "Impact Man": 2,
    "Bounce Man": 3,
    "Fuse Man": 4,
    "Tundra Man": 5,
    "Torch Man": 6,
    "Blast Man": 7,
    "Yellow Devil MK-III": 8,
    "Mawverne": 9,
    "Wily Machine 11 V1": 10,
    "Wily Machine 11 V2": 11,
}

damage_type_to_weapons: dict[DamageType, list[int]] = {
    DamageType.BusterLv0: [0],
    DamageType.BusterLv1: [9],
    DamageType.BusterLv2: [9],
    DamageType.PowerShot1: [9, 10],
    DamageType.PowerShot2: [9, 10],
    DamageType.FinalBuster: [9, 10],
    DamageType.Block: [1],
    DamageType.PowerBlock: [1, 10],
    DamageType.AcidBarrier: [2],
    DamageType.AcidRain: [2],
    DamageType.AcidBuster: [2],
    DamageType.PowerAcidBarrier: [2, 10],
    DamageType.PowerAcidRain: [2, 10],
    DamageType.PowerAcidBuster: [2, 10],
    DamageType.PileDash: [3],
    DamageType.PileBurst: [3],
    DamageType.PowerPileDash: [3, 10],
    DamageType.PowerPileBurst: [3, 10],
    DamageType.BounceBall: [4],
    DamageType.PowerBounceBall: [4, 10],
    DamageType.ThunderShot: [5],
    DamageType.ThunderBulb: [5],
    DamageType.ThunderBurst: [5],
    DamageType.PowerThunderShot: [5, 10],
    DamageType.PowerThunderBulb: [5, 10],
    DamageType.PowerThunderBurst: [5, 10],
    DamageType.TundraStorm: [6],
    DamageType.PowerTundraStorm: [6, 10],
    DamageType.RisingTorch: [7],
    DamageType.TorchShot: [7],
    DamageType.PowerRisingTorch: [7, 10],
    DamageType.PowerTorchShot: [7, 10],
    DamageType.Blast1: [8],
    DamageType.Blast2: [8],
    DamageType.Blast3: [8],
    DamageType.Blast4: [8],
    DamageType.PowerBlast: [8, 10],
}

weapon_to_main_damage: dict[int, DamageType] = {
    1: DamageType.Block,
    2: DamageType.AcidBuster,
    3: DamageType.PileDash,
    4: DamageType.BounceBall,
    5: DamageType.ThunderBulb,
    6: DamageType.TundraStorm,
    7: DamageType.TorchShot,
    8: DamageType.Blast2,  # this one is mostly flavor, Blast1 is too easy
}

cost_per_damage_type: dict[DamageType, float] = {
    DamageType.BusterLv0: 0,
    DamageType.BusterLv1: 0,
    DamageType.BusterLv2: 0,
    DamageType.PowerShot1: 0,
    DamageType.PowerShot2: 0,
    DamageType.FinalBuster: 0,
    DamageType.Block: 4.0,
    DamageType.PowerBlock: 6.0,
    DamageType.AcidBarrier: 8.0,
    DamageType.AcidRain: 8.0,
    DamageType.AcidBuster: 2.0,  # Acid Buster is hard to quantify, as it's as many shots as can be hit in the timer
    DamageType.PowerAcidBarrier: 10.0,
    DamageType.PowerAcidRain: 10.0,
    DamageType.PowerAcidBuster: 4.0,  # do it like this so it should prio non-power
    DamageType.PileDash: 6.0,
    DamageType.PileBurst: 6.0,  # You get one dash and one burst
    DamageType.PowerPileDash: 8.0,
    DamageType.PowerPileBurst: 8.0,
    DamageType.BounceBall: 2.0,
    DamageType.PowerBounceBall: 4.0,
    DamageType.ThunderShot: 4.0,
    DamageType.ThunderBulb: 4.0,
    DamageType.ThunderBurst: 4.0,
    DamageType.PowerThunderShot: 6.0,
    DamageType.PowerThunderBulb: 6.0,
    DamageType.PowerThunderBurst: 6.0,
    DamageType.TundraStorm: 8.0,
    DamageType.PowerTundraStorm: 14.0,
    DamageType.RisingTorch: 2.0,
    DamageType.TorchShot: 2.0,
    DamageType.PowerRisingTorch: 10.0,
    DamageType.PowerTorchShot: 10.0,
    DamageType.Blast1: 2.0,
    DamageType.Blast2: 4.0,
    DamageType.Blast3: 6.0,
    DamageType.Blast4: 8.0,
    DamageType.PowerBlast: 10.0,
}


# Some damage types are impractical to hit with, so we should only consider them
standard_damage_types = [DamageType.Block, DamageType.AcidBuster, DamageType.PileDash, DamageType.BounceBall,
                         DamageType.ThunderBulb, DamageType.TundraStorm, DamageType.TorchShot,
                         DamageType.Blast1, DamageType.Blast2, DamageType.Blast3, DamageType.Blast4]


power_damage_types = [DamageType.PowerBlock, DamageType.PowerAcidBuster, DamageType.PowerPileDash,
                      DamageType.PowerBounceBall, DamageType.PowerThunderBulb, DamageType.PowerTundraStorm,
                      DamageType.PowerTorchShot, DamageType.PowerBlast]


@dataclass
class Boss:
    name: str
    damage: dict[DamageType, int]
    default_health: float = 56.0

    def __copy__(self):
        return Boss(self.name, {d_type: damage for d_type, damage in self.damage.items()},
                    default_health=self.default_health)

    def can_defeat(self, weapon_energy: dict[int, int]) -> tuple[bool, dict[DamageType, int]]:
        used = {}
        # first, if buster is possible we should use that
        # this includes the Charge Buster and Power Shot, but not final buster
        if self.damage[DamageType.BusterLv0] > 0:
            used[DamageType.BusterLv0] = 1
            return True, used

        if self.damage[DamageType.BusterLv1] > 0 or self.damage[DamageType.BusterLv2] > 0:
            for weapon in damage_type_to_weapons[DamageType.BusterLv1]:
                used[DamageType.BusterLv1] = 1
            return True, used

        if self.damage[DamageType.PowerShot1] > 0 or self.damage[DamageType.PowerShot2] > 0:
            for weapon in damage_type_to_weapons[DamageType.PowerShot1]:
                used[DamageType.BusterLv1] = 1
            return True, used

        health = self.default_health
        # everything from here will use energy
        damage_efficiency = sorted({d_type: (self.damage[d_type]) / cost_per_damage_type[d_type]
                                    for d_type in [*standard_damage_types, *power_damage_types]}.items(),
                                   key=lambda t: t[1], reverse=True)
        while damage_efficiency:
            d_type, eff = damage_efficiency.pop(0)
            if eff == 0:
                # out of weapons that can damage, break the while
                break
            main_weapon = -1
            for weapon in damage_type_to_weapons[d_type]:
                if weapon < 9:
                    main_weapon = weapon

            # MM11 grants you 1 final shot that drains the rest of your remaining energy if you're below the req amount
            # so we can use ceiling to mimic that
            uses = math.ceil(weapon_energy[main_weapon] / cost_per_damage_type[d_type])
            if uses > 0:
                needed_uses = math.ceil(health / self.damage[d_type])
                health -= (min(needed_uses, uses) * self.damage[d_type])
                used[d_type] = uses
                if health <= 0:
                    return True, used

        return False, used

    def get_flexibility(self) -> float:
        return sum(damage > 0 for damage in self.damage.values()) * sum(self.damage.values())

    def get_vulnerabilities(self) -> list[list[int]]:
        vulnerabilities = []
        for d_type in [DamageType.BusterLv0, DamageType.BusterLv1, DamageType.BusterLv2, DamageType.PowerShot1,
                       DamageType.PowerShot2, *standard_damage_types, *power_damage_types]:
            if cost_per_damage_type[d_type] > 0:
                uses_max = math.ceil(56 / cost_per_damage_type[d_type])
                if uses_max * self.damage[d_type] >= 56:
                    vulnerabilities.append(damage_type_to_weapons[d_type])
            else:
                # This weapon is free, always add if it does damage
                if self.damage[d_type] > 0:
                    vulnerabilities.append(damage_type_to_weapons[d_type])
        return vulnerabilities

    def get_weaknesses(self, damage: dict[DamageType, int] | None = None, include_buster: bool = False) -> list[DamageType]:
        if not damage:
            damage = self.damage
        weaknesses = []
        for d_type in [*standard_damage_types, *power_damage_types]:
            # the math here ends up being symmetric, the lowest amount of damage needs a 1:1 ratio with cost
            if damage[d_type] >= max(8, math.ceil(cost_per_damage_type[d_type])):
                weaknesses.append(d_type)
        if include_buster:
            for d_type in [DamageType.BusterLv0, DamageType.BusterLv1, DamageType.BusterLv2,
                           DamageType.PowerShot1, DamageType.PowerShot2,]:
                if damage[d_type] >= 0:
                    weaknesses.append(d_type)
        return weaknesses

    def generate_weakness(self, world: "MM11World", shuffle_remap: dict[DamageType, DamageType]) -> None:
        from .options import RandomWeaknesses, StrictWeaknesses
        new_weaknesses = self.damage.copy()

        # first handle random
        if world.options.random_weakness:
            if world.options.random_weakness == RandomWeaknesses.option_shuffled:
                for old, new in shuffle_remap.items():
                    new_weaknesses[new] = self.damage[old]
            else:
                for d_type in self.damage:
                    new_weaknesses[d_type] = min(20, max(0, int(world.random.normalvariate(5, 4))))
            if not self.get_weaknesses(new_weaknesses):
                # need to guarantee at least one weakness
                weakness = world.random.choice(standard_damage_types)
                new_weaknesses[weakness] = world.random.randint(max(8, math.ceil(cost_per_damage_type[weakness])), 20)

        # now we can handle strict
        if world.options.strict_weakness:
            # this may warrant elaboration
            # MM11 has very loose damage numbers lol
            for d_type in new_weaknesses:
                if d_type == DamageType.BusterLv0:
                    new_weaknesses[d_type] = 0
                elif d_type in (DamageType.BusterLv1, DamageType.BusterLv2, DamageType.PowerShot1, DamageType.PowerShot2, DamageType.FinalBuster):
                    if world.options.strict_weakness == StrictWeaknesses.option_include_charge:
                        if new_weaknesses[d_type] < 8:
                            new_weaknesses[d_type] = 0
                    else:
                        new_weaknesses[d_type] = 0
                else:
                    if new_weaknesses[d_type] < 8:
                        new_weaknesses[d_type] = 0

        # next is plando
        if self.name in world.options.plando_weakness:
            for p_weapon, damage in world.options.plando_weakness[self.name].items():
                d_type = getattr(DamageType, p_weapon)  # should be safe, schema should prevent otherwise
                new_weaknesses[d_type] = damage
                if not self.get_weaknesses(new_weaknesses):
                    # need to roll a new weakness
                    weakness = world.random.choice([dt for dt in standard_damage_types if dt != d_type])
                    new_weaknesses[weakness] = world.random.randint(max(8, math.ceil(cost_per_damage_type[weakness])), 20)

        # Special cases
        if self.name == "Bounce Man":
            # Because he's made of rubber, thunder bursts don't spawn
            new_weaknesses[DamageType.ThunderBurst] = 0
            new_weaknesses[DamageType.PowerThunderBurst] = 0

        # Starting RBM
        if boss_names[self.name] == world.options.starting_robot_master.value:
            new_weaknesses[DamageType.BusterLv0] = 2  # Maybe consider 1, but that's evil lmao

        # finally apply
        self.damage = new_weaknesses

    def set_damage(self, damage: dict[int, int]):
        # Internal, used for UT
        for damage_type, damage_val in damage.items():
            self.damage[DamageType(damage_type)] = damage_val


bosses: dict[int, Boss] = {
    0: Boss("Block Man", {
        DamageType.BusterLv0: 2,
        DamageType.BusterLv1: 2,
        DamageType.BusterLv2: 6,
        DamageType.PowerShot1: 6,
        DamageType.PowerShot2: 10,
        DamageType.FinalBuster: 16,
        DamageType.Block: 2,
        DamageType.PowerBlock: 2,
        DamageType.AcidBarrier: 0,
        DamageType.AcidRain: 0,
        DamageType.AcidBuster: 2,
        DamageType.PowerAcidBarrier: 2,
        DamageType.PowerAcidRain: 2,
        DamageType.PowerAcidBuster: 2,
        DamageType.PileDash: 4,
        DamageType.PileBurst: 4,
        DamageType.PowerPileDash: 4,
        DamageType.PowerPileBurst: 6,
        DamageType.BounceBall: 2,
        DamageType.PowerBounceBall: 2,
        DamageType.ThunderShot: 2,
        DamageType.ThunderBulb: 2,
        DamageType.ThunderBurst: 4,
        DamageType.PowerThunderShot: 2,
        DamageType.PowerThunderBulb: 4,
        DamageType.PowerThunderBurst: 4,
        DamageType.TundraStorm: 8,
        DamageType.PowerTundraStorm: 8,
        DamageType.RisingTorch: 4,
        DamageType.TorchShot: 2,
        DamageType.PowerRisingTorch: 4,
        DamageType.PowerTorchShot: 2,
        DamageType.Blast1: 8,
        DamageType.Blast2: 10,
        DamageType.Blast3: 16,
        DamageType.Blast4: 22,
        DamageType.PowerBlast: 20,
    }, default_health=56*2),
    1: Boss("Acid Man", {
        DamageType.BusterLv0: 2,
        DamageType.BusterLv1: 2,
        DamageType.BusterLv2: 6,
        DamageType.PowerShot1: 6,
        DamageType.PowerShot2: 10,
        DamageType.FinalBuster: 16,
        DamageType.Block: 10,
        DamageType.PowerBlock: 10,
        DamageType.AcidBarrier: 0,
        DamageType.AcidRain: 0,
        DamageType.AcidBuster: 2,
        DamageType.PowerAcidBarrier: 2,
        DamageType.PowerAcidRain: 2,
        DamageType.PowerAcidBuster: 2,
        DamageType.PileDash: 4,
        DamageType.PileBurst: 4,
        DamageType.PowerPileDash: 4,
        DamageType.PowerPileBurst: 6,
        DamageType.BounceBall: 2,
        DamageType.PowerBounceBall: 2,
        DamageType.ThunderShot: 2,
        DamageType.ThunderBulb: 2,
        DamageType.ThunderBurst: 4,
        DamageType.PowerThunderShot: 2,
        DamageType.PowerThunderBulb: 4,
        DamageType.PowerThunderBurst: 4,
        DamageType.TundraStorm: 8,
        DamageType.PowerTundraStorm: 8,
        DamageType.RisingTorch: 4,
        DamageType.TorchShot: 2,
        DamageType.PowerRisingTorch: 4,
        DamageType.PowerTorchShot: 2,
        DamageType.Blast1: 2,
        DamageType.Blast2: 4,
        DamageType.Blast3: 8,
        DamageType.Blast4: 12,
        DamageType.PowerBlast: 10,
    }),
    2: Boss("Impact Man", {
        DamageType.BusterLv0: 2,
        DamageType.BusterLv1: 2,
        DamageType.BusterLv2: 6,
        DamageType.PowerShot1: 6,
        DamageType.PowerShot2: 10,
        DamageType.FinalBuster: 16,
        DamageType.Block: 4,
        DamageType.PowerBlock: 4,
        DamageType.AcidBarrier: 0,
        DamageType.AcidRain: 0,
        DamageType.AcidBuster: 8,
        DamageType.PowerAcidBarrier: 8,
        DamageType.PowerAcidRain: 6,
        DamageType.PowerAcidBuster: 10,
        DamageType.PileDash: 2,
        DamageType.PileBurst: 2,
        DamageType.PowerPileDash: 2,
        DamageType.PowerPileBurst: 2,
        DamageType.BounceBall: 2,
        DamageType.PowerBounceBall: 2,
        DamageType.ThunderShot: 2,
        DamageType.ThunderBulb: 2,
        DamageType.ThunderBurst: 4,
        DamageType.PowerThunderShot: 2,
        DamageType.PowerThunderBulb: 4,
        DamageType.PowerThunderBurst: 4,
        DamageType.TundraStorm: 8,
        DamageType.PowerTundraStorm: 8,
        DamageType.RisingTorch: 4,
        DamageType.TorchShot: 2,
        DamageType.PowerRisingTorch: 4,
        DamageType.PowerTorchShot: 2,
        DamageType.Blast1: 2,
        DamageType.Blast2: 4,
        DamageType.Blast3: 8,
        DamageType.Blast4: 12,
        DamageType.PowerBlast: 10,
    }),
    3: Boss("Bounce Man", {
        DamageType.BusterLv0: 2,
        DamageType.BusterLv1: 2,
        DamageType.BusterLv2: 6,
        DamageType.PowerShot1: 6,
        DamageType.PowerShot2: 10,
        DamageType.FinalBuster: 16,
        DamageType.Block: 4,
        DamageType.PowerBlock: 4,
        DamageType.AcidBarrier: 0,
        DamageType.AcidRain: 0,
        DamageType.AcidBuster: 2,
        DamageType.PowerAcidBarrier: 4,
        DamageType.PowerAcidRain: 2,
        DamageType.PowerAcidBuster: 4,
        DamageType.PileDash: 8,
        DamageType.PileBurst: 8,
        DamageType.PowerPileDash: 8,
        DamageType.PowerPileBurst: 12,
        DamageType.BounceBall: 2,
        DamageType.PowerBounceBall: 2,
        DamageType.ThunderShot: 2,
        DamageType.ThunderBulb: 2,
        DamageType.ThunderBurst: 2,
        DamageType.PowerThunderShot: 2,
        DamageType.PowerThunderBulb: 2,
        DamageType.PowerThunderBurst: 2,
        DamageType.TundraStorm: 8,
        DamageType.PowerTundraStorm: 8,
        DamageType.RisingTorch: 4,
        DamageType.TorchShot: 2,
        DamageType.PowerRisingTorch: 4,
        DamageType.PowerTorchShot: 2,
        DamageType.Blast1: 2,
        DamageType.Blast2: 4,
        DamageType.Blast3: 8,
        DamageType.Blast4: 12,
        DamageType.PowerBlast: 10,
    }),
    4: Boss("Fuse Man", {
        DamageType.BusterLv0: 2,
        DamageType.BusterLv1: 2,
        DamageType.BusterLv2: 6,
        DamageType.PowerShot1: 6,
        DamageType.PowerShot2: 10,
        DamageType.FinalBuster: 16,
        DamageType.Block: 4,
        DamageType.PowerBlock: 4,
        DamageType.AcidBarrier: 0,
        DamageType.AcidRain: 0,
        DamageType.AcidBuster: 2,
        DamageType.PowerAcidBarrier: 4,
        DamageType.PowerAcidRain: 2,
        DamageType.PowerAcidBuster: 4,
        DamageType.PileDash: 4,
        DamageType.PileBurst: 4,
        DamageType.PowerPileDash: 4,
        DamageType.PowerPileBurst: 6,
        DamageType.BounceBall: 8,
        DamageType.PowerBounceBall: 8,
        DamageType.ThunderShot: 2,
        DamageType.ThunderBulb: 2,
        DamageType.ThunderBurst: 2,
        DamageType.PowerThunderShot: 2,
        DamageType.PowerThunderBulb: 2,
        DamageType.PowerThunderBurst: 2,
        DamageType.TundraStorm: 2,
        DamageType.PowerTundraStorm: 2,
        DamageType.RisingTorch: 4,
        DamageType.TorchShot: 2,
        DamageType.PowerRisingTorch: 4,
        DamageType.PowerTorchShot: 2,
        DamageType.Blast1: 2,
        DamageType.Blast2: 4,
        DamageType.Blast3: 8,
        DamageType.Blast4: 12,
        DamageType.PowerBlast: 10,
    }),
    5: Boss("Tundra Man", {
        DamageType.BusterLv0: 2,
        DamageType.BusterLv1: 2,
        DamageType.BusterLv2: 6,
        DamageType.PowerShot1: 6,
        DamageType.PowerShot2: 10,
        DamageType.FinalBuster: 16,
        DamageType.Block: 4,
        DamageType.PowerBlock: 4,
        DamageType.AcidBarrier: 0,
        DamageType.AcidRain: 0,
        DamageType.AcidBuster: 2,
        DamageType.PowerAcidBarrier: 4,
        DamageType.PowerAcidRain: 2,
        DamageType.PowerAcidBuster: 4,
        DamageType.PileDash: 4,
        DamageType.PileBurst: 4,
        DamageType.PowerPileDash: 4,
        DamageType.PowerPileBurst: 6,
        DamageType.BounceBall: 2,
        DamageType.PowerBounceBall: 2,
        DamageType.ThunderShot: 8,
        DamageType.ThunderBulb: 8,
        DamageType.ThunderBurst: 8,
        DamageType.PowerThunderShot: 10,
        DamageType.PowerThunderBulb: 16,
        DamageType.PowerThunderBurst: 16,
        DamageType.TundraStorm: 2,
        DamageType.PowerTundraStorm: 2,
        DamageType.RisingTorch: 4,
        DamageType.TorchShot: 2,
        DamageType.PowerRisingTorch: 4,
        DamageType.PowerTorchShot: 2,
        DamageType.Blast1: 2,
        DamageType.Blast2: 4,
        DamageType.Blast3: 8,
        DamageType.Blast4: 12,
        DamageType.PowerBlast: 10,
    }),
    6: Boss("Torch Man", {
        DamageType.BusterLv0: 2,
        DamageType.BusterLv1: 2,
        DamageType.BusterLv2: 6,
        DamageType.PowerShot1: 6,
        DamageType.PowerShot2: 10,
        DamageType.FinalBuster: 16,
        DamageType.Block: 4,
        DamageType.PowerBlock: 4,
        DamageType.AcidBarrier: 0,
        DamageType.AcidRain: 0,
        DamageType.AcidBuster: 2,
        DamageType.PowerAcidBarrier: 4,
        DamageType.PowerAcidRain: 2,
        DamageType.PowerAcidBuster: 4,
        DamageType.PileDash: 4,
        DamageType.PileBurst: 4,
        DamageType.PowerPileDash: 4,
        DamageType.PowerPileBurst: 6,
        DamageType.BounceBall: 2,
        DamageType.PowerBounceBall: 2,
        DamageType.ThunderShot: 2,
        DamageType.ThunderBulb: 2,
        DamageType.ThunderBurst: 4,
        DamageType.PowerThunderShot: 2,
        DamageType.PowerThunderBulb: 4,
        DamageType.PowerThunderBurst: 4,
        DamageType.TundraStorm: 12,
        DamageType.PowerTundraStorm: 18,
        DamageType.RisingTorch: 2,
        DamageType.TorchShot: 2,
        DamageType.PowerRisingTorch: 2,
        DamageType.PowerTorchShot: 2,
        DamageType.Blast1: 2,
        DamageType.Blast2: 2,
        DamageType.Blast3: 2,
        DamageType.Blast4: 4,
        DamageType.PowerBlast: 4,
    }),
    7: Boss("Blast Man", {
        DamageType.BusterLv0: 2,
        DamageType.BusterLv1: 2,
        DamageType.BusterLv2: 6,
        DamageType.PowerShot1: 6,
        DamageType.PowerShot2: 10,
        DamageType.FinalBuster: 16,
        DamageType.Block: 2,
        DamageType.PowerBlock: 2,
        DamageType.AcidBarrier: 0,
        DamageType.AcidRain: 0,
        DamageType.AcidBuster: 2,
        DamageType.PowerAcidBarrier: 4,
        DamageType.PowerAcidRain: 2,
        DamageType.PowerAcidBuster: 4,
        DamageType.PileDash: 4,
        DamageType.PileBurst: 4,
        DamageType.PowerPileDash: 4,
        DamageType.PowerPileBurst: 6,
        DamageType.BounceBall: 2,
        DamageType.PowerBounceBall: 2,
        DamageType.ThunderShot: 2,
        DamageType.ThunderBulb: 2,
        DamageType.ThunderBurst: 4,
        DamageType.PowerThunderShot: 2,
        DamageType.PowerThunderBulb: 4,
        DamageType.PowerThunderBurst: 4,
        DamageType.TundraStorm: 8,
        DamageType.PowerTundraStorm: 8,
        DamageType.RisingTorch: 12,
        DamageType.TorchShot: 4,
        DamageType.PowerRisingTorch: 12,
        DamageType.PowerTorchShot: 8,
        DamageType.Blast1: 2,
        DamageType.Blast2: 4,
        DamageType.Blast3: 6,
        DamageType.Blast4: 8,
        DamageType.PowerBlast: 8,
    }),
    8: Boss("Yellow Devil MK-III", {
        DamageType.BusterLv0: 2,
        DamageType.BusterLv1: 2,
        DamageType.BusterLv2: 6,
        DamageType.PowerShot1: 6,
        DamageType.PowerShot2: 10,
        DamageType.FinalBuster: 16,
        DamageType.Block: 2,
        DamageType.PowerBlock: 2,
        DamageType.AcidBarrier: 0,
        DamageType.AcidRain: 0,
        DamageType.AcidBuster: 2,
        DamageType.PowerAcidBarrier: 2,
        DamageType.PowerAcidRain: 2,
        DamageType.PowerAcidBuster: 2,
        DamageType.PileDash: 4,
        DamageType.PileBurst: 2,
        DamageType.PowerPileDash: 8,
        DamageType.PowerPileBurst: 4,
        DamageType.BounceBall: 2,
        DamageType.PowerBounceBall: 2,
        DamageType.ThunderShot: 2,
        DamageType.ThunderBulb: 2,
        DamageType.ThunderBurst: 2,
        DamageType.PowerThunderShot: 2,
        DamageType.PowerThunderBulb: 2,
        DamageType.PowerThunderBurst: 2,
        DamageType.TundraStorm: 2,
        DamageType.PowerTundraStorm: 4,
        DamageType.RisingTorch: 2,
        DamageType.TorchShot: 2,
        DamageType.PowerRisingTorch: 4,
        DamageType.PowerTorchShot: 2,
        DamageType.Blast1: 2,
        DamageType.Blast2: 4,
        DamageType.Blast3: 8,
        DamageType.Blast4: 16,
        DamageType.PowerBlast: 12,
    }),
    9: Boss("Mawverne", {
        DamageType.BusterLv0: 2,
        DamageType.BusterLv1: 2,
        DamageType.BusterLv2: 4,
        DamageType.PowerShot1: 4,
        DamageType.PowerShot2: 8,
        DamageType.FinalBuster: 16,
        DamageType.Block: 2,
        DamageType.PowerBlock: 2,
        DamageType.AcidBarrier: 0,
        DamageType.AcidRain: 0,
        DamageType.AcidBuster: 2,
        DamageType.PowerAcidBarrier: 2,
        DamageType.PowerAcidRain: 2,
        DamageType.PowerAcidBuster: 2,
        DamageType.PileDash: 6,
        DamageType.PileBurst: 6,
        DamageType.PowerPileDash: 8,
        DamageType.PowerPileBurst: 8,
        DamageType.BounceBall: 6,
        DamageType.PowerBounceBall: 6,
        DamageType.ThunderShot: 2,
        DamageType.ThunderBulb: 2,
        DamageType.ThunderBurst: 2,
        DamageType.PowerThunderShot: 2,
        DamageType.PowerThunderBulb: 2,
        DamageType.PowerThunderBurst: 2,
        DamageType.TundraStorm: 2,
        DamageType.PowerTundraStorm: 4,
        DamageType.RisingTorch: 2,
        DamageType.TorchShot: 2,
        DamageType.PowerRisingTorch: 2,
        DamageType.PowerTorchShot: 2,
        DamageType.Blast1: 2,
        DamageType.Blast2: 4,
        DamageType.Blast3: 6,
        DamageType.Blast4: 8,
        DamageType.PowerBlast: 6,
    }),
    10: Boss("Wily Machine 11 V1", {
        DamageType.BusterLv0: 2,
        DamageType.BusterLv1: 2,
        DamageType.BusterLv2: 4,
        DamageType.PowerShot1: 4,
        DamageType.PowerShot2: 4,
        DamageType.FinalBuster: 14,
        DamageType.Block: 2,
        DamageType.PowerBlock: 2,
        DamageType.AcidBarrier: 0,
        DamageType.AcidRain: 0,
        DamageType.AcidBuster: 10,
        DamageType.PowerAcidBarrier: 16,
        DamageType.PowerAcidRain: 10,
        DamageType.PowerAcidBuster: 14,
        DamageType.PileDash: 4,
        DamageType.PileBurst: 4,
        DamageType.PowerPileDash: 8,
        DamageType.PowerPileBurst: 8,
        DamageType.BounceBall: 2,
        DamageType.PowerBounceBall: 2,
        DamageType.ThunderShot: 2,
        DamageType.ThunderBulb: 2,
        DamageType.ThunderBurst: 2,
        DamageType.PowerThunderShot: 2,
        DamageType.PowerThunderBulb: 2,
        DamageType.PowerThunderBurst: 2,
        DamageType.TundraStorm: 2,
        DamageType.PowerTundraStorm: 2,
        DamageType.RisingTorch: 2,
        DamageType.TorchShot: 2,
        DamageType.PowerRisingTorch: 2,
        DamageType.PowerTorchShot: 2,
        DamageType.Blast1: 4,
        DamageType.Blast2: 6,
        DamageType.Blast3: 8,
        DamageType.Blast4: 12,
        DamageType.PowerBlast: 10,
    }),
    11: Boss("Wily Machine 11 V2", {
        DamageType.BusterLv0: 2,
        DamageType.BusterLv1: 2,
        DamageType.BusterLv2: 4,
        DamageType.PowerShot1: 4,
        DamageType.PowerShot2: 4,
        DamageType.FinalBuster: 12,
        DamageType.Block: 2,
        DamageType.PowerBlock: 2,
        DamageType.AcidBarrier: 0,
        DamageType.AcidRain: 0,
        DamageType.AcidBuster: 6,
        DamageType.PowerAcidBarrier: 16,
        DamageType.PowerAcidRain: 10,
        DamageType.PowerAcidBuster: 10,
        DamageType.PileDash: 4,
        DamageType.PileBurst: 4,
        DamageType.PowerPileDash: 6,
        DamageType.PowerPileBurst: 6,
        DamageType.BounceBall: 2,
        DamageType.PowerBounceBall: 2,
        DamageType.ThunderShot: 6,
        DamageType.ThunderBulb: 4,
        DamageType.ThunderBurst: 4,
        DamageType.PowerThunderShot: 8,
        DamageType.PowerThunderBulb: 6,
        DamageType.PowerThunderBurst: 4,
        DamageType.TundraStorm: 2,
        DamageType.PowerTundraStorm: 2,
        DamageType.RisingTorch: 2,
        DamageType.TorchShot: 2,
        DamageType.PowerRisingTorch: 2,
        DamageType.PowerTorchShot: 2,
        DamageType.Blast1: 2,
        DamageType.Blast2: 4,
        DamageType.Blast3: 6,
        DamageType.Blast4: 8,
        DamageType.PowerBlast: 8,
    }),
}
