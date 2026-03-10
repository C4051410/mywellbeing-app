import flet as ft
from database.connection import connect

def main(page: ft.Page):
    page.title = "Flet Application"

    conn = connect()
    cur = conn.cursor()
    cur.execute("select * from users")
    row = cur.fetchall()
    cur.close()
    conn.close()

    text = ft.Text("Hello World")
    page.add(ft.Row(controls=[text]))
    page.add(ft.Text(f"first row of db: {row}"))
ft.run(main)
