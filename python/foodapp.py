import flet as ft
from flet import KeyboardType, ExpansionPanel

#stores total calories
total_calories = 0
total_salts = 0
total_proteins = 0
calorie_goal = 0
salt_goal = 0
protein_goal = 0
def FoodApp():
    #used to display the food and calories when they are entered
    food_list = ft.Column()
    #allows users to enter the food they want to submit
    food_search = ft.TextField(hint_text = "Enter Your Food")
    #allows you to enter the calories of the item, this uses input filter to only allow digits
    calories_search = ft.TextField(hint_text = "Enter Your Calories",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9]*$",replacement_string=""))
    #allows you to enter salt count of the item
    salt_search = ft.TextField(hint_text = "Enter Your Salt",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9].*$",replacement_string=""))
    #allows you to enter the protein of the item
    protein_search = ft.TextField(hint_text = "Enter Your Protein",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9].*$",replacement_string=""))
    #allows user to enter goals
    enter_calorie = ft.TextField(hint_text = "Enter Your Calorie Goal",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9]*$",replacement_string=""))
    enter_salt = ft.TextField(hint_text = "Enter Your Salt Goal",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9].*$",replacement_string=""))
    enter_protein = ft.TextField(hint_text ="Enter Your Protein Goal", input_filter = ft.InputFilter(allow=True,regex_string="^[0-9].*$",replacement_string=""))
    #is used to display the progress towards the users overall calorie goal
    calorie_bar = ft.ProgressBar(width = 200, height = 20,value = 0, color = "green")
    salt_bar = ft.ProgressBar(width = 200, height = 20,value = 0, color = "blue")
    protein_bar = ft.ProgressBar(width = 200, height = 20,value = 0, color = "red")
    #used to create a button to set goal
    set_goal_btn = ft.ElevatedButton("Set Goal")
    #used to set on_click before container using lambda
    set_goal_btn.on_click = lambda e: open_dlg(e)

    #used to save the calorie goal
    def save_goal(e):#
        global calorie_goal
        global salt_goal
        global protein_goal
        #checks that value isn't empty or 0
        if enter_calorie.value != "" and enter_calorie.value != "0"\
                and enter_salt.value != "" and enter_salt.value != "0"\
                and enter_protein.value != "" and enter_protein.value != "0":
            #store value as int and closes dialog box
            calorie_goal = int(enter_calorie.value)
            salt_goal = float(enter_salt.value)
            protein_goal = float(enter_protein.value)
            #hide button after being entered
            set_goal_btn.visible = False
            # closes dialog box and updates page
            dlg.open = False
            e.page.update()
    #creates dialog box for entering calorie goal
    dlg = ft.AlertDialog(title = "Enter Your Calorie Count",
                         #creates text and provides enter option
                         content = ft.Column([
                             ft.Text("Please Enter Your Calorie Count"),enter_calorie,
                                ft.Text("Please Enter Your Salt Count"),enter_salt,
                                ft.Text("Please Enter Your Protein Count"),enter_protein,]),
                         #saves option using save_goal
                         actions=[ft.ElevatedButton("Save",on_click=save_goal)])
    #is used to open the dialog box
    def open_dlg (e):
        e.page.overlay.append(dlg)
        dlg.open = True
        e.page.update()



    #returns all the items in a container to be used on the page
    def add_food(e):
        #used to grab global variable
        global total_calories
        global calorie_goal
        global salt_goal
        global protein_goal
        global total_proteins
        global total_salts
        # used to reference progress bars outside of function
        nonlocal calorie_bar
        nonlocal salt_bar
        nonlocal protein_bar
        #makes sure both fields have values in them
        if food_search.value != "" and calories_search.value != "" and calorie_goal != 0\
                and salt_search.value != "" and salt_goal != 0 and protein_search.value != "" and protein_goal != 0:
            #add calories, salt and protein to total
            total_calories = total_calories + int(calories_search.value)
            total_salts = total_salts + float(salt_search.value)
            total_proteins = total_proteins + float(protein_search.value)
            #updates the progress bar
            calorie_bar.value = total_calories/calorie_goal
            salt_bar.value = total_salts/salt_goal
            protein_bar.value = total_proteins/protein_goal
            #retrieves and displays food and calorie values
            display_text = f"{food_search.value} - {calories_search.value}"
            food_list.controls.append(ft.ExpansionTile(width=300,title=food_search.value,expanded=True,
                                                       controls=[ft.ListTile(title=ft.Text("Calories"),
                                                                             subtitle=ft.Text(calories_search.value),),
                                                                 ft.ListTile(title=ft.Text("Salt"),subtitle=ft.Text(salt_search.value),),
                                                                 ft.ListTile(title=ft.Text("Protein"),subtitle=ft.Text(protein_search.value),),
                                                                 ]))
            #resets all values and updates all relevant fields.
            food_search.value = ""
            calories_search.value = ""
            salt_search.value = ""
            protein_search.value = ""
            food_search.update()
            calories_search.update()
            salt_search.update()
            protein_search.update()
            calorie_bar.update()
            salt_bar.update()
            protein_bar.update()
            e.page.update()



    return ft.Container(content =ft.Column([
                                            food_search,calories_search,salt_search,protein_search,
                                            ft.FloatingActionButton("Enter",on_click=add_food),ft.Text("Calories"),calorie_bar
                                            ,ft.Text("Salts"),salt_bar,ft.Text("Proteins"),protein_bar,food_list,set_goal_btn,
    ]))
