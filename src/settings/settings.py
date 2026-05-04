'''
File for settings page - accessible by clicking 'settings' on nav bar
'''

import flet as ft
import platform
from components.userpfp import Userpfp
from components.bottom_nav import NavBar
from components.responsive import Responsive
from settings.settings_services import retrieve_notification_status, update_notification_status


class SettingsPage(ft.Column):
    def __init__(self, page: ft.Page,user_id):
        super().__init__()
        self.this_page = page
        self.user_id = user_id
        self.r = Responsive(page)

        #checks the notification status
        self.is_enabled = retrieve_notification_status(user_id)
        self.uerpfp = Userpfp(page)

        # container for the page header and text and profile picture
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Text("Settings", size=35, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                            ft.Text("Manage your account", size=13, color=ft.Colors.GREY_500)
                        ],
                        spacing=2
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=ft.padding.only(top=20, left=15, right=15, bottom=20)
        )

        #wraps the account settings button into a styled white card using a ListTile
        account_card = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=5,shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
            ink=True,
            on_click=lambda _: self.this_page.go("/account-settings"),
            content=ft.ListTile(
                leading=ft.Icon(ft.Icons.PERSON_OUTLINE, color=ft.Colors.BLUE, size=30),
                title=ft.Text("Manage Account & Goals", weight=ft.FontWeight.BOLD, size=15),
                subtitle=ft.Text("Update password, calories, and water goals", color=ft.Colors.GREY_600, size=12),
                trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT)
            )
        )

        # visual switch control that defaults to the users saved db status
        self.notification_switch = ft.Switch(
            value=self.is_enabled,
            on_change=self.toggle_notification,
            active_color=ft.Colors.GREEN
        )

        # Dynamic icon that changes the colour and shape based on the notification status
        self.notification_icon = ft.Icon(
            ft.Icons.NOTIFICATIONS_ACTIVE if self.is_enabled else ft.Icons.NOTIFICATIONS_OFF,
            color=ft.Colors.GREEN if self.is_enabled else ft.Colors.RED,
            size=30
        )

        # wraps the notifications into a styled white card
        notification_card = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=5,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
            ink=True,
            on_click=self.handle_notification_card_click,
            content=ft.ListTile(
                leading=self.notification_icon,
                title=ft.Text("Notifications", weight=ft.FontWeight.BOLD, size=15),
                subtitle=ft.Text("Turn on/off app notifications", color=ft.Colors.GREY_600, size=12),
                trailing=self.notification_switch
            )
        )

        # wraps the logout button into a styled white card
        logout_card = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=5,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
            ink=True,
            on_click=self.handle_logout,
            content=ft.ListTile(
                leading=ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED, size=30),
                title=ft.Text("Logout", weight=ft.FontWeight.BOLD, color=ft.Colors.RED, size=15),
                subtitle=ft.Text("Sign out of your account", color=ft.Colors.GREY_600, size=12),
            )
        )

        self.nav_bar = NavBar(page)

        # groups the cards together with small grey section headers
        menu_column = ft.Column(
            controls=[
                ft.Text("ACCOUNT", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
                account_card,
                ft.Container(height=10),
                ft.Text("PREFERENCES", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
                notification_card,
                ft.Container(height=10),
                ft.Text("SESSION", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
                logout_card
            ],
            spacing=10
        )

        # assembles the header and the menu cards into a scrollable view
        content_column = ft.Column(
            controls=[
                header,
                ft.Container(content=menu_column, padding=ft.padding.symmetric(horizontal=15), expand=True)
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        self.controls = [content_column, self.nav_bar]
        self.expand = True
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        page.on_resize = self.resize

    # used to open the devices settings to show notifications
    async def open_device_notification(self):
        #used to determine the specific platform
        system = platform.system()
        try:
            if system == "Android":
                await self.page.launch_url("app-settings:")
            elif system == "Windows":
                await self.page.launch_url("ms-settings:notifications")
            elif system == "Darwin":
                await self.page.launch_url("app-settings:")
        except Exception as e:
            print(e)

    def handle_notification_card_click(self, e):
        # toggles switch programmatically when the listTile is clicked
        self.notification_switch.value = not self.notification_switch.value
        self.toggle_notification(e)

    #used to toggle the notification
    def toggle_notification(self, e):
        # gets the current value of the switch
        self.is_enabled = self.notification_switch.value

        #updates the status and flips the status
        update_notification_status(self.user_id, not self.is_enabled)

        # if turning ON, updates icon to green active bell, show success snackbar, and opens OS settings
        if self.is_enabled:
            self.notification_icon.name = ft.Icons.NOTIFICATIONS_ACTIVE
            self.notification_icon.color = ft.Colors.GREEN
            self.page.overlay.append(ft.SnackBar(
                content=ft.Text("Notification Turned On"),
                bgcolor=ft.Colors.GREEN_400,
                open=True
            ))
            #as they have clicked turn on, try and open the notification settings in device
            self.page.run_task(self.open_device_notification)

        # if turning OFF, update icon to red disabled bell and show snackbar
        else:
            self.notification_icon.name = ft.Icons.NOTIFICATIONS_OFF
            self.notification_icon.color = ft.Colors.RED
            self.page.overlay.append(ft.SnackBar(
                content=ft.Text("Notification Turned Off"),
                bgcolor=ft.Colors.RED_400,
                open=True
            ))

        # updates the UI to reflect changes
        self.this_page.update()

    def handle_logout(self, e):
        # Wipes session data
        self.this_page.user_id = None
        self.this_page.clean()

        # Navigate back to the login/register screen
        self.this_page.go("/login")


    # handles element resizing when window size changes
    def resize(self,e ):
        self.r = Responsive(self.this_page)
        self.userpfp.resize()
        self.nav_bar.resize()
        self.update()

def main_settings(page: ft.Page,user_id):
    settings_page = SettingsPage(page,user_id)
    return settings_page