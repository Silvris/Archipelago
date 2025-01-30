from __future__ import annotations

from typing import List, Dict, Callable
from math import ceil

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

from Options import OptionSet

@dataclass
class MonsterRancher2DXArchipelagoOptions:
    monster_rancher_2_dx_unlocked_main_breeds: MonsterRancher2DXUnlockedMainBreeds
    monster_rancher_2_dx_unlocked_sub_breeds: MonsterRancher2DXUnlockedSubBreeds


class MonsterRancher2DXGame(Game):
    name = "Monster Rancher 2 DX"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PS1
    ]

    is_adult_only_or_unrated = False
    options_cls = MonsterRancher2DXArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return []

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [

        ]

    def unlocked_monster(self, monster: str) -> bool:
        default_mons = [
            "Ape",
            "Arrow Head",
            "ColorPandora",
            "Gaboo",
            "Jell",
            "Hare",
            "Hopper",
            "Kato",
            "Mocchi",
            "Monol",
            "Naga",
            "Pixie",
            "Plant",
            "Suezo",
            "Tiger",
            "Zuum",
        ]
        return (monster in default_mons or
                monster in self.archipelago_options.monster_rancher_2_dx_unlocked_main_breeds or
                monster in self.archipelago_options.monster_rancher_2_dx_unlocked_sub_breeds)

    def apes(self):
        apes = [
            "Ape",
            "Bossy",
            "Rock Ape",
            "Gibberer",
            "Tropical Ape",
            "Gold Dust",
        ]

        if self.unlocked_monster("King Ape"):
            apes.append("King Ape")

        return apes

    def arrowheads(self):
        arrowheads = [
            "Arrow Head",
            "Priarocks",
            "Renocraft",
            "MustardArrow",
            "Sumopion"
        ]

        if self.unlocked_monster("Durahan"):
            arrowheads.append("Plated Arrow")

        if self.unlocked_monster("Joker"):
            arrowheads.append("Selketo")

        if self.unlocked_monster("Mock"):
            arrowheads.append("Log Sawer")

        if self.unlocked_monster("Silver Face"):
            arrowheads.append("Silver Face")

        return arrowheads

    def bajarls(self):
        bajarls = [
            "Bajarl",
            "Boxer Bajarl",
            "Magic Bajarl",
            "Gym Bajarl",
            "Ultrarl",
        ]

        if self.unlocked_monster("Joker"):
            bajarls.append("Jaba")

        return bajarls

    def bakus(self):
        bakus = [
            "Baku",
            "Magmax",
            "Higante",
            "Gontar",
            "Giga Pint",
            "Nussie",
            "Icebergy",
            "Shishi",
            "Dango"
        ]

        if self.unlocked_monster("Durahan"):
            bakus.append("War Baku")

        if self.unlocked_monster("Joker"):
            bakus.append("Baku Clown")

        return bakus

    def beaclons(self):
        beaclons = [
            "Beaclon",
            "Bethelgeus",
            "Rocklon",
            "Melcarba",
            "Sloth Beetle",
            "Eggplantern"
        ]

        if self.unlocked_monster("Bajarl"):
            beaclons.append("KautRoarKaut")

        if self.unlocked_monster("Ducken"):
            beaclons.append("Ducklon")

        if self.unlocked_monster("Durahan"):
            beaclons.append("Centurion")

        if self.unlocked_monster("Joker"):
            beaclons.append("Jaggernaut")

        return beaclons

    def centaurs(self):
        centaurs = [
            "Centaur",
            "Antares",
            "Dragoon",
            "Trojan",
            "Ferious",
            "Celious",
            "Blue Thunder",
            "Trotter"
        ]

        if self.unlocked_monster("Bajarl"):
            centaurs.append("Bazoo")

        if self.unlocked_monster("Durahan"):
            centaurs.append("Chariot")

        if self.unlocked_monster("Joker"):
            centaurs.append("Reaper")

        if self.unlocked_monster("Sniper"):
            centaurs.append("Sniper")

        return centaurs

    def colorpandoras(self):
        colorpandoras = [
            "ColorPandora",
            "Liquid Cube",
            "PeachTreeBug",
            "Dice",
            "Tram"
        ]
        return colorpandoras

    def dragons(self):
        dragons = [
            "Dragon",
            "Crab Dragon",
            "Gariel",
            "Stone Dragon",
            "Tecno Dragon",
            "Oscerot",
            "Ragnaroks",
            "Tiamat",
            "Hound Dragon",
            "Moo"
        ]

        if self.unlocked_monster("Bajarl"):
            dragons.append("Dodongo")

        if self.unlocked_monster("Beaclon"):
            dragons.append("Corkasus")

        if self.unlocked_monster("Durahan"):
            dragons.append("Armor Dragon")

        if self.unlocked_monster("Joker"):
            dragons.append("Death Dragon")

        if self.unlocked_monster("Metalner"):
            dragons.append("Gidras")

        if self.unlocked_monster("Magma Heart"):
            dragons.append("Magma Heart")

        return dragons

    def duckens(self):
        duckens = [
            "Ducken",
            "Blocken",
            "Ticken",
            "Cawken",
            "Watermelony",
        ]
        return duckens

    def durahans(self):
        durahans = [
            "Durahan",
            "Lorica",
            "Vesuvius",
            "Kelmadics",
            "Leziena",
            "Hound Knight",
            "Kokushi Muso",
            "Ruby Knight",
            "Shogun",
        ]

        if self.unlocked_monster("Beaclon"):
            durahans.append("Hercules")

        if self.unlocked_monster("Joker"):
            durahans.append("Genocider")

        if self.unlocked_monster("Metalner"):
            durahans.append("Metal Glory")

        if self.unlocked_monster("Mock"):
            durahans.append("Wood Knight")

        if self.unlocked_monster("Phoenix"):
            durahans.append("Garuda")

        return durahans

    def gaboos(self):
        gaboos = [
            "Gaboo",
            "Jelly Gaboo",
            "Frozen Gaboo",
            "GabooSoldier",
            "Mad Gaboo",
        ]

        if self.unlocked_monster("Joker"):
            gaboos.append("Dokoo")

        return gaboos

    def galis(self):
        galis = [
            "Gali",
            "Stone Mask",
            "Furred Mask",
            "Aqua Mask",
            "Galirous",
            "Purple Mask",
            "Pink Mask",
            "Colorful",
            "Suezo Mask",
            "Fanged Mask",
            "Brown Mask",
            "Scaled Mask",
        ]

        return galis

    def ghosts(self):
        return ["Ghost", "Chef"]

    def golems(self):
        golems = [
            "Golem",
            "Dagon",
            "Tyrant",
            "Amenhotep",
            "Moaigon",
            "Gobi",
            "Poseidon",
            "Black Golem",
            "Marble Guy",
            "Pink Golem",
            "Ecologuardia",
            "Titan",
            "Big Blue",
            "Magna",
            "Scaled Golem",
            "Forward Golem",
            "Dream Golem",
        ]

        if self.unlocked_monster("Bajarl"):
            golems.append("Dao")

        if self.unlocked_monster("Baku"):
            golems.append("Sleepyhead")

        if self.unlocked_monster("Beaclon"):
            golems.append("Strong Horn")

        if self.unlocked_monster("Durahan"):
            golems.append("Battle Rocks")

        if self.unlocked_monster("Joker"):
            golems.append("Angolmor")

        if self.unlocked_monster("Metalner"):
            golems.append("Astro")

        if self.unlocked_monster("Mock"):
            golems.append("Wood Golem")

        if self.unlocked_monster("Wracky"):
            golems.append("Mariomax")

        if self.unlocked_monster("Zilla"):
            golems.append("Pressure")

        if self.unlocked_monster("Sand Golem"):
            golems.append("Sand Golem")

        return golems

    def hares(self):
        return [
            "Hare",
            "Prince Hare",
            "Rocky Fur",
            "Jelly Hare",
            "Evil Hare",
            "Purple Hare",
            "Fairy Hare",
            "Leaf Hare",
            "Four Eyed",
            "Blue Hare",
            "Wild Hare",
            "Scaled Hare",
            "Kung Fu Hare",
            "Tornado"
        ]

    def hengers(self):
        hengers = [
            "Henger",
            "Garlant",
            "Proto",
            "Gaia",
            "Black Henger",
            "Omega",
            "Skeleton",
        ]

        if self.unlocked_monster("Joker"):
            hengers.append("End Bringer")

        if self.unlocked_monster("Metalner"):
            hengers.append("Heuy")

        if self.unlocked_monster("Mock"):
            hengers.append("Automaton")

        return hengers

    def hoppers(self):
        hoppers = [
            "Hopper",
            "Draco Hopper",
            "Mustachios",
            "Pink Hopper",
            "Fairy Hopper",
            "Rear Eyed",
            "Skipper",
            "Frog Hopper",
        ]

        if self.unlocked_monster("Bajarl"):
            hoppers.append("Emerald Eye")

        if self.unlocked_monster("Jill"):
            hoppers.append("Snow Hopper")

        if self.unlocked_monster("Joker"):
            hoppers.append("Sneak Hopper")

        if self.unlocked_monster("Metalner"):
            hoppers.append("Springer")

        if self.unlocked_monster("Mock"):
            hoppers.append("Woody Hopper")

        if self.unlocked_monster("Bloody Eye"):
            hoppers.append("Bloody Eye")

        return hoppers

    def jells(self):
        return [
            "Jell",
            "Noble Jell",
            "Wall Mimic",
            "Muddy Jell",
            "Clay",
            "Purple Jell",
            "Pink Jam",
            "Chloro Jell",
            "Eye Jell",
            "Icy Jell",
            "Worm Jell",
            "Scaled Jell",
            "Metal Jell"
        ]

    def jills(self):
        jills = [
            "Jill",
            "Wondar",
            "Bengal",
            "Pong Pong",
            "Zorjil",
            "Pierry",
            "Pithecan"
        ]

        if self.unlocked_monster("Joker"):
            jills.append("Skull Capped")

        if self.unlocked_monster("Bighand"):
            jills.append("Bighand")

    def jokers(self):
        jokers = [
            "Joker",
            "Flare Death",
            "Tombstone",
            "Hell Heart",
            "Blue Terror",
            "Bloodshed",
        ]

        if self.unlocked_monster("Bajarl"):
            jokers.append("Odium")

        return jokers

    def katos(self):
        katos = [
            "Kato",
            "Draco Kato",
            "Gordish",
            "Pink Kato",
            "Citronie",
            "Blue Kato",
            "Ninja Kato",
            "Axer",
        ]

        if self.unlocked_monster("Joker"):
            katos.append("Tainted Cat")

        if self.unlocked_monster("Crescent"):
            katos.append("Crescent")

        return katos

    def metalners(self):
        return ["Metalner", "Love Seeker", "Metazorl", "Chinois"]

    def mews(self):
        return ["Mew", "Eared Mew", "Aqua Mew", "Mum Mew", "Bowwow", "Swimmer"]

    def mocchis(self):
        mocchis = [
            "Mocchi",
            "Draco Mocchi",
            "Gelatine",
            "Nyankoro",
            "Manna",
            "Fake Penguin",
            "Caloriena",
            "GentleMocchi",
            "Mocchini",
        ]

        if self.unlocked_monster("Durahan"):
            mocchis.append("KnightMocchi")

        if self.unlocked_monster("Joker"):
            mocchis.append("Hell Pierrot")

        if self.unlocked_monster("White Mocchi"):
            mocchis.append("White Mocchi")

        return mocchis

    def mocks(self):
        mocks = [
            "Mock",
            "Pole Mock",
            "White Birch",
        ]

        if self.unlocked_monster("Joker"):
            mocks.append("Ebony")

        return mocks

    def monols(self):
        monols = [
            "Monol",
            "Ivory Wall",
            "Obelisk",
            "Furred Wall",
            "Ice Candy",
            "Asphaultum",
            "Romper Wall",
            "New Leaf",
            "Sandy",
            "Blue Sponge",
            "Soboros",
            "Jura Wall",
            "Dominos",
            "Galaxy",
            "Scribble",
        ]

        if self.unlocked_monster("Burning Wall"):
            monols.append("Burning Wall")

    def nagas(self):
        nagas = [
            "Naga",
            "Bazula",
            "Trident",
            "Edgehog",
            "Aqua Cutter",
            "Crimson Eyed",
            "Ripper",
            "Jungler",
            "Cyclops",
            "Striker",
            "Earth Keeper",
            "Stinger",
            "Time Noise"
        ]

        if self.unlocked_monster("Punisher"):
            nagas.append("Punisher")

        return nagas

    def nitons(self):
        nitons = [
            "Niton",
            "Ammon",
            "Clear Shell",
            "Stripe Shell",
            "Disc Niton",
            "Dribbler",
            "Radial Niton",
        ]

        if self.unlocked_monster("Bajarl"):
            nitons.append("Alabia Niton")

        if self.unlocked_monster("Durahan"):
            nitons.append("Knight Niton")

        if self.unlocked_monster("Metalner"):
            nitons.append("Metal Shell")

        if self.unlocked_monster("Mock"):
            nitons.append("Baum Kuchen")

        return nitons

    def phoenixes(self):
        phoenixes = [
            "Phoenix",
            "Cinder Bird",
        ]

        if self.unlocked_monster("Blue Phoenix"):
            phoenixes.append("Blue Phoenix")

        return phoenixes

    def pixies(self):
        pixies = [
            "Pixie",
            "Daina",
            "Angel",
            "Granity",
            "Lepus",
            "Nagisa",
            "Kitten",
            "Silhouette",
            "Allure",
            "Serenity",
            "Vanity",
            "Mint",
            "Night Flyer",
            "Dixie",
            "Kasumi",
            "Mia",
            "Poison",
        ]

        if self.unlocked_monster("Bajarl"):
            pixies.append("Jinnee")

        if self.unlocked_monster("Centaur"):
            pixies.append("Unico")

        if self.unlocked_monster("Durahan"):
            pixies.append("Janne")

        if self.unlocked_monster("Jill"):
            pixies.append("Snowy")

        if self.unlocked_monster("Joker"):
            pixies.append("Lilim")

        if self.unlocked_monster("Metalner"):
            pixies.append("Futurity")

        if self.unlocked_monster("Mock"):
            pixies.append("Dryad")

        if self.unlocked_monster("Wracky"):
            pixies.append("Jilt")

        return pixies

    def plants(self):
        return [
            "Plant",
            "Gold Plant",
            "Rock Plant",
            "Hare Plant",
            "Mirage Plant",
            "Black Plant",
            "Weeds",
            "Queen Plant",
            "Usaba",
            "Blue Plant",
            "Fly Plant",
            "Scaled Plant"
        ]

    def suezos(self):
        suezos = [
            "Suezo",
            "Orion",
            "Rocky Suezo",
            "Furred Suezo",
            "Clear Suezo",
            "Red Eye",
            "Purple Suezo",
            "Pink Eye",
            "Green Suezo",
            "Horn",
            "Fly Eye",
            "Melon Suezo",
            "Birdie",
            "Bronze Suezo",
            "Silver Suezo",
            "Gold Suezo",
            # Sueki Suezo cannot be used here, Sueki lives for a single week
        ]

        if self.unlocked_monster("White Suezo"):
            suezos.append("White Suezo")

        return suezos

    def tigers(self):
        tigers = [
            "Tiger",
            "Balon",
            "Rock Hound",
            "Hare Hound",
            "Jelly Hound",
            "Terror Dog",
            "Cabalos",
            "Daton",
            "Tropical Dog",
            "Mono Eyed",
            "Jagd Hound",
            "Datonare",
            "White Hound"
        ]

        if self.unlocked_monster("Kamui"):
            tigers.append("Kamui")

    def undines(self):
        undines = ["Undine", "Mermaid"]

        if self.unlocked_monster("Joker"):
            undines.append("Siren")

        return undines

    def worms(self):
        return [
            "Worm",
            "Mask Worm",
            "Rock Worm",
            "Corone",
            "Jelly Worm",
            "Black Worm",
            "Purple Worm",
            "Red Worm",
            "Flower Worm",
            "Eye Worm",
            "Drill Tusk",
            "Scaled Worm",
            "Express Worm",
        ]

    def wrackys(self):
        wrackys = [
            "Wracky",
            "Draco Doll",
            "Pebbly",
            "Henger Doll",
            "Baby Doll",
            "Satan Clause",
            "Santy"
        ]

        if self.unlocked_monster("Bajarl"):
            wrackys.append("Bakky")

        if self.unlocked_monster("Durahan"):
            wrackys.append("Petit Knight")

        if self.unlocked_monster("Joker"):
            wrackys.append("Tricker")

        if self.unlocked_monster("Metalner"):
            wrackys.append("Metal Glay")

        if self.unlocked_monster("Mock"):
            wrackys.append("Mocky")

        return wrackys

    def zillas(self):
        zillas = [
            "Zilla",
            "Gigalon",
            "Pink Zilla",
            "Gooji",
            "Deluxe Liner"
        ]

        if self.unlocked_monster("Zilla King"):
            zillas.append("Zilla King")

        return zillas

    def zuums(self):
        zuums = [
            "Zuum",
            "Crab Saurian",
            "Hachiro",
            "Salamander",
            "NobleSaurian",
            "Rock Saurian",
            "Spot Saurian",
            "JellySaurian",
            "Tasman",
            "BlackSaurian",
            "Naga Saurian",
            "FairySaurian",
            "AlohaSaurian",
            "Mustardy",
            "HoundSaurian",
            "ShellSaurian",
            "ZebraSaurian",
        ]

        if self.unlocked_monster("Bajarl"):
            zuums.append("Sand Saurian")

        if self.unlocked_monster("Joker"):
            zuums.append("Basilisk")

        if self.unlocked_monster("Mock"):
            zuums.append("Wood Saurian")

        if self.unlocked_monster("Wild Saurian"):
            zuums.append("Wild Saurian")

        return zuums

    def monsters(self):
        monster_functions: Dict[str, Callable[[], List[str]]] = {
            "Ape": self.apes,
            "Arrow Head": self.arrowheads,
            "Bajarl": self.bajarls,
            "Baku": self.bakus,
            "Beaclon": self.beaclons,
            "Centaur": self.centaurs,
            "ColorPandora": self.colorpandoras,
            "Dragon": self.dragons,
            "Ducken": self.duckens,
            "Durahan": self.durahans,
            "Gaboo": self.gaboos,
            "Gali": self.galis,
            "Ghost": self.ghosts,
            "Golem": self.golems,
            "Hare": self.hares,
            "Henger": self.hengers,
            "Hopper": self.hoppers,
            "Jell": self.jells,
            "Jill": self.jills,
            "Joker": self.jokers,
            "Metalner": self.metalners,
            "Mew": self.mews,
            "Mocchi": self.mocchis,
            "Mock": self.mocks,
            "Monol": self.monols,
            "Naga": self.nagas,
            "Niton": self.nitons,
            "Phoenix": self.phoenixes,
            "Pixie": self.pixies,
            "Plant": self.plants,
            "Suezo": self.suezos,
            "Tiger": self.tigers,
            "Undine": self.undines,
            "Worm": self.worms,
            "Wracky": self.wrackys,
            "Zilla": self.zillas,
            "Zuum": self.zuums,
        }

        monsters = []
        for monster, function in monster_functions.items():
            if self.unlocked_monster(monster):
                monsters.extend(function())

        return monsters

    @staticmethod
    def sueki_tournaments():
        return [
            "New Year Cup",
            "Torles Tourney",
            "Blizzard Cup",
            "Parepare Cup (Spring)",
            "IMa Official Cup (E)",
            "IMa Official Cup (D)",
            "Spring Carnival (D)",
            "Blue Sky Cup",
            "Gemini Cup",
            "Freshmen's Cup",
            "Nageel Cup",
            "Desert Moon Cup",
            "Monster Pups' Cup",
            "Artemis Cup",
            "Rookie Cup",
            "Galoe Cup",
            "Maple Cup",
            "Parepare Cup (Winter)"
        ]

    @staticmethod
    def tournaments():
        return [
            # January
            "Sirius Cup",
            "Torble University Cup",
            "New Year Cup",
            # February
            "Greatest 4",
            "Poannka Cup",
            "Torles Tourney",
            "Kawrea Cup",
            "Blizzard Cup",
            "Durahan Invitational",
            # March
            "Parepare Cup (Spring)",
            "Troron Cup",
            # April
            "Spring Carnival (D)",
            "Phoenix Cup"
            "Spring Carnival (C)",
            "Legend Cup",
            "Spring Carnival (B)",
            # May
            "IMa Chairman Cup (Spring)",
            "M-1 Grand Prix",
            "Colart Cup",
            "Taurus Cup",
            "Blue Sky Cup",
            "Gemini Cup",
            # June
            "Freshmen's Cup",
            "Elder's Cup", # Might be issues with this one, can cause fun situations
            # July
            "Papas' Cup (Summer)",
            "Crab Cup",
            "Nageel Cup",
            "IMa - FIMBa Elimination Qualifier",
            # August
            "Torble Sea Cup",
            "Winner's Cup",
            "Dragon Invitational",
            "Desert Moon Cup",
            "Summer Carnival",
            "Monster Pups' Cup",
            "IMa - FIMBA Meet",
            # September
            "Telomeann Cup",
            "Manseitan Cup",
            "Artemis Cup",
            # October
            "Papas' Cup (Autumn)",
            "Kasseitan Cup",
            "Rookie Cup",
            "Hero's Cup",
            "Heel's Cup", # might also be problematic? nature is difficult to manip
            # November
            "World Monsters Cup",
            "Torble Port Cup",
            "Galoe Cup",
            "Mandy Cup",
            "Maple Cup",
            "IMa Chairman Cup (Autumn)",
            # December
            "Parepare Cup (Winter)",
            "Larox Cup",
            # IMa Official
            "IMa Official Cup (S)",
            "IMa Official Cup (A)",
            "IMa Official Cup (B)",
            "IMa Official Cup (C)",
            "IMa Official Cup (D)",
            "IMa Official Cup (E)",
        ]

    @staticmethod
    def expeditions():
        return ["Kawrea", "Torles Mountains", "Parepare"]

    # Techs!

    @staticmethod
    def ape_techs():
        return [
            "Sneeze",
            "Swing-Throw",
            "Blast",
            "Boomerang",
            "Grab-Throw",
            "Big Banana",
            "Roll Assault",
            "Bomb",
            "Big Bomb",
            "Tasty Banana"
        ]

    @staticmethod
    def arrowhead_techs():
        return [
            "Claw Pinch",
            "Bloodsuction",
            "Somersault",
            "Somersaults",
            "Sting Slash",
            "Long Punch",
            "Sting",
            "TripleStings",
            "Tail Swing",
            "Tail Swings",
            "Death Scythe",
            "Jumping Claw",
            "Aerial Claw",
            "Acrobatics",
            "Meteor",
            "Cyclone",
            "Hidden Sting",
            "Energy Shot",
            "Energy Shots",
            "Javelin",
            "Roll Assault",
            "Fist Missile",
        ]

    @staticmethod
    def bajarl_techs():
        return [
            "Hook",
            "1-2-Hook",
            "Straight",
            "Uppercut",
            "1-2-Uppercut",
            "1-2-Smash",
            "Magic Punch",
            "Mystic Combo",
            "Mystic Punch",
            "Magic Pot",
            "Mystic Pot",
            "Miracle Pot",
            "Bajarl Beam"
        ]

    @staticmethod
    def baku_techs():
        return [
            "Bite",
            "Two Bites",
            "Three Bites",
            "Tongue Slap",
            "Roar",
            "Two Roars",
            "MillionRoars",
            "Diving Press",
            "Sneeze",
            "Mating Song",
            "Gust Breath",
            "Hypnotism",
            "Nap"
        ]

    @staticmethod
    def beaclon_techs():
        return [
            "Heavy Punch",
            "MaximalPunch",
            "Horn Attack",
            "SpinningHorn",
            "Punch Combo",
            "Beaclon Combo",
            "Triple Stabs",
            "Dive Assault",
            "Spiral Dive",
            "Tremor",
            "Horn Combo",
            "Horn Smash",
            "Earthquake",
            "Top Assault",
            "Rolling Bomb",
            "Flying Press",
            "Horn Cannon",
            "Frantic Horn",
            "Fist Missile",
        ]

    @staticmethod
    def centaur_techs():
        return [
            "Stab Combo",
            "Triple Stabs",
            "Stab-Throw",
            "Z Slash",
            "Turn Stab",
            "Mind Flare",
            "Mind Blast",
            "Cross Slash",
            "Energy Shot",
            "Javelin",
            "Death Thrust",
            "Rush Slash",
            "Energy Shots",
            "Jump Javelin",
            "Meteor Drive",
        ]

    @staticmethod
    def colorpandora_techs():
        return [
            "Giant Whip",
            "Two Swings",
            "Kamikaze",
            "Vital Ritual",
            "Cracker",
            "Megacracker",
            "Triple Shots",
            "Delta Attack",
            "Shotgun",
            "Megashotgun",
            "Giant Wheel",
            "Spiral Rush",
            "Meteor Drive"
        ]

    @staticmethod
    def dragon_techs():
        return [
            "Tail Attack",
            "Two Bites",
            "Dragon Punch",
            "Wing Attack",
            "Wing Combo",
            "Claw Combo",
            "Claw",
            "Spinning Claw",
            "Flutter",
            "Flutters",
            "Trample",
            "Fire Breath",
            "Dragon Combo",
            "Inferno",
            "Glide Charge",
            "SlammingDown",
            "Flying Combo",
        ]

    @staticmethod
    def ducken_techs():
        return [
            "Explosion",
            "Ducken Dance",
            "Surprise",
            "Bound Charge",
            "Bound Stamp",
            "Bound",
            "Eye Beam",
            "Beam Shower",
            "Maximal Beam",
            "Bombing",
            "Boomerang",
            "Missile",
            "Two Missiles",
            "Big Missile",
            "Falling Beak",
            "Frantic Beam"
        ]

    @staticmethod
    def durahan_techs():
        return [
            
        ]

