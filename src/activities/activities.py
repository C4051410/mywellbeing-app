import os
import csv
from datetime import datetime, timedelta
import flet as ft

from activities.strava_api import connect_strava, get_saved_activities, format_strava_activities, save_tokens_for_user, load_tokens_for_user
from components.bottom_nav import NavBar
from components.responsive import Responsive


class ActivitiesPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.r = Responsive(page)

        # --- LOAD REAL DATA FROM CSV ---
        tot_dist, tot_time, runs_count, activities_list = self.load_activity_data()

        # 1. Page Header
        header = ft.Container(
            content=ft.Text("Activities", size=32, weight=ft.FontWeight.BOLD),
            padding=ft.padding.only(top=20, left=10)
        )

        if load_tokens_for_user(self.main_page.user_id):
            button_text = "Strava Connected"
        else:
            button_text = "Connect Strava"

        strava_button = ft.OutlinedButton(
            button_text,
            icon=ft.Icons.LINK,
            on_click=self.connect_strava_clicked,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE,
                color=ft.Colors.WHITE,
                side=ft.BorderSide(color=ft.Colors.BLUE),
            )
        )

        # 2. Weekly Stats Dashboard (Totals Only)
        stats_card = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            content=ft.Column([
                ft.Text("THIS WEEK'S TOTALS", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
                ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    controls=[
                        ft.Column([
                            ft.Text(tot_dist, size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                            ft.Text("KM", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),

                        ft.Container(width=1, height=40, bgcolor=ft.Colors.GREY_200),

                        ft.Column([
                            ft.Text(tot_time, size=28, weight=ft.FontWeight.BOLD),
                            ft.Text("TIME", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),

                        ft.Container(width=1, height=40, bgcolor=ft.Colors.GREY_200),

                        ft.Column([
                            ft.Text(runs_count, size=28, weight=ft.FontWeight.BOLD),
                            ft.Text("ACTIVITIES", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    ]
                )
            ])
        )

        # 3. Individual Activities Feed OR Empty State
        feed_column = ft.Column(scroll=ft.ScrollMode.HIDDEN, expand=True, spacing=15)

        record_btn = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.FIBER_MANUAL_RECORD, color=ft.Colors.WHITE),
                ft.Text("RECORD NEW ACTIVITY", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLUE,
            height=50,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25)),
            on_click=self.start_activity
        )

        if not activities_list:
            # Empty State
            feed_column.controls.append(
                ft.Container(
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Container(height=25),
                            ft.Icon(ft.Icons.MAP_OUTLINED, size=80, color=ft.Colors.GREY_300),
                            ft.Text("Ready to crush it?", size=24, weight=ft.FontWeight.BOLD),
                            ft.Text("Track your runs, walks, and rides.", color=ft.Colors.GREY_500, size=14),
                            ft.Container(height=20),
                        ]
                    ),
                    expand=True, alignment=ft.Alignment(0, 0)
                )
            )
        else:
            # Populated History Feed
            feed_column.controls.append(
                ft.Text("ALL RECENT ACTIVITIES", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500)
            )

            # Map the activity types to unique icons!
            icon_map = {
                "Run": ft.Icons.DIRECTIONS_RUN,
                "Walk": ft.Icons.DIRECTIONS_WALK,
                "Cycle": ft.Icons.DIRECTIONS_BIKE
            }

            for act in reversed(activities_list):  # Read newest first
                act_icon = icon_map.get(act["type"], ft.Icons.FITNESS_CENTER)
                feed_column.controls.append(
                    ft.Container(
                        bgcolor=ft.Colors.WHITE,
                        border_radius=10,
                        padding=5,
                        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
                        content=ft.ListTile(
                            leading=ft.Container(
                                content=ft.Icon(act_icon, color=ft.Colors.WHITE),
                                bgcolor=ft.Colors.BLUE_400,
                                padding=10,
                                border_radius=25
                            ),
                            title=ft.Text(f"{act['type']} • {act['date']}", weight=ft.FontWeight.BOLD, size=14),
                            subtitle=ft.Text(f"{act['dist']} km in {act['time']}", color=ft.Colors.GREY_600, size=12),
                        )
                    )
                )

        # 4. Add Navigation Bar
        self.nav_bar = NavBar(page)

        # Main Layout Assembly
        content_column = ft.Column(
            controls=[
                header,
                ft.Container(content=strava_button, padding=ft.padding.symmetric(horizontal=15), margin=ft.margin.only(bottom=16)),
                ft.Container(content=stats_card, padding=ft.padding.symmetric(horizontal=15), margin=ft.margin.only(bottom=16)),
                ft.Container(content=record_btn, padding=ft.padding.symmetric(horizontal=15), margin=ft.margin.only(bottom=16)),
                ft.Container(content=feed_column, padding=ft.padding.symmetric(horizontal=15), expand=True)
            ],
            expand=True
        )

        self.controls = [content_column, self.nav_bar]
        self.expand = True
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN


    # --- DATA CALCULATION & FORMATTING ---
    def load_activity_data(self):
        total_distance = 0.0
        total_runs = 0
        total_seconds = 0
        activities_list = []
        file_path = "../database/activities_history.csv"

        now = datetime.now()
        start_of_week = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

        # load local app-recorded activities
        if os.path.isfile(file_path):
            try:
                with open(file_path, mode="r") as file:
                    reader = csv.reader(file)
                    next(reader)
                    for row in reader:
                        if len(row) >= 3:
                            date_str = row[0]
                            dist = float(row[1])
                            secs = int(row[2])
                            act_type = row[3] if len(row) >= 4 else "Run"

                            run_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")

                            if run_date >= start_of_week:
                                total_distance += dist
                                total_seconds += secs
                                total_runs += 1

                            activities_list.append({
                                "date": run_date.strftime("%b %d, %H:%M"),
                                "dist": f"{dist:.2f}",
                                "time": self.format_time(secs),
                                "type": act_type,
                                "source": "app"
                            })
            except Exception as e:
                print(f"Error reading stats: {e}")

        # load Strava activities for this logged-in user
        try:
            current_user_id = getattr(self.main_page, "user_id", None)
            print("LOAD ACTIVITY PAGE USER ID:", current_user_id)

            if current_user_id is not None:
                strava_activities = get_saved_activities(current_user_id)
                if strava_activities:
                    formatted_strava = format_strava_activities(strava_activities)
                    for act in formatted_strava:
                        act["source"] = "Strava"
                    activities_list.extend(formatted_strava)
        except Exception as e:
            print(f"Error loading Strava activities: {e}")

        tot_time_str = self.format_time(total_seconds)

        return f"{total_distance:.1f}", tot_time_str, str(total_runs), activities_list

    def format_time(self, seconds):
        if seconds == 0:
            return "0s"
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"

    # --- EVENT HANDLERS ---
    def start_activity(self, e):
        self.main_page.go("/map")

    def connect_strava_clicked(self, e):
        try:
            current_user_id = getattr(self.main_page, "user_id", None)
            print("CONNECT BUTTON CLICKED")
            print("PAGE USER ID:", current_user_id)

            if current_user_id is None:
                raise ValueError("No logged-in user found on page.user_id")

            tokens = connect_strava()
            print("TOKENS RETURNED:", tokens)

            save_tokens_for_user(current_user_id, tokens)
            print("TOKENS SAVED TO DB")

            self.main_page.snack_bar = ft.SnackBar(
                content=ft.Text("Strava connected successfully"),
                open=True
            )
            self.main_page.update()

        except Exception as ex:
            print("STRAVA CONNECTION ERROR:", ex)
            self.main_page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Strava connection failed: {ex}"),
                open=True
            )
            self.main_page.update()


def main_activities(page: ft.Page):
    return ActivitiesPage(page)