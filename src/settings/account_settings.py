import flet as ft
from components.bottom_nav import NavBar
from components.responsive import Responsive
from settings.settings_services import update_password, update_goals


class AccountSettingsPage(ft.Column):
    def __init__(self, page: ft.Page, user_id):
        super().__init__()
        self.main_page = page
        self.user_id = user_id
        self.r = Responsive(page)

        # 1. Reset Password Fields.
        self.current_pw = ft.TextField(label="Current Password",password=True,can_reveal_password=True)
        self.new_pw = ft.TextField(label="New Password", password=True, can_reveal_password=True)
        self.confirm_pw = ft.TextField(label="Confirm Password", password=True)

        # 2. Reset Goals Fields (Using input_filter for numeric performance - PDF 1)
        self.cal_goal = ft.TextField(
            label="Daily Calorie Goal",
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
        )
        self.water_goal = ft.TextField(
            label="Daily Water Goal (ml)",
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
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
            self.current_pw,
            self.new_pw,
            self.confirm_pw,
            ft.ElevatedButton("Update Password", on_click=self.handle_pw_reset),
            ft.Divider(height=40),
            ft.Text("Health Goals", size=20, weight="bold"),
            self.cal_goal,
            self.water_goal,
            ft.ElevatedButton("Update Goals", on_click=self.handle_goal_reset),
            NavBar(page)  # Added Nav Bar as per System Description
        ]
        self.expand = True

    def handle_pw_reset(self, e):
        #calls upon update password
        success,message = update_password(self.user_id,self.current_pw.value,self.new_pw.value,self.confirm_pw.value)
        #if returns true, display snackbar to show success
        if success:
            self.page.overlay.append(ft.SnackBar(
                content=ft.Text("Password Updated"),
                bgcolor=ft.Colors.GREEN_400,
                open=True
            ))
            self.page.update()
        #else displays failure with specific message
        else:
            self.page.overlay.append(ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.RED_400,
                open=True
            ))
            self.page.update()
            return

    def handle_goal_reset(self, e):
        success, message = update_goals(self.user_id, self.cal_goal.value, self.water_goal.value)
        if success is True:
            self.page.overlay.append(ft.SnackBar(
                content=ft.Text("Goals Updated"),
                bgcolor=ft.Colors.GREEN_400,
                open=True
            ))
            self.page.update()
            return
        else:
            self.page.overlay.append(ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.RED_400,
                open=True
            ))
            self.page.update()
            return


    def show_snack(self, message, color):
        self.main_page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
        self.main_page.snack_bar.open = True
        self.main_page.update()


def main_account_settings(page: ft.Page, user_id):
    return AccountSettingsPage(page, user_id)