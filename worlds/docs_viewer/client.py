import pkgutil
import zipfile
import os
from collections import Counter
from io import BytesIO
from typing import Type

from kvui import (ThemedApp, ScrollBox, MainLayout, ContainerLayout, ApAsyncImage, MDScreenManager, MDScreen)
from kivy.lang.builder import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from Utils import init_logging

from worlds.AutoWorld import AutoWorldRegister, World, WebWorld


class WorldButton(MDButton):
    name: str = StringProperty("")
    path: str

    def __init__(self, name, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.path = path


class DocumentVisual(MDCard):
    name: str = StringProperty("")
    description: str = StringProperty("")
    authors: str = StringProperty("")
    language: str = StringProperty("")
    relative_path: str = StringProperty("")
    button: MDButton = ObjectProperty(None)
    multilang: bool = False

    def __init__(self, name, description, authors, language, relative_path, multilang,  *args, **kwargs):
        self.multilang = multilang
        super().__init__(*args, **kwargs)
        self.name = name
        self.description = description
        self.authors = authors
        self.language = language
        self.relative_path = relative_path
        self.button.bind(on_release=self.open_doc)


    def open_doc(self, button: MDButton):
        pass


class DocumentView(MDScreen):
    name = "DocumentView"


class DocumentSelect(MDScreen):
    name = "DocumentSelect"
    scroll: ScrollBox = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll.layout.spacing = 5

    def check_exists(self, world: Type[World], path: str) -> str | None:
        if not path.endswith(".md"):
            path += ".md"
        if world.zip_path:
            zf = zipfile.ZipFile(BytesIO(open(world.zip_path, 'rb').read()))
            docs = zipfile.Path(zf, f"{os.path.basename(world.zip_path).split('.')[0]}/docs/{path}")
            if docs.exists():
                return docs.name
            return None
        else:
            rel_path = f"/docs/{path}"
            if os.path.exists(f"{os.path.dirname(world.__file__)}{rel_path}"):
                return rel_path
            return None

    def populate(self, world: Type[World]):
        # first clear any already present
        self.scroll.layout.clear_widgets()
        # Make the game info
        web: WebWorld = getattr(world, "web", None)
        if web:
            for lang in web.game_info_languages:
                rel_path = self.check_exists(world, f"{lang}_{world.game}")
                if rel_path:
                    self.scroll.layout.add_widget(DocumentVisual(f"{world.game} Info",
                                                                 f"Game info for {world.game} "
                                                                 f"for language {lang.upper()}.","",
                                                                 lang.upper(), rel_path, True))
            lang_count = Counter([tutorial.tutorial_name for tutorial in web.tutorials])
            for tutorial in web.tutorials:
                path = self.check_exists(world, tutorial.file_name)
                if path:
                    self.scroll.layout.add_widget(DocumentVisual(tutorial.tutorial_name, tutorial.description,
                                                                 ", ".join(tutorial.authors), tutorial.language, path,
                                                                 lang_count[tutorial.tutorial_name] > 1))

        else:
            self.scroll.layout.add_widget(MDLabel("No documents could be found for this game."))


class DocsViewer(ThemedApp):
    base_title: str = "Archipelago Docs Viewer"
    container: ContainerLayout
    main: MainLayout
    scrollbox: ScrollBox
    visual: MainLayout
    screen_manager: MDScreenManager
    doc_select: DocumentSelect
    doc_view: DocumentView

    def add_world_button(self, world: Type[World], path: str):
        button = WorldButton(world.game, path)
        self.scrollbox.layout.add_widget(button)
        button.bind(on_release=lambda x: self.show_world_docs(world))

    def show_world_docs(self, world: Type[World]):
        self.screen_manager.current = self.doc_select.name
        self.doc_select.populate(world)

    def build(self):
        self.set_colors()
        self.container = Builder.load_string(pkgutil.get_data(__name__, "docs.kv").decode("utf-8"))
        self.main = self.container.main
        self.scrollbox = self.container.scrollbox
        self.visual = self.container.visual
        self.screen_manager = self.container.screen_manager
        self.doc_select = DocumentSelect()
        self.doc_view = DocumentView()
        self.screen_manager.add_widget(self.doc_select)
        self.screen_manager.add_widget(self.doc_view)

        for name, world in AutoWorldRegister.world_types.items():
            if world.zip_path:
                zf = zipfile.ZipFile(BytesIO(open(world.zip_path, 'rb').read()))
                docs = zipfile.Path(zf, f"{os.path.basename(world.zip_path).split('.')[0]}/docs/")
                if docs.exists() and docs.is_dir():
                    self.add_world_button(world, str(world.zip_path))
            else:
                if os.path.exists(os.path.join(os.path.dirname(world.__file__), "docs")):
                    self.add_world_button(world, os.path.dirname(world.__file__))

        # Uncomment to re-enable the Kivy console/live editor
        # Ctrl-E to enable it, make sure numlock/capslock is disabled
        from kivy.modules.console import create_console
        create_console(Window, self.container)

        return self.container


def launch():
    DocsViewer().run()


if __name__ == "__main__":
    init_logging("DocsViewer")
    launch()
