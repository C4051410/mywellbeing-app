import flet as ft

total_calories = 0
calorie_goal = 1500
def FitnessApp():
    exercise_list = ft.Column()
    exercise_search = ft.SearchBar(bar_hint_text="Enter your exercise")
    calories_search = ft.TextField(hint_text="Enter your calories",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9]*$",replacement_string=""))
    enter_calorie = ft.TextField(hint_text="Enter your calories",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9]*$",replacement_string=""))
    calories_ring = ft.ProgressRing(value=0,color="red")
    set_goal_btn = ft.Button("Set Goal")
    set_goal_btn.on_click = lambda e: open_dlg(e)

    def save_goal(e):
        global calorie_goal
        if enter_calorie.value != "" and enter_calorie.value != 0:
            calorie_goal = int(enter_calorie.value)
            set_goal_btn.visible = False
            dlg.open = False
            e.page.update()



    dlg = ft.AlertDialog(title="Enter Your Goal",
                         content=ft.Column([
                             ft.Text("Please enter your goal"),enter_calorie,

                         ],),actions=[ft.ElevatedButton("Save",on_click=save_goal)])

    def open_dlg(e):
        e.page.overlay.append(dlg)
        dlg.open = True
        e.page.update()

    def add_clicked(e):
        global total_calories
        nonlocal calories_ring
        if exercise_search.value != "" and calories_ring.value != "":
            display_text = f" Exercise {exercise_search.value}-{calories_search.value} calories"
            exercise_list.controls.append(ft.Text(display_text))
            total_calories += int(calories_search.value)
            calories_ring.value = total_calories/calorie_goal
            exercise_search.value = ""
            calories_search.value = ""
            exercise_search.update()
            calories_search.update()
            calories_ring.update()

    return ft.Container(content=ft.Column([exercise_search,calories_search,
                                           ft.FloatingActionButton("Enter",on_click=add_clicked),
                                           calories_ring,exercise_list,set_goal_btn]))