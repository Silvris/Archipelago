import asyncio

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.tabbedpanel import TabbedPanel

import Utils
import typing
from kvui import ContainerLayout, MainLayout, KivyJSONtoTextParser, ScrollBox, context_type, GameManager
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.boxlayout import BoxLayout

from CommonClient import CommonContext, server_loop, gui_enabled, get_base_parser


class DeathLinkApp(GameManager):
    base_title: str = "DeathLink MultiTool"

    def build(self):
        container = super().build()
        panel = TabbedPanel(text="DeathLink MultiTool")
        self.multitool = GridLayout()
        panel.content = self.multitool
        self.scrollbox = ScrollBox()
        self.multitool.add_widget(self.scrollbox)

        self.tabs.add_widget(panel)
        return container





class DeathLinkContext(CommonContext):
    game = ""
    tags = {"DeathLink", "TextOnly"}

    def run_gui(self):
        # reminder that gui can be swapped out as needed
        self.ui = DeathLinkApp(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def launch():
    async def main(args):
        ctx = DeathLinkContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="KH2 Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
