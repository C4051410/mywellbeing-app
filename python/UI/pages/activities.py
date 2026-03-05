'''
File for activities page - accessible by clicking 'activities' on nav bar
'''

import flet as ft

from components.userpfp import Userpfp
from components.bottom_nav import navBar
from components.responsive import Responsive

class ActivitiesPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.r = Responsive(page)


def main_activities(page: ft.Page):
    activities_page = ActivitiesPage(page)

    return activities_page