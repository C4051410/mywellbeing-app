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
        self.main_page = page
        self.r = Responsive(page)
        #1. Page Header
        header = ft.Container(content=ft.Text("Nutrition",size=32,weight=ft.FontWeight.BOLD),
                              padding=ft.padding.only(top=20,left=10)
        )
        stats_card = ft.Container(bgcolor=ft.Colors.WHITE,border_radius=15,padding=20,
                                  shadow = ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
                                  content = ft.Column([ft.Text("Today",size=12,weight=ft.FontWeight.BOLD,color=ft.Colors.GREY),
                                                       ft.Divider(height=10,color=ft.Colors.TRANSPARENT),
                                                       ft.Row(
                                                           alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                           controls = [
                                                               ft.Column([
                                                                   ft.Text("Calories",size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.DEEP_ORANGE),
                                                                   ft.Text("1908",size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400)
                                                               ]),
                                                               ft.Container(width=1,height=40,bgcolor=ft.Colors.GREY_200),

                                                               ft.Column([
                                                                   ft.Text("Proteins",size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.DEEP_ORANGE),
                                                                   ft.Text("20.9",size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400)
                                                               ])
                                                           ]
                                                       )])
        )
        food_logs = ft.Container(expand=True,bgcolor=ft.Colors.WHITE,border_radius=15,padding=20,)
        self.nav = navBar(page)
        self.expand = True
        self.controls = [
            header,
            stats_card,
            food_logs,
            self.nav
        ]

def main_nutrition(page: ft.Page):
    nutrition_page = NutritionPage(page)
    return nutrition_page