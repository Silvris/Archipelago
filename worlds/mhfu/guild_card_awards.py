import typing
from .data.monsters import monster_ids, elder_dragons
from .quests import get_quest_by_id, get_area_quests, location_name_to_id, MHFURegion, MHFULocation, hub_rank_max
from .options import VillageQuestDepth, GuildQuestDepth, Awards
from .rules import can_reach_rank, can_hunt_all_monsters, can_complete_all_quests, can_complete_any_quest

from worlds.generic.Rules import add_rule

if typing.TYPE_CHECKING:
    from . import MHFUWorld, hub_rank_max
    from .rules import MHFULogicMixin

award_start = max(location_name_to_id.values())

all_monsters = list(monster_ids.keys())
crowns = sorted(set(all_monsters) - {"Fatalis", "Crimson Fatalis", "White Fatalis", "Lao-Shan Lung", "Shen Gaoren",
                                     "Ashen Lao-Shan Lung", "Akantor", "Ukanlos", "Yama Tsukami"})
capturable = sorted(set(all_monsters).difference(elder_dragons.keys()))
subspecies = [
    "Pink Rathian",
    "Blue Yian Kut-Ku",
    "Purple Gypceros",
    "Silver Rathalos",
    "Gold Rathian",
    "Black Diablos",
    "White Monoblos",
    "Red Khezu",
    "Green Plesioth",
    "Black Gravios",
    "Azure Rathalos",
    "Ashen Lao-Shan Lung",
    "Copper Blangonga",
    "Emerald Congalala",
    "Plum Daimyo Hermitaur",
    "Terra Shogun Ceanataur",
]

class GuildCardAward(typing.NamedTuple):
    id: int
    village: int = 0
    guild: int = 0
    training: bool = False
    treasure: bool = False
    monster: list[str] | None = None
    area: list[int] | None = None
    grindy: bool = False

guild_card_awards: dict[str, GuildCardAward] = {
    "Village Chief's Glove": GuildCardAward(award_start + 1, village=1),
    "Village Chief's Hat": GuildCardAward(award_start + 2, village=1),
    "Village Chief's Scarf": GuildCardAward(award_start + 3, village=1),
    "Village Chief's Coat": GuildCardAward(award_start + 4, village=1),
    "Mane Necklace": GuildCardAward(award_start + 5, monster=["Kirin"]),
    "Blood Onyx": GuildCardAward(award_start + 6, monster=["Akantor"]),
    "King's Crown": GuildCardAward(award_start + 7, monster=crowns, grindy=True),
    "Miniature Crown": GuildCardAward(award_start + 8, monster=crowns, grindy=True),
    "Bronze Medal": GuildCardAward(award_start + 9, guild=1),
    "Silver Medal": GuildCardAward(award_start + 10, guild=1),
    "Gold Medal": GuildCardAward(award_start + 11, guild=2),
    "Black Belt Badge": GuildCardAward(award_start + 12, guild=2, training=True),
    "Expert Badge": GuildCardAward(award_start + 13, guild=2, training=True),
    "Legend Badge": GuildCardAward(award_start + 14, guild=2, training=True),
    "Rare Species Report": GuildCardAward(award_start + 15, monster=subspecies),
    "Ecology Research Report": GuildCardAward(award_start + 16, monster=capturable),
    "Azure Stone": GuildCardAward(award_start + 17, village=1, guild=2, grindy=True),
    "Great Hornfly": GuildCardAward(award_start + 18, village=1, guild=2, grindy=True),
    "Springnight Carp": GuildCardAward(award_start + 19, village=1, grindy=True),
    "Dosbiscus": GuildCardAward(award_start + 20),
    "Grateful Letter": GuildCardAward(award_start + 21, guild=2, grindy=True),
    "Sage's Bracelet": GuildCardAward(award_start + 22, monster=["Crimson Fatalis"], grindy=True), # ???????????? trusting JP guide here
    "Wyverian Artisan's Hammer": GuildCardAward(award_start + 23, grindy=True),
    "Hunter's Progress": GuildCardAward(award_start + 24, area=[11, 20, 21, 6, 17, 3, 4, 18, 5, 19, 2, 16, 13, 15, 14], grindy=True),
    "Nekoht's Whiskers": GuildCardAward(award_start + 25, village=2),
    "Nekoht's Bell": GuildCardAward(award_start + 26, village=2),
    "Nekoht's Coat": GuildCardAward(award_start + 27, village=2),
    "Pokke Village Gourd": GuildCardAward(award_start + 28, village=2),
    "Orichalcum Shield": GuildCardAward(award_start + 29, guild=3),
    "Platinum Shield": GuildCardAward(award_start + 30, guild=3),
    "Gold Shield": GuildCardAward(award_start + 31, guild=3),
    "Supreme Hunter's Crest": GuildCardAward(award_start + 32, guild=3, village=2, grindy=True),
    "Igneous Ring": GuildCardAward(award_start + 33, monster=["Fatalis"]),
    "Ring of Fire": GuildCardAward(award_start + 34, monster=["Crimson Fatalis"]),
    "Powder-White Crown": GuildCardAward(award_start + 35, monster=["White Fatalis"]),
    "Golden Snowshoes": GuildCardAward(award_start + 36, monster=["Furious Rajang"]),
    "Ukanlos Bead": GuildCardAward(award_start + 37, monster=["Ukanlos"]),
    "Epic Hunts Armband": GuildCardAward(award_start + 38, guild=3, village=2),
    "Warrior's Medal": GuildCardAward(award_start + 39, guild=3, training=True),
    "Guardian's Award": GuildCardAward(award_start + 40, area=[1, 12], grindy=True),
    "Flower Bouquet from the Guild": GuildCardAward(award_start + 41, guild=3, grindy=True),
    "Adventurer's Helm": GuildCardAward(award_start + 42, guild=3, treasure=True),
    "Trenya's Flag": GuildCardAward(award_start + 43, guild=3, grindy=True),
    "The Ultimate Catnip": GuildCardAward(award_start + 44, guild=3, grindy=True),
    "Letter to my Fearless Leader": GuildCardAward(award_start + 45, guild=3, grindy=True), # not really but its very time consuming
    "Member's Card": GuildCardAward(award_start + 46, guild=3),
    "Wyverian Artisan's Mitten": GuildCardAward(award_start + 47, guild=3, grindy=True),
    "Hunter's Miracle": GuildCardAward(award_start + 48, area=[26, 27, 28, 29, 30, 31]),
}