class MonsterRancher2DXUnlockedMainBreeds(OptionSet):
    """
    Indicates which unlockable main breeds can be rolled for objectives in Monster Rancher 2 DX
    """
    valid_keys = {
        "Baku",
        "Bajarl",
        "Beaclon",
        "Centaur",
        "Dragon",
        "Ducken",
        "Durahan",
        "Gali",
        "Ghost",
        "Golem",
        "Henger",
        "Jill",
        "Joker",
        "Metalner",
        "Mew",
        "Mock",
        "Niton",
        "Phoenix",
        "Undine",
        "Worm",
        "Wracky",
        "Zilla",
    }

    default = valid_keys


class MonsterRancher2DXUnlockedSubBreeds(OptionSet):
    """
    Indicates which unlockable sub breeds can be rolled for objectives in Monster Rancher 2 DX
    """
    valid_keys = {
        "White Mocchi",
        "White Suezo",
        "Bighand",
        "Kamui",
        "Crescent",
        "Sniper",
        "Sand Golem",
        "Burning Wall",
        "King Ape",
        "Wild Saurian",
        "Mad Clay",
        "Zilla King",
        "Silver Face",
        "Bloody Eye",
        "Blue Phoenix",
        "Punisher",
        "Magma Heart",
    }

    default = valid_keys