import csv
import difflib
import os
from datetime import date

from plyer import notification

from nutrition.nutrition_queries import save_foodlog
import flet as ft

def main_foodlog(page:ft.Page):
    food_db = {}
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, 'foods.csv')
    try:
        with open(csv_path,mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                food_db[row['name'].lower()] = row
    except FileNotFoundError:
        print('foods.csv does not exist')

    def go_back(e):
        page.go("/nutrition")

    def find_food_values(e):
        search_query = food_input.value.strip().lower()
        page.overlay.clear()
        if search_query in food_db:
            data = food_db[search_query]
            calories_input.value = str(data['calories'])
            salts_input.value = str(data['salts'])
            proteins_input.value = str(data['proteins'])
            calories_input.update()
            salts_input.update()
            proteins_input.update()
            page.overlay.append(ft.SnackBar(
                content=ft.Text(f"Found values for '{data['name']}'"),
                bgcolor=ft.Colors.BLUE_400,
                open=True
            ))
            page.update()
        elif len(search_query) > 2:
            matches = difflib.get_close_matches(search_query,list(food_db.keys()),n=1,cutoff=0.6)
            if matches:
                suggestion = matches[0]
                page.overlay.append(ft.SnackBar(
                    content=ft.Text(f"Did You Mean '{suggestion}'?"),
                    action = "Yes!",
                    on_action = lambda _: apply_suggestion(suggestion),
                    bgcolor=ft.Colors.BLUE_400,
                    open=True
                ))
            page.update()
        else:
            pass
    def apply_suggestion(suggestion):
        food_input.value = suggestion.title()
        find_food_values(suggestion)
        food_input.update()

    def save_and_finish(e):
        food = food_input.value
        calories = calories_input.value
        salts = salts_input.value
        proteins = proteins_input.value
        mealtype = meal_type.value

        if not all([food, calories, salts, proteins, mealtype]):
            page.overlay.append(ft.SnackBar(
                content=ft.Text("Please Fill in All Fields"),
                bgcolor=ft.Colors.RED_400,
                open=True
            ))
            page.update()
            return
        save_foodlog(food, calories, salts, proteins,str(date.today()),mealtype,page.user_id)
        page.overlay.append(ft.SnackBar(
            content=ft.Text("Food Logged"),
            bgcolor=ft.Colors.GREEN_400,
            open=True
        ))
        notification.notify(
            title="Food Log Logged",
            message=f"{food} Recorded",
            app_name="MyWellBeing"

        )
        page.update()
        page.go("/nutrition")
    food_input = ft.TextField(hint_text ="Enter Food Name",height=40,on_blur=find_food_values)
    calories_input = ft.TextField(
        hint_text="Calories",
        input_filter=ft.InputFilter(allow=True,regex_string=r"^[0-9]*$",replacement_string=""),
        height=40
    )
    salts_input = ft.TextField(
        hint_text="Salts (g)",
        input_filter=ft.InputFilter(allow=True,regex_string=r"^\d*\.?\d*$",replacement_string=""),
        height=40
    )
    proteins_input = ft.TextField(
        hint_text="Proteins (g)",
        input_filter=ft.InputFilter(allow=True,regex_string=r"^\d*\.?\d*$",replacement_string=""),
        height=40
    )
    meal_type = ft.Dropdown(
        hint_text="Meal Type",
        options=[
            ft.DropdownOption(key="Breakfast",text="Breakfast"),
            ft.DropdownOption(key="Lunch",text="Lunch"),
            ft.DropdownOption(key="Dinner",text="Dinner"),
            ft.DropdownOption(key="Snack",text="Snack")
        ]
    )
    back_button = ft.Container(
        content=ft.FloatingActionButton(
            content=ft.Icon(ft.Icons.ARROW_BACK, color=ft.Colors.BLACK),
            bgcolor=ft.Colors.WHITE,
            on_click=go_back,
            mini=True
        ),
    )
    save_button = ft.FloatingActionButton(
        content=ft.Text("LOG FOOD"),
        bgcolor=ft.Colors.GREEN_400,
        width=140,
        on_click=save_and_finish,

    )
    return ft.Column(
        controls=[
            back_button,
            ft.Text("Enter Food Name"),
            food_input,
            ft.Text("Calories"),
            calories_input,
            ft.Text("Salts"),
            salts_input,
            ft.Text("Proteins"),
            proteins_input,
            ft.Text("Meal Type"),
            meal_type,
            save_button,
        ],
        width = 300,
        scroll = ft.ScrollMode.AUTO
    )

