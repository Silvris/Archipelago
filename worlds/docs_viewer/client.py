import pkgutil

from kvui import (ThemedApp, ScrollBox, MainLayout, ContainerLayout, ApAsyncImage, MDScreenManager, MDScreen)
from kivy.lang.builder import Builder
from Utils import init_logging

class DocumentView(MDScreen):
    pass


class DocumentSelect(MDScreen):
    pass


class DocsViewer(ThemedApp):
    base_title: str = "Archipelago Docs Viewer"
    container: ContainerLayout
    main: MainLayout

    def build(self):
        self.set_colors()
        self.container = Builder.load_string(pkgutil.get_data(__name__, "docs.kv").decode("utf-8"))


def launch():
    DocsViewer().run()


if __name__ == "__main__":
    init_logging("DocsViewer")
    launch()
