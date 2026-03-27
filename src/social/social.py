'''
File for social page - accessible by clicking 'social' on nav bar
'''

import flet as ft

from components.userpfp import Userpfp
from components.bottom_nav import NavBar
from components.responsive import Responsive
from social.social_service import add_friend_by_username, list_friends

#Sizes of all elements on homepage (as a percent of screen)
page_title_size = 0.1
page_desc_size = 0.03
leaderboard_v_size = 0.18
standings_v_size = 0.08
activity_v_size=0.18

class SocialPage(ft.Column):
    def __init__(self, page: ft.Page, user_id):
        super().__init__()

        self.this_page = page
        # Store the current user id
        self.user_id = user_id
        self.r = Responsive(page)

            # placeholder data
        self.user_name = "User"
        self.user_rank = 4
        self.user_points = 320

        self.leaderboard_data = [
           {"name": "User A", "points": 520},
           {"name": "User B", "points": 470},
           {"name": "User C", "points": 410},
           {"name": "User", "points": 320},
                ]
        self.activity_data = [
            {"name": "User 1", "activity": "completed a workout", "time": "Today"},
            {"name": "User 2", "activity": "logged nutrition", "time": "Today"},
            {"name": "User 3", "activity": "recorded a run", "time": "Yesterday"},
                ]

        self.page_title = ft.Text(
            value="Social",
            size=self.r.w(page_title_size),
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK
            )

        self.page_desc = ft.Text(
            value="Connect with other users",
            size=self.r.w(page_desc_size),
            color=ft.Colors.GREY
                )
        self.userpfp = Userpfp(page)

        self.rank_container = ft.Container(bgcolor=ft.Colors.ORANGE_200, border_radius=10, padding=20,
                                                   content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                                  controls=[
                                                                      ft.Text(f"Rank #{self.user_rank}", size=20,
                                                                              weight=ft.FontWeight.BOLD),
                                                                      ft.Text(f"{self.user_points} pts", size=18)]))
        self.leaderboard_title = ft.Text(
            value="Leaderboard",
            size=self.r.w(page_desc_size),
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK
            )

        self.first_container = ft.Container(
             border=ft.Border.all(width=2, color=ft.Colors.GREY_400),
             border_radius=8,
             padding=10
             )

        self.second_container = ft.Container(
             border=ft.Border.all(width=2, color=ft.Colors.GREY_400),
             border_radius=8,
             padding=10
             )

        self.third_container = ft.Container(
             border=ft.Border.all(width=2, color=ft.Colors.GREY_400),
             border_radius=8,
             padding=10
             )

        self.activity_title = ft.Text(
             value="Recent Activity",
             size=self.r.w(page_desc_size),
             weight=ft.FontWeight.BOLD,
             color=ft.Colors.BLACK
            )

        self.activity_container = ft.Container(
             border=ft.Border.all(width=2, color=ft.Colors.GREY_400),
             border_radius=8,
             padding=10

            )

        self.nav_bar = NavBar(page)
        self.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        expand=True,
                        controls=[
                            self.page_title,
                            self.page_desc
                        ]
                    ),
                    self.userpfp
                ]
            ),
            self.rank_container,
            self.leaderboard_title,
            self.first_container,
            self.second_container,
            self.third_container,
            self.activity_title,
            self.activity_container,
            self.nav_bar
        ]

        self.expand = True
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.set_widget_size()
        self.load_leaderboard()
        self.load_activity()
        page.on_resize = self.resize

        # Load leaderboard data into the 3 containers
    def load_leaderboard(self):
            sorted_users = sorted(
                self.leaderboard_data,
                key=lambda x: x["points"],
                reverse=True
            )

            self.first_container.content = ft.Text(
                f"1. {sorted_users[0]['name']} - {sorted_users[0]['points']} pts"
            )

            self.second_container.content = ft.Text(
                f"2. {sorted_users[1]['name']} - {sorted_users[1]['points']} pts"
            )

            self.third_container.content = ft.Text(
                f"3. {sorted_users[2]['name']} - {sorted_users[2]['points']} pts"
            )

        # Load activity feed into activity container
    def load_activity(self):
            activity_controls = []

            for item in self.activity_data:
                activity_controls.append(
                    ft.ListTile(
                        title=ft.Text(item["name"]),
                        subtitle=ft.Text(item["activity"]),
                        trailing=ft.Text(item["time"])
                    )
                )

            self.activity_container.content = ft.Column(activity_controls)

    #Set size of all text on screen
    def set_text_size(self):
        self.page_title.size = self.r.w(page_title_size)
        self.page_desc.size = self.r.w(page_desc_size)
        self.activity_title.size = self.r.w(page_desc_size)
        self.leaderboard_title.size = self.r.w(page_desc_size)


    #Set width and height of all widgets on the screen
    def set_widget_size(self):
        #leaderboard widget - rectangle
        self.rank_container.height = self.r.h(leaderboard_v_size)
        #Standings widgets - rectangle
        self.first_container.height = self.r.h(standings_v_size)
        self.second_container.height = self.r.h(standings_v_size)
        self.third_container.height = self.r.h(standings_v_size)
        #Friends activity widget - rectangle
        self.activity_container.height = self.r.h(activity_v_size)

    def resize(self, e):
        self.r = Responsive(self.this_page)

        #Resize all text on the page
        self.set_text_size()
        self.set_widget_size()

        self.userpfp.resize()
        self.nav_bar.resize()

        self.update()

def main_social(page: ft.Page, user_id):
    social_page = SocialPage(page, user_id)

    return social_page