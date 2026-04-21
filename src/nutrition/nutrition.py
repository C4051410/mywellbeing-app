'''
File for nutrition page - accessible by clicking 'nutrition' on nav bar
'''
import csv
import os
from datetime import date, timedelta
import flet as ft

from components.userpfp import Userpfp
from components.bottom_nav import NavBar
from components.responsive import Responsive
from nutrition.nutrition_queries import retrieve_waterlog, retrieve_foodlog, retrieve_daily_stats, retrieve_user_goals

#used to generate the nutrition page
class NutritionPage(ft.Column):
    #constructor method used to create page
    def __init__(self, page: ft.Page,user_id):
        super().__init__()
        self.main_page = page
        self.r = Responsive(page) # lets page access size and layout
        self.food_db = {}
        current_dir = os.path.dirname(__file__)
        csv_path = os.path.join(current_dir, 'foods.csv')
        try:
            with open(csv_path,mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.food_db[row['name'].lower()] = row
        except FileNotFoundError:
            print('foods.csv not found')
        self.water_input = ft.TextField(hint_text="ml",input_filter=ft.InputFilter(allow=True,regex_string=r"^[0-9]*$",replacement_string=""),height=40)
        self.foodlog_list = ft.Column()
        self.foodlog_list.controls.append(ft.Text("ALL RECENT FOOD LOGS", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500))
        self.waterlog_list = ft.Column()
        self.waterlog_list.controls.append(ft.Text("ALL RECENT WATER LOGS", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500))
        self.userpfp = Userpfp(page)
        # used to retrieve posts from database
        def retrieve_posts():
            two_days = date.today() - timedelta(days=2) # used to find two days ago
            f_rows = retrieve_foodlog(user_id,str(two_days))
            if len(f_rows) == 0:
                self.foodlog_list.controls.append(
                    ft.Container(
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(height=25),
                                ft.Icon(ft.Icons.FASTFOOD, size=80, color=ft.Colors.GREY_300),
                                ft.Text("Enter Your Foods", size=24, weight=ft.FontWeight.BOLD),
                                ft.Text("Keep Track of Your Daily Goals", color=ft.Colors.GREY_500, size=14),
                                ft.Container(height=20),
                            ]
                        ),
                        expand=True, alignment=ft.Alignment(0, 0)
                    )
                )
            else:
                for data in f_rows:
                    self.foodlog_list.controls.append(ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            border_radius=10,
                            padding=5,
                            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
                            ink=True,
                            content=ft.ListTile(
                                title=ft.Text(f"{str(data[0])} • {str(data[5])} • {str(data[4])}"),
                                subtitle=ft.Text(f"{str(data[1])} kcal • {str(data[2])}g • {str(data[3])}g")
                            )))
            w_rows = retrieve_waterlog(user_id,str(two_days))
            if len(w_rows) == 0:
                self.waterlog_list.controls.append(
                    ft.Container(
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(height=25),
                                ft.Icon(ft.Icons.WATER_DROP, size=80, color=ft.Colors.GREY_300),
                                ft.Text("Enter Your Water", size=24, weight=ft.FontWeight.BOLD),
                                ft.Text("Keep Track of Your Water Intake", color=ft.Colors.GREY_500, size=14),
                                ft.Container(height=20),
                            ]
                        ),
                        expand=True, alignment=ft.Alignment(0, 0)
                    )
                )
            else:
                for data in w_rows:
                    self.waterlog_list.controls.append(ft.Container(
                        bgcolor=ft.Colors.WHITE,
                        border_radius=10,
                        padding=5,
                        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
                        ink=True,
                        content=ft.ListTile(
                            title=ft.Text(f"{str(data[0])}ml {str(data[1])}"),
                        )
                    ))

        retrieve_posts() #used to retrieve posts before creating display
        self.header = ft.Container(content=ft.Row(controls=[ft.Text("Nutrition",size=32,weight=ft.FontWeight.BOLD),self.userpfp],alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
        #used to retrieve daily stats
        total_calories, total_salts, total_proteins, total_water = retrieve_daily_stats(user_id, date.today()) #retrieves users totals from today
        goal_calories, goal_salts, goal_proteins, goal_water = retrieve_user_goals(user_id) # retrieves users goals
        self.calories_text = ft.Text(f"{total_calories:.0f} / {goal_calories:.0f}",size=12,weight=ft.FontWeight.BOLD,color=ft.Colors.GREY_400)
        self.calories_bar = ft.ProgressBar(width=100, height=20,color=ft.Colors.ORANGE_400,value=total_calories / goal_calories)
        self.protein_text = ft.Text(f"{total_proteins:.2f} / {goal_proteins:.2f}",size=12, weight=ft.FontWeight.BOLD,color=ft.Colors.GREY_400)
        self.protein_bar = ft.ProgressBar(width=100, height=20,color=ft.Colors.RED_400,value=total_proteins / goal_proteins)
        self.salts_text = ft.Text(f"{total_salts:.2f} / {goal_salts:.2f}",size=12,weight=ft.FontWeight.BOLD,color=ft.Colors.GREY_400)
        self.salts_bar = ft.ProgressBar(width=100, height=20,color=ft.Colors.LIGHT_GREEN_400,value=total_salts / goal_salts)
        self.water_text = ft.Text(f"{total_water:.0f} / {goal_water:.0f}", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400)
        self.water_bar = ft.ProgressBar(width=100, height=20, color=ft.Colors.LIGHT_BLUE_400,value=total_water / goal_water)
        #creates container used to display the users totals from the day compared to their goals
        self.stats_card = ft.Container(bgcolor=ft.Colors.WHITE,border_radius=10,padding=10,
                                  shadow = ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
                                  content = ft.Column([ft.Text("Today",size=20,
                                        weight=ft.FontWeight.BOLD,color=ft.Colors.BLACK),
                                       ft.Divider(height=5,color=ft.Colors.TRANSPARENT),
                                       ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                           controls = [
                                               ft.Column([
                                                   ft.Text("Calories",size=28,weight=ft.FontWeight.BOLD, color=ft.Colors.DEEP_ORANGE),#displays the title
                                                   self.calories_text,
                                                   self.calories_bar
                                               ]),

                                               ft.Column([
                                                   ft.Text("Proteins",size=28,weight=ft.FontWeight.BOLD,color=ft.Colors.RED_ACCENT),
                                                   self.protein_text,
                                                   self.protein_bar
                                               ]),
                                           ]),
                                       ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                              controls = [
                                                  ft.Column([
                                                      ft.Text("Salts", size=28,weight=ft.FontWeight.BOLD,color=ft.Colors.GREEN_ACCENT),
                                                      self.salts_text,
                                                      self.salts_bar
                                                  ]),
                                                  ft.Column([
                                                      ft.Text("Water", size=28,weight=ft.FontWeight.BOLD,color=ft.Colors.LIGHT_BLUE_ACCENT),
                                                      self.water_text,
                                                      self.water_bar
                                                  ])
                                              ])
                                       ])
        )
        self.enter_food_btn = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, color=ft.Colors.BLACK, size=14),
                ft.Text("Enter A Food", size=12, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
            bgcolor=ft.Colors.WHITE,
            height=38,
            expand=True,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(color=ft.Colors.GREEN_400, width=1.5)
            ),
            on_click=self.enter_foodlog
        )
        self.enter_water_btn = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, color=ft.Colors.BLACK, size=14),
                ft.Text("Enter A Water", size=12, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
            bgcolor=ft.Colors.WHITE,
            height=38,
            expand=True,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(color=ft.Colors.BLUE_400, width=1.5)
            ),
            on_click=self.enter_water_log
        )
        scrollable = ft.Column([ #specifies the content which should be allowed to be scrolled
            self.header,
            self.stats_card,
            self.enter_food_btn,
            self.enter_water_btn,
            self.foodlog_list,
            self.waterlog_list,
        ],expand=True,scroll=ft.ScrollMode.HIDDEN)
        self.nav_bar = NavBar(page)
        self.controls = [
            scrollable,
            self.nav_bar,

        ]
        self.expand = True #expandeds pages when possible
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN #sets alignment for page


    def enter_foodlog(self,e):
        self.main_page.go("/log-food")

    def enter_water_log(self,e):
        self.main_page.go("/log-water")

#function called to call upon the page
def main_nutrition(page: ft.Page,user_id):
    nutrition_page = NutritionPage(page,user_id) # creates page using class
    return nutrition_page # returns page