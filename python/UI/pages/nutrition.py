'''
File for nutrition page - accessible by clicking 'nutrition' on nav bar
'''

import os
import flet as ft
import psycopg2
from dotenv import load_dotenv

from components.userpfp import Userpfp
from components.bottom_nav import navBar
from components.responsive import Responsive

load_dotenv()
db_url = os.getenv('DATABASE_URL')

def get_connection():
    try:
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None
conn = get_connection()

class NutritionPage(ft.Column):

    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.r = Responsive(page)
        self.food_input = ft.TextField(hint_text="Food",height=40)
        self.calories_input = ft.TextField(hint_text="Calories",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9].*$",replacement_string=""),height=40)
        self.salts_input = ft.TextField(hint_text="Salts",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9].*$",replacement_string=""),height=40)
        self.proteins_input = ft.TextField(hint_text="Proteins",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9].*$",replacement_string=""),height=40)
        self.foodlog_list = ft.Column()
        def handle_submit(e):
            food = self.food_input.value
            calories = self.calories_input.value
            salts = self.salts_input.value
            proteins = self.proteins_input.value
            if not food or not calories or not salts or not proteins:
                print("Nope")
                return
            self.foodlog_list.controls.append(ft.ExpansionTile(title=food,
                                                               controls=[
                                                                   ft.ListTile(title="Calories",subtitle=calories),
                                                                   ft.ListTile(title="Salts",subtitle=salts),
                                                                   ft.ListTile(title="Proteins",subtitle=proteins),
                                                               ]))
            if conn is not None:
                cur = conn.cursor()
                cur.execute("INSERT INTO foodlog (title,calories,salts,proteins,user_id) VALUES (%s,%s,%s,%s,1)  ",(food,calories,salts,proteins))
                print("Executed")
                conn.commit()
                cur.close()
            self.food_input.value = ""
            self.calories_input = ""
            self.salts_input = ""
            self.proteins_input = ""
            self.update()


        def retrieve_posts():
            if conn is not None:
                cur = conn.cursor()
                cur.execute("SELECT title,calories,salts,proteins FROM foodlog WHERE user_id = 1")
                rows = cur.fetchall()
                for data in rows:
                    self.foodlog_list.controls.append(ft.ExpansionTile(title=data[0],
                                                               controls=[
                                                                   ft.ListTile(title="Calories",subtitle=str(data[1])),
                                                                   ft.ListTile(title="Salts",subtitle=str(data[2])),
                                                                   ft.ListTile(title="Proteins",subtitle=str(data[3])),
                                                               ]))
                    print(data[0],data[1],data[2],data[3])
                cur.close()

        retrieve_posts()
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
                                         self.food_input,
                                         ft.Text("Enter Calories",size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                         self.calories_input,
                                         ft.Text("Enter Salts",size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                         self.salts_input,
                                         ft.Text("Enter Proteins",size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                         self.proteins_input,
                                         ft.ElevatedButton("Enter Food",on_click=handle_submit),

                                     ])
                                     )
        self.display_foodlog = ft.Container(bgcolor=ft.Colors.WHITE,border_radius=5,padding=10,
                                            content = self.foodlog_list)
        scrollable = ft.Column([
            self.header,
            self.stats_card,
            self.enter_foodlog,
            self.display_foodlog,
        ],height=600,scroll=ft.ScrollMode.HIDDEN)
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