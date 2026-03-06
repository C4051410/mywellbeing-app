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
        self.header = ft.Container(content=ft.Text("Nutrition",size=32,weight=ft.FontWeight.BOLD),
                              padding=ft.padding.only(top=10,left=10)
        )
        self.stats_card = ft.Container(bgcolor=ft.Colors.WHITE,border_radius=5,padding=5,
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
                                                               ft.Container(width=1,height=20,bgcolor=ft.Colors.GREY_200),

                                                               ft.Column([
                                                                   ft.Text("Proteins",size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.DEEP_ORANGE),
                                                                   ft.Text("20.9",size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400)
                                                               ])
                                                           ]
                                                       )])
        )
        self.enter_foodlog = ft.Container(bgcolor=ft.Colors.WHITE,border_radius=5,padding=10,
                                     content = ft.Column([
                                         ft.Text("Enter Food",size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                         ft.TextField(hint_text="Food",height=40),
                                         ft.Text("Enter Calories",size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                         ft.TextField(hint_text="Calories",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9].*$",replacement_string=""),height=40),
                                         ft.Text("Enter Salts",size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                         ft.TextField(hint_text="Salts",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9]*$",replacement_string=""),height=40),
                                         ft.Text("Enter Proteins",size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                         ft.TextField(hint_text="Proteins",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9]*$",replacement_string=""),height=40),
                                         ft.ElevatedButton("Enter Food")

                                     ])
                                     )
        self.display_foodlog = ft.Container(bgcolor=ft.Colors.WHITE,border_radius=5,padding=10,
                                            content = ft.Column([
                                                ft.ExpansionTile(title="Fish and Chips",
                                                                 controls=[ft.ListTile(title="Calories",subtitle="1324"),
                                                                           ft.ListTile(title="Salts",subtitle="6.5"),
                                                                           ft.ListTile(title="Calories",subtitle="10")])
                                            ])
                                            )
        scrollable = ft.Column([
            self.header,
            self.stats_card,
            self.enter_foodlog,
            self.display_foodlog,
        ],height=600,scroll=ft.ScrollMode.ALWAYS)
        self.navBar = navBar(page)
        self.controls = [
            scrollable,
            self.navBar,

        ]
        self.expand = True
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

def main_nutrition(page: ft.Page):
    nutrition_page = NutritionPage(page)
    return nutrition_page