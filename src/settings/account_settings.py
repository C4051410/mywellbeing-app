import flet as ft
from components.bottom_nav import NavBar
from components.responsive import Responsive
from settings.settings_services import update_password, update_goals, delete_account


class AccountSettingsPage(ft.Column):
    def __init__(self, page: ft.Page, user_id):
        super().__init__()
        self.main_page = page
        self.user_id = user_id
        self.r = Responsive(page)

        # 1. Reset Password Fields.
        self.current_pw = ft.TextField(label="Current Password",password=True,can_reveal_password=True,
                                       input_filter=ft.InputFilter(allow=True,regex_string=r"^[^\s]*$",
                                                                   replacement_string=""))
        self.new_pw = ft.TextField(label="New Password", password=True, can_reveal_password=True,
                                   input_filter=ft.InputFilter(allow=True,regex_string=r"^[^\s]*$",
                                                               replacement_string=""))
        self.confirm_pw = ft.TextField(label="Confirm Password", password=True,
                                       input_filter=ft.InputFilter(allow=True,regex_string=r"^[^\s]*$",
                                                                   replacement_string=""))

        # 2. Reset Goals Fields (Using input_filter for numeric performance )
        self.cal_goal = ft.TextField(
            label="Daily Calorie Goal",
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
        )
        self.water_goal = ft.TextField(
            label="Daily Water Goal (ml)",
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
        )

        # Delete Account button
        self.delete_acc_btn = ft.ElevatedButton(
            "Delete Account",
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE,
            icon=ft.Icons.DELETE_FOREVER,
            on_click=self.confirm_delete_account
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
            ft.Divider(height=40),

            # Added Warning when deleting account
            ft.Text("Warning!", size=20, weight="bold", color=ft.Colors.RED_400),
            ft.Text("Are you sure you want to delete this account?", size=12,
                    color=ft.Colors.GREY_700),
            self.delete_acc_btn,
            NavBar(page)
        ]
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO # Added scrolling so it can fit any screen

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

    def handle_delete_account(self, e):
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

    def confirm_delete_account(self, e):
        self.dlg = ft.AlertDialog(
            title=ft.Text("Delete Account"),
            content=ft.Text(
                "Are you sure you want to delete your account? All your data will be permanently removed. This action cannot be undone."),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dlg),
                ft.TextButton("Delete", on_click=self.execute_delete_account, style=ft.ButtonStyle(color=ft.Colors.RED))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.overlay.append(self.dlg)
        self.dlg.open = True
        self.page.update()

    def close_dlg(self, e):
        self.dlg.open = False
        self.page.update()

    def execute_delete_account(self, e):
        self.dlg.open = False
        self.page.update()

        # Communicates directly via Service Layer
        success, message = delete_account(self.user_id)
        if success:
            self.page.overlay.append(ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.GREEN_400,
                open=True
            ))

            # Wipe session
            self.page.user_id = None
            self.page.clean()

            # Display account deletion acknowledgement so they know it worked
            restart_msg = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=ft.Colors.GREEN, size=60),
                    ft.Text("Account Deleted", size=24, weight="bold"),
                    ft.Text("Your account and all associated data have been permanently deleted.",
                            text_align=ft.TextAlign.CENTER),
                    ft.Text("Please restart the application to continue.", color=ft.Colors.GREY_700,
                            text_align=ft.TextAlign.CENTER)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True,
                alignment=ft.Alignment(0, 0)
            )
            self.page.add(restart_msg)
            self.page.update()
        else:
            self.page.overlay.append(ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.RED_400,
                open=True
            ))
            self.page.update()



    def show_snack(self, message, color):
        self.main_page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
        self.main_page.snack_bar.open = True
        self.main_page.update()


def main_account_settings(page: ft.Page, user_id):
    return AccountSettingsPage(page, user_id)