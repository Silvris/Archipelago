import os.path
import Utils
from kvui import ScrollBox
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
        menu_button = MDActionTopAppBarButton(icon="menu", theme_text_color="Custom",
                                              text_color=self.theme_cls.onPrimaryColor)
        self.appbar = MDTopAppBar(
            MDTopAppBarLeadingButtonContainer(
                menu_button
            ),
            MDTopAppBarTitle(text="Select Player YAML Options", pos_hint={"center_x": 0.5},
                             theme_text_color="Custom", text_color=self.theme_cls.onPrimaryColor),
            pos_hint={"center_y": 0.95, "center_x": 0.5},
            theme_bg_color="Custom",
            md_bg_color=self.theme_cls.primaryColor
        )
        self.layout.add_widget(self.appbar)
        self.add_widget(self.layout)


class GenerateGUI(MDApp):
    screen_manager: MDScreenManager
    yaml_selection: MDScreen
    title = "Archipelago Generate"

    def build(self):
        from kvui import KivyJSONtoTextParser
        text_colors = KivyJSONtoTextParser.TextColors()
        self.theme_cls.theme_style = getattr(text_colors, "theme_style", "Dark")
        self.theme_cls.primary_palette = getattr(text_colors, "primary_palette", "Green")
        self.yaml_selection = YamlSelectScreen(name="yaml_select")
        navigation_layout = MDNavigationLayout()
        self.naviation_drawer = MDNavigationDrawer(

        )
        self.screen_manager = MDScreenManager()

        self.screen_manager.add_widget(self.yaml_selection)
        self.screen_manager.md_bg_color = self.theme_cls.backgroundColor
        return self.screen_manager


if __name__ == "__main__":
    GenerateGUI().run()
