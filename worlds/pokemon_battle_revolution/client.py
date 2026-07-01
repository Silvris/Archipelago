import argparse
import asyncio
import dolphin_memory_engine
from CommonClient import CommonContext, ClientCommandProcessor, gui_enabled, get_base_parser, server_loop


BATTLE_REV_SAVE_FILE_PTR = 0x8045DE80
BATTLE_REV_SAVE_FILE_INDEX = BATTLE_REV_SAVE_FILE_PTR + 0x50
BATTLE_REV_SAVE_SIZE = 0x6FF00  # mult by current save index to find current player



class PBRContext(CommonContext):
    game = "Pokémon Battle Revolution"
    tags = {"AP"}
    items_handling = 0b111


async def game_watcher(ctx: PBRContext) -> None:
    pass


async def main(args: "argparse.Namespace") -> None:
    ctx = PBRContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()
    ctx.watcher_task = asyncio.create_task(game_watcher(ctx), name="GameWatcher")
    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch_pbr_client(*launch_args: str) -> None:
    import colorama
    import urllib.parse
    colorama.init()
    parser = get_base_parser()
    parser.add_argument("url", type=str, nargs="?", help="Archipelago Webhost uri to auto connect to.")
    args = parser.parse_args(launch_args)

    # handle if text client is launched using the "archipelago://name:pass@host:port" url from webhost
    if args.url:
        url = urllib.parse.urlparse(args.url)
        if url.scheme == "archipelago":
            if url.password:
                args.password = urllib.parse.unquote(url.password)
            if url.username:
                args.connect = f'{urllib.parse.unquote(url.username)}:None@{url.hostname}:{url.port}'
            else:
                args.connect = f'{url.hostname}:{url.port}'

        else:
            parser.error(f"bad url, found {args.url}, expected url in form of archipelago://archipelago.gg:38281")

    asyncio.run(main(args))
    colorama.deinit()