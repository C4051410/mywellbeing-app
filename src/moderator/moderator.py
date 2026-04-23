import flet as ft

from components.responsive import Responsive
from database.connection import connect

from src.moderator.moderator_queries import delete_posts_moderator, retrieve_users_moderators

conn = connect()
class ModeratorApp(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.mod_page = page
        self.r = Responsive(page)
        self.Title = ft.Text("MODERATOR PAGE")
        self.user_posts = ft.Column()
        self.search_bar = ft.TextField(label="SEARCH FOR USERS",
                                       on_change = self.on_search_change)
        self.expand = True
        self.scroll = ft.ScrollMode.HIDDEN
        self.retrieve_posts()
        self.controls = [
            self.Title,
            self.search_bar,
            self.user_posts,
        ]

    def retrieve_posts(self,search_query=""):
        self.user_posts.controls.clear()
        rows = retrieve_users_moderators(search_query)
        for data in rows:
            posts_id = data[2]
            src = data[3]
            delete_button = ft.ElevatedButton(
                content=ft.Text("DEL", size=10),
                on_click=lambda e, p_id=posts_id, s=src: self.delete_posts(p_id,s))
            posts_row = (ft.Row(controls=[ft.Text(str(data[0]),size=10,expand=True),
                                          ft.Text(str(data[1]),size=10,expand=True),
                                          ft.Column(controls=[delete_button],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,expand=True)]))
            row_outline = (ft.Container(content=posts_row,
                                        border= ft.border.all(1,ft.Colors.OUTLINE_VARIANT),
                                        padding=10,
                                        border_radius=5,))
            self.user_posts.controls.append(row_outline)

    def delete_posts(self,post_id: int,src:str):
        delete_posts_moderator(post_id,src)
        self.user_posts.controls.clear()
        self.retrieve_posts()

    def on_search_change(self,e):
        self.retrieve_posts(search_query=self.search_bar.value)



def main_moderator(page: ft.Page):
    mod_page = ModeratorApp(page)
    return mod_page