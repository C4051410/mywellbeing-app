import flet as ft

def main(page: ft.Page):
    page.title = "Flet Application"
    text = ft.Text("Hello World")
    page.add(ft.Row(controls=[text]))
ft.run(main)
