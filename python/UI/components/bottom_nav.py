'''
Used for re-usable navigation bar component which will appear at the bottom of the screen throughout the app
'''

import flet as ft

from components.responsive import Responsive

#Size of all components on the page
navbar_height = 0.08

class navBar(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.r = Responsive(page)
        self.bgcolor = "#dbdbdb"

        self.height = self.r.h(navbar_height)
        self.width = page.width

        self.content=ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Container(
                        content=ft.Column(
                            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.HOME_ROUNDED),
                                ft.Text("Home")
                            ]
                        )
                    ),
                    ft.Container(
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.DIRECTIONS_RUN_ROUNDED),
                                ft.Text("Activities")
                            ]
                        )
                    ),
                    ft.Container(
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.FOOD_BANK_ROUNDED),
                                ft.Text("Nutrition")
                            ]
                        )
                    ),
                    ft.Container(
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.PEOPLE_OUTLINE_OUTLINED),
                                ft.Text("Social")
                            ]
                        )
                    ),
                    ft.Container(
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.SETTINGS),
                                ft.Text("Settings")
                            ]
                        )
                    )
                ]
            )
