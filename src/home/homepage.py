'''
File used for main homepage that logged-in users will be met with
'''
from datetime import date

import flet as ft

from components.userpfp import Userpfp
from components.bottom_nav import NavBar
from components.responsive import Responsive
from database.user_queries import get_user
from nutrition.nutrition_queries import retrieve_daily_stats

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
        calories_goal = user_data[9] or 0
        salts_goal = user_data[14] or 0
        protein_goal = user_data[15] or 0
        water_goal = user_data[16] or 0
        steps = user_data[11] or 0
        daily_calories,daily_salts,daily_proteins,daily_water = retrieve_daily_stats(user_id,date.today())

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

        self.calories_text = ft.Text(f"Calories: {daily_calories} / {calories_goal} Kcal",size=self.r.w(widget_text_size))
        self.salts_text = ft.Text(f"Salt: {daily_salts} / {salts_goal} g",size=self.r.w(widget_text_size))
        self.protein_text = ft.Text(f"Protein: {daily_proteins} / {protein_goal} g",size=self.r.w(widget_text_size))
        self.water_text = ft.Text(f"Water: {daily_water} / {water_goal} ml",size=self.r.w(widget_text_size))


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
        self.foodlog_container = ft.Container(
            border = ft.Border.all(width=2, color=ft.Colors.GREY_400),
            content=ft.Column(
                controls=[
                    self.calories_text,
                    self.salts_text,
                    self.protein_text,
                    self.water_text
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

        async def open_url(): # used to create link to UN website, using async to perform the launch in the background
            await self.this_page.launch_url("https://globalgoals.org/goals/3-good-health-and-well-being/")

        self.un_link = ft.GestureDetector( #used to allow users to click on the img and take them to UN website
            mouse_cursor = ft.MouseCursor.CLICK,
            on_tap = open_url,
            content = ft.Image(
                src = "unGoal.png",
                height = 100,
                width = 350,
            )
        )

        #Create user profile picture image
        self.userpfp = Userpfp(page)

        #Create NavBar element
        self.nav_bar = NavBar(page)

        main_contnet = ft.Column(controls=[
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
                    self.foodlog_container
                ]
            ),
            self.friends_container,
            self.streak_container,
            self.un_link],expand=True,scroll=ft.ScrollMode.HIDDEN)
        self.controls = [main_contnet,self.nav_bar]

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
        self.foodlog_container.width = self.r.w(calories_h_size)
        self.foodlog_container.height = self.r.w(calories_h_size)
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