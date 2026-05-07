'''
File used for profile setup - users will be redirected here after registration
'''

import flet as ft
from auth.auth_services import save_setup, save_session


def setupGoalsPage(user_id, on_setup_complete):
    message = ft.Text()
    def fail_snackbar(message, e):
        e.page.overlay.clear()
        e.page.overlay.append(ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.RED_400,
            open=True
        ))
        e.page.update()
    def success_snackbar(message,e):
        e.page.overlay.clear()
        e.page.overlay.append(ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.GREEN_400,
            open = True
        ))
    #only allow integer values
    age = ft.TextField(label="Age",input_filter=ft.InputFilter(allow=True,regex_string=r"^[0-9]*$",replacement_string=""))
    #provide dropdown option of different genders
    gender = ft.Dropdown(label="Gender", options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female"),ft.dropdown.Option("Non-Binary"), ft.dropdown.Option("Other")])
    height = ft.TextField(label="Height (cm)",input_filter=ft.InputFilter(allow=True,regex_string=r"^[0-9]*$",replacement_string=""))
    #only allow integers and "."
    current_weight = ft.TextField(label="Current Weight (kg)",input_filter=ft.InputFilter(allow=True,regex_string=r"^\d*\.?\d*$",replacement_string=""))
    goal_weight = ft.TextField(label="Goal Weight (kg)",input_filter=ft.InputFilter(allow=True,regex_string=r"^\d*\.?\d*$",replacement_string=""))
    goal_salts = ft.TextField(hint_text="Salts (g)",input_filter=ft.InputFilter(allow=True,regex_string=r"^\d*\.?\d*$",replacement_string=""),height=40)
    goal_proteins = ft.TextField(hint_text="Protein Goal (g)",input_filter=ft.InputFilter(allow=True,regex_string=r"^\d*\.?\d*$",replacement_string=""),height=40)
    goal_fats = ft.TextField(hint_text="Fats Goal (g)",input_filter=ft.InputFilter(allow=True,regex_string=r"^\d*\.?\d*$",replacement_string=""),height=40)
    goal_carbs = ft.TextField(hint_text="Carbohydrates Goal (g)",input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*\.?\d*$",replacement_string=""), height=40)
    goal_water = ft.TextField(hint_text="Water (ml)",input_filter=ft.InputFilter(allow=True,regex_string=r"^[0-9]*$",replacement_string=""),height=40)
    #give options of different dropdown options
    activity_level = ft.Dropdown(label="Activity Level", options=[ft.dropdown.Option("Sedentary: no exercise"),
        ft.dropdown.Option("Light: exercise 1-3 times/week"), ft.dropdown.Option("Moderate: exercise 4-5 times/week"),
                                                                  ft.dropdown.Option("Active: daily exercise")])

    # Map the selected setup activity level to a weekly activity goal
    def map_activity_level_to_weekly_goal(activity_level_value):
        mapping = {
            "Sedentary: no exercise": 0,
            "Light: exercise 1-3 times/week": 3,
            "Moderate: exercise 4-5 times/week": 5,
            "Active: daily exercise": 7,
        }
        return mapping.get(activity_level_value, 3)

    def handle_continue(e):
        if not all([age.value, gender.value, height.value, current_weight.value, goal_weight.value,goal_salts.value,goal_proteins.value,goal_water.value,activity_level.value]):
            fail_snackbar("Please Enter All Fields",e)
            e.page.update()
            return

        try:
            # converting text values into integers for calculations
            age_val = int(age.value)
            height_val = float(height.value)
            current_weight_val = float(current_weight.value)
            goal_weight_val = float(goal_weight.value)
            salts_val = float(goal_salts.value)
            protein_val = float(goal_proteins.value)
            fats_val = float(goal_fats.value)
            carbs_val = float(goal_carbs.value)
            water_val = int(goal_water.value)



            # input validation
            if age_val < 13 or age_val > 100:
                fail_snackbar("Age must be between 13 and 100", e)
                e.page.update()
                return

            if height_val < 100 or height_val > 300:
                fail_snackbar("Height must between 100cm and 300cm", e)
                e.page.update()
                return

            if current_weight_val < 40 or current_weight_val > 500:
                fail_snackbar("Current Weight must between 40kg and 500kg", e)
                e.page.update()
                return
            if goal_weight_val < 40 or goal_weight_val > 500:
                fail_snackbar("Target Weight must be between 40kg and 500kg", e)
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

            weekly_activity_goal = map_activity_level_to_weekly_goal(activity_level.value)
            # save and store users setup data
            success = save_setup(user_id, age_val, gender.value, height_val, current_weight_val, goal_weight_val,
                                 calorie_goal,salts_val,protein_val,fats_val,carbs_val,water_val,weekly_activity_goal)
            if not success:
                fail_snackbar("Error Upon Completion, Please Try Again", e)
                e.page.update()
                return
            save_session(user_id)
            success_snackbar("Successfully Set Up",e)
            on_setup_complete(user_id)

        except ValueError:
            message.value = "Please enter valid numbers"
            e.page.update()

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[ft.Colors.ORANGE_100, ft.Colors.WHITE, ft.Colors.DEEP_ORANGE_50],
        ),
        content=ft.Column(
            controls=[
                ft.Container(height=20),
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    border_radius=24,
                    padding=ft.padding.symmetric(horizontal=28, vertical=32),
                    shadow=ft.BoxShadow(spread_radius=0, blur_radius=30,
                                        color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 8)),
                    margin=ft.margin.symmetric(horizontal=20),
                    content=ft.Column([
                        ft.Text("Set Up Your Profile", size=24, weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER),
                        ft.Text("Help us personalise your experience", size=13,
                                color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER),
                        ft.Divider(height=16, color=ft.Colors.TRANSPARENT),
                        ft.Text("About You", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.DEEP_ORANGE),
                        age, gender,
                        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                        ft.Text("Body Metrics", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.DEEP_ORANGE),
                        height, current_weight, goal_weight,
                        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                        ft.Text("Nutrition Goals", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.DEEP_ORANGE),
                        goal_salts, goal_proteins, goal_water,goal_fats,goal_carbs,
                        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                        ft.Text("Activity Level", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.DEEP_ORANGE),
                        activity_level,
                        ft.Divider(height=16, color=ft.Colors.TRANSPARENT),
                        message,
                        ft.Container(
                            content=ft.Text("Continue", color=ft.Colors.WHITE,
                                            weight=ft.FontWeight.BOLD, size=15,
                                            text_align=ft.TextAlign.CENTER),
                            bgcolor=ft.Colors.DEEP_ORANGE,
                            border_radius=12,
                            padding=ft.padding.symmetric(vertical=14),
                            on_click=handle_continue,
                            ink=True,
                            expand=True,
                        ),
                    ], scroll=ft.ScrollMode.HIDDEN, spacing=10),
                ),
                ft.Container(height=20),
            ],
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
    )