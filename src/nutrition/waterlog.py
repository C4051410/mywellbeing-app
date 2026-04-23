from plyer import notification

from nutrition.nutrition_services import save_waterlog
from datetime import date
import flet as ft

#used to return page
def main_waterlog(page:ft.Page):

    #used to allow user to go back to nutrition page
    def go_back(e):
        page.go("/nutrition")

    #used to save waterlog
    def save_and_finish(e):
        #retrievs entered value
        water = water_input.value
        #tries and saves waterlog
        success,message = save_waterlog(water,date.today(),page.user_id)
        #if failed, display snackbar explaining why
        if success == False:
            page.overlay.append(ft.SnackBar(
                content=ft.Text("Please Enter a Value"),
                bgcolor=ft.Colors.RED_400,
                open=True,
            ))
            page.update()
            return
        #else display snackbar showing success
        else:
            page.overlay.append(ft.SnackBar(
                content=ft.Text("Water Logged"),
                bgcolor=ft.Colors.GREEN_400,
                open=True,
            ))
            page.update()
            #sends user back to nutrition automatically
            page.go("/nutrition")
    #lets user input only interger values
    water_input = ft.TextField(
        hint_text="Enter Amount (ml)",
        input_filter = ft.InputFilter(allow=True,regex_string=r"^[0-9]*$",replacement_string=""),
        height=40
    )
    #creates button to let user go back
    back_button = ft.Container(
        content=ft.FloatingActionButton(
            content=ft.Icon(ft.Icons.ARROW_BACK, color=ft.Colors.BLACK),
            bgcolor=ft.Colors.WHITE,
            on_click=go_back,
            mini=True
        ),
    )
    #used to let user confirm
    save_button = ft.FloatingActionButton(
        content=ft.Text("LOG WATER"),
        bgcolor=ft.Colors.GREEN_400,
        width=140,
        on_click=save_and_finish,

    )
    #returns column of content in controls
    return ft.Column(
        controls=[
            back_button,
            ft.Text("Enter The Amount Of Water"),
            water_input,
            save_button,
        ],
        width = 300,
        scroll = ft.ScrollMode.AUTO
    )

