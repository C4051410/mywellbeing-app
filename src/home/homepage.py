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
widget_text_size = 0.055
steps_h_size = 0.4
calories_h_size = 0.4
friends_v_size = 0.15
streak_v_size = 0.40

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
        tot_dist, tot_time, activities_completed, activities_list = load_activity_data(page)
        activities_completed = int(activities_completed)

        # Get last activity (if exists)
        if activities_list:
            last = activities_list[0]
            act_type = last["type"]
            act_title = last["title"]
            act_time = last["time"]

            # Build a readable summary depending on type
            if act_type in ("Run", "Cycle"):
                act_summary = f"{last['dist']} km • {act_time}"
            elif act_type == "Walk":
                act_summary = f"{last.get('steps', '—')} steps • {act_time}"
            elif act_type in ("Workout", "WeightLifting"):
                act_summary = f"{last['calories']} kcal • {act_time}"
            else:
                act_summary = act_time

            last_activity_text = f"{act_title} • {act_summary}"
        else:
            last_activity_text = "No recent activity"

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
        self.activities_bar = ft.ProgressBar(value=(activities_completed / daily_goal) if daily_goal else 0, width=150, height=15, color=ft.Colors.BLUE, border_radius=10, bgcolor="F3F4F6")

        # calorie progress display
        self.calories_text = ft.Text(f"{daily_calories} / {calories_goal}", size=self.r.w(widget_text_size), weight=ft.FontWeight.BOLD)
        self.calories_bar = ft.ProgressBar(value=(daily_calories / calories_goal) if calories_goal else 0, width=150, height=15, color=ft.Colors.DEEP_ORANGE, border_radius=10, bgcolor="#F3F4F6")

        self.salts_text = ft.Text(f"Salt: {daily_salts} / {salts_goal} g",size=self.r.w(widget_text_size))
        self.protein_text = ft.Text(f"Protein: {daily_proteins} / {protein_goal} g",size=self.r.w(widget_text_size))
        self.water_text = ft.Text(f"Water: {daily_water} / {water_goal} ml",size=self.r.w(widget_text_size))


        for name, activity, f_streak in friends_data:
            print(name + " " + activity)
            friends_list.append(
                ft.ListTile(title=ft.Text(name, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            subtitle=ft.Text(activity, size=14, color=ft.Colors.WHITE70),
                            dense=True,
                            visual_density=ft.VisualDensity.COMPACT,
                            trailing = ft.Text(f"Streak : {f_streak}🔥"))
            )

        # TODO: add strava activities to streak
        self.current_streak_text = ft.Text(f"{streak[0]}", size=25, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
        self.longest_streak_text = ft.Text(f"{streak[1]}")

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
                    ft.Text("Activities Completed", color=ft.Colors.GREY_500, size=15),
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
                    ft.Text("Calories Consumed", color=ft.Colors.GREY_500, size=15),
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
            border_radius=15,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            padding=0,
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Container(
                        padding=20,
                        width=350,
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.Alignment(-1, 0),
                            end=ft.alignment.Alignment(1, 0),
                            colors=["#FF69D2", "#E92020"]
                        ),
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.current_streak_text,
                                ft.Text(
                                    "Current Streak",
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE70,
                                    size=20
                                )
                            ]
                        )
                    ),
                    # recent activities
                    ft.Container(
                        padding=20,
                        bgcolor=ft.Colors.WHITE,
                        width=350,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text("Last Activity:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                                ft.Text(last_activity_text, size=14, color=ft.Colors.GREY_600)
                            ]
                        )
                    )

                ]
            )
        )

        async def open_url(): # used to create link to UN website, using async to perform the launch in the background
            await self.this_page.launch_url("https://globalgoals.org/goals/3-good-health-and-well-being/")

        self.un_link = ft.GestureDetector( #used to allow users to click on the img and take them to UN website
            mouse_cursor=ft.MouseCursor.CLICK,
            on_tap=open_url,
            content=ft.Container(
                border_radius=15,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Image(
                    src="unGoal.png",
                    width=350,
                    height=60,
                    fit=ft.BoxFit.COVER,
                    border_radius=15,
                )
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
        #self.streak_container.height = self.r.h(streak_v_size)

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