'''
File for social page - accessible by clicking 'social' on nav bar
'''

import flet as ft

from components.userpfp import Userpfp
from components.bottom_nav import NavBar
from components.responsive import Responsive

# Sizes of all elements on homepage (as a percent of screen)
page_title_size = 0.1
page_desc_size = 0.03

class SocialPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.r = Responsive(page)
        self.this_page = page

        # --- HEADER ---
        self.page_title = ft.Text(value="Social", size=self.r.w(page_title_size), color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)
        self.page_desc = ft.Text(value="Connect with friends", size=self.r.w(page_desc_size), color=ft.Colors.GREY)
        self.userpfp = Userpfp(page)

        # --- MOCK DATA FOR UI ---
        # Later, you can fetch this from your PostgreSQL database!
        leaderboard_data = [
            {"rank": 1, "name": "Sarah Connor", "pts": "12,450", "color": ft.Colors.AMBER},
            {"rank": 2, "name": "Michael Smith", "pts": "10,200", "color": ft.Colors.GREY_400},
            {"rank": 3, "name": "You", "pts": "8,400", "color": ft.Colors.BROWN_400}
        ]

        activity_feed_data = [
            {"name": "Sarah Connor", "action": "crushed a 5km run!", "time": "2 hours ago", "icon": ft.Icons.DIRECTIONS_RUN},
            {"name": "David Wallace", "action": "hit their daily calorie goal.", "time": "4 hours ago", "icon": ft.Icons.LOCAL_FIRE_DEPARTMENT},
            {"name": "Michael Smith", "action": "completed a 45 min workout.", "time": "Yesterday", "icon": ft.Icons.FITNESS_CENTER},
            {"name": "Pam Beesly", "action": "logged 3 liters of water.", "time": "Yesterday", "icon": ft.Icons.WATER_DROP},
        ]

        # --- LEADERBOARD CARD ---
        leaderboard_controls = [
            ft.Text("WEEKLY LEADERBOARD", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
            ft.Divider(height=5, color=ft.Colors.TRANSPARENT)
        ]

        for user in leaderboard_data:
            leaderboard_controls.append(
                ft.ListTile(
                    leading=ft.CircleAvatar(content=ft.Text(str(user["rank"])), bgcolor=user["color"], color=ft.Colors.WHITE),
                    title=ft.Text(user["name"], weight=ft.FontWeight.BOLD),
                    trailing=ft.Text(f"{user['pts']} pts", color=ft.Colors.DEEP_ORANGE, weight=ft.FontWeight.BOLD)
                )
            )

        self.leaderboard_card = ft.Container(
            bgcolor=ft.Colors.WHITE, border_radius=10, padding=15, shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            content=ft.Column(leaderboard_controls)
        )

        # --- FRIENDS ACTIVITY FEED ---
        feed_controls = [
            ft.Text("FRIENDS ACTIVITY", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
            ft.Divider(height=5, color=ft.Colors.TRANSPARENT)
        ]

        for activity in activity_feed_data:
            feed_controls.append(
                ft.ListTile(
                    leading=ft.Icon(activity["icon"], color=ft.Colors.BLUE_400, size=30),
                    title=ft.Text(activity["name"], weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"{activity['action']}\n{activity['time']}", color=ft.Colors.GREY_600),
                )
            )

        self.activity_card = ft.Container(
            bgcolor=ft.Colors.WHITE, border_radius=10, padding=15, shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            content=ft.Column(feed_controls)
        )

        self.nav_bar = NavBar(page)

        # --- LAYOUT ASSEMBLY ---
        header_row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Column(expand=True, controls=[self.page_title, self.page_desc]), self.userpfp])

        scrollable_content = ft.Column(
            controls=[header_row, self.leaderboard_card, self.activity_card],
            scroll=ft.ScrollMode.HIDDEN, expand=True, spacing=20
        )

        self.controls = [ft.Container(content=scrollable_content, expand=True, padding=ft.padding.all(15)), self.nav_bar]
        self.expand = True
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        self.set_text_size()
        page.on_resize = self.resize

    def set_text_size(self):
        self.page_title.size = self.r.w(page_title_size)
        self.page_desc.size = self.r.w(page_desc_size)

    def resize(self, e):
        self.r = Responsive(self.this_page)
        self.set_text_size()
        self.userpfp.resize()
        self.nav_bar.resize()
        self.update()

def main_social(page: ft.Page):
    return SocialPage(page)