import os
import base64
import threading
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Item, ItemClassification, MultiWorld, Tutorial, CollectionState
from Options import OptionError
from settings import Group, UserFilePath
from typing import Any, ClassVar

from .client import PinballRSClient
from .items import PinballRSItem, ALL_ITEMS, item_lookup, MAIN_ITEMS, AREA_ITEMS, FILLER_ITEM_WEIGHTS, EVOLUTION_ITEMS
from .names import RUBY_BOARD, SAPPHIRE_BOARD, AREAS, EVO_ARROW, EVO_MODE
from .options import PokemonPinballRSOptions, StartingBoard, EvoMode
from .regions import create_regions, location_lookup
from .rom import PinballRSProcedurePatch, patch_rom, PINBALLRSHASH
from .rules import set_rules


class PokemonPinballRSSettings(Group):
    class RomFile(UserFilePath):
        """File name of the Pokemon Pinball RS EN rom"""
        description = "Pokemon Pinball Ruby & Sapphire ROM File"
        copy_to: str | None = "Pokemon Pinball RS.gba"
        md5s = [PINBALLRSHASH]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class PokemonPinballRSWebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [

        Tutorial(
           "Multiworld Setup Guide",
           "A guide to setting up the Pokemon Pinball Ruby & Sapphire randomizer connected to an Archipelago Multiworld.",
           "English",
           "setup_en.md",
           "setup/en",
           ["Silvris"]
        )
    ]


class PokemonPinballRSWorld(World):
    """
    Pokémon Pinball Ruby & Sapphire combines traditional fast pinball gameplay with a Pokémon twist! Catch over 200
    Pokémon across two separate boards and aim for a high score!
    """

    game = "Pokemon Pinball Ruby & Sapphire"
    web = PokemonPinballRSWebWorld()
    settings: ClassVar[PokemonPinballRSSettings]
    options_dataclass = PokemonPinballRSOptions
    options: PokemonPinballRSOptions
    item_name_to_id = item_lookup
    location_name_to_id = location_lookup
    possible_mons: set[int]
    rom_name: bytearray

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.possible_mons = set()
        self.rom_name = bytearray()
        self.rom_name_available_event = threading.Event()

    create_regions = create_regions

    def create_item(self, name: str) -> "Item":
        data = ALL_ITEMS.get(name, None)
        if data is None:
            raise OptionError(f"{name} is not a valid item for Pokemon Pinball Ruby & Sapphire")
        return PinballRSItem(name, data.classification, data.idx, self.player)

    def create_items(self) -> None:
        itempool = [self.create_item(name) for name, data in MAIN_ITEMS.items() for _ in range(data.num)
                    if name not in (RUBY_BOARD, SAPPHIRE_BOARD, EVO_ARROW, EVO_MODE) and
                    data.board == 0 or
                    (not self.options.single_board or data.board == (self.options.starting_board.value + 1))]
        if self.options.starting_board == StartingBoard.option_ruby:
            board_name = RUBY_BOARD
            other_board = SAPPHIRE_BOARD
        else:
            board_name = SAPPHIRE_BOARD
            other_board = RUBY_BOARD
        self.push_precollected(self.create_item(board_name))
        if not self.options.single_board:
            itempool.append(self.create_item(other_board))

        # evo
        if self.options.evo_mode == EvoMode.option_arrows:
            itempool.extend([self.create_item(EVO_ARROW) for _ in range(3)])
        elif self.options.evo_mode == EvoMode.option_full:
            itempool.append(self.create_item(EVO_MODE))
        else:
            self.push_precollected(self.create_item(EVO_MODE))
        itempool.extend([self.create_item(name) for name, data in EVOLUTION_ITEMS.items()])

        # handle areas
        ruby_start = self.random.randint(0, 5)
        sapphire_start = self.random.randint(7, 12)
        for area, data in AREA_ITEMS.items():
            if (data.idx & 0xFF < 7 and self.options.single_board
                    and self.options.starting_board == StartingBoard.option_sapphire):
                continue
            elif (data.idx & 0xFF >= 7 and self.options.single_board
                  and self.options.starting_board == StartingBoard.option_ruby):
                continue
            if area in (AREAS[ruby_start], AREAS[sapphire_start]):
                self.push_precollected(self.create_item(area))
            else:
                itempool.append(self.create_item(area))

        unfilled = len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool)
        itempool += [self.create_item(filler)
                     for filler in self.random.choices(
                list(FILLER_ITEM_WEIGHTS.keys()), weights=list(FILLER_ITEM_WEIGHTS.values()), k=unfilled)]

        self.multiworld.itempool += itempool

    set_rules = set_rules

    def collect(self, state: CollectionState, item: "Item") -> bool:
        changed = super().collect(state, item)
        if changed and item.name == EVO_MODE:
            state.prog_items[self.player][EVO_ARROW] += 3

        return changed

    def remove(self, state: CollectionState, item: "Item") -> bool:
        changed = super().remove(state, item)

        if changed and item.name == EVO_MODE:
            state.prog_items[self.player][EVO_ARROW] -= 3
            if state.prog_items[self.player][EVO_ARROW] <= 0:
                del state.prog_items[self.player][EVO_ARROW]

        return changed

    def generate_output(self, output_directory: str) -> None:
        try:
            patch = PinballRSProcedurePatch(player=self.player, player_name=self.player_name)
            patch_rom(self, patch)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def modify_multidata(self, multidata: dict[str, Any]) -> None:
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.player_name]