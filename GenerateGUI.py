import logging
import os
import os.path
import traceback

import Utils
import typing
import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from Generate import main as GenerateMain
from Main import main as ERmain

from kvui import ScrollBox
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon, MDIconButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.appbar import MDTopAppBar, MDTopAppBarLeadingButtonContainer, MDActionTopAppBarButton, MDTopAppBarTitle
from kivymd.uix.navigationdrawer import (MDNavigationLayout, MDNavigationDrawer, MDNavigationDrawerItem,
                                         MDNavigationDrawerItemText, MDNavigationDrawerItemLeadingIcon,
                                         MDNavigationDrawerLabel, MDNavigationDrawerMenu, MDNavigationDrawerDivider)
from kivymd.uix.textfield import MDTextField


class YamlLabel(MDGridLayout):
    path: str
    name: str

    def __init__(self, *args, **kwargs):
        if "text" in kwargs:
            text = kwargs.pop("text")
        else:
            text = ""
        super().__init__(*args, **kwargs)
        self.md_bg_color = self.theme_cls.surfaceDimColor
        self.cols = 2
        self.size_hint_y = None
        self.height = dp(40)
        self.path = text
        self.name = os.path.basename(text)
        label = MDLabel(text=self.name, valign="top")
        self.add_widget(label)
        label.height = label.texture_size[1]

        def remove_self(button):
            self.parent.remove_widget(self)

        remove_button = MDIconButton(icon="minus", size_hint_x=None, width=dp(25))
        remove_button.bind(on_release=remove_self)
        self.add_widget(remove_button)


class YamlSelectScreen(MDScreen):
    file_manager: MDFileManager
    layout: MDRelativeLayout
    yaml_view: ScrollBox

    def add_yaml(self, yaml_path):
        print(yaml_path)
        self.yaml_view.layout.add_widget(YamlLabel(text=yaml_path))
        self.file_manager.close()

    def exit_manager(self, *args):
        self.file_manager.close()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_manager = MDFileManager(exit_manager=self.exit_manager, select_path=self.add_yaml, selector="file")
        self.layout = MDRelativeLayout()
        self.yaml_card = MDCard(style="filled", pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(0.8, 0.8))
        self.yaml_view = ScrollBox()
        self.yaml_view.scroll_type = ["content", "bars"]
        self.yaml_view.layout.orientation = "vertical"
        self.yaml_view.layout.spacing = dp(5)
        self.yaml_card.add_widget(self.yaml_view)
        self.layout.add_widget(self.yaml_card)

        def show_filemanager(button):
            path = Utils.local_path("players")
            self.file_manager.show(path)

        add_button = MDIconButton(icon="plus", style="filled", pos_hint={"center_x": 0.95, "center_y": 0.05},
                                  theme_text_color="Custom", text_color=self.theme_cls.onPrimaryColor)
        add_button.bind(on_release=show_filemanager)
        self.layout.add_widget(add_button)
        self.appbar = MDTopAppBar(
            MDTopAppBarLeadingButtonContainer(
                MDActionTopAppBarButton(icon="menu", theme_text_color="Custom",
                                        text_color=self.theme_cls.onPrimaryColor,
                                        on_release=MDApp.get_running_app().show_menu)
            ),
            MDTopAppBarTitle(text="Select Player YAML Options", pos_hint={"center_x": 0.5},
                             theme_text_color="Custom", text_color=self.theme_cls.onPrimaryColor),
            pos_hint={"center_y": 0.95, "center_x": 0.5},
            theme_bg_color="Custom",
            md_bg_color=self.theme_cls.primaryColor
        )
        self.layout.add_widget(self.appbar)
        self.add_widget(self.layout)


class TextInputHandler(logging.Handler):
    buffer: list[str]

    def emit(self, data: logging.LogRecord):
        self.buffer.append(data.message)
        self.flush()

    def flush(self):
        pass

    def __init__(self):
        super().__init__()
        self.buffer = []


