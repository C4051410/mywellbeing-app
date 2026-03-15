import flet as ft
from UI.components.bottom_nav import NavBar
from UI.components.responsive import Responsive
from database.settings_queries import update_password, update_goals


class AccountSettingsPage(ft.Column):
    def __init__(self, page: ft.Page, user_id):
        super().__init__()
        self.main_page = page
        self.user_id = user_id
        self.r = Responsive(page)

        # 1. Reset Password Fields
        self.new_pw = ft.TextField(label="New Password", password=True, can_reveal_password=True)
        self.confirm_pw = ft.TextField(label="Confirm Password", password=True)

        # 2. Reset Goals Fields
        self.cal_goal = ft.TextField(
            label="Daily Calorie Goal",
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]+$"), replacement_string="")
        )
        self.water_goal = ft.TextField(
            label="Daily Water Goal (ml)",
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]+$", replacement_string=""),
        )



