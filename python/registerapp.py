import flet as ft
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv('DATABASE_URL')
def get_connection():
    try:
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None

def RegisterApp():
    register = ft.Text("Please enter your details")
    username = ft.TextField(label="Enter your username")
    password = ft.TextField(label="Enter your password", password=True, can_reveal_password=True)
    confirm_password = ft.TextField(label="Confirm your password",password=True, can_reveal_password=True)
    email = ft.TextField(label="Enter your email")
    age = ft.TextField(label="Enter your age",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9]*$",replacement_string=""))
    def check_register():
        conn = get_connection()
        if conn is None:
            return False
        else:
            if username.value == "" or password.value == "" or confirm_password.value == ""  or email.value == "" or age.value == "" or age.value == "":
                print("Failed to enter")
            else:
                try:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO users (username, password, email, age,role) VALUES (%s, %s, %s, %s, %s)",(username.value,password.value,email.value,age.value, "user"))
                    conn.commit()
                    cur.close()
                    conn.close()
                except Exception as e:
                    print(f"Error: {e}")
                    conn.close()
    return ft.Container(ft.Column([register, username, password,confirm_password,email,age,ft.ElevatedButton("Enter",on_click=check_register)]))