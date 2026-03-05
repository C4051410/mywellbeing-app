'''
File that is used for running all UI elements within the app

MAY BE UNNECESSARY ONCE MERGED WITH REST OF APPLICATION
'''

import flet as ft

from pages.homepage import main_homepage
from pages.activities import main_activities
from pages.nutrition import main_nutrition
from pages.social import main_social
from pages.settings import main_settings
from pages.map import main_map

def main(page: ft.Page):
    page.title = "My Wellbeing"

    def route_change():
        page.clean()
        if page.route != current_page:
            print("Changing")
            if page.route == "/home":
                page.add(main_homepage(page))
            if page.route == "/activities":
                page.add(main_activities(page))
            if page.route == "/nutrition":
                page.add(main_nutrition(page))
            if page.route == "/social":
                page.add(main_social(page))
            if page.route == "/settings":
                page.add(main_settings(page))
            if page.route == "/map":
                    page.add(main_map(page))

            page.update()

    page.on_route_change = route_change

    # Default to light mode
    # TODO - Allow user to change mode in settings
    page.theme_mode = ft.ThemeMode.LIGHT

    # Font to be used throughout app
    page.fonts = {
        "Dubai": "/assets/DUBAI-REGULAR.TTF"
    }

    page.theme = ft.Theme(
        font_family="Dubai",
    )

    # TODO - REMOVE FROM FINAL BUILD - FOR TESTING ONLY
    # Mobile phone like resolution
    page.window.width = 360
    page.window.height = 800
    page.window.resizable = False
    page.window.alignment = ft.Alignment.CENTER

    # Ensures nav bar stretches across full screen
    page.padding = 10

    page.update()

    page.add(main_homepage(page))

current_page = "/homepage"

def testFunc():
    print("Someting")

ft.run(main, assets_dir='assets')