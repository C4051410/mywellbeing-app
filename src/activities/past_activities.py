from datetime import datetime
import flet as ft
from activities.activity_queries import save_activity
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

    # used to enter the exercises
    exercise_search = ft.SearchBar(bar_hint_text="Enter your exercise", controls=search_exercises, expand=True,
                                        on_tap=open_search, on_change=handle_search_change,
                                        view_size_constraints=ft.BoxConstraints(max_height=200, max_width=400))
    calories_input = ft.TextField(hint_text="Calories",input_filter=ft.InputFilter(allow=True,regex_string=r"^[0-9]*$",replacement_string=""),height=40) # only allow numerical values

    hours = ft.Dropdown(
        label="Hrs",
        width=60,
        height=40,
        text_size= 8,
        label_style=ft.TextStyle(size=8),
        options=[ft.dropdown.Option(str(i)) for i in range(0, 25)]
    )

    minutes = ft.Dropdown(
        label="Mins",
        width=60,
        height=40,
        text_size= 8,
        label_style=ft.TextStyle(size=8),
        options=[ft.dropdown.Option(str(i)) for i in range(0, 60)]
    )

    seconds = ft.Dropdown(
        label="Secs",
        width=60,
        height=40,
        text_size= 8,
        label_style=ft.TextStyle(size=8),
        options=[ft.dropdown.Option(str(i)) for i in range(0, 60)]
    )
    reps_input = ft.TextField(hint_text="Reps",
                                input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$",
                                replacement_string=""), height=40,width=120)
    distance_input = ft.TextField(
                                hint_text="Distance",input_filter=ft.InputFilter(allow=True,regex_string=r"^\d*\.?\d*$",
                                replacement_string=""),height=40,width=120) # only allow numerical values + "."

    duration = ft.Row([ft.Text("Time (Optional)"),hours, minutes, seconds],expand=True)
    reps = ft.Row([ft.Text("Reps (Optional)" ),reps_input],expand=True)
    distance = ft.Row([ft.Text("Distance (Optional)"),distance_input],expand=True)

    save_activity = ft.FloatingActionButton(content=ft.Text("FINISH", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                         bgcolor=ft.Colors.RED, width=140)


    enter_past_exercises = ft.Column(controls=[exercise_search,
                                                calories_input,duration,reps,distance,save_activity])
    return ft.Column(controls=[enter_past_exercises],width=300)