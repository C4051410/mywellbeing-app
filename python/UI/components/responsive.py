'''
File to be used to ensure elements fit accurately within all screen sizes
'''

import flet as ft

class Responsive:
    def __init__(self, page: ft.Page):
        self.page = page

#Returns pixel size relevant to page size
    def w(self, percent):
        return self.page.width * percent

    def h(self, percent):
        return self.page.height * percent