from datetime import datetime
import flet as ft
from plyer import notification
from activities.activity_queries import  save_past_activities

exercises = [
    "Push-ups",
    "Squats",
    "Lunges",
    "Plank",
    "Burpees",
    "Mountain Climbers",
    "Jumping Jacks",
    "Sit-ups",
    "Crunches",
    "Glute Bridges",
    "Tricep Dips",
    "High Knees",
    "Russian Twists",
    "Leg Raises",
    "Bicycle Crunches",
    "Calf Raises",
    "Supermans",
    "Wall Sit",
    "Hip Thrusts",
    "Side Plank",
]
def main_past_activities(page: ft.Page):
    async def handle_item_selected(e):
        # retrieve the value in the search bar
        exercise_search.value = e.control.data
        # pauses the function until the dropdown closes
        await exercise_search.close_view()
        # updates search bar
        exercise_search.update()

    def handle_search_change(e):
        search_query = e.data.lower()

        filtered_exercises = [
            ex for ex in exercises if search_query in ex.lower()
        ]

        new_controls = [
            ft.ListTile(
                title=ft.Text(ex),
                on_click=handle_item_selected,
                data=ex
            )
            for ex in filtered_exercises
        ]

        # Update the search bar's dropdown content
        exercise_search.controls = new_controls
        exercise_search.update()

    # is used to store and show the exercises in the search bar
    search_exercises = [
        ft.ListTile(title=ft.Text(ex), on_click=handle_item_selected, data=ex)
        for ex in exercises
    ]

    # used to open the search bar
    async def open_search(e):
        # waits for list to appear before
        await exercise_search.open_view()

    def go_back(e):
        page.go("/activities")

    def get_duration():
        h = hours.value
        if h is not None:
            h = int(hours.value)
        else:
            h = 0
        m = minutes.value
        if m is not None:
            m = int(minutes.value)
        else:
            m = 0
        s = seconds.value
        if s is not None:
            s = int(seconds.value)
        else:
            s = 0
        total = h*3600 + m*60 + s
        return total


    def save_and_finish():
        duration_seconds = get_duration()
        if exercise_search.value != "" and calories_input.value != "":
            exercise = exercise_search.value
            calories = calories_input.value
            distance = distance_input.value or None
            reps = reps_input.value or None
            if duration_seconds == None:
                duration_seconds = 0
            start_date = datetime.now()
            save_past_activities(page.user_id,exercise,calories,duration_seconds,reps,distance,start_date)
            notification.notify(
                title = "Activity Logged",
                message = f"{exercise} Recorded",
                app_name = "MyWellBeing"

            )
            page.go("/activities")

    # used to enter the exercises
    exercise_search = ft.SearchBar(bar_hint_text="Enter your exercise", controls=search_exercises, expand=True,
                                        on_tap=open_search, on_change=handle_search_change,
                                        view_size_constraints=ft.BoxConstraints(max_height=200, max_width=400))
    calories_input = ft.TextField(hint_text="Calories",input_filter=ft.InputFilter(allow=True,regex_string=r"^[0-9]*$",replacement_string=""),height=40) # only allow numerical values

    hours = ft.Dropdown(
        label="Hrs",
        width=80,
        height=40,
        text_size= 12,
        label_style=ft.TextStyle(size=8),
        options=[ft.dropdown.Option(str(i)) for i in range(0, 25)]
    )

    minutes = ft.Dropdown(
        label="Mins",
        width=80,
        height=40,
        text_size= 12,
        label_style=ft.TextStyle(size=8),
        options=[ft.dropdown.Option(str(i)) for i in range(0, 60)]
    )

    seconds = ft.Dropdown(
        label="Secs",
        width=80,
        height=40,
        text_size= 12,
        label_style=ft.TextStyle(size=8),
        options=[ft.dropdown.Option(str(i)) for i in range(0, 60)]
    )
    reps_input = ft.TextField(hint_text="Reps",
                                input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$",
                                replacement_string=""), height=40,width=120)
    distance_input = ft.TextField(
                                hint_text="Distance (km)",input_filter=ft.InputFilter(allow=True,regex_string=r"^\d*\.?\d*$",
                                replacement_string=""),height=40,width=120) # only allow numerical values + "."

    duration = ft.Row([hours, minutes, seconds],expand=True)
    reps = ft.Row([ft.Text("Reps (Optional)" ),reps_input],expand=True)
    distance = ft.Row([ft.Text("Distance (Optional)"),distance_input],expand=True)

    save_button = ft.FloatingActionButton(content=ft.Text("FINISH", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                         bgcolor=ft.Colors.RED, width=140,on_click=save_and_finish)
    top_back_button = ft.Container(
        content=ft.FloatingActionButton(
            content=ft.Icon(ft.Icons.ARROW_BACK, color=ft.Colors.BLACK),
            bgcolor=ft.Colors.WHITE,
            on_click=go_back,
            mini=True
        ),
    )
    return ft.Container(
        expand=True,
        padding=ft.padding.all(16),
        content=ft.Column(
            controls=[
                # Header
                ft.Row(
                    controls=[
                        top_back_button,
                        ft.Text("Log Activity", size=28, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=8,
                ),
                ft.Text("Record a past workout", size=13, color=ft.Colors.GREY_500),
                exercise_search,
                calories_input,
                duration,
                reps,
                distance,
                save_button,
            ],
            scroll=ft.ScrollMode.HIDDEN,
            spacing=8,
            expand=True,
        )
    )