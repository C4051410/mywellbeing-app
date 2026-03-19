
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
        self.user_list = ft.Column()
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
            cur.execute("SELECT username,email,role,id FROM users WHERE role != %s",("admin",))
            rows = cur.fetchall()
            self.user_list.controls.clear()
            for data in rows:
                user_id = data[3]
                delete_button = ft.ElevatedButton(
                    content=ft.Text("DEL", size=10),
                    on_click=lambda e,u_id=user_id: self.delete_user(u_id))
                moderator_button=ft.ElevatedButton(
                    content=ft.Text("MOD", size=10))
                user_row = (ft.Row(controls = [
                    ft.Text(str(data[0]),expand=2,size=10),
                    ft.Text(str(data[1]), expand=2,size=10),
                    ft.Text(str(data[2]),expand=2,size=10),
                    ft.Column(controls=[delete_button, moderator_button],
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

    def delete_user(self,user_id: int):
        if conn is not None:
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id = %s",(user_id,))
            conn.commit()
            cur.close()
            self.user_list.controls.clear()
            self.retrieve_users()

def main_admin(page: ft.Page):
    admin_page = AdminApp(page)
    return admin_page

