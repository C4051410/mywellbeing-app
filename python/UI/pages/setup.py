'''
File used for profile setup - users will be redirected here after registration
'''

import flet as ft
from database.queries import save_setup

def setupGoalsPage(user_id, on_setup_complete):
    message = ft.Text()

    # user data fields
    age = ft.TextField(label="Age")
    gender = ft.Dropdown(label="Gender", options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female")])
    height = ft.TextField(label="Height (cm)")
    current_weight = ft.TextField(label="Current Weight (kg)")
    goal_weight = ft.TextField(label="Goal Weight (kg)")

    def handle_continue(e):
        if not all([age.value, gender.value, height.value, current_weight.value, goal_weight.value]):
            message.value = "Please fill in all fields"
            e.page.update()
            return

        try:
            # converting text values into integers for calculations
            age_val = int(age.value)
            height_val = float(height.value)
            current_weight_val = float(current_weight.value)
            goal_weight_val = float(goal_weight.value)

            # input validation
            if age_val < 13 or age_val > 100:
                message.value = "Age must be between 13 and 100"
                e.page.update()
                return

            if height_val < 100 or height_val > 300:
                message.value = "Height must between 100cm and 300cm"
                e.page.update()
                return

            if current_weight_val <= 0 or goal_weight_val <= 0:
                message.value = "Weight must be greater than 0"
                e.page.update()
                return

            # TODO: calculate calories correctly
            calorie_goal = 2000

            # save and store users setup data
            save_setup(user_id, age_val, gender.value, height_val, current_weight_val, goal_weight_val, calorie_goal)
            on_setup_complete(user_id, age_val, gender.value, height_val, current_weight_val, goal_weight_val)

        except ValueError:
            message.value = "Please enter valid numbers"
            e.page.update()

    return ft.Container(
        content=ft.Column([
            ft.Text("Set Up Your Goals", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Enter your details to calculate your calorie goal"),
            age, gender, height, current_weight, goal_weight,
            ft.ElevatedButton("Continue", on_click=handle_continue),
            message
        ])
    )