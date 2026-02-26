import flet as ft
from flet import KeyboardType


def FoodApp():
    #used to display the food and calories when they are entered
    food_list = ft.Column()
    #allows users to enter the food they want to submit
    food_search = ft.TextField(hint_text = "Enter Your Food")
    #allows you to enter the calories of the item, this uses input filter to only allow digits
    calories_search = ft.TextField(hint_text = "Enter Your Calories",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9]*$",replacement_string=""))
    #is used to display the progress towards the users overall calorie goal
    progress_bar = ft.ProgressBar(width = 200, height = 20,value = 0.5, color = "green")
    #returns all the items in a container to be used on the page
    return ft.Container(content =ft.Column([food_list,food_search,calories_search,ft.ElevatedButton("Enter"),progress_bar]))
