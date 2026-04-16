from datetime import datetime, timedelta
import flet as ft

from activities.activity_queries import get_activities
from activities.strava_api import connect_strava, get_saved_activities, format_strava_activities, save_tokens_for_user, load_tokens_for_user
from components.bottom_nav import NavBar
from components.responsive import Responsive

ACTIVITY_DISPLAY = {
    "Run":          {"primary": "dist",     "primary_unit": "km",    "label": lambda act: f"{act['dist']} km in {act['time']}"},
    "Walk":         {"primary": "steps",    "primary_unit": "steps", "label": lambda act: f"{act.get('steps', '—')} steps in {act['time']}"},
    "Cycle":        {"primary": "dist",     "primary_unit": "km",    "label": lambda act: f"{act['dist']} km in {act['time']}"},
    "WeightLifting":{"primary": "calories", "primary_unit": "kcal",  "label": lambda act: f"{act.get('calories', '—')} kcal in {act['time']}"},
    "Workout":      {"primary": "calories", "primary_unit": "kcal",  "label": lambda act: f"{act.get('calories', '—')} kcal in {act['time']}"},
}
DEFAULT_DISPLAY = {"label": lambda act: f"{act['dist']} km in {act['time']}"}

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

        self.strava_button = ft.OutlinedButton(
            button_text,
            icon=ft.Icons.LINK,
            on_click=self.connect_strava_clicked,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.DEEP_ORANGE,
                color=ft.Colors.WHITE,
                side=ft.BorderSide(color=ft.Colors.DEEP_ORANGE),
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
        feed_column = ft.Column(spacing=15)

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



        past_exercises = ft.ElevatedButton(content=ft.Row([
                ft.Icon(ft.Icons.FIBER_MANUAL_RECORD, color=ft.Colors.WHITE),
                ft.Text("RECORD PAST ACTIVITY", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLUE,
            height=50,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25)),
            on_click=self.past_activity
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
                "Cycle": ft.Icons.DIRECTIONS_BIKE,
                "WeightLifting": ft.Icons.FITNESS_CENTER,
            }

            for act in activities_list:
                act_icon = icon_map.get(act["type"], ft.Icons.FITNESS_CENTER)
                act_type = act["type"]
                if act_type == "WeightLifting":
                    parts = []
                    if act.get("calories"):
                        parts.append(f"{act['calories']} kcal")
                    if act.get("heart_rate"):
                        parts.append(f"{act['heart_rate']} bpm avg")
                    parts.append(f" {act['time']}")
                    subtitle_text = " • ".join(parts)
                elif act_type in ("Run", "Cycle"):
                    subtitle_text = f"{act['dist']} km • {act['time'].replace('m', ' mins')}"
                elif act_type == "Walk":
                    subtitle_text = f"{act.get('steps', act['dist'] + ' km')} in {act['time']}"
                elif act_type == "Workout":
                    parts = []
                    if act.get("calories") and int(act["calories"]) > 0:
                        parts.append(f"{act['calories']} kcal")
                        # Only show distance for workouts if it exists and is > 0
                    if act.get("dist") and float(act["dist"]) > 0:
                        parts.append(f"{act['dist']} km")
                        # Only show reps for workouts if it exists and is > 0
                    if act.get("reps") and int(act["reps"]) > 0:
                        parts.append(f"{act['reps']} reps")

                    parts.append(act["time"])
                    subtitle_text = " • ".join(parts)
                else:
                    subtitle_text = act['time']

                feed_column.controls.append(
                    ft.Container(
                        bgcolor=ft.Colors.WHITE,
                        border_radius=10,
                        padding=5,
                        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
                        content=ft.ListTile(
                            leading=ft.Container(
                                width=40,
                                height=40,
                                content=ft.Stack(
                                    controls=[
                                        # activity icon background
                                        ft.Container(
                                            width=40,
                                            height=40,
                                            bgcolor=ft.Colors.BLUE_400,
                                            border_radius=20,
                                            alignment=ft.alignment.Alignment(0, 0),
                                            content=ft.Icon(
                                                act_icon,
                                                color=ft.Colors.WHITE,
                                                size=20
                                            ),
                                        ),

                                        # only show strava badge for imported activities
                                        ft.Container(
                                            visible=(act.get("source") == "Strava"),
                                            alignment=ft.alignment.Alignment(1, 1),
                                            content=ft.Container(
                                                width=16,
                                                height=16,
                                                border_radius=7,
                                                bgcolor=ft.Colors.WHITE,
                                                padding=2,
                                                content=ft.Image(
                                                    width=22,
                                                    height=22,
                                                    src="strava.png",
                                                    fit="cover",
                                                    margin=ft.margin.all(-3),
                                                ),
                                            ),
                                        ),

                                    ]
                                )
                            ),
                            title=ft.Text(f"{act['title']} • {act['date']}", weight=ft.FontWeight.BOLD, size=13, max_lines=1),
                            subtitle=ft.Text(subtitle_text, color=ft.Colors.GREY_600, size=12),
                        )
                    )
                )

        # 4. Add Navigation Bar
        self.nav_bar = NavBar(page)

        # Main Layout Assembly
        content_column = ft.Column(
            controls=[
                header,
                ft.Container(content=self.strava_button, padding=ft.padding.symmetric(horizontal=15), margin=ft.margin.only(bottom=16)),
                ft.Container(content=stats_card, padding=ft.padding.symmetric(horizontal=15), margin=ft.margin.only(bottom=16)),
                ft.Container(content=record_btn, padding=ft.padding.symmetric(horizontal=15), margin=ft.margin.only(bottom=16)),
                ft.Container(content=past_exercises,padding=ft.padding.symmetric(horizontal=15), margin=ft.margin.only(bottom=16)),
                ft.Container(content=feed_column, padding=ft.padding.symmetric(horizontal=15), expand=True)
            ],
            scroll=ft.ScrollMode.AUTO,
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

        now = datetime.now()
        start_of_week = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

        # load locally recorded activities
        try:
            current_user_id = getattr(self.main_page, "user_id", None)
            print("LOAD ACTIVITY PAGE USER ID:", current_user_id)

            if current_user_id is not None:
                rows = get_activities(current_user_id)
                for title,activity_type, distance_km, start_date, duration_seconds,calories,reps, source in rows:
                    dist = float(distance_km or 0)
                    secs = int(duration_seconds or 0)
                    cal = int(calories or 0)
                    reps = int(reps or 0)

                    if start_date and start_date >= start_of_week:
                        total_distance += dist
                        total_seconds += secs
                        total_runs += 1

                    activities_list.append({
                        "title": title,
                        "date": start_date.strftime("%b %d, %H:%M") if start_date else "No date",
                        "datetime": start_date,
                        "dist": f"{dist:.2f}",
                        "time": self.format_time(secs),
                        "type": activity_type or "Run",
                        "source": source or "app",
                        "calories": f"{cal:}",
                        "reps": f"{reps:}"
                    })
        except Exception as e:
            print(f"Error reading DB activities: {e}")

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

                        # adds strava activities to weekly totals
                        if act.get("datetime") and act["datetime"] >= start_of_week:
                            total_distance += float(act.get("dist") or 0)
                            total_seconds += int(act.get("seconds") or 0)
                            total_runs += 1

                    activities_list.extend(formatted_strava)
        except Exception as e:
            print(f"Error loading Strava activities: {e}")

        tot_time_str = self.format_time(total_seconds)

        # sort activities by time new to old
        activities_list.sort(key=lambda x: x["datetime"] or datetime.min, reverse=True)
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

    def past_activity(self, e):
        self.main_page.go("/past_activities")

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
            # update strava button text
            self.strava_button.text = "Strava Connected"
            self.strava_button.disabled = True

            self.main_page.snack_bar = ft.SnackBar(
                content=ft.Text("Strava connected successfully"),
                open=True
            )

            self.main_page.update()
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