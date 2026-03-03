'''
Used for re-usable navigation bar component which will appear at the bottom of the screen throughout the app
'''

import flet as ft

class navBar(ft.Row):
    def init(self):
        self.controls=[
            ft.Button(
                icon=ft.Icons.HOME_ROUNDED,
                content="Home",
                style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
            ),
            ft.Button(
                icon=ft.Icons.DIRECTIONS_RUN_ROUNDED,
                content="Activities",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
            ),
            ft.Button(
                icon=ft.Icons.FOOD_BANK,
                content="Nutrition",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
            ),
            ft.Button(
                icon=ft.Icons.PEOPLE_OUTLINE_OUTLINED,
                content="Social",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
            ),
            ft.Button(
                icon=ft.Icons.SETTINGS,
                content="Settings",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
            )
        ]
        self.expand = True
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
