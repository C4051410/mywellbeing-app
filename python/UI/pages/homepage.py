'''
File used for main homepage that logged-in users will be met with
'''

import flet as ft
from components.userpfp import Userpfp
from components.bottom_nav import NavBar
from components.responsive import Responsive

# Mock Data
user = "Username"
steps = 4250
step_goal = 10000

# Sizes of all elements on homepage (as percent of screen)
welcome_text_size = 0.08
motivational_msg_size = 0.035

class WorkoutApp(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.r = Responsive(page)
        self.this_page = page

        # --- 1. DATA LOADING ---
        # Get your real goal from the settings page session!
        cal_goal = page.session.store.get("cal_goal") if page.session.store else "2500"

        # --- 2. HEADER SECTION ---
        self.welcome_text = ft.Text(
            value=f"Hi, {user}!",
            size=self.r.w(welcome_text_size),
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK
        )

        self.motivational_text = ft.Text(
            value="You're doing great today!",
            size=self.r.w(motivational_msg_size),
            color=ft.Colors.GREY_600
        )

        self.userpfp = Userpfp(page)

        # --- 3. DAILY PROGRESS CARD ---
        # Replacing PieChart with a clean ProgressBar
        self.step_progress = ft.ProgressBar(
            value=steps/step_goal,
            color=ft.Colors.DEEP_ORANGE,
            bgcolor=ft.Colors.GREY_200,
            height=10,
            border_radius=5
        )

        self.daily_status_card = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.DIRECTIONS_RUN_ROUNDED, color=ft.Colors.DEEP_ORANGE),
                    ft.Text("DAILY STEPS", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
                ]),
                ft.Text(f"{steps:,}", size=32, weight=ft.FontWeight.BOLD),
                self.step_progress,
                ft.Text(f"{int((steps/step_goal)*100)}% of your {step_goal:,} goal", size=12, color=ft.Colors.GREY_400)
            ], spacing=10)
        )

        # --- 4. STATS GRID (Calories & Streak) ---
        self.calories_box = ft.Container(
            expand=1, bgcolor=ft.Colors.ORANGE_50, border_radius=15, padding=15,
            content=ft.Column([
                ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, color=ft.Colors.ORANGE_700),
                ft.Text("Target", size=12, color=ft.Colors.ORANGE_700, weight=ft.FontWeight.BOLD),
                ft.Text(f"{cal_goal} kcal", size=18, weight=ft.FontWeight.BOLD)
            ], spacing=2)
        )

        self.streak_box = ft.Container(
            expand=1, bgcolor=ft.Colors.BLUE_50, border_radius=15, padding=15,
            content=ft.Column([
                ft.Icon(ft.Icons.BOLT, color=ft.Colors.BLUE_700),
                ft.Text("Streak", size=12, color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD),
                ft.Text("5 Days", size=18, weight=ft.FontWeight.BOLD)
            ], spacing=2)
        )

        # --- 5. ACTIVITY SUMMARY ---
        # Replacing BarChart with a simple horizontal summary
        self.summary_card = ft.Container(
            bgcolor=ft.Colors.WHITE, border_radius=15, padding=20,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            content=ft.Column([
                ft.Text("RECENT ACTIVITY", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
                    title=ft.Text("Yesterday: Goal Reached!"),
                    subtitle=ft.Text("10,240 steps logged")
                )
            ])
        )

        self.nav_bar = NavBar(page)

        # --- LAYOUT ASSEMBLY ---
        self.controls = [
            ft.Row([
                ft.Column([self.welcome_text, self.motivational_text], expand=True),
                self.userpfp
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            self.daily_status_card,

            ft.Row([self.calories_box, self.streak_box], spacing=15),

            self.summary_card,

            self.nav_bar
        ]

        self.expand = True
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.set_text_size()
        page.on_resize = self.resize

    def set_text_size(self):
        self.welcome_text.size = self.r.w(welcome_text_size)
        self.motivational_text.size = self.r.w(motivational_msg_size)

    def resize(self, e):
        self.r = Responsive(self.this_page)
        self.set_text_size()
        self.userpfp.resize()
        self.nav_bar.resize()
        self.update()

def main_homepage(page: ft.Page):
    return WorkoutApp(page)