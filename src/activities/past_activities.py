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

    # display the stored exercises
    exercise_list = ft.Column()
    # used to enter the exercises
    exercise_search = ft.SearchBar(bar_hint_text="Enter your exercise", controls=search_exercises, expand=True,
                                        on_tap=open_search, on_change=handle_search_change,
                                        view_size_constraints=ft.BoxConstraints(max_height=200, max_width=400))

    enter_past_exercises = ft.Column(controls=[ft.Text("Enter Past Exercises"),exercise_search,
                                                    ])
    return ft.Stack(controls=[enter_past_exercises])