def create_awards(world: "MHFUWorld"):
    menu = world.get_region(world.origin_region_name)
    guild_card = MHFURegion("Guild Card", world.player, world.multiworld, "a great achievement")
    menu.connect(guild_card)
    world.multiworld.regions.append(guild_card)
    monster_set = set()
    area_set = set()
    for location in world.get_locations():
        if location.monsters:
            monster_set.update(location.monsters)
        if location.qid:
            quest_info = get_quest_by_id(f"m{location.qid:05}")
            area_set.add(quest_info.stage)
    for name, award in guild_card_awards.items():
        # quickly just run through our checks
        if award.grindy and world.options.guild_card_awards.value < Awards.option_on:
            continue
        if award.guild > world.options.guild_depth.value:
            continue
        if award.village > world.options.village_depth.value:
            continue
        if award.training and not world.options.training_quests:
            continue
        if award.treasure and not world.options.treasure_quests:
            continue
        if award.monster and not monster_set.issuperset(award.monster):
            continue
        if award.area and not area_set.issuperset(award.area):
            continue
        # pass all of these? its a valid location
        guild_card.add_locations({name: award.id}, MHFULocation)
        loc = world.get_location(name)
        # now set the rule as given
        # for ranks, assume that the max rank is required for this
        if award.village:
            add_rule(loc, lambda state, rank=award.village: can_reach_rank(state, world.player, 1, rank - 1, hub_rank_max[1, rank - 1] - 1))
        if award.guild:
            add_rule(loc, lambda state, rank=award.guild: can_reach_rank(state, world.player, 0, rank, hub_rank_max[0, rank] - 1))
        if award.monster:
            add_rule(loc, lambda state, mons=tuple(award.monster): can_hunt_all_monsters(state, mons, world.player))
        if award.area:
            for area in award.area:
                quests = [q.qid for q in get_area_quests(world.rank_requirements.keys(), (area,))]
                add_rule(loc, lambda state, qids=tuple(quests): can_complete_any_quest(state, qids, world.player))