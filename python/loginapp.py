import os
import flet as ft
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
def get_connection():
    try:
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None

def LoginApp():
    login = ft.Text("Please enter your login details")
    username = ft.TextField(label="Enter your username")
    password = ft.TextField(label="Enter your password",password=True,can_reveal_password=True)
    def check_login():
        conn = get_connection()
        if conn is None:
            return False
        else:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s", (username.value,))
            rows = cur.fetchall()
            for row in rows:
                print(row)
                if row is None:
                    print("Login failed")
                    return False
                if row[3] != password.value:
                    print("Login failed")
                else:
                    print("Login successful")
                    return True
            cur.close()
            conn.close()


    return ft.Container(ft.Column([login,username,password,ft.ElevatedButton("Enter",on_click=check_login)]))