
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
        self.delete_button = ft.ElevatedButton(content=ft.Text("DEL", size=10))
        self.moderator_button = ft.ElevatedButton(content=ft.Text("MOD", size=10))
        self.retrieve_users()
        self.expand = True
        self.scroll = ft.ScrollMode.HIDDEN
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
                user_row = (ft.Row(controls = [
                ft.Text(str(data[0]),expand=2,size=10),
                ft.Text(str(data[1]), expand=2,size=10),
                ft.Text(str(data[2]),expand=2,size=10),
                ft.Column(controls=[self.delete_button,
                self.moderator_button],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True)]))

                row_outline = (ft.Container(
                    content = user_row,
                    border = ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                    padding = 10,
                    border_radius = 5,
                ))
                self.user_list.controls.append(row_outline)
            cur.close()

def main_admin(page: ft.Page):
    admin_page = AdminApp(page)
    return admin_page

