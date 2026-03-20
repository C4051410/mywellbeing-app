import flet as ft

from admin.admin import main_admin
from auth.authpage import authPage
from activities.activities import main_activities
from database.connection import connect
from home.homepage import main_homepage
from activities.map import main_map
from nutrition.nutrition import main_nutrition
from settings.settings import main_settings
from settings.account_settings import main_account_settings
from social.social import main_social


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
            if page.route == "/account-settings":
                page.add(main_account_settings(page, getattr(page, "user_id", None)))

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
        from home.homepage import WorkoutApp
        page.user_id = user_id

        page.clean()
        if (check_admin(user_id)):
            page.add(main_admin(page))
        else:
            page.add(WorkoutApp(page, user_id))
        page.update()

    def on_register_success(user_id):
        from auth.setup import setupGoalsPage
        page.user_id = user_id
        page.clean()
        page.add(setupGoalsPage(user_id, on_setup_complete))
        page.update()

    def check_admin(user_id):
        conn = connect()
        if conn is not None:
            cur = conn.cursor()
            cur.execute("SELECT role FROM users WHERE id = %s",(user_id,))
            user = cur.fetchone()
            if user is None or user[0] != "admin":
                return False
            else:
                return True


    def on_setup_complete(user_id, age, gender, height, current_weight, goal_weight):
        page.user_id = user_id

        page.clean()
        page.add(main_homepage(page, user_id))
        page.update()

    page.add(authPage(on_login_success, on_register_success))

current_page = "/homepage"

ft.run(main, assets_dir="assets")