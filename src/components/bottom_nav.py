"""
    Module is used to create the navigation bar at the bottom of each
    of the main pages to allow the users to connect with each other
"""
import flet as ft
from .responsive import Responsive

# Size of all components on the page (as percent of screen size)
navbar_height = 0.12
button_width = 0.15
text_size = 0.025
padding = 0.008

class NavBar(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.main_page = page

        def nav_item(icon, label, route):
            return ft.Container(
                expand=True,
                on_click=lambda e: page.go(route),
                border_radius=10,
                padding=ft.padding.symmetric(vertical=8),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                    controls=[
                        ft.Icon(icon, size=24, color=ft.Colors.GREY_600),
                        ft.Text(label, size=11, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                    ]
                )
            )

        self.bgcolor = ft.Colors.WHITE
        self.border = ft.Border(top=ft.BorderSide(color=ft.Colors.GREY_200, width=1))
        self.padding = ft.padding.symmetric(horizontal=8, vertical=4)
        self.content = ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            controls=[
                nav_item(ft.Icons.HOME_ROUNDED,          "Home",       "/home"),
                nav_item(ft.Icons.DIRECTIONS_RUN_ROUNDED,"Activities", "/activities"),
                nav_item(ft.Icons.FOOD_BANK_ROUNDED,     "Nutrition",  "/nutrition"),
                nav_item(ft.Icons.PEOPLE,        "Social",     "/social"),
                nav_item(ft.Icons.SETTINGS,              "Settings",   "/settings"),
            ]
        )

    def resize(self):
        self.r = Responsive(self.main_page)
