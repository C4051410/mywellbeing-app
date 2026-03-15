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
        label = "Daily Water Goal (ml)",
        input_filter = ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
    )

        # 3. Assemble the UI
        self.controls = [
            ft.Container(
            content=ft.Column([
                ft.Text("Settings", size=32, weight="bold"),
                ft.Text("Manage your goals and security", color="grey"),
            ]),
            padding=ft.padding.only(bottom=20)
        ),
        ft.Text("Security", size=20, weight="bold"),
        self.new_pw,
        self.confirm_pw,
        ft.ElevatedButton("Update Password", on_click=self.handle_pw_reset),
        ft.Divider(height=40),
        ft.Text("Health Goals", size=20, weight="bold"),
        self.cal_goal,
        self.water_goal,
        ft.ElevatedButton("Update Goals", on_click=self.handle_goal_reset),
        NavBar(page)
    ]
    self.expand = True

    def handle_pw_reset(self, e):
    # Edge case. Password Mismatch
    if self.new_pw.value != self.confirm_pw.value:
        self.show_snack("Passwords do not match", ft.Colors.RED)
        return

    # Security Requirement (NRF7): Password check
    if len(self.new_pw.value) < 8:
        self.show_snack("Password must be at least 8 characters", ft.Colors.RED)
        return

    success = update_password(self.user_id, self.new_pw.value)
    if success is True:
        self.show_snack("Password updated successfully", ft.Colors.GREEN)
    else:
        self.show_snack(f"Database error: {success}", ft.Colors.RED)

def handle_goal_reset(self, e):
    # Edge Case. Ensures fields are not empty
    if not self.cal_goal.value or not self.water_goal.value:
        self.show_snack("Please fill in both goals", ft.Colors.ORANGE)
        return

    success = update_goals(self.user_id, int(self.cal_goal.value), int(self.water_goal.value))
    if success is True:
        self.show_snack("Goals updated successfully!", ft.Colors.GREEN)
    else:
        self.show_snack(f"Error: {success}", ft.Colors.RED)

def show_snack(self, message, color):
        self.main_page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
        self.main_page.snack_bar.open = True
        self.main_page.update()


def main_account_settings(page: ft.Page, user_id):
    return AccountSettingsPage(page, user_id)










