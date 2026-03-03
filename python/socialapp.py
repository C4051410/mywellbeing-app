import os
import flet as ft
import psycopg2
from dotenv import load_dotenv
#load variables from .env
load_dotenv()
#retrieves the url to the postgresSQL link in .env
db_url = os.getenv('DATABASE_URL')
#is used to check that the database url is valid and works
def get_connection():
    try:
        #tries to connect to the database and return the connection if valid
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        #if an error occurs it returns None while also printing error
        print(f"Error: {e}")
        return None
def SocialApp():
    #used to store the different workouts and food logs
    social_list = ft.Column()
    #try connecting to the database
    conn = get_connection()
    #if the connection isn't valid, return none
    if conn is None:
        print("No database connection")
    else:
        #allow us to interact with database
        cur = conn.cursor()
        #retrieve all workouts with title, calories, duration
        cur.execute("SELECT title,calories,duration FROM workouts")
        #get all rows retrieved from statement above
        rows = cur.fetchall()
        for data in rows:
            #go through each row and create a post for each one with there details
            social_list.controls.append(ft.ExpansionTile(width = 300,title = str(data[0]),expanded=True,
                                                         controls=[ft.ListTile(title = "Calories",subtitle=str(data[1])),
                                                                   ft.ListTile(title = "Duration",subtitle=str(data[2]))]))
        #this ime retrieve all food logs with title, calories, salts, proteins
        cur.execute("SELECT title,calories,salts,proteins FROM foodlog")
        #gets all rows from above statement
        rows = cur.fetchall()
        for data in rows:
            #goes through each row and create a post for each one
            social_list.controls.append(ft.ExpansionTile(width = 300,title = str(data[0]),expanded=True,
                                                         controls=[ft.ListTile(title = "Calories",subtitle=str(data[1])),
                                                                   ft.ListTile(title = "Salts",subtitle=str(data[2])),
                                                                   ft.ListTile(title = "Proteins",subtitle=str(data[3]))]))

    #returns the container with header and social list
    return ft.Container(content=ft.Column([ft.Text("SOCIAL PAGE"),social_list]))