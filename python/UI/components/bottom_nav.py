import flet as ft
from components.responsive import Responsive

# Size of all components on the page (as percent of screen size)
navbar_height = 0.12
button_width = 0.15
text_size = 0.025
padding = 0.008


class navBar(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        # FIX: Renamed to main_page to avoid overwriting Flet's built-in property!
        self.main_page = page

        self.r = Responsive(page)
        self.border = ft.Border.only(top=ft.BorderSide(color=ft.Colors.GREY_600, width=2))
        self.height = self.r.h(navbar_height)
        self.padding = self.r.w(padding)

        # Text elements
        self.home_text = ft.Text(value="Home", size=self.r.w(text_size))
        self.activities_text = ft.Text(value="Activities", size=self.r.w(text_size))
        self.nutrition_text = ft.Text(value="Nutrition", size=self.r.w(text_size))
        self.social_text = ft.Text(value="Social", size=self.r.w(text_size))
        self.settings_text = ft.Text(value="Settings", size=self.r.w(text_size))

        # Container elements for buttons
        self.home_container = ft.Container(
            width=self.r.w(button_width), border=ft.Border.all(1, ft.Colors.GREY_400), border_radius=5,
            on_click=self.home_pressed, alignment=ft.Alignment.CENTER,
            content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                              controls=[ft.Icon(ft.Icons.HOME_ROUNDED), self.home_text])
        )

        self.activities_container = ft.Container(
            width=self.r.w(button_width), border=ft.Border.all(1, ft.Colors.GREY_400), border_radius=5,
            on_click=self.activities_pressed, alignment=ft.Alignment.CENTER,
            content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                              controls=[ft.Icon(ft.Icons.DIRECTIONS_RUN_ROUNDED), self.activities_text])
        )

        self.nutrition_container = ft.Container(
            width=self.r.w(button_width), border=ft.Border.all(1, ft.Colors.GREY_400), border_radius=5,
            on_click=self.nutrition_pressed, alignment=ft.Alignment.CENTER,
            content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                              controls=[ft.Icon(ft.Icons.FOOD_BANK_ROUNDED), self.nutrition_text])
        )

        self.social_container = ft.Container(
            width=self.r.w(button_width), border=ft.Border.all(1, ft.Colors.GREY_400), border_radius=5,
            on_click=self.social_pressed, alignment=ft.Alignment.CENTER,
            content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                              controls=[ft.Icon(ft.Icons.PEOPLE_OUTLINE_OUTLINED), self.social_text])
        )

        self.settings_container = ft.Container(
            width=self.r.w(button_width), border=ft.Border.all(1, ft.Colors.GREY_400), border_radius=5,
            on_click=self.settings_pressed, alignment=ft.Alignment.CENTER,
            content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                              controls=[ft.Icon(ft.Icons.SETTINGS), self.settings_text])
        )

        # Row of elements
        self.content = ft.Row(
            expand=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[self.home_container, self.activities_container, self.nutrition_container, self.social_container,
                      self.settings_container]
        )

    def set_size(self):
        self.height = self.r.h(navbar_height)
        self.padding = self.r.w(padding)
        self.home_container.width = self.r.w(button_width)
        self.activities_container.width = self.r.w(button_width)
        self.nutrition_container.width = self.r.w(button_width)
        self.social_container.width = self.r.w(button_width)
        self.settings_container.width = self.r.w(button_width)

        self.home_text.size = self.r.w(text_size)
        self.activities_text.size = self.r.w(text_size)
        self.nutrition_text.size = self.r.w(text_size)
        self.social_text.size = self.r.w(text_size)
        self.settings_text.size = self.r.w(text_size)

    def resize(self):
        # FIX: Use main_page here too
        self.r = Responsive(self.main_page)
        self.set_size()

    # --- ALL UPDATED ROUTING FUNCTIONS ---
    async def home_pressed(self, e):
        await self.main_page.push_route("/home")

    async def activities_pressed(self, e):
        await self.main_page.push_route("/activities")

    async def nutrition_pressed(self, e):
        await self.main_page.push_route("/nutrition")

    async def social_pressed(self, e):
        await self.main_page.push_route("/social")

    async def settings_pressed(self, e):
        await self.main_page.push_route("/settings")