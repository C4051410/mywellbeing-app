"""
    This module is used to display the front end of the admin page
    which allows the admin to search for users and moderators and
    change their roles or delete their accounts as required
"""
import flet as ft

from admin.admin_services import retrieve_users_admin, remove_users_admin, make_moderators_admin
from auth.auth_services import clear_session
from components.responsive import Responsive



#use class to make factory for making page
class AdminApp(ft.Column):
    # constructor used to make page
    def __init__(self, page: ft.Page):
        #refers to parent class, so it knows it's in a column
        super().__init__()
        #sets page to admin_page
        self.admin_page = page
        # makes page responsive to size change
        self.r = Responsive(page)
        self.Title = ft.Text("ADMIN PAGE")
        #creates search bar
        self.search_bar = ft.TextField(label="SEARCH FOR USERS",
                                       on_change=self.on_search_change)
        #will store users
        self.user_list = ft.Column()
        #updates user_list
        self.retrieve_users()
        #awlays try to expand when page size change
        self.expand = True
        #allows for scrolling
        self.scroll = ft.ScrollMode.HIDDEN
        #add content to page
        self.controls = [
            self.Title,
            self.search_bar,
            self.user_list
        ]

    def retrieve_users(self,search_query=""):
        #retrieve all users and moderators, with optional query
        rows = retrieve_users_admin(search_query)
        #remove users from lists
        self.user_list.controls.clear()
        for data in rows:
            #for each user create a row with details and buttons
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
            #adds each row to user_list
            self.user_list.controls.append(row_outline)

    def delete_user(self,user_id: int):
        #calls upon delete user function
        remove_users_admin(user_id)
        #updates user_list
        self.user_list.controls.clear()
        self.retrieve_users()


    def make_moderator(self,user_id: int):
        #calls upon make_moderator
        make_moderators_admin(user_id)
        self.user_list.controls.clear()
        self.retrieve_users()

    def on_search_change(self,e):
        #gets results which match the search bar
        self.retrieve_users(search_query=self.search_bar.value)



def main_admin(page: ft.Page):
    admin_page = AdminApp(page)
    clear_session()
    return admin_page

