import flet as ft

from components.responsive import Responsive


class ModeratorApp(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.mod_page = page
        self.r = Responsive(page)
        self.Title = ft.Text("MODERATOR PAGE")
        self.expand = True
        self.scroll = ft.ScrollMode.HIDDEN
        self.controls = [
            self.Title,
        ]


def main_moderator(page: ft.Page):
    mod_page = ModeratorApp(page)
    return mod_page