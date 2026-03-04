'''
File used for main homepage that logged-in users will be met with
'''

import flet as ft

from components.userpfp import Userpfp
from components.bottom_nav import navBar
from components.responsive import Responsive

#TODO - Retrieve name of logged in user and pfp
user = "Username"

#Sizes of all elements on homepage (as percent of screen)
welcome_text_size = 0.1
motivational_msg_size = 0.03

class WorkoutApp(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.r = Responsive(page)

        #TODO-Add slight variations to the welcome and motivational message

        #Welcome text to be shown to the user
        self.welcome_text = ft.Text(
            value=f"Welcome {user}!",
            size=self.r.w(welcome_text_size),
            color=ft.Colors.BLACK
        )

        #Motivational text to be shown to the user
        self.motivational_text = ft.Text(
            value="Lets crush your workout goals today!",
            size=self.r.w(motivational_msg_size),
            color="grey"
        )

        #Create user profile picture image
        self.userpfp = Userpfp(page)

        #Create navBar element
        self.navBar = navBar(page)

        self.controls=[
            ft.Row(
                expand=True,
                #Adds white space in-between text and profile pic
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                #Ensures bot text and profile pic are aligned to the top of the screen
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Column(
                        expand=True,
                        controls=[
                            self.welcome_text,
                            self.motivational_text
                        ]
                    ),
                    self.userpfp
                ],
            ),
            self.navBar
        ]
        #Expand, take all available space
        self.expand = True
        #Spread the two elements apart
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        self.this_page = page
        page.on_resize = self.resize

    #Function to be ran when page resizes
    def resize(self, e):
        self.r = Responsive(self.this_page)

        #Resize text size
        self.welcome_text.size = self.r.w(welcome_text_size)
        self.motivational_text.size = self.r.w(motivational_msg_size)

        #Resize profile picture size
        self.userpfp.resize()
        #Resize navBar
        self.navBar.resize()

        #Update the page contents
        self.update()

def main(page: ft.Page):
    page.title = "My Wellbeing"

    #Default to light mode
    #TODO - Allow user to change mode in settings
    page.theme_mode = ft.ThemeMode.LIGHT

    #Font to be used throughout app
    page.fonts = {
        "Dubai": "/assets/DUBAI-REGULAR.TTF"
    }

    page.theme = ft.Theme(
        font_family = "Dubai",
    )

    #TODO - REMOVE FROM FINAL BUILD - FOR TESTING ONLY
    #Mobile phone like resolution
    #page.window.width=360
    #page.window.height=800
    #page.window.resizable=False
    #page.window.alignment = ft.Alignment.CENTER


    #Ensures nav bar stretches across full screen
    page.padding = 0

    page.update()

    app = WorkoutApp(page)

    page.add(app)