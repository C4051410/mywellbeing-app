'''
Used for re-usable navigation bar component which will appear at the bottom of the screen throughout the app
'''

import flet as ft

from components.responsive import Responsive

#Size of all components on the page
navbar_height = 0.12
button_width = 0.15
text_size =0.01

#A container of all that is shown on the navBar
class navBar(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.r = Responsive(page)
        #Top border that will separate bar from whatever is shown on screen
        self.border = ft.Border.only(top=ft.BorderSide(color=ft.Colors.GREY_600, width=2))

        #Height of navbar
        self.height = self.r.h(navbar_height)

        #Padding of elements from edge of nav bar
        self.padding = self.r.w(0.008)

        #Text elements for buttons - separated so they can be dynamically resized to page size
        self.home_text = ft.Text(
            value="Home",
            size=self.r.w(text_size)
        )

        self.activities_text = ft.Text(
            value="Activities",
            size=self.r.w(text_size)
        )

        self.nutrition_text= ft.Text(
            value="Nutrition",
            size=self.r.w(text_size)
        )

        self.social_text = ft.Text(
            value="Social",
            size=self.r.w(text_size)
        )

        self.settings_text = ft.Text(
            value="Settings",
            size=self.r.w(text_size)
        )

        #Container elements for buttons - like above

        self.home_container = ft.Container(
            # Width of a button - set the same for all buttons
            width=self.r.w(button_width),
            # Border settings for each individual button
            border=ft.Border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            # Function to call when button is clicked
            on_click=self.home_pressed,
            # Center it
            alignment=ft.Alignment.CENTER,
            # Icon and text
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.HOME_ROUNDED),
                    self.home_text
                ]
            )
        )

        self.activities_container = ft.Container(
            width=self.r.w(button_width),
            border=ft.Border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            on_click=self.activities_pressed,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.DIRECTIONS_RUN_ROUNDED),
                    self.activities_text
                ]
            )
        )

        self.nutrition_container = ft.Container(
            width=self.r.w(button_width),
            border=ft.Border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            on_click=self.nutrition_pressed,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.FOOD_BANK_ROUNDED),
                    self.nutrition_text
                ]
            )
        )

        self.social_container = ft.Container(
            width=self.r.w(button_width),
            border=ft.Border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            on_click=self.social_pressed,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.PEOPLE_OUTLINE_OUTLINED),
                    self.social_text
                ]
            )
        )

        self.settings_container = ft.Container(
            width=self.r.w(button_width),
            border=ft.Border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            on_click=self.settings_pressed,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.SETTINGS),
                    self.settings_text
                ]
            )
        )


        #Row of elements
        self.content=ft.Row(
            #Take as much space as possible (horizontally)
            expand=True,
            #Evenly space objects apart
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                #Individual buttons
                controls=[
                    self.home_container,
                    self.activities_container,
                    self.nutrition_container,
                    self.social_container,
                    self.settings_container
                ]
            )

    def resize(self):
        print("Resizing navBar")

    #TODO-Route user to correct page upon clicking taskbar
    def home_pressed(self):
        print("Home Pressed")

    def activities_pressed(self):
        print("Activities Pressed")

    def nutrition_pressed(self):
        print("Nutrition pressed")

    def social_pressed(self):
        print("Social pressed")

    def settings_pressed(self):
        print("Settings pressed")