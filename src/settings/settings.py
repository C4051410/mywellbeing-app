'''
File for settings page - accessible by clicking 'settings' on nav bar
'''

import flet as ft

from components.userpfp import Userpfp
from components.bottom_nav import NavBar
from components.responsive import Responsive
from settings.settings_services import retrieve_notification_status, update_notification_status

#Sizes of all elements on homepage (as a percent of screen)
page_title_size = 0.1
page_desc_size = 0.03
user_info_v_size = 0.15
account_v_size = 0.25
target_v_size = 0.25

class SettingsPage(ft.Column):
    def __init__(self, page: ft.Page,user_id):
        super().__init__()

        self.r = Responsive(page)
        self.is_enabled = retrieve_notification_status(user_id)
        self.page_title = ft.Text(
            value="Social",
            size=self.r.w(page_title_size),
            color=ft.Colors.BLACK
        )

        self.page_desc = ft.Text(
            value="Connect with friends",
            size=self.r.w(page_desc_size),
            color=ft.Colors.GREY
        )

        self.user_info_container = ft.Container(
            bgcolor=ft.Colors.BLUE_300
        )

        # Updated account container to include the button for the new page
        self.account_container = ft.Container(
            border=ft.Border.all(width=2, color=ft.Colors.GREY_400),
            alignment=ft.Alignment.CENTER,
            content=ft.ElevatedButton(
                "Manage Account & Goals",
                on_click=lambda _: self.this_page.go("/account-settings")
            ),
            padding=10
        )
        self.ntf_btn = ft.ElevatedButton(
            "Toggle Notifications ",
            icon=ft.Icons.NOTIFICATIONS_OFF if self.is_enabled else ft.Icons.NOTIFICATIONS_ACTIVE,
            color=ft.Colors.RED if self.is_enabled else ft.Colors.GREEN)
        def toggle_notification(e):
            update_notification_status(user_id,self.is_enabled)
            self.is_enabled = not self.is_enabled
            if self.is_enabled:
                self.ntf_btn.icon = ft.Icons.NOTIFICATIONS_OFF
                self.ntf_btn.color = ft.Colors.RED
                self.page.overlay.append(ft.SnackBar(
                    content=ft.Text("Notification Turned On"),
                    bgcolor=ft.Colors.GREEN_400,
                    open=True
                ))
            else:
                self.ntf_btn.icon = ft.Icons.NOTIFICATIONS_ON
                self.ntf_btn.color = ft.Colors.GREEN
                self.page.overlay.append(ft.SnackBar(
                    content=ft.Text("Notification Turned Off"),
                    bgcolor=ft.Colors.RED_400,
                    open=True
                ))
            self.page.update()
            self.ntf_btn.update()

        self.ntf_btn.on_click=toggle_notification

        self.notification_container = ft.Container(
            border=ft.Border.all(width=2, color=ft.Colors.GREY_400),
            alignment=ft.Alignment.CENTER,
            content=self.ntf_btn,
            )

        self.userpfp = Userpfp(page)

        self.nav_bar = NavBar(page)

        self.controls=[
            ft.Row(
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        expand=True,
                        controls=[
                            self.page_title,
                            self.page_desc
                        ]
                    ),
                    self.userpfp
                ]
            ),
            self.user_info_container,
            self.account_container,
            self.notification_container,
            self.nav_bar
        ]

        self.expand=True
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        self.set_widget_size()
        self.set_text_size()

        self.this_page = page
        page.on_resize = self.resize

    def set_text_size(self):
        self.page_title.size = self.r.w(page_title_size)
        self.page_desc.size = self.r.w(page_desc_size)

    def set_widget_size(self):
        self.user_info_container.height = self.r.h(user_info_v_size)
        self.account_container.height = self.r.h(account_v_size)
        self.notification_container.height = self.r.h(target_v_size)

    def resize(self,e ):
        self.r = Responsive(self.this_page)

        self.set_text_size()
        self.set_widget_size()

        self.userpfp.resize()
        self.nav_bar.resize()

        self.update()

def main_settings(page: ft.Page,user_id):
    settings_page = SettingsPage(page,user_id)

    return settings_page