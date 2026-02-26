import flet as ft
from flet import KeyboardType
#stores total calories
total_calories = 0
def FoodApp():
    #used to display the food and calories when they are entered
    food_list = ft.Column()
    #allows users to enter the food they want to submit
    food_search = ft.TextField(hint_text = "Enter Your Food")
    #allows you to enter the calories of the item, this uses input filter to only allow digits
    calories_search = ft.TextField(hint_text = "Enter Your Calories",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9]*$",replacement_string=""))
    #is used to display the progress towards the users overall calorie goal
    progress_bar = ft.ProgressBar(width = 200, height = 20,value = 0, color = "green")
    #returns all the items in a container to be used on the page
    def add_clicked(e):
        #used to grab global variable total_calories
        global total_calories
        # used to reference progress bar outside of function
        nonlocal progress_bar
        #makes sure both fields have values in them
        if food_search.value != "" and calories_search.value != "":
            #add calories to total
            total_calories = total_calories + int(calories_search.value)
            #updates the progress bar
            progress_bar.value = total_calories/2500
            #retrieves and displays food and calorie values
            display_text = f"{food_search.value} - {calories_search.value}"
            food_list.controls.append(ft.Text(display_text))
            #resets all values and updates all relevant fields.
            food_search.value = ""
            calories_search.value = ""
            food_search.update()
            calories_search.update()
            progress_bar.update()



    return ft.Container(content =ft.Column([food_search,calories_search,
                                            ft.FloatingActionButton("Enter",on_click=add_clicked),progress_bar
                                            ,food_list]))
