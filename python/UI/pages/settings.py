'''
File for settings page - accessible by clicking 'settings' on nav bar
'''

import flet as ft

from UI.components.userpfp import Userpfp
from UI.components.bottom_nav import NavBar
from UI.components.responsive import Responsive

#Sizes of all elements on homepage (as a percent of screen)
page_title_size = 0.1
page_desc_size = 0.03
user_info_v_size = 0.15
account_v_size = 0.25
target_v_size = 0.25

class SettingsPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.r = Responsive(page)

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

        self.account_container = ft.Container(
            border=ft.Border.all(width=2, color=ft.Colors.GREY_400)
        )

        self.targets_conatiner = ft.Container(
            border=ft.Border.all(width=2, color=ft.Colors.GREY_400),
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
            self.targets_conatiner,
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
        self.targets_conatiner.height = self.r.h(target_v_size)

    def resize(self,e ):
        self.r = Responsive(self.this_page)

        self.set_text_size()
        self.set_widget_size()

        self.userpfp.resize()
        self.nav_bar.resize()

        self.update()

def main_settings(page: ft.Page):
    settings_page = SettingsPage(page)

    return settings_page