
import flet as ft
from components.responsive import Responsive
from database.connection import connect

from admin.admin_queries import make_moderators_admin, delete_users_admin, retrieve_users_admin

conn = connect()
class AdminApp(ft.Column):
    def __init__(self, page: ft.Page):

        super().__init__()
        self.admin_page = page
        self.r = Responsive(page)
        self.Title = ft.Text("ADMIN PAGE")
        self.search_bar = ft.TextField(label="SEARCH FOR USERS",
                                       on_change=self.on_search_change)
        self.user_list = ft.Column()
        self.retrieve_users()
        self.expand = True
        self.scroll = ft.ScrollMode.HIDDEN
        self.controls = [
            self.Title,
            self.search_bar,
            self.user_list
        ]

    def retrieve_users(self,search_query=""):
        rows = retrieve_users_admin(search_query)
        self.user_list.controls.clear()
        for data in rows:
            user_id = data[3]
            delete_button = ft.ElevatedButton(
                content=ft.Text("DEL", size=10),
                on_click=lambda e,u_id=user_id: self.delete_user(u_id))
            moderator_button=ft.ElevatedButton(
                content=ft.Text("MOD", size=10),
                on_click = lambda e, u_id=user_id: self.make_moderator(u_id))
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

    def delete_user(self,user_id: int):
        delete_users_admin(user_id)
        self.user_list.controls.clear()
        self.retrieve_users()


    def make_moderator(self,user_id: int):
        make_moderators_admin(user_id)
        self.user_list.controls.clear()
        self.retrieve_users()

    def on_search_change(self,e):
        self.retrieve_users(search_query=self.search_bar.value)



def main_admin(page: ft.Page):
    admin_page = AdminApp(page)
    return admin_page

