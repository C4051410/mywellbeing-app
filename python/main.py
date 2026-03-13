import flet as ft
from auth.authpage import authPage
from python.UI.pages.activities import main_activities
from python.UI.pages.homepage import main_homepage
from python.UI.pages.map import main_map
from python.UI.pages.nutrition import main_nutrition
from python.UI.pages.settings import main_settings
from python.UI.pages.social import main_social


def main(page: ft.Page):
    def route_change():
        page.clean()
        uid = getattr(page,"user_id",None)
        if uid is None:
            print("User not logged in")
        else:
            print("User logged in",uid)
        if page.route != current_page:
            if page.route == "/home":
                page.add(main_homepage(page,uid))
            if page.route == "/activities":
                page.add(main_activities(page))
            if page.route == "/nutrition":
                page.add(main_nutrition(page,uid))
            if page.route == "/social":
                page.add(main_social(page))
            if page.route == "/settings":
                page.add(main_settings(page))
            if page.route == "/map":
                    page.add(main_map(page))

            page.update()
    page.on_route_change = route_change
    page.title = "My Wellbeing"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {"Dubai": "/assets/DUBAI-REGULAR.TTF"}
    page.theme = ft.Theme(font_family="Dubai")
    page.window.width = 360
    page.window.height = 800
    page.padding = 10
    page.window.resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.update()

    def on_login_success(user_id):
        from UI.pages.homepage import WorkoutApp
        page.user_id = user_id

        page.clean()
        page.add(WorkoutApp(page, user_id))
        page.update()

    def on_register_success(user_id):
        from UI.pages.setup import setupGoalsPage
        page.user_id = user_id

        page.clean()
        page.add(setupGoalsPage(user_id, on_setup_complete))
        page.update()

    def on_setup_complete(user_id, age, gender, height, current_weight, goal_weight):
        from UI.pages.homepage import WorkoutApp
        page.user_id = user_id

        page.clean()
        page.add(main_homepage(page, user_id))
        page.update()

    page.add(authPage(on_login_success, on_register_success))

current_page = "/homepage"

ft.run(main,assets_dir="UI/assets")