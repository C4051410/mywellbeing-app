from plyer import notification

from nutrition.nutrition_queries import save_waterlog
from datetime import date
import flet as ft

def main_waterlog(page:ft.Page):
    def go_back(e):
        page.go("/nutrition")

    def save_and_finish(e):
        water = water_input.value
        if not water:
            page.overlay.append(ft.SnackBar(
                content=ft.Text("Please Enter a Value"),
                bgcolor=ft.Colors.RED_400,
                open=True,
            ))
            page.update()
            return
        save_waterlog(water,str(date.today()),page.user_id)
        page.overlay.append(ft.SnackBar(
            content=ft.Text("Water Logged"),
            bgcolor=ft.Colors.GREEN_400,
            open=True,
        ))
        notification.notify(
            title="Water Logged",
            message=f"{water}ml Recorded",
            app_name="MyWellBeing"
        )
        page.update()
        page.go("/nutrition")

    water_input = ft.TextField(
        hint_text="Enter Amount (ml)",
        input_filter = ft.InputFilter(allow=True,regex_string=r"^[0-9]*$",replacement_string=""),
        height=40
    )
    back_button = ft.Container(
        content=ft.FloatingActionButton(
            content=ft.Icon(ft.Icons.ARROW_BACK, color=ft.Colors.BLACK),
            bgcolor=ft.Colors.WHITE,
            on_click=go_back,
            mini=True
        ),
    )
    save_button = ft.FloatingActionButton(
        content=ft.Text("LOG WATER"),
        bgcolor=ft.Colors.GREEN_400,
        width=140,
        on_click=save_and_finish,

    )
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

