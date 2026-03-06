import flet as ft

from components.userpfp import Userpfp
from components.bottom_nav import navBar
from components.responsive import Responsive


class ActivitiesPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.r = Responsive(page)

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
                            ft.Text("14.2", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.DEEP_ORANGE),
                            ft.Text("KM", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),

                        ft.Container(width=1, height=40, bgcolor=ft.Colors.GREY_200),  # Visual Divider

                        # Time Stat
                        ft.Column([
                            ft.Text("1h 12m", size=28, weight=ft.FontWeight.BOLD),
                            ft.Text("TIME", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),

                        ft.Container(width=1, height=40, bgcolor=ft.Colors.GREY_200),  # Visual Divider

                        # Activities Stat
                        ft.Column([
                            ft.Text("3", size=28, weight=ft.FontWeight.BOLD),
                            ft.Text("RUNS", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    ]
                )
            ])
        )

        # 3. Strava-Style Empty State / Prompt (Centered)
        record_prompt = ft.Container(
            expand=True,  # Pushes the nav bar to the bottom
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.MAP_OUTLINED, size=80, color=ft.Colors.GREY_300),
                    ft.Text("Ready to crush it?", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Track your runs, walks, and rides.", color=ft.Colors.GREY_500, size=14),

                    ft.Container(height=30),  # Spacer

                    # Centered Big Orange Record Button
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

        # 4. Add the reusable bottom navigation bar
        self.nav = navBar(page)

        # Assemble the page layout
        self.controls = [
            header,
            ft.Container(content=stats_card, padding=ft.padding.symmetric(horizontal=15)),
            record_prompt,
            self.nav
        ]

        self.expand = True
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        # --- Event Handlers ---

    async def start_activity(self, e):
        await self.main_page.push_route("/map")


def main_activities(page: ft.Page):
    activities_page = ActivitiesPage(page)
    return activities_page