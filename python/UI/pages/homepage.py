'''
File used for main homepage that logged-in users will be met with
'''

import os
import csv
import datetime
import flet as ft
from components.userpfp import Userpfp
from components.bottom_nav import NavBar
from components.responsive import Responsive

# Safely try to import the database function
try:
    from database.queries import get_user
except ImportError:
    get_user = None

# --- MOCK DATA ---
steps = 2000
calories = 800
step_goal = 10000
cal_goal = 2500

class WorkoutApp(ft.Column):
    def __init__(self, page: ft.Page, user_id: int):
        super().__init__()

        self.r = Responsive(page)
        self.this_page = page

        # Make the entire homepage scrollable!
        self.scroll = ft.ScrollMode.HIDDEN
        self.spacing = 20

        # --- DATABASE FETCH WITH FAILSAFE ---
        user_name = "Test User"
        if get_user is not None:
            try:
                user_data = get_user(user_id)
                if user_data:
                    user_name = user_data[1]
            except Exception:
                pass

        # --- 1. HEADER SECTION ---
        current_hour = datetime.datetime.now().hour
        if current_hour < 12:
            greeting = "Good Morning,"
        elif 12 <= current_hour < 18:
            greeting = "Good Afternoon,"
        else:
            greeting = "Good Evening,"

        self.welcome_text = ft.Text(
            value=f"{greeting}\n{user_name}",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK
        )

        self.motivational_text = ft.Text(
            value="Lets crush your workout goals today!",
            size=14,
            color=ft.Colors.GREY_600
        )

        self.userpfp = Userpfp(page)

        self.header_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column([self.welcome_text, self.motivational_text], spacing=0),
                self.userpfp
            ],
        )

        # --- 2. CLEAN DAILY PROGRESS CARD ---
        self.progress_card = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            content=ft.Column([
                ft.Text("DAILY PROGRESS", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),

                ft.Row([
                    # Steps Column
                    ft.Column([
                        ft.Icon(ft.Icons.DIRECTIONS_WALK, color=ft.Colors.BLUE_500, size=30),
                        ft.Text(f"{steps:,} / {step_goal:,}", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("Steps", size=12, color=ft.Colors.GREY_400),
                        ft.ProgressBar(value=steps/step_goal, color=ft.Colors.BLUE_500, bgcolor=ft.Colors.BLUE_50, width=100)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),

                    # Custom Divider
                    ft.Container(width=1, height=80, bgcolor=ft.Colors.GREY_200),

                    # Calories Column
                    ft.Column([
                        ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, color=ft.Colors.DEEP_ORANGE_500, size=30),
                        ft.Text(f"{calories:,} / {cal_goal:,}", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("Calories", size=12, color=ft.Colors.GREY_400),
                        ft.ProgressBar(value=calories/cal_goal, color=ft.Colors.DEEP_ORANGE_500, bgcolor=ft.Colors.ORANGE_50, width=100)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
            ])
        )

        # --- 3. QUICK ACTIONS BAR ---
        def action_btn(icon, label, color, route):
            return ft.GestureDetector(
                on_tap=lambda _: page.go(route),
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(icon, color=color, size=24),
                        padding=15,
                        bgcolor=ft.Colors.GREY_100,
                        border_radius=50
                    ),
                    ft.Text(label, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5)
            )

        self.actions_row = ft.Row([
            action_btn(ft.Icons.PLAY_ARROW, "Start", ft.Colors.GREEN_500, "/map"),
            action_btn(ft.Icons.RESTAURANT, "Nutrition", ft.Colors.ORANGE_500, "/nutrition"),
            action_btn(ft.Icons.PEOPLE, "Social", ft.Colors.BLUE_500, "/social"),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)


        # --- 4. RECENT ACTIVITIES FEED (DYNAMIC) ---
        feed_controls = [
            ft.Text("RECENT ACTIVITIES", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
            ft.Divider(height=5, color=ft.Colors.TRANSPARENT)
        ]

        recent_activities = self.get_recent_activities()

        # Icon mapping for dynamic feed
        icon_map = {
            "Run": (ft.Icons.DIRECTIONS_RUN, ft.Colors.DEEP_ORANGE_400),
            "Walk": (ft.Icons.DIRECTIONS_WALK, ft.Colors.BLUE_400),
            "Cycle": (ft.Icons.DIRECTIONS_BIKE, ft.Colors.GREEN_400)
        }

        if not recent_activities:
            # Empty state if no CSV exists or it's empty
            feed_controls.append(
                ft.Text("No activities recorded yet. Time to get moving!", size=14, color=ft.Colors.GREY_400, text_align=ft.TextAlign.CENTER)
            )
        else:
            # Generate a list tile for each of the most recent activities (up to 3)
            for act in recent_activities:
                act_icon, act_color = icon_map.get(act["type"], (ft.Icons.FITNESS_CENTER, ft.Colors.GREY_400))
                feed_controls.append(
                    ft.ListTile(
                        leading=ft.Container(content=ft.Icon(act_icon, color=ft.Colors.WHITE), bgcolor=act_color, padding=10, border_radius=25),
                        title=ft.Text(act["type"], size=14, weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"{act['date']} • {act['dist']}km in {act['time']}", size=12, color=ft.Colors.GREY_500),
                    )
                )

        self.feed_card = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=15,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            content=ft.Column(feed_controls, spacing=0)
        )

        # --- 5. NAVIGATION ---
        self.nav_bar = NavBar(page)

        # Layout Assembly
        self.controls = [
            self.header_row,
            self.progress_card,
            self.actions_row,
            self.feed_card,
            ft.Container(height=20), # Extra spacer before nav bar
            self.nav_bar
        ]

        self.expand = True
        page.on_resize = self.resize

    # --- DATA FETCHING METHODS ---
    def get_recent_activities(self):
        activities_list = []
        file_path = "activities_history.csv"

        if not os.path.isfile(file_path):
            return activities_list

        try:
            with open(file_path, mode="r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    if len(row) >= 3:
                        date_str = row[0]
                        dist = float(row[1])
                        secs = int(row[2])
                        act_type = row[3] if len(row) >= 4 else "Run"

                        run_date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")

                        # Format the seconds into readable time
                        hours = secs // 3600
                        minutes = (secs % 3600) // 60
                        s = secs % 60
                        if hours > 0:
                            time_str = f"{hours}h {minutes}m"
                        elif minutes > 0:
                            time_str = f"{minutes}m {s}s"
                        else:
                            time_str = f"{s}s"

                        activities_list.append({
                            "date": run_date.strftime("%b %d"), # E.g., "Mar 15"
                            "dist": f"{dist:.2f}",
                            "time": time_str,
                            "type": act_type
                        })
        except Exception as e:
            print(f"Error reading stats: {e}")

        # Reverse the list so the newest are first, then slice to keep only the top 3!
        return list(reversed(activities_list))[:3]

    def resize(self, e):
        self.r = Responsive(self.this_page)
        self.userpfp.resize()
        self.nav_bar.resize()
        self.update()

def main_homepage(page: ft.Page):
    homepage = WorkoutApp(page, 1)
    return homepage