'''
File for nutrition page - accessible by clicking 'nutrition' on nav bar
'''
import csv
import os
import difflib
from datetime import date, timedelta

import flet as ft
import flet_permission_handler as fph
from plyer import notification

from components.userpfp import Userpfp
from components.bottom_nav import NavBar
from components.responsive import Responsive
from src.database.connection import connect

conn = connect()
#used to generate the nutrition page
class NutritionPage(ft.Column):
    #constructor method used to create page
    def __init__(self, page: ft.Page,user_id):
        super().__init__()
        self.ph = fph.PermissionHandler()
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
        self.food_input = ft.TextField(hint_text="Food",height=40,on_blur=self.find_food_values)
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
        self.userpfp = Userpfp(page)
        async def check_notification():
            status = await self.ph.request(fph.Permission.NOTIFICATION)
            return status
        #used to handle when Enter Food button is pressed
        async def handle_food_submit(e):
            food = self.food_input.value
            calories = self.calories_input.value
            salts = self.salts_input.value
            proteins = self.proteins_input.value
            mealtype = self.meal_types.value
            if not food or not calories or not salts or not proteins or not mealtype: # makes sure values arent empty
                print("Nope")
                return
            self.foodlog_list.controls.append(ft.ExpansionTile(title=food, subtitle = str(date.today()) + " " + mealtype ,
                                                               controls=[
                                                                   ft.ListTile(title="Calories",subtitle=calories),
                                                                   ft.ListTile(title="Salts",subtitle=salts),
                                                                   ft.ListTile(title="Proteins",subtitle=proteins),
                                                               ])) # adds all elements entered to foodlog_list
            if conn is not None: #checks that database connection is valid
                cur = conn.cursor()
                cur.execute("INSERT INTO foodlog (title,calories,salts,proteins,date,mealtype,user_id) VALUES (%s,%s,%s,%s,%s,%s,%s)  ",(food,calories,salts,proteins,str(date.today()),mealtype,user_id,))
                print("Executed")
                conn.commit()
                cur.close()
            notif_status = await check_notification()
            if notif_status == fph.PermissionStatus.GRANTED:
                notification.notify(
                    title = "Food Logged",
                    message = f"Meal Added - {food}",
                    app_name = "MyWellBeing",
                )
            self.food_input.value = "" #used to empty textfield
            self.calories_input.value = ""
            self.salts_input.value = ""
            self.proteins_input.value = ""
            self.meal_types.value = ""
            refresh_stats()
            page.overlay.append(ft.SnackBar(
                content=ft.Text("Food Entered",weight=ft.FontWeight.BOLD),bgcolor=ft.Colors.GREEN, open=True))
            self.update() #updates the page
        #used to handle when Enter Water button is pressed
        def handle_water_submit(e):
            water = self.water_input.value
            if not water: #checks water field isn't empty
                print("Nope")
                return
            self.waterlog_list.controls.append(ft.ListTile(title=str(date.today()),subtitle=water)) #adds date and amount to tile
            if conn is not None: #checks database connection is valid
                cur = conn.cursor()
                cur.execute("INSERT INTO waterlog (water,date,user_id) VALUES (%s,%s,%s)",(water,str(date.today()),user_id,))
                conn.commit()
                cur.close()
            refresh_stats()
            page.overlay.append(ft.SnackBar(
                content=ft.Text("Water Entered", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.GREEN, open=True))
            self.update() #updates the page

        # used to retrieve posts from database
        def retrieve_posts():
            two_days = date.today() - timedelta(days=2) # used to find two days ago
            if conn is not None: # makes sure database connection is valid
                cur = conn.cursor()
                cur.execute("SELECT title,calories,salts,proteins,mealtype,date FROM foodlog WHERE user_id = %s AND date > (%s) ORDER BY date DESC",(user_id,str(two_days),))
                rows = cur.fetchall() # retrieves all results from query
                for data in rows:
                    self.foodlog_list.controls.append(ft.ExpansionTile(title=data[0],subtitle=str(data[5]) + " " + str(data[4]),
                                                               controls=[
                                                                   ft.ListTile(title="Calories",subtitle=str(data[1])),
                                                                   ft.ListTile(title="Salts",subtitle=str(data[2])),
                                                                   ft.ListTile(title="Proteins",subtitle=str(data[3])),
                                                               ])) #takes values from db and display them
                cur.execute("SELECT water,date FROM waterlog WHERE user_id = %s AND date > (%s) ORDER BY date DESC",(user_id,str(two_days),))
                rows = cur.fetchall()
                for data in rows:
                    self.waterlog_list.controls.append(ft.ListTile(title=str(data[0]) + " ml",subtitle=str(data[1]))) #used to display water values from db
                cur.close()
                page.update()

        retrieve_posts() #used to retrieve posts before creating display
        self.header = ft.Container(content=ft.Row(controls=[ft.Text("Nutrition",size=32,weight=ft.FontWeight.BOLD),self.userpfp],alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
        #used to retrieve daily stats
        def retrieve_daily_stats():
            total_c = 0
            total_s = 0.0
            total_p = 0.0
            total_w = 0
            if conn is not None:
                cur = conn.cursor()
                cur.execute("SELECT calories,salts,proteins FROM foodlog WHERE user_id = %s AND date = %s",(user_id,str(date.today()),))
                rows = cur.fetchall()
                for data in rows: #retrieves stats from today and totals them
                    total_c = total_c + data[0]
                    total_s = total_s + data[1]
                    total_p = total_p + data[2]
                cur.execute("SELECT water FROM waterlog WHERE user_id = %s AND date = %s",(user_id,str(date.today()),))
                rows = cur.fetchall()
                for data in rows: # find total water from today
                    total_w = total_w + data[0]

                return total_c, total_s, total_p,total_w # returns all variables
        #used to retrieve the users set goals
        def retrieve_user_goals():
            goal_c = 1
            goal_s = 1.0
            goal_p = 1.0
            goal_w = 1
            if conn is not None:
                cur = conn.cursor()
                cur.execute("SELECT calories_goal, salts_goal, proteins_goal,water_goal FROM user_stats WHERE user_id = %s",(user_id,))
                rows = cur.fetchall()
                for data in rows:
                    goal_c = data[0]
                    goal_s = data[1]
                    goal_p = data[2]
                    goal_w = data[3]
                return goal_c, goal_s, goal_p, goal_w

        total_calories, total_salts, total_proteins, total_water = retrieve_daily_stats() #retrieves users totals from today
        goal_calories, goal_salts, goal_proteins, goal_water = retrieve_user_goals() # retrieves users goals
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
        def refresh_stats():
            total_calories, total_salts, total_proteins, total_water = retrieve_daily_stats()
            goal_calories, goal_salts, goal_proteins, goal_water = retrieve_user_goals()
            self.calories_text.value = f"{total_calories:.0f} / {goal_calories:.0f}"
            self.protein_text.value = f"{total_proteins:.2f} / {goal_proteins:.2f}"
            self.salts_text.value = f"{total_salts:.2f} / {goal_salts:.2f}"
            self.water_text.value = f"{total_water:.0f} / {goal_water:.0f}"
            self.calories_bar.value = total_calories / goal_calories
            self.protein_bar.value = total_proteins / goal_proteins
            self.salts_bar.value = total_salts / goal_salts
            self.water_bar.value = total_water / goal_water

            self.update()

        # creates tile that allows users to enter food logs
        self.enter_foodlog = ft.ExpansionTile(bgcolor=ft.Colors.WHITE,title="Enter Food",
                                              collapsed_bgcolor = ft.Colors.GREY_400,
                                              shape=ft.RoundedRectangleBorder(radius=15),
                                              collapsed_shape=ft.RoundedRectangleBorder(radius=15),
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
                                         ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                                         ft.ElevatedButton("Enter Food",on_click=handle_food_submit), #used to call on function when pressed
                                         ft.Divider(height=5,color=ft.Colors.TRANSPARENT)

                                     ])
        # creates tile that allow users to enter water logs
        self.enter_waterlog = ft.ExpansionTile(bgcolor=ft.Colors.WHITE,title="Enter Water",
                                               collapsed_bgcolor=ft.Colors.GREY_400,
                                               shape=ft.RoundedRectangleBorder(radius=15),
                                               collapsed_shape=ft.RoundedRectangleBorder(radius=15),
                                               controls = [
                                                   ft.Text("Enter Amount"),
                                                   self.water_input,
                                                   ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                                                   ft.ElevatedButton("Enter",on_click=handle_water_submit),
                                                   ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                                               ])
        #used to display food logs in tile
        self.display_foodlog = ft.ExpansionTile(bgcolor=ft.Colors.WHITE,title="Food Logs",
                                                collapsed_bgcolor=ft.Colors.GREY_400,
                                                shape=ft.RoundedRectangleBorder(radius=15),
                                                collapsed_shape=ft.RoundedRectangleBorder(radius=15),
                                            controls = [self.foodlog_list])
        #used to display water logs in tile
        self.display_waterlog = ft.ExpansionTile(bgcolor=ft.Colors.WHITE,title="Water Logs",
                                                 collapsed_bgcolor=ft.Colors.GREY_400,
                                                 shape=ft.RoundedRectangleBorder(radius=15),
                                                 collapsed_shape=ft.RoundedRectangleBorder(radius=15),
                                             controls = [self.waterlog_list])
        scrollable = ft.Column([ #specifies the content which should be allowed to be scrolled
            self.header,
            self.stats_card,
            self.enter_foodlog,
            self.enter_waterlog,
            self.display_foodlog,
            self.display_waterlog,
        ],expand=True,scroll=ft.ScrollMode.HIDDEN)
        self.nav_bar = NavBar(page)
        self.controls = [
            scrollable,
            self.nav_bar,

        ]
        self.expand = True #expandeds pages when possible
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN #sets alignment for page

    def find_food_values(self,e):
        search_query = self.food_input.value.strip().lower()
        self.main_page.overlay.clear()
        if search_query in self.food_db:
            data = self.food_db[search_query]
            self.calories_input.value = str(data['calories'])
            self.salts_input.value = str(data['salts'])
            self.proteins_input.value = str(data['proteins'])
            self.calories_input.update()
            self.salts_input.update()
            self.proteins_input.update()
            self.main_page.overlay.append(ft.SnackBar(
                content=ft.Text(f"Found values for '{data['name']}'"),
                bgcolor=ft.Colors.BLUE_400,
                open=True
            ))
            self.main_page.update()
            self.update()
        elif len(search_query)>2:
            food_names = list(self.food_db.keys())
            matches = difflib.get_close_matches(search_query,food_names,n=1,cutoff=0.6)
            if matches:
                suggestion = matches[0]
                self.main_page.overlay.append(ft.SnackBar(
                    content=ft.Text(f"Did you mean {suggestion.title()}?"),action="Yes!",
                    on_action = lambda _: self.apply_suggestion(suggestion),bgcolor=ft.Colors.BLUE_400,
                    open=True))
            self.main_page.update()

        else:
            pass
    def apply_suggestion(self,suggestion):
        self.food_input.value = suggestion.title()
        self.find_food_values(None)
        self.update()

#function called to call upon the page
def main_nutrition(page: ft.Page,user_id):
    nutrition_page = NutritionPage(page,user_id) # creates page using class
    return nutrition_page # returns page