import flet as ft
from flet import KeyboardType
#stores total calories
total_calories = 0
calorie_goal = 0
def FoodApp():
    #used to display the food and calories when they are entered
    food_list = ft.Column()
    #allows users to enter the food they want to submit
    food_search = ft.TextField(hint_text = "Enter Your Food")
    #allows you to enter the calories of the item, this uses input filter to only allow digits
    calories_search = ft.TextField(hint_text = "Enter Your Calories",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9]*$",replacement_string=""))
    #allows user to enter goals
    enter_goal = ft.TextField(hint_text = "Enter Your Goal",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9]*$",replacement_string=""))
    #is used to display the progress towards the users overall calorie goal
    progress_bar = ft.ProgressBar(width = 200, height = 20,value = 0, color = "green")
    #used to create a button to set goal
    set_goal_btn = ft.ElevatedButton("Set Goal")
    #used to set on_click before container using lambda
    set_goal_btn.on_click = lambda e: open_dlg(e)

    #used to save the calorie goal
    def save_goal(e):#
        global calorie_goal
        #checks that value isn't empty or 0
        if enter_goal.value != "" and enter_goal.value != "0":
            #store value as int and closes dialog box
            calorie_goal = int(enter_goal.value)
            #hide button after being entered
            set_goal_btn.visible = False
            # closes dialog box and updates page
            dlg.open = False
            e.page.update()
    #creates dialog box for entering calorie goal
    dlg = ft.AlertDialog(title = "Enter Your Calorie Count",
                         #creates text and provides enter option
                         content = ft.Column([
                             ft.Text("Please Enter Your Calorie Count"),enter_goal,]),
                         #saves option using save_goal
                         actions=[ft.ElevatedButton("Save",on_click=save_goal)])
    #is used to open the dialog box
    def open_dlg (e):
        e.page.overlay.append(dlg)
        dlg.open = True
        e.page.update()



    #returns all the items in a container to be used on the page
    def add_food(e):
        #used to grab global variable total_calories
        global total_calories
        global calorie_goal
        # used to reference progress bar outside of function
        nonlocal progress_bar
        #makes sure both fields have values in them
        if food_search.value != "" and calories_search.value != "" and calorie_goal != 0:
            #add calories to total
            total_calories = total_calories + int(calories_search.value)
            #updates the progress bar
            progress_bar.value = total_calories/calorie_goal
            #retrieves and displays food and calorie values
            display_text = f"{food_search.value} - {calories_search.value}"
            food_list.controls.append(ft.Text(display_text))
            #resets all values and updates all relevant fields.
            food_search.value = ""
            calories_search.value = ""
            food_search.update()
            calories_search.update()
            progress_bar.update()



    return ft.Container(content =ft.Column([
                                            food_search,calories_search,
                                            ft.FloatingActionButton("Enter",on_click=add_food),progress_bar
                                            ,food_list,set_goal_btn
    ]))
