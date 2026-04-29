'''
File used for main homepage that logged-in users will be met with
'''
from datetime import date

import flet as ft

from activities.activities import load_activity_data
from components.userpfp import Userpfp
from components.bottom_nav import NavBar
from components.responsive import Responsive
from home.home_services import retrieve_friends_activities, retrieve_current_streaks,retrieve_username
from nutrition.nutrition_services import retrieve_daily_stats,retrieve_user_goals

#Sizes of all elements on homepage (as percent of screen)
welcome_text_size = 0.1
motivational_msg_size = 0.04
widget_text_size = 0.035
steps_h_size = 0.4
calories_h_size = 0.4
friends_v_size = 0.15
streak_v_size = 0.225

class WorkoutApp(ft.Column):
    def __init__(self, page: ft.Page, user_id):
        super().__init__()
        self.r = Responsive(page)
        # temporary to pass tests
        self.steps_text = ft.Text("3000")
        self.steps_container = ft.Container(width=100, height=100)
        self.foodlog_container = ft.Container(width=100, height=100)

        #gets username
        user = retrieve_username(user_id)
        steps = 3000
        #retrieves users goal and current stats
        calories_goal, salts_goal, protein_goal, water_goal = retrieve_user_goals(user_id)
        daily_calories, daily_salts, daily_proteins, daily_water = retrieve_daily_stats(user_id, date.today())
        #retrieves friends data
        friends_data = retrieve_friends_activities(user_id,date.today())
        friends_list = []
        #gets users current streak and best streak
        streak = retrieve_current_streaks(user_id)

        # ignore other return values, only need activitiy count
        _, _, activities_completed, _ = load_activity_data(page)
        activities_completed = int(activities_completed)

        daily_goal = 5

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

        # activities progress display
        self.activities_text = ft.Text(value=f"{activities_completed} / {daily_goal}", size=self.r.w(widget_text_size), weight=ft.FontWeight.BOLD)
        self.activities_bar = ft.ProgressBar(value=(activities_completed / daily_goal) if daily_goal else 0, width=150, height=10, color=ft.Colors.BLUE, border_radius=5)

        # calorie progress display
        self.calories_text = ft.Text(f"{daily_calories} / {calories_goal} Kcal", size=self.r.w(widget_text_size), weight=ft.FontWeight.BOLD)
        self.calories_bar = ft.ProgressBar(value=(daily_calories / calories_goal) if calories_goal else 0, width=150, height=10, color=ft.Colors.DEEP_ORANGE, border_radius=5, bgcolor="#FFDBBB")

        self.salts_text = ft.Text(f"Salt: {daily_salts} / {salts_goal} g",size=self.r.w(widget_text_size))
        self.protein_text = ft.Text(f"Protein: {daily_proteins} / {protein_goal} g",size=self.r.w(widget_text_size))
        self.water_text = ft.Text(f"Water: {daily_water} / {water_goal} ml",size=self.r.w(widget_text_size))


        for name, activity, f_streak in friends_data:
            print(name + " " + activity)
            friends_list.append(
                ft.ListTile(title=ft.Text(name),
                            subtitle=ft.Text(activity),
                            dense=True,
                            visual_density=ft.VisualDensity.COMPACT,
                            trailing = ft.Text(f"Streak : {f_streak}🔥"))
            )

        self.current_streak_text = ft.Text(f"Current Streak: {streak[0]}")
        self.longest_streak_text = ft.Text(f"Longest Streak: {streak[1]}")

        # activities widget
        self.activity_container = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Activities Completed", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500, size=15),
                    self.activities_text,
                    self.activities_bar,
                ]
            )
        )

        #Calories widget
        self.calories_container = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Calories Consumed", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500, size=15),
                    self.calories_text,
                    self.calories_bar
                ]
            )
        )

        #Friends widget
        self.friends_container = ft.Container(
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            gradient=ft.LinearGradient(begin=ft.alignment.Alignment(-1, 0), end=ft.alignment.Alignment(1, 0), colors=["#8A2BE2", "#4C6EF5",]),
            content= ft.Column(
                controls=friends_list,
                scroll = ft.ScrollMode.ALWAYS,
                spacing = 0,
                expand = 1
            )
        )
        if friends_list == []:
            self.friends_container = ft.Container(
                border_radius=15,
                padding=20,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
                gradient=ft.LinearGradient(begin=ft.alignment.Alignment(-1, 0), end=ft.alignment.Alignment(1, 0),
                                           colors=["#4C6EF5", "#8A2BE2"]),
                expand = 1,
                content= ft.Column(
                    controls = [ft.Text("Your feed is empty", weight=ft.FontWeight.BOLD, size=18, color=ft.Colors.WHITE70),
                                ft.Text("Follow more friends to see their activity.", size=14, color=ft.Colors.WHITE70),])
            )
        #Streak widget
        self.streak_container = ft.Container(
            border=ft.Border.all(width=2, color=ft.Colors.GREY_400),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content = ft.Column(
                [
                    self.current_streak_text,
                    self.longest_streak_text
                ]
            )
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

        main_contnet = ft.Column(
            controls=[
                #Row with text and pfp
                ft.Row(
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
                #Row with activities and calories
                ft.Row(
                    spacing=8,
                    controls=[
                        ft.Container(content=self.activity_container, expand=1),
                        ft.Container(content=self.calories_container, expand=1),
                    ]
                ),

                # friends/social widget
                ft.Container(
                    expand = 1,
                    padding=ft.padding.only(top=20),
                    content=ft.Container(
                        expand=1,
                        content=self.friends_container
                    )
                ),

                # streak widget
                self.streak_container,

                # UN link
                self.un_link
            ],
            expand=True,
            scroll=ft.ScrollMode.HIDDEN
        )
        self.controls = [main_contnet,self.nav_bar]

        #Expand, take all available space
        self.expand = True
        #Spread the elements apart
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.this_page = page
        page.on_resize = self.resize
        #Initially set the widget and text size
        self.set_widget_size()
        self.set_text_size()



    #Set text size of all text on the page
    def set_text_size(self):
        self.welcome_text.size = self.r.w(welcome_text_size)
        self.motivational_text.size = self.r.w(motivational_msg_size)

        self.activities_text.size = self.r.w(widget_text_size)
        self.calories_text.size = self.r.w(widget_text_size)


    def set_widget_size(self):
        #Set width and height of widgets
        #Steps - Square
        full_width = self.this_page.width * 0.95
        self.activity_container.height = self.r.w(steps_h_size)
        #Calories - Square
        self.calories_container.height = self.r.w(calories_h_size)
        #Friends - Rectangle
        self.friends_container.height = self.r.h(friends_v_size)
        self.friends_container.width = self.this_page.width * 0.95
        #Streak - Long rectange
        self.streak_container.width = full_width
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