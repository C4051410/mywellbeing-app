'''
File for social page - accessible by clicking 'social' on nav bar
'''

import flet as ft

from components.userpfp import Userpfp
from components.bottom_nav import navBar
from components.responsive import Responsive

class SocialPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.r = Responsive(page)


def main_social(page: ft.Page):
    social_page = SocialPage(page)

    return social_page