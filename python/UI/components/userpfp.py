'''
File for re-usable profile picture component which will be used throughout the app
'''

import flet as ft

from components.responsive import Responsive

#Source of the user profile picture
#TODO- obtain user pfp from DB
userpfpImage = "defaultUserimg.png"

#Size of all elements (as percent of screen size)
pfp_size = 0.2

class Userpfp(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.r = Responsive(page)

        #Profile pic element
        self.profilePic = ft.Image(
            src=userpfpImage,
            #Fills the container like a profile picture would
            fit=ft.BoxFit.COVER,
        )

        self.content= self.profilePic
        #Align it to the right
        self.alignment = ft.Alignment.CENTER_RIGHT

        self.set_size()

    def set_size(self):
        #Set the size to 12% of screen size
        size = self.r.w(pfp_size)

        self.width = size
        self.height = size
        self.border_radius = size/2

    #Resize the element when page size changes
    def resize(self):
        #Refresh responsive class with new page width and height
        self.r = Responsive(self.page)
        self.set_size()