'''
File for social page - accessible by clicking 'social' on nav bar
'''

import flet as ft

from UI.components.userpfp import Userpfp
from UI.components.bottom_nav import NavBar
from UI.components.responsive import Responsive

#Sizes of all elements on homepage (as a percent of screen)
page_title_size = 0.1
page_desc_size = 0.03
leaderboard_v_size = 0.18
standings_v_size = 0.08
activity_v_size=0.18

class SocialPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.r = Responsive(page)

        self.page_title = ft.Text(
            value="Social",
            size=self.r.w(page_title_size),
            color=ft.Colors.BLACK
        )

        self.page_desc = ft.Text(
            value="Connect with friends",
            size=self.r.w(page_desc_size),
            color=ft.Colors.GREY
        )

        self.rank_container = ft.Container(
            bgcolor = ft.Colors.ORANGE_200
        )

        self.leaderboard_title = ft.Text(
            value = "Leaderboard",
            size = self.r.w(page_desc_size),
            color=ft.Colors.BLACK
        )

        self.first_container = ft.Container(
            border = ft.Border.all(width=2, color=ft.Colors.GREY_400)
        )

        self.second_container = ft.Container(
            border = ft.Border.all(width=2, color=ft.Colors.GREY_400)
        )

        self.third_container = ft.Container(
            border=ft.Border.all(width=2, color=ft.Colors.GREY_400)
        )

        self.activity_title = ft.Text(
            value = "Friends Activity",
            size = self.r.w(page_desc_size),
            color=ft.Colors.BLACK
        )

        self.activity_container = ft.Container(
            border = ft.Border.all(width=2, color=ft.Colors.GREY_400)
        )

        self.userpfp = Userpfp(page)

        self.nav_bar = NavBar(page)

        self.controls =[
            #Header row
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

        self.expand=True
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.set_widget_size()

        self.this_page = page
        page.on_resize = self.resize

    #Set size of all text on screen
    def set_text_size(self):
        self.page_title.size = self.r.w(page_title_size)
        self.page_desc.size = self.r.w(page_desc_size)
        self.activity_title = self.r.w(page_desc_size)
        self.leaderboard_title = self.r.w(page_desc_size)


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

def main_social(page: ft.Page):
    social_page = SocialPage(page)

    return social_page