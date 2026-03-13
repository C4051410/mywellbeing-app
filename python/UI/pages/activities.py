import os
import csv
from datetime import datetime, timedelta
import flet as ft

from UI.components.userpfp import Userpfp
from UI.components.bottom_nav import NavBar
from UI.components.responsive import Responsive


class ActivitiesPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.r = Responsive(page)

        # --- LOAD REAL DATA FROM CSV ---
        dist_str, time_str, runs_str = self.calculate_weekly_stats()

        # 1. Page Header
        header = ft.Container(
            content=ft.Text("Activities", size=32, weight=ft.FontWeight.BOLD),
            padding=ft.padding.only(top=20, left=10)
        )

        # 2. Weekly Stats Dashboard
        stats_card = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            content=ft.Column([
                ft.Text("THIS WEEK", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    controls=[
                        # Distance Stat
                        ft.Column([
                            ft.Text(dist_str, size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.DEEP_ORANGE),
                            ft.Text("KM", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),

                        ft.Container(width=1, height=40, bgcolor=ft.Colors.GREY_200),

                        # Time Stat
                        ft.Column([
                            ft.Text(time_str, size=28, weight=ft.FontWeight.BOLD),
                            ft.Text("TIME", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),

                        ft.Container(width=1, height=40, bgcolor=ft.Colors.GREY_200),

                        # Activities Stat
                        ft.Column([
                            ft.Text(runs_str, size=28, weight=ft.FontWeight.BOLD),
                            ft.Text("RUNS", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    ]
                )
            ])
        )

        # 3. Strava-Style Empty State
        record_prompt = ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.MAP_OUTLINED, size=80, color=ft.Colors.GREY_300),
                    ft.Text("Ready to crush it?", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Track your runs, walks, and rides.", color=ft.Colors.GREY_500, size=14),
                    ft.Container(height=30),
                    ft.Button(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.FIBER_MANUAL_RECORD, color=ft.Colors.WHITE),
                                ft.Text("RECORD ACTIVITY", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        bgcolor=ft.Colors.DEEP_ORANGE,
                        width=280,
                        height=60,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)),
                        on_click=self.start_activity
                    )
                ]
            )
        )

        # 4. Add Navigation Bar
        self.nav = NavBar(page)

        self.controls = [header, ft.Container(content=stats_card, padding=ft.padding.symmetric(horizontal=15)),
                         record_prompt, self.nav]
        self.expand = True
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    # --- MONDAY TO SUNDAY DATA CALCULATION ---
    def calculate_weekly_stats(self):
        total_distance = 0.0
        total_runs = 0
        total_seconds = 0
        file_path = "activities_history.csv"

        if not os.path.isfile(file_path):
            return "0.0", "0s", "0"

        now = datetime.now()
        start_of_week = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

        try:
            with open(file_path, mode="r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    if len(row) >= 3:  # Make sure we have Date, Dist, AND Time
                        run_date = datetime.strptime(row[0], "%Y-%m-%d %H:%M")

                        if run_date >= start_of_week:
                            total_distance += float(row[1])
                            total_runs += 1
                            total_seconds += int(row[2])  # Add the real seconds!
        except Exception as e:
            print(f"Error reading stats: {e}")

        # Smart Time Formatter
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if hours > 0:
            time_display = f"{hours}h {minutes}m"
        elif minutes > 0:
            time_display = f"{minutes}m {seconds}s"
        else:
            time_display = f"{seconds}s"  # If under a minute, just show seconds!

        return f"{total_distance:.1f}", time_display, str(total_runs)

    # --- EVENT HANDLERS ---
    def start_activity(self, e):
        # FIX: Updated to official Flet routing command
        self.main_page.go("/map")

def main_activities(page: ft.Page):
    return ActivitiesPage(page)