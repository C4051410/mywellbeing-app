'''
File for settings page - accessible by clicking 'settings' on nav bar
'''

import flet as ft

from components.userpfp import Userpfp
from components.bottom_nav import navBar
from components.responsive import Responsive

class SettingsPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.r = Responsive(page)


def main_settings(page: ft.Page):
    settings_page = SettingsPage(page)

    return settings_page