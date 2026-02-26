import flet as ft

#TODO - Retrieve name of logged in user and pfp
user = "Username"
userpfp = "defaultUserimg.png"

@ft.control
class WorkoutApp(ft.Column):
    def init(self):
        #Welcome message and profile picture to be displayed
        self.welcome_message = ft.Text(f"Welcome {user}!")
        self.userpfp = ft.Image(src=userpfp, height=50, width=50)

        self.controls=[
            ft.Row(
                tight=True,
                controls=[
                    self.welcome_message,
                    self.userpfp
                ],
            ),
        ]


def main(page: ft.Page):
    page.title = "My Wellbeing"
    #Default to light mode
    #TODO - Allow user to change mode in settings
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    app = WorkoutApp()

    page.add(app)

ft.run(main, assets_dir="assets")