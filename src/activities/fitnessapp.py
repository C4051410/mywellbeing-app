import flet as ft
from database.user_queries import get_user, user_calories
from components.bottom_nav import NavBar
from components.userpfp import Userpfp

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
    "Running",
    "Walking"
]


def FitnessApp(page, user_id):
    user_data = get_user(user_id) # loads user data
    # loads users calorie goal and todays existing calories
    calorie_goal = user_data[10] or 0
    total_calories = user_data[6]or 0

    #used to create drop down menu for the search bar
    async def handle_change(e):
        #retrieve the value in the search bar
        exercise_search.value = e.control.data
        #pauses the function until the dropdown closes
        await exercise_search.close_view()
        #updates search bar
        exercise_search.update()
    #is used to store and show the exercises in the search bar
    search_exercises =[
        ft.ListTile(title=ft.Text(ex),on_click=handle_change,data=ex)
        for ex in exercises
    ]
    #used to open the search bar
    async def open_search(e):
        #waits for list to appear before
        await exercise_search.open_view()
    #display the stored exercises
    exercise_list = ft.Column()
    #used to enter the exercises
    exercise_search = ft.SearchBar(bar_hint_text="Enter your exercise",controls=search_exercises,expand=True,on_tap=open_search,on_change=handle_change)
    #used to enter the calories
    calories_search = ft.TextField(hint_text="Enter your calories",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9]*$",replacement_string=""))
    #set calorie goals
    calorie_set = ft.TextField(hint_text="Enter your calories",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9]*$",replacement_string=""))
    #used to display calorie goal
    calories_text = ft.Text(f"{total_calories} / {calorie_goal}", size=12, weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_400)
    calories_ring = ft.ProgressBar(width=200, height=16, color=ft.Colors.DEEP_ORANGE,
                                   value=(total_calories / calorie_goal) if calorie_goal else 0)

    #used to set goal
    set_goal_btn = ft.ElevatedButton("Set Goal")
    #used to set on_click before container using lambda
    set_goal_btn.on_click = lambda e: open_dlg(e)

    def save_goal(e):
        nonlocal calorie_goal
        #checks that calorie_set is not empty or 0
        if calorie_set.value != "" and calorie_set.value != 0:
            #sets calorie_goal and hides button
            calorie_goal = int(calorie_set.value)
            set_goal_btn.visible = False
            dlg.open = False
            e.page.update()


    #creates alertdialog that allows to set goal
    dlg = ft.AlertDialog(title="Enter Your Goal",
                         content=ft.Column([
                             ft.Text("Please enter your goal"),calorie_set,

                         ],),actions=[ft.ElevatedButton("Save",on_click=save_goal)])
    #used to open dialog option when clicked
    def open_dlg(e):
        #add it to front of page and updates it
        e.page.overlay.append(dlg)
        dlg.open = True
        e.page.update()
    #add fitness goals and add them to page
    def add_fitness(e):
        nonlocal total_calories
        #makes sure the two fields aren't blank
        if exercise_search.value != "" and calories_search.value != "":
            calories = int(calories_search.value)
            #add expansion_tile to display the exercise and number calories
            exercise_list.controls.append(ft.ExpansionTile(width=300,title=exercise_search.value,expanded=True,
                                                           controls=[ft.ListTile(title=ft.Text("Calories"),
                                                                                 subtitle=ft.Text(calories_search.value),
                                                                                 )]))
            #adds to total calories
            total_calories += int(calories_search.value)
            #adds to calorie_ring
            calories_ring.value = total_calories/calorie_goal if calorie_goal else 0
            #updates all values and page
            exercise_search.value = ""
            calories_search.value = ""
            exercise_search.update()
            calories_search.update()
            calories_ring.update()

    header = ft.Container(
        content=ft.Row(
            controls=[ft.Text("Fitness", size=32, weight=ft.FontWeight.BOLD), Userpfp(page)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

    nav_bar = NavBar(page)
    scrollable = ft.Column(
    controls = [header, exercise_search, calories_search,
                ft.ElevatedButton("Log Exercise", on_click=add_fitness, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
                calories_text, calories_ring, exercise_list, set_goal_btn],
    expand = True, scroll = ft.ScrollMode.HIDDEN, spacing = 12
    )
    return ft.Column(
        controls=[scrollable, nav_bar],
        expand=True,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )