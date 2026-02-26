import flet as ft

#TODO - Retrieve name of logged in user and pfp
user = "Username"
userpfp = "defaultUserimg.png"

#Default style of all text on screen

@ft.control
class WorkoutApp(ft.Column):
    def init(self):
        #Welcome message and profile picture to be displayed
        self.welcome_message = ft.Column(
            controls=[
                #Greeting for the user
                ft.Text(
                    value=f"Welcome {user}!",
                    size=90,
                    color=ft.Colors.BLACK
                ),
                #Generic motivational message
                ft.Text(
                    value="Lets crush your workout goals today!",
                    size=40,
                    color="grey"
                )
            ]
        )

        self.userpfp = ft.Container(
                        content=ft.Image(src=userpfp),
                        border_radius=ft.border_radius.all(100),
                        alignment=ft.Alignment.CENTER_RIGHT,
                        on_click=self.open_sidebar
                    )

        self.controls=[
            ft.Row(
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    self.welcome_message,
                    self.userpfp
                ],
            ),
            ft.Column(
                visible=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                self.userpfp,
                                ft.ListView(
                                    controls=[
                                        #TODO - Add links to other pages
                                        ft.Text(value="Settings"),
                                        ft.Text(value="Page 2"),
                                        ft.Text(value="Page 3")
                                    ]
                                )
                            ]
                        ),
                        bgcolor=ft.Colors.GREY
                    )
                ]
            )
        ]

    def open_sidebar(self, e):
        #Open the sidebar
        pass


def main(page: ft.Page):
    page.title = "My Wellbeing"
    #Default to light mode
    #TODO - Allow user to change mode in settings
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {
        "Dubai": "/assets/DUBAI-REGULAR.TTF"
    }

    page.theme = ft.Theme(
        font_family = "Dubai",
    )

    page.update()

    app = WorkoutApp()

    page.add(app)

ft.run(main, assets_dir="assets")