class GenerateScreen(MDScreen):
    layout: MDRelativeLayout
    generate_log: MDTextField
    channel: TextInputHandler
    generate_task: asyncio.Task

    def async_gen(self):
        erargs, seed = GenerateMain(log_channel=self.channel)
        multiworld = ERmain(erargs, seed)

    def generate(self):
        import threading
        self.generate_log.text = ""
        self.channel.buffer.clear()
        threading.Thread(target=self.async_gen, name="GenerateMain").start()
        self.logger.removeHandler(self.channel)

    def update_log(self, _):
        self.generate_log.set_text(self.generate_log, self.generate_log.text + "\n".join(self.channel.buffer))
        self.channel.buffer.clear()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processes = []
        self.layout = MDRelativeLayout()
        generate_layout = MDGridLayout(spacing=20, cols=1,
                                       pos_hint={"center_x": 0.5, "center_y": 0.1}, size_hint=(0.5, 0.75))
        self.generate_log = MDTextField(multiline=True, readonly=True, size_hint=(0.5, 0.9),
                                        max_height=dp(200), mode="filled")
        generate_button = MDButton(
            MDButtonIcon(icon="check-underline"),
            MDButtonText(text="Generate"),
            on_release=lambda x: self.generate(),

        )
        generate_layout.add_widget(generate_button)
        generate_layout.add_widget(self.generate_log)
        self.layout.add_widget(generate_layout)
        self.appbar = MDTopAppBar(
            MDTopAppBarLeadingButtonContainer(
                MDActionTopAppBarButton(icon="menu", theme_text_color="Custom",
                                        text_color=self.theme_cls.onPrimaryColor,
                                        on_release=MDApp.get_running_app().show_menu)
            ),
            MDTopAppBarTitle(text="Generate Seed", pos_hint={"center_x": 0.5},
                             theme_text_color="Custom", text_color=self.theme_cls.onPrimaryColor),
            pos_hint={"center_y": 0.95, "center_x": 0.5},
            theme_bg_color="Custom",
            md_bg_color=self.theme_cls.primaryColor
        )
        self.layout.add_widget(self.appbar)
        self.add_widget(self.layout)

        self.channel = TextInputHandler()
        self.channel.setLevel(logging.INFO)
        self.logger = logging.getLogger()

        Clock.schedule_interval(self.update_log, 0.5)

class GenerateGUI(MDApp):
    layout: MDRelativeLayout
    screen_manager: MDScreenManager
    yaml_selection: MDScreen
    generate_menu: MDScreen
    title = "Archipelago Generate"
    navigation_drawer: MDNavigationDrawer

    def show_menu(self, _):
        self.navigation_drawer.set_state("toggle")

    def change_screen(self, screen_name: str):
        self.screen_manager.current = screen_name
        self.navigation_drawer.set_state("closed")

    def build(self):
        from kvui import KivyJSONtoTextParser
        text_colors = KivyJSONtoTextParser.TextColors()
        self.theme_cls.theme_style = getattr(text_colors, "theme_style", "Dark")
        self.theme_cls.primary_palette = getattr(text_colors, "primary_palette", "Green")
        self.yaml_selection = YamlSelectScreen(name="yaml_select")
        self.generate_menu = GenerateScreen(name="generate")
        navigation_layout = MDNavigationLayout()
        self.navigation_drawer = MDNavigationDrawer(
            MDNavigationDrawerMenu(
                MDNavigationDrawerLabel(text="Archipelago Generate"),
                MDNavigationDrawerItem(
                    MDNavigationDrawerItemLeadingIcon(icon="note-edit"),
                    MDNavigationDrawerItemText(text="Edit Host Settings")
                ),
                MDNavigationDrawerItem(
                    MDNavigationDrawerItemLeadingIcon(icon="list-box"),
                    MDNavigationDrawerItemText(text="Select Player YAMLs"),
                    on_release=lambda _: self.change_screen("yaml_select")
                ),
                MDNavigationDrawerItem(
                    MDNavigationDrawerItemLeadingIcon(icon="plus"),
                    MDNavigationDrawerItemText(text="Generate"),
                    on_release=lambda _: self.change_screen("generate")
                ),
                MDNavigationDrawerDivider()
            ),
            drawer_type="modal"
        )
        self.screen_manager = MDScreenManager()

        self.screen_manager.add_widget(self.yaml_selection)
        self.screen_manager.add_widget(self.generate_menu)
        self.screen_manager.md_bg_color = self.theme_cls.backgroundColor
        navigation_layout.add_widget(self.screen_manager)
        navigation_layout.add_widget(self.navigation_drawer)
        return navigation_layout


async def main():
    await GenerateGUI().async_run()

if __name__ == "__main__":
    asyncio.run(main())
