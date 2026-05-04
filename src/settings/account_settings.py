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

        # created top back button to navigate back to main settings
        top_back_button = ft.Container(
            content=ft.FloatingActionButton(
                content=ft.Icon(ft.Icons.ARROW_BACK, color=ft.Colors.BLACK),
                bgcolor=ft.Colors.WHITE,
                on_click=self.go_back,
                mini=True
            ),
            margin=ft.margin.only(right=10)
        )

        # Container for the page header text and back button
        header = ft.Container(
            content=ft.Row(
                controls=[
                    top_back_button,
                    ft.Column(
                        controls=[
                            ft.Text("Account", size=28, weight=ft.FontWeight.BOLD),
                            ft.Text("Manage your goals and security", size=13, color=ft.Colors.GREY_500),
                        ],
                        spacing=0
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.only(top=20, left=15, right=15, bottom=10)
        )

        # Reset Password Fields. rgex prevents spaces from being entered
        self.current_pw = ft.TextField(label="Current Password",password=True,can_reveal_password=True,
                                       input_filter=ft.InputFilter(allow=True,regex_string=r"^[^\s]*$",
                                                                   replacement_string=""))
        self.new_pw = ft.TextField(label="New Password", password=True, can_reveal_password=True,
                                   input_filter=ft.InputFilter(allow=True,regex_string=r"^[^\s]*$",
                                                               replacement_string=""))
        self.confirm_pw = ft.TextField(label="Confirm Password", password=True,
                                       input_filter=ft.InputFilter(allow=True,regex_string=r"^[^\s]*$",
                                                                   replacement_string=""))

        # Wraps the password styles into a style white card
        password_section = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
            content=ft.Column(
                controls=[
                    ft.Text("Security", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    self.current_pw,
                    self.new_pw,
                    self.confirm_pw,
                    ft.ElevatedButton(
                        "Update Password",
                        bgcolor=ft.Colors.BLUE,
                        color=ft.Colors.WHITE,
                        on_click=self.handle_pw_reset
                    )
                ]
            )
        )

        # Reset Goals Fields (Using input_filter for numeric performance )
        self.cal_goal = ft.TextField(
            label="Daily Calorie Goal",
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
        )
        self.water_goal = ft.TextField(
            label="Daily Water Goal (ml)",
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
        )

        self.weekly_activity_goal = ft.TextField(
            label="Weekly Activity Goal",
            input_filter=ft.InputFilter(
                allow=True,
                regex_string=r"^[0-9]*$",
                replacement_string=""
            )
        )

        # wraps the goal fields into a styled white card
        goals_section = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
            content=ft.Column(
                controls=[
                    ft.Text("Health Goals", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    self.cal_goal,
                    self.water_goal,
                    self.weekly_activity_goal,
                    ft.ElevatedButton(
                        "Update Goals",
                        bgcolor=ft.Colors.BLUE,
                        color=ft.Colors.WHITE,
                        on_click=self.handle_goal_reset
                    )
                ]
            )
        )

        # Delete Account button
        self.delete_acc_btn = ft.ElevatedButton(
            "Delete Account",
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE,
            icon=ft.Icons.DELETE_FOREVER,
            on_click=self.confirm_delete_account
        )

        #wraps the warning text and delete button into a styled white card
        danger_section = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
            content=ft.Column(
                controls=[
                    ft.Text("Warning!", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_400),
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    ft.Text("Are you sure you want to delete this account? This action cannot be undone.", size=13,
                            color=ft.Colors.GREY_700),
                    self.delete_acc_btn
                ]
            )
        )

        self.nav_bar = NavBar(page)

        # Assembles all the cards into a single scrollable column
        content_column = ft.Column(
            controls=[
                header,
                ft.Container(content=password_section, padding=ft.padding.symmetric(horizontal=15),
                             margin=ft.margin.only(bottom=15)),
                ft.Container(content=goals_section, padding=ft.padding.symmetric(horizontal=15),
                             margin=ft.margin.only(bottom=15)),
                ft.Container(content=danger_section, padding=ft.padding.symmetric(horizontal=15),
                             margin=ft.margin.only(bottom=20)),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        self.controls = [content_column, self.nav_bar]
        self.expand = True
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    # Sends the user back to the main settings page
    def go_back(self, e):
        self.main_page.go("/settings")

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
        # attempts to update goals via the service layer
        success, message = update_goals(self.user_id, self.cal_goal.value, self.water_goal.value, self.weekly_activity_goal.value)

        #displays success message if updated correctly
        if success is True:
            self.page.overlay.append(ft.SnackBar(
                content=ft.Text("Goals Updated"),
                bgcolor=ft.Colors.GREEN_400,
                open=True
            ))
            self.page.update()
            return
        # else displays specific error message
        else:
            self.page.overlay.append(ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.RED_400,
                open=True
            ))
            self.page.update()
            return

    def confirm_delete_account(self, e):
        # creates an alert dialog to double check if the user actually wants to delete
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
        # adds dialog to page overlay and opens it
        self.page.overlay.append(self.dlg)
        self.dlg.open = True
        self.page.update()

    def close_dlg(self, e):
        # closes the dialog if they hit cancel
        self.dlg.open = False
        self.page.update()

    def execute_delete_account(self, e):
        # close the confirmation dialog
        self.dlg.open = False
        self.page.update()

        # calls the service layer to actually delete the user from the db
        success, message = delete_account(self.user_id)

        # if successful, display success message and cleans the page
        if success:
            self.page.overlay.append(ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.GREEN_400,
                open=True
            ))

            # Wipes user session session
            self.page.user_id = None
            self.page.clean()

            # Display a visual confirmation screen telling them to restart
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

        #if it fails, display error message
        else:
            self.page.overlay.append(ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.RED_400,
                open=True
            ))
            self.page.update()

def main_account_settings(page: ft.Page, user_id):
    return AccountSettingsPage(page, user_id)