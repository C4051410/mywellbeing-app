
import flet as ft
from components.responsive import Responsive
from database.connection import connect

conn = connect()
class AdminApp(ft.Column):
    def __init__(self, page: ft.Page):

        super().__init__()
        self.admin_page = page
        self.r = Responsive(page)
        self.Title = ft.Text("ADMIN PAGE")
        self.user_list = ft.Column(controls=[ft.Text("Users")])
        self.retrieve_users()
        self.controls = [
            self.Title,
            self.user_list
        ]

    def retrieve_users(self):
        if conn is not None:
            cur = conn.cursor()
            cur.execute("SELECT username,email,role FROM users WHERE role != %s",("admin",))
            rows = cur.fetchall()
            for data in rows:
                self.user_list.controls.append(ft.Row(controls = [ft.Text(str(data[0])),ft.Text(str(data[1])),ft.Text(str(data[2]))]))
                print()
            cur.close()

def main_admin(page: ft.Page):
    admin_page = AdminApp(page)
    return admin_page

