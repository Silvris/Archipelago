from typing import TYPE_CHECKING
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class PokemonBW2Client(BizHawkClient):
    game = "Pokemon Black 2 and White 2"
    system = "DS"
    patch_suffix = (".apblack2", ".apwhite2")

    def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        return False

    def set_auth(self, ctx: "BizHawkClientContext") -> None:
        pass

    def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        pass