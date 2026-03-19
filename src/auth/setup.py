'''
File used for profile setup - users will be redirected here after registration
'''

import flet as ft
from database.user_queries import save_setup

def setupGoalsPage(user_id, on_setup_complete):
    message = ft.Text()

    # user data fields
    age = ft.TextField(label="Age")
    gender = ft.Dropdown(label="Gender", options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female")])
    height = ft.TextField(label="Height (cm)")
    current_weight = ft.TextField(label="Current Weight (kg)")
    goal_weight = ft.TextField(label="Goal Weight (kg)")
    activity_level = ft.Dropdown(label="Activity Level", options=[ft.dropdown.Option("Sedentary: no exercise"),
        ft.dropdown.Option("Light: exercise 1-3 times/week"), ft.dropdown.Option("Moderate: exercise 4-5 times/week"),
                                                                  ft.dropdown.Option("Active: daily exercise")])

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

            # bmr calculations by gender
            if gender.value == "Male":
                bmr = 66.5 + (13.75 * current_weight_val) + (5.003 * height_val) - (6.75 * age_val)
            else:
                bmr = 655.1 + (9.563 * current_weight_val) + (1.850 * height_val) - (4.676 * age_val)

            # calorie calculations based on activity level
            if activity_level.value == "Sedentary: no exercise":
                daily_calories = bmr * 1.2
            elif activity_level.value == "Light: exercise 1-3 times/week":
                daily_calories = bmr * 1.5
            elif activity_level.value == "Moderate: exercise 4-5 times/week":
                daily_calories = bmr * 1.7
            else:
                daily_calories = bmr * 1.9

            # weight loss
            if goal_weight_val < current_weight_val:
                calorie_goal = round(daily_calories - 500)

            # weight gain
            elif goal_weight_val > current_weight_val:
                calorie_goal = round(daily_calories + 300)

            # maintain weight
            else:
                calorie_goal = round(daily_calories)

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
            age, gender, height, current_weight, goal_weight, activity_level,
            ft.ElevatedButton("Continue", on_click=handle_continue),
            message
        ])
    )