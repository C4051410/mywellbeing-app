'''
File for nutrition page - accessible by clicking 'nutrition' on nav bar
'''

import os
from datetime import date, timedelta

import flet as ft
import psycopg2
from dotenv import load_dotenv

from components.userpfp import Userpfp
from components.bottom_nav import NavBar
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
#used to generate the nutrition page
class NutritionPage(ft.Column):
    #constructor method used to create page
    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.r = Responsive(page) # lets page access size and layout
        self.food_input = ft.TextField(hint_text="Food",height=40)
        self.calories_input = ft.TextField(hint_text="Calories",input_filter=ft.InputFilter(allow=True,regex_string=r"^[0-9]*$",replacement_string=""),height=40) # only allow numerical values
        self.salts_input = ft.TextField(hint_text="Salts",input_filter=ft.InputFilter(allow=True,regex_string=r"^\d*\.?\d*$",replacement_string=""),height=40) # only allow numerical values + "."
        self.proteins_input = ft.TextField(hint_text="Proteins",input_filter=ft.InputFilter(allow=True,regex_string=r"^\d*\.?\d*$",replacement_string=""),height=40)
        self.water_input = ft.TextField(hint_text="ml",input_filter=ft.InputFilter(allow=True,regex_string=r"^[0-9]*$",replacement_string=""),height=40)
        self.meal_types = ft.Dropdown(hint_text="Enter Meal Type", width=200, options=[
            ft.DropdownOption(key="Breakfast", text="Breakfast"),
            ft.DropdownOption(key="Lunch", text="Lunch"),
            ft.DropdownOption(key="Dinner", text="Dinner"),
            ft.DropdownOption(key="Snack", text="Snack"),]) # allow users to only select given options
        self.foodlog_list = ft.Column()
        self.waterlog_list = ft.Column()
        #used to handle when Enter Food button is pressed
        def handle_food_submit(e):
            food = self.food_input.value
            calories = self.calories_input.value
            salts = self.salts_input.value
            proteins = self.proteins_input.value
            mealtype = self.meal_types.value
            if not food or not calories or not salts or not proteins or not mealtype: # makes sure values arent empty
                print("Nope")
                return
            self.foodlog_list.controls.append(ft.ExpansionTile(title=food, subtitle = str(date.today()) ,
                                                               controls=[
                                                                   ft.ListTile(title="Calories",subtitle=calories),
                                                                   ft.ListTile(title="Salts",subtitle=salts),
                                                                   ft.ListTile(title="Proteins",subtitle=proteins),
                                                                   ft.ListTile(title="Meal Type",subtitle=mealtype),
                                                               ])) # adds all elements entered to foodlog_list
            if conn is not None: #checks that database connection is valid
                cur = conn.cursor()
                cur.execute("INSERT INTO foodlog (title,calories,salts,proteins,date,mealtype,user_id) VALUES (%s,%s,%s,%s,%s,%s,1)  ",(food,calories,salts,proteins,str(date.today()),mealtype,))
                print("Executed")
                conn.commit()
                cur.close()
            self.food_input.value = "" #used to empty textfield
            self.calories_input.value = ""
            self.salts_input.value = ""
            self.proteins_input.value = ""
            self.meal_types.value = ""
            self.update() #updates the page
        #used to handle when Enter Water button is pressed
        def handle_water_submit(e):
            water = self.water_input.value
            if not water: #checks water field isn't empty
                print("Nope")
                return
            self.foodlog_list.controls.append(ft.ListTile(title=str(date.today()),subtitle=water)) #adds date and amount to tile
            if conn is not None: #checks database connection is valid
                cur = conn.cursor()
                cur.execute("INSERT INTO waterlog (water,date,user_id) VALUES (%s,%s,1)",(water,str(date.today()),))
                conn.commit()
                cur.close()
            self.update() #updates the page

        # used to retrieve posts from database
        def retrieve_posts():
            two_days = date.today() - timedelta(days=2) # used to find two days ago
            if conn is not None: # makes sure database connection is valid
                cur = conn.cursor()
                cur.execute("SELECT title,calories,salts,proteins,mealtype,date FROM foodlog WHERE user_id = 1 AND date > (%s) ORDER BY date DESC",(str(two_days),))
                rows = cur.fetchall() # retrieves all results from query
                for data in rows:
                    self.foodlog_list.controls.append(ft.ExpansionTile(title=data[0],subtitle=str(data[5]) + " " + str(data[4]),
                                                               controls=[
                                                                   ft.ListTile(title="Calories",subtitle=str(data[1])),
                                                                   ft.ListTile(title="Salts",subtitle=str(data[2])),
                                                                   ft.ListTile(title="Proteins",subtitle=str(data[3])),
                                                               ])) #takes values from db and display them
                cur.execute("SELECT water,date FROM waterlog WHERE user_id = 1 AND date > (%s) ORDER BY date DESC",(str(two_days),))
                rows = cur.fetchall()
                for data in rows:
                    self.waterlog_list.controls.append(ft.ListTile(title=str(data[0]) + " ml",subtitle=str(data[1]))) #used to display water values from db
                cur.close()
                page.update()

        retrieve_posts() #used to retrieve posts before creating display
        self.header = ft.Container(content=ft.Text("Nutrition",size=32,weight=ft.FontWeight.BOLD),
                              padding=ft.padding.only(top=10,left=10) #creates header for page
        )
        #used to retrieve daily stats
        def retrieve_daily_stats():
            total_c = 0
            total_s = 0.0
            total_p = 0.0
            total_w = 0
            if conn is not None:
                cur = conn.cursor()
                cur.execute("SELECT calories,salts,proteins FROM foodlog WHERE user_id = 1 AND date = %s",(str(date.today()),))
                rows = cur.fetchall()
                for data in rows: #retrieves stats from today and totals them
                    total_c = total_c + data[0]
                    total_s = total_s + data[1]
                    total_p = total_p + data[2]
                cur.execute("SELECT water FROM waterlog WHERE user_id = 1 AND date = %s",(str(date.today()),))
                rows = cur.fetchall()
                for data in rows: # find total water from today
                    total_w = total_w + data[0]

                return total_c, total_s, total_p,total_w # returns all variables
        #used to retrieve the users set goals
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

        total_calories, total_salts, total_proteins, total_water = retrieve_daily_stats() #retrieves users totals from today
        goal_calories, goal_salts, goal_proteins, goal_water = retrieve_user_goals() # retrieves users goals
        #creates container used to display the users totals from the day compared to their goals
        self.stats_card = ft.Container(bgcolor=ft.Colors.WHITE,border_radius=5,padding=5,
                                  shadow = ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
                                  content = ft.Column([ft.Text("Today",size=12,
                                                        weight=ft.FontWeight.BOLD,color=ft.Colors.GREY),
                                                       ft.Divider(height=10,color=ft.Colors.TRANSPARENT),
                                                       ft.Row(
                                                           alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                           controls = [
                                                               ft.Column([
                                                                   ft.Text("Calories",size=28,
                                                                           weight=ft.FontWeight.BOLD,
                                                                           color=ft.Colors.DEEP_ORANGE),#displays the title
                                                                   ft.Text(f"{total_calories:.0f} / {goal_calories:.0f}",
                                                                           size=12,
                                                                           weight=ft.FontWeight.BOLD,
                                                                           color=ft.Colors.GREY_400),#displays the numbers
                                                                   ft.ProgressBar(width = 100, height = 20,
                                                                                  color = ft.Colors.ORANGE_400,
                                                                                  value = total_calories/goal_calories),#visual representation
                                                               ]),

                                                               ft.Column([
                                                                   ft.Text("Proteins",size=28,
                                                                           weight=ft.FontWeight.BOLD,
                                                                           color=ft.Colors.RED_ACCENT),
                                                                   ft.Text(f"{total_proteins:.2f} / {goal_proteins:.2f}",
                                                                           size=12, weight=ft.FontWeight.BOLD,
                                                                           color=ft.Colors.GREY_400),
                                                                   ft.ProgressBar(width = 100, height = 20,
                                                                                  color = ft.Colors.RED_400,
                                                                                  value = total_proteins/goal_proteins),
                                                               ]),
                                                           ]
                                                       ),
                                                       ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                              controls = [
                                                                  ft.Column([
                                                                      ft.Text("Salts", size=28,
                                                                              weight=ft.FontWeight.BOLD,
                                                                              color=ft.Colors.GREEN_ACCENT),
                                                                      ft.Text(f"{total_salts:.2f} / {goal_salts:.2f}",
                                                                              size=12,
                                                                              weight=ft.FontWeight.BOLD,
                                                                              color=ft.Colors.GREY_400),
                                                                      ft.ProgressBar(width = 100, height = 20,
                                                                                     color = ft.Colors.LIGHT_GREEN_400,
                                                                                     value = total_salts/goal_salts),
                                                                  ]),
                                                                  ft.Column([
                                                                      ft.Text("Water", size=28,
                                                                              weight=ft.FontWeight.BOLD,
                                                                              color=ft.Colors.LIGHT_BLUE_ACCENT),
                                                                      ft.Text(f"{total_water:.0f} / {goal_water:.0f}",
                                                                              size=12,
                                                                              weight=ft.FontWeight.BOLD,
                                                                              color=ft.Colors.GREY_400),
                                                                      ft.ProgressBar(width = 100, height = 20,
                                                                                     color=ft.Colors.LIGHT_BLUE_400,
                                                                                     value=total_water/goal_water),
                                                                  ])
                                                              ]
                                                              )
                                                       ])
        )
        # creates tile that allows users to enter food logs
        self.enter_foodlog = ft.ExpansionTile(bgcolor=ft.Colors.WHITE,title="Enter Food",
                                              collapsed_bgcolor = ft.Colors.GREY_400,
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
                                         ft.ElevatedButton("Enter Food",on_click=handle_food_submit), #used to call on function when pressed

                                     ])
        # creates tile that allow users to enter water logs
        self.enter_waterlog = ft.ExpansionTile(bgcolor=ft.Colors.WHITE,title="Enter Water",
                                               collapsed_bgcolor=ft.Colors.GREY_400,
                                               controls = [
                                                   ft.Text("Enter Amount"),
                                                   self.water_input,
                                                   ft.ElevatedButton("Enter",on_click=handle_water_submit),
                                               ])
        #used to display food logs in tile
        self.display_foodlog = ft.ExpansionTile(bgcolor=ft.Colors.WHITE,title="Food Logs",
                                                collapsed_bgcolor=ft.Colors.GREY_400,
                                            controls = [self.foodlog_list])
        #used to display water logs in tile
        self.display_waterlog = ft.ExpansionTile(bgcolor=ft.Colors.WHITE,title="Water Logs",
                                                 collapsed_bgcolor=ft.Colors.GREY_400,
                                             controls = [self.waterlog_list])
        scrollable = ft.Column([ #specifies the content which should be allowed to be scrolled
            self.header,
            self.stats_card,
            self.enter_foodlog,
            self.enter_waterlog,
            self.display_foodlog,
            self.display_waterlog,
        ],height=600,scroll=ft.ScrollMode.HIDDEN)
        self.nav_bar = NavBar(page)
        self.controls = [
            scrollable,
            self.nav_bar,

        ]
        self.expand = True #expandeds pages when possible
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN #sets alignment for page

#function called to call upon the page
def main_nutrition(page: ft.Page):
    nutrition_page = NutritionPage(page) # creates page using class
    return nutrition_page # returns page