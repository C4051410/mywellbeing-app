'''
File used for main homepage that logged-in users will be met with
'''

import flet as ft

from components.userpfp import Userpfp
from components.bottom_nav import navBar

#TODO - Retrieve name of logged in user and pfp
user = "Username"

#Default style of all text on screen

#Welcome message to be displayed
welcome_message = ft.Column(
    controls=[
        #Greeting for the user
        ft.Text(
            value=f"Welcome {user}!",
            size=90,
            color=ft.Colors.BLACK
        ),
        #Generic motivational message
        ft.Text(
            value="Lets crush your workout goals today!",
            size=40,
            color="grey"
        )
    ]
)


class WorkoutApp(ft.Column):
    def init(self):
        self.controls=[
            ft.Row(
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    welcome_message,
                    Userpfp()
                ],
            ),
            navBar()
        ]
        self.expand = True
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

def main(page: ft.Page):
    page.title = "My Wellbeing"
    #Default to light mode
    #TODO - Allow user to change mode in settings
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {
        "Dubai": "/assets/DUBAI-REGULAR.TTF"
    }

    page.theme = ft.Theme(
        font_family = "Dubai",
    )

    page.update()

    app = WorkoutApp()

    page.add(app)