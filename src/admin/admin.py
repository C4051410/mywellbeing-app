
import flet as ft
from components.responsive import Responsive

class AdminApp(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.admin_page = page
        self.r = Responsive(page)
        self.Title = ft.Text("ADMIN PAGE")
        self.user_list = ft.Column(controls=[ft.Text("Users")])
        self.controls = [
            self.Title,
            self.user_list
        ]

def main_admin(page: ft.Page):
    admin_page = AdminApp(page)
    return admin_page

