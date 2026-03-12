'''
File for nutrition page - accessible by clicking 'nutrition' on nav bar
'''

import os
from datetime import date, timedelta

import flet as ft
import psycopg2
from dotenv import load_dotenv

from components.userpfp import Userpfp
from components.bottom_nav import navBar
from components.responsive import Responsive
from flet import control

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
        self.calories_input = ft.TextField(hint_text="Calories",input_filter=ft.InputFilter(allow=True,regex_string=r"^[0-9]*$",replacement_string=""),height=40)
        self.salts_input = ft.TextField(hint_text="Salts",input_filter=ft.InputFilter(allow=True,regex_string=r"^\d*\.?\d*$",replacement_string=""),height=40)
        self.proteins_input = ft.TextField(hint_text="Proteins",input_filter=ft.InputFilter(allow=True,regex_string=r"^\d*\.?\d*$",replacement_string=""),height=40)
        self.water_input = ft.TextField(hint_text="ml",input_filter=ft.InputFilter(allow=True,regex_string=r"^[0-9]*$",replacement_string=""),height=40)
        self.meal_types = ft.Dropdown(hint_text="Enter Meal Type", width=200, options=[
            ft.DropdownOption(key="Breakfast", text="Breakfast"),
            ft.DropdownOption(key="Lunch", text="Lunch"),
            ft.DropdownOption(key="Dinner", text="Dinner"),
            ft.DropdownOption(key="Snack", text="Snack"),])
        self.foodlog_list = ft.Column()
        self.waterlog_list = ft.Column()
        def handle_food_submit(e):
            food = self.food_input.value
            calories = self.calories_input.value
            salts = self.salts_input.value
            proteins = self.proteins_input.value
            mealtype = self.meal_types.value
            if not food or not calories or not salts or not proteins or not mealtype:
                print("Nope")
                return
            self.foodlog_list.controls.append(ft.ExpansionTile(title=food,
                                                               controls=[
                                                                   ft.ListTile(title="Calories",subtitle=calories),
                                                                   ft.ListTile(title="Salts",subtitle=salts),
                                                                   ft.ListTile(title="Proteins",subtitle=proteins),
                                                                   ft.ListTile(title="Meal Type",subtitle=mealtype),
                                                               ]))
            if conn is not None:
                cur = conn.cursor()
                cur.execute("INSERT INTO foodlog (title,calories,salts,proteins,date,mealtype,user_id) VALUES (%s,%s,%s,%s,%s,%s,1)  ",(food,calories,salts,proteins,str(date.today()),mealtype,))
                print("Executed")
                conn.commit()
                cur.close()
            self.food_input.value = ""
            self.calories_input.value = ""
            self.salts_input.value = ""
            self.proteins_input.value = ""
            self.meal_types.value = ""
            self.update()

        def handle_water_submit(e):
            water = self.water_input.value
            self.foodlog_list.controls.append(ft.ExpansionTile(title="Water",controls=[ft.ListTile(title="ml",subtitle=water),]))
            if not water:
                print("Nope")
                return
            if conn is not None:
                cur = conn.cursor()
                cur.execute("INSERT INTO waterlog (water,date,user_id) VALUES (%s,%s,1)",(water,str(date.today()),))
                conn.commit()
                cur.close()
            self.update()


        def retrieve_posts():
            two_days = date.today() - timedelta(days=2)
            if conn is not None:
                cur = conn.cursor()
                cur.execute("SELECT title,calories,salts,proteins,mealtype,date FROM foodlog WHERE user_id = 1 AND date > (%s) ORDER BY date DESC",(str(two_days),))
                rows = cur.fetchall()
                for data in rows:
                    self.foodlog_list.controls.append(ft.ExpansionTile(title=data[0],subtitle=str(data[5]) + " " + str(data[4]),
                                                               controls=[
                                                                   ft.ListTile(title="Calories",subtitle=str(data[1])),
                                                                   ft.ListTile(title="Salts",subtitle=str(data[2])),
                                                                   ft.ListTile(title="Proteins",subtitle=str(data[3])),
                                                               ]))
                cur.execute("SELECT water,date FROM waterlog WHERE user_id = 1 AND date > (%s) ORDER BY date DESC",(str(two_days),))
                rows = cur.fetchall()
                for data in rows:
                    self.waterlog_list.controls.append(ft.ListTile(title=str(data[0]) + " ml",subtitle=str(data[1])))
                cur.close()
                page.update()

        retrieve_posts()
        #1. Page Header
        self.header = ft.Container(content=ft.Text("Nutrition",size=32,weight=ft.FontWeight.BOLD),
                              padding=ft.padding.only(top=10,left=10)
        )
        def retrieve_daily_status():
            total_c = 0
            total_s = 0.0
            total_p = 0.0
            total_w = 0
            if conn is not None:
                cur = conn.cursor()
                cur.execute("SELECT calories,salts,proteins FROM foodlog WHERE user_id = 1 AND date = %s",(str(date.today()),))
                rows = cur.fetchall()
                for data in rows:
                    total_c = total_c + data[0]
                    total_s = total_s + data[1]
                    total_p = total_p + data[2]
                cur.execute("SELECT water FROM waterlog WHERE user_id = 1 AND date = %s",(str(date.today()),))
                rows = cur.fetchall()
                for data in rows:
                    total_w = total_w + data[0]

                return total_c, total_s, total_p,total_w

        def retrieve_user_goals():
            goal_c = 0
            goal_s = 0.0
            goal_p = 0.0
            goal_w = 0
            if conn is not None:
                cur = conn.cursor()
                cur.execute("SELECT calories_goal, salts_goal, proteins_goal,water_goal FROM foodgoals WHERE user_id = 1")
                rows = cur.fetchall()
                for data in rows:
                    goal_c = goal_c + data[0]
                    goal_s = goal_s + data[1]
                    goal_p = goal_p + data[2]
                    goal_w = goal_w + data[3]
                return goal_c, goal_s, goal_p, goal_w

        total_calories, total_salts, total_proteins, total_water = retrieve_daily_status()
        goal_calories, goal_salts, goal_proteins, goal_water = retrieve_user_goals()
        self.stats_card = ft.Container(bgcolor=ft.Colors.WHITE,border_radius=5,padding=5,
                                  shadow = ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
                                  content = ft.Column([ft.Text("Today",size=12,weight=ft.FontWeight.BOLD,color=ft.Colors.GREY),
                                                       ft.Divider(height=10,color=ft.Colors.TRANSPARENT),
                                                       ft.Row(
                                                           alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                           controls = [
                                                               ft.Column([
                                                                   ft.Text("Calories",size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.DEEP_ORANGE),
                                                                   ft.Text(f"{total_calories:.0f} / {goal_calories:.0f}",size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400)
                                                               ]),

                                                               ft.Column([
                                                                   ft.Text("Proteins",size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.DEEP_ORANGE),
                                                                   ft.Text(f"{total_proteins:.2f} / {goal_proteins:.2f}",size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400)
                                                               ]),
                                                           ]
                                                       ),
                                                       ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                              controls = [
                                                                  ft.Column([
                                                                      ft.Text("Salts", size=28,
                                                                              weight=ft.FontWeight.BOLD,
                                                                              color=ft.Colors.DEEP_ORANGE),
                                                                      ft.Text(f"{total_salts:.2f} / {goal_salts:.2f}",
                                                                              size=12,
                                                                              weight=ft.FontWeight.BOLD,
                                                                              color=ft.Colors.GREY_400)
                                                                  ]),
                                                                  ft.Column([
                                                                      ft.Text("Water", size=28,
                                                                              weight=ft.FontWeight.BOLD,
                                                                              color=ft.Colors.DEEP_ORANGE),
                                                                      ft.Text(f"{total_water:.0f} / {goal_water:.0f}",
                                                                              size=12,
                                                                              weight=ft.FontWeight.BOLD,
                                                                              color=ft.Colors.GREY_400)
                                                                  ])
                                                              ]
                                                              )
                                                       ])
        )
        self.enter_foodlog = ft.ExpansionTile(bgcolor=ft.Colors.WHITE,title="Enter Food",
                                     controls = [
                                         ft.Text("Enter Food",size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                         self.food_input,
                                         ft.Text("Enter Calories",size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                         self.calories_input,
                                         ft.Text("Enter Salts",size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                         self.salts_input,
                                         ft.Text("Enter Proteins",size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                         self.proteins_input,
                                         ft.Text("Enter Meal Type",size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                         self.meal_types,
                                         ft.ElevatedButton("Enter Food",on_click=handle_food_submit),

                                     ])
        self.enter_waterlog = ft.ExpansionTile(bgcolor=ft.Colors.WHITE,title="Enter Water",
                                               controls = [
                                                   ft.Text("Enter Amount"),
                                                   self.water_input,
                                                   ft.ElevatedButton("Enter",on_click=handle_water_submit),
                                               ])
        self.display_foodlog = ft.ExpansionTile(bgcolor=ft.Colors.WHITE,title="Food Logs",
                                            controls = [self.foodlog_list])

        self.display_waterlog = ft.ExpansionTile(bgcolor=ft.Colors.WHITE,title="Water Logs",
                                             controls = [self.waterlog_list])
        scrollable = ft.Column([
            self.header,
            self.stats_card,
            self.enter_foodlog,
            self.enter_waterlog,
            self.display_foodlog,
            self.display_waterlog,
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