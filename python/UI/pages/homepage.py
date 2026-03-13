'''
File used for main homepage that logged-in users will be met with
'''

import flet as ft

from UI.components.userpfp import Userpfp
from UI.components.bottom_nav import NavBar
from UI.components.responsive import Responsive
from database.queries import get_user

#Sizes of all elements on homepage (as percent of screen)
welcome_text_size = 0.1
motivational_msg_size = 0.03
widget_text_size = 0.035
steps_h_size = 0.4
calories_h_size = 0.4
friends_v_size = 0.15
streak_v_size = 0.225

class WorkoutApp(ft.Column):
    def __init__(self, page: ft.Page, user_id):
        super().__init__()
        self.r = Responsive(page)
        # retrieves logged in users data
        user_data = get_user(user_id)

        # order of unpacked values: id, username, email, role
        user = user_data[1]
        calories = user_data[9] or 0
        steps = user_data[11] or 0

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
            color=ft.Colors.GREY
        )

        #Text for steps widget
        self.steps_text = ft.Text(
            value=f'{steps}',
            size=self.r.w(widget_text_size)
        )

        self.calories_text = ft.Text(
            value=f'{calories}',
            size=self.r.w(widget_text_size)
        )

        #Steps widget
        self.steps_container = ft.Container(
            border = ft.Border.all(width=2, color=ft.Colors.GREY_400),
            content=ft.Column(
                controls=[
                    self.steps_text
                ]
            )
        )

        #Calories widget
        self.calories_container = ft.Container(
            border = ft.Border.all(width=2, color=ft.Colors.GREY_400),
            content=ft.Column(
                controls=[
                    self.calories_text
                ]
            )
        )

        #Friends widget
        self.friends_container = ft.Container(
            bgcolor = ft.Colors.BLUE_300
        )

        #Streak widget
        self.streak_container = ft.Container(
            border=ft.Border.all(width=2, color=ft.Colors.GREY_400)
        )

        #Create user profile picture image
        self.userpfp = Userpfp(page)

        #Create NavBar element
        self.nav_bar = NavBar(page)

        self.controls=[
            #Row with text and pfp
            ft.Row(
                #Adds white space in-between text and profile pic
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
            #Row with steps and calories
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                #vertical_alignment = ft.CrossAxisAlignment.START,
                controls=[
                    self.steps_container,
                    self.calories_container
                ]
            ),
            self.friends_container,
            self.streak_container,
            self.nav_bar
        ]
        #Expand, take all available space
        self.expand = True
        #Spread the elements apart
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        #Initially set the widget and text size
        self.set_widget_size()
        self.set_text_size()

        self.this_page = page
        page.on_resize = self.resize

    #Set text size of all text on the page
    def set_text_size(self):
        self.welcome_text.size = self.r.w(welcome_text_size)
        self.motivational_text.size = self.r.w(motivational_msg_size)

        self.steps_text.size = self.r.w(widget_text_size)
        self.calories_text.size = self.r.w(widget_text_size)


    def set_widget_size(self):
        #Set width and height of widgets
        #Steps - Square
        self.steps_container.width = self.r.w(steps_h_size)
        self.steps_container.height = self.r.w(steps_h_size)
        #Calories - Square
        self.calories_container.width = self.r.w(calories_h_size)
        self.calories_container.height = self.r.w(calories_h_size)
        #Friends - Rectangle
        self.friends_container.height = self.r.h(friends_v_size)
        #Streak - Long rectange
        self.streak_container.height = self.r.h(streak_v_size)

    #Function to be ran when page resizes
    def resize(self, e):
        self.r = Responsive(self.this_page)

        #Resize text size
        self.set_text_size()

        #Resize all the widgets
        self.set_widget_size()

        #Resize profile picture size
        self.userpfp.resize()
        #Resize nav_bar
        self.nav_bar.resize()

        #Update the page contents
        self.update()

def main_homepage(page: ft.Page,user_id):
    homepage = WorkoutApp(page,user_id)

    return homepage