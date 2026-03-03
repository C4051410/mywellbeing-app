'''
File for re-usable profile pciture component which will be used throughout the app
'''

import flet as ft

userpfpImage = "defaultUserimg.png"

class Userpfp(ft.Container):
    def init(self):
        self.content=ft.Image(src=userpfpImage)
        self.border_radius=ft.BorderRadius.all(100)
        self.alignment = ft.Alignment.CENTER_RIGHT

