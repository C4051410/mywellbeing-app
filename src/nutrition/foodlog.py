"""
    This module is used to create the food logs by displaying the user
    with a range of options to provide nutritional values for each food
    as it also contains a database of common foods with pre-stored values
"""
import csv
import os
from datetime import date
import flet as ft
from nutrition.nutrition_services import search_food_db, save_foodlog


def main_foodlog(page:ft.Page):
    #used to store food db
    food_db = {}
    #tries to find location of db
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, 'foods.csv')
    #tries to open file and extract content, if not fails
    try:
        with open(csv_path,mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                food_db[row['name'].lower()] = row
    except FileNotFoundError:
        print('foods.csv does not exist')
    #allows user to go back to nutrition
    def go_back(e):
        page.go("/nutrition")

    #used to try and find value in db
    def find_food_values(e):
        #strip each value and lowercase it
        search_query = food_input.value.strip().lower()
        #use function to return matchtype and value
        match_type, values = search_food_db(search_query,food_db)
        #if either None then not in db and returns
        if match_type == None or values == None:
            return
        page.overlay.clear()
        #if match_type exact, returns values stored in db and alerts user
        if match_type == "exact":
            data = values
            calories_input.value = str(data['calories'])
            salts_input.value = str(data['salts'])
            proteins_input.value = str(data['proteins'])
            fats_input.value = str(data.get('fats'))
            carbs_input.value = str(data.get('carbs'))
            calories_input.update()
            salts_input.update()
            proteins_input.update()
            carbs_input.update()
            fats_input.update()
            page.overlay.append(ft.SnackBar(
                content=ft.Text(f"Found values for '{data['name']}'"),
                bgcolor=ft.Colors.BLUE_400,
                open=True
            ))
            page.update()
        #if suggestion, it produces a snackbar asking the user if they meant ___
        if match_type == "suggestion":
            page.overlay.append(ft.SnackBar(
                content=ft.Text(f"Did You Mean '{values}'?"),
                action = "Yes!",
                on_action = lambda _: apply_suggestion(values),
                bgcolor=ft.Colors.BLUE_400,
                open=True
            ))
            page.update()
        else:
            pass
    #used to add suggestion values to fields
    def apply_suggestion(suggestion):
        food_input.value = suggestion.title()
        find_food_values(suggestion)
        food_input.update()
    #used to save foodlog
    def save_and_finish(e):
        food = food_input.value
        calories = calories_input.value
        salts = salts_input.value
        proteins = proteins_input.value
        mealtype = meal_type.value
        fats = fats_input.value
        carbohydrates = carbs_input.value

        calories = int(calories) if calories else 0.0
        salts = float(salts) if salts else 0.0
        proteins = float(proteins) if proteins else 0.0
        fats = float(fats) if fats else 0.0
        carbohydrates = float(carbohydrates) if carbohydrates else 0.0

        #retrievs all values from fields and tries to save
        success,message = save_foodlog(food, calories, salts, proteins, fats, carbohydrates, date.today(),mealtype,page.user_id)
        #if failed, will return snack bar with problem
        if success == False:
            page.overlay.append(ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.RED_400,
                open=True
            ))
            page.update()
            return
        #else will return with green snackbar
        else:
            page.overlay.append(ft.SnackBar(
                content=ft.Text("Food Logged"),
                bgcolor=ft.Colors.GREEN_400,
                open=True
            ))
            page.update()
            #sends user back to nutrition
            page.go("/nutrition")
    #creates the different textfield, this is used for entering food and trying to find suggestions
    food_input = ft.TextField(hint_text ="Enter Food Name",height=40,on_blur=find_food_values)
    #only allows integers to be typed
    calories_input = ft.TextField(
        hint_text="Calories",
        input_filter=ft.InputFilter(allow=True,regex_string=r"^[0-9]*$",replacement_string=""),
        height=40
    )
    #only allows floats or ints to be typed
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
    fats_input = ft.TextField(
        hint_text="Fats (g)",
        input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*\.?\d*$", replacement_string=""),
        height=40
    )
    carbs_input = ft.TextField(
        hint_text="Carbs (g)",
        input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*\.?\d*$", replacement_string=""),
        height=40
    )
    #gives a selection of options
    meal_type = ft.Dropdown(
        hint_text="Meal Type",
        options=[
            ft.DropdownOption(key="Breakfast",text="Breakfast"),
            ft.DropdownOption(key="Lunch",text="Lunch"),
            ft.DropdownOption(key="Dinner",text="Dinner"),
            ft.DropdownOption(key="Snack",text="Snack")
        ]
    )
    #back button allows users to return back to nutrition
    back_button = ft.Container(
        content=ft.FloatingActionButton(
            content=ft.Icon(ft.Icons.ARROW_BACK, color=ft.Colors.BLACK),
            bgcolor=ft.Colors.WHITE,
            on_click=go_back,
            mini=True
        ),
    )
    #allows users to save food
    save_button = ft.FloatingActionButton(
        content=ft.Text("LOG FOOD"),
        bgcolor=ft.Colors.GREEN_400,
        width=140,
        on_click=save_and_finish,

    )
    #returns all of this in a column
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
            ft.Text("Fats"),
            fats_input,
            ft.Text("Carbohydrates"),
            carbs_input,
            ft.Text("Meal Type"),
            meal_type,
            save_button,
        ],
        width = 300,
        scroll = ft.ScrollMode.AUTO
    )

