import flet as ft

from components.responsive import Responsive
from database.connection import connect
from moderator.moderator_services import retrieve_posts_moderator, remove_posts_moderator


#use class to make factory for making page
class ModeratorApp(ft.Column):
    #constructor used to make page
    def __init__(self, page: ft.Page):
        #refers to parent class, so it knows it's in a column
        super().__init__(page)
        #sets page to mod_page
        self.mod_page = page
        #makes page responsive to size change
        self.r = Responsive(page)
        self.Title = ft.Text("MODERATOR PAGE")
        #will store user posts
        self.user_posts = ft.Column()
        #creates search bar
        self.search_bar = ft.TextField(label="SEARCH FOR USERS",
                                       on_change = self.on_search_change)
        #always try to expand when page changes size
        self.expand = True
        #allow page to scroll
        self.scroll = ft.ScrollMode.HIDDEN
        #updates user_posts
        self.retrieve_posts()
        #add content to page
        self.controls = [
            self.Title,
            self.search_bar,
            self.user_posts,
        ]

    def retrieve_posts(self,search_query=""):
        #clear user posts
        self.user_posts.controls.clear()
        #retrieve all users, with optional search_query
        rows = retrieve_posts_moderator(search_query)
        for data in rows:
            #for each post create a row with the details and buttons
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
            #add each row to user_posts
            self.user_posts.controls.append(row_outline)

    def delete_posts(self,post_id: int,src:str):
        #calls upon delete post function
        remove_posts_moderator(post_id,src)
        #updates user_posts
        self.user_posts.controls.clear()
        self.retrieve_posts()

    def on_search_change(self,e):
        #gets results which match search bar
        self.retrieve_posts(search_query=self.search_bar.value)


def main_moderator(page: ft.Page):
    mod_page = ModeratorApp(page)
    return mod_page