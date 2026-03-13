import flet as ft
from auth.authpage import authPage

def main(page: ft.Page):
    page.title = "My Wellbeing"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {"Dubai": "/assets/DUBAI-REGULAR.TTF"}
    page.theme = ft.Theme(font_family="Dubai")
    page.window.width = 360
    page.window.height = 800
    page.padding = 10
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.update()

    def on_login_success(user_id):
        from UI.pages.homepage import WorkoutApp
        page.clean()
        page.add(WorkoutApp(page, user_id))
        page.update()

    def on_register_success(user_id):
        from UI.pages.setup import setupGoalsPage
        page.clean()
        page.add(setupGoalsPage(user_id, on_setup_complete))
        page.update()

    def on_setup_complete(user_id, age, gender, height, current_weight, goal_weight):
        from UI.pages.homepage import WorkoutApp

        page.clean()
        page.add(WorkoutApp(page, user_id))
        page.update()

    page.add(authPage(on_login_success, on_register_success))

ft.run(main)