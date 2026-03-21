import flet as ft

from components.responsive import Responsive
from database.connection import connect

conn = connect()
class ModeratorApp(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.mod_page = page
        self.r = Responsive(page)
        self.Title = ft.Text("MODERATOR PAGE")
        self.user_posts = ft.Column()
        self.expand = True
        self.scroll = ft.ScrollMode.HIDDEN
        self.retrieve_posts()
        self.controls = [
            self.Title,
            self.user_posts,
        ]

    def retrieve_posts(self):
        if conn is not None:
            cur = conn.cursor()
            cur.execute("SELECT f.title, u.username,f.id FROM foodlog f JOIN users u on f.user_id = u.id")
            rows = cur.fetchall()
            for data in rows:
                posts_row = (ft.Row(controls=[ft.Text(str(data[0]),size=10),
                                              ft.Text(str(data[1]),size=10)]))
                row_outline = (ft.Container(content=posts_row,
                                            border= ft.border.all(1,ft.Colors.OUTLINE_VARIANT),
                                            padding=10,
                                            border_radius=5,))
                self.user_posts.controls.append(row_outline)
            cur.close()



def main_moderator(page: ft.Page):
    mod_page = ModeratorApp(page)
    return mod_page