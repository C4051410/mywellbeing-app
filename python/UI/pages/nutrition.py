'''
File for nutrition page - accessible by clicking 'nutrition' on nav bar
'''

import flet as ft

from components.userpfp import Userpfp
from components.bottom_nav import navBar
from components.responsive import Responsive

class NutritionPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.r = Responsive(page)


def main_nutrition(page: ft.Page):
    nutrition_page = NutritionPage(page)

    return nutrition_page