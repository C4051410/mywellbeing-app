import flet as ft
from auth.register import register
from auth.login import login
from auth.auth_services import login_user, register_user, refresh_inactivity_timer, save_session


def authPage(on_login_success, on_register_success):
    # signup fields
    username = ft.TextField(label="Username",input_filter=ft.InputFilter(allow=True,regex_string="^[^\s]*$",replacement_string=""))
    email = ft.TextField(label="Email",input_filter=ft.InputFilter(allow=True,regex_string="^[^\s]*$",replacement_string=""))
    password = ft.TextField(label="Password", password=True,input_filter=ft.InputFilter(allow=True,regex_string="^[^\s]*$",replacement_string=""))
    def fail_snackbar(message,e):
        e.page.overlay.clear()
        e.page.overlay.append(ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.RED_400,
            open = True
        ))
        e.page.update()
    # fields only show on the signup page
    signup = [username]

    def handle_login(e):
        success,user = login_user(email.value, password.value)
        #logs in user if successful
        if success:
            #save the login for the next time they load the app
            save_session(user[0])
            # refreshes the inactivity timer used to send email notification
            refresh_inactivity_timer(user[0],user[1])
            on_login_success(user[0])
        #displays specific failed category
        else:
            fail_snackbar(user,e)
            e.page.update()

    def handle_register(e):
        # registers users
        e.page.update()
        success,user = register_user(username.value,email.value, password.value)
        #successfully registers user if successful
        if success:
            on_register_success(user)
        #display specific failed category
        else:
            fail_snackbar(user,e)
            e.page.update()

    def show_register(e):
        for field in signup:
            # makes username and name visible
            field.visible = True
        signup_buttons.visible = True
        login_buttons.visible = False
        e.page.update()

    def show_login(e):
        for field in signup:
            # hides username and name fields
            field.visible = False
        signup_buttons.visible = False
        login_buttons.visible = True
        e.page.update()

    # buttons to show when user is registering
    signup_buttons = ft.Column([
        ft.ElevatedButton("Register", on_click=handle_register),
        ft.TextButton("Already have an account? Login", on_click=show_login)
    ])

    # buttons to show when the user is logging in
    login_buttons = ft.Column([
        ft.ElevatedButton("Login", on_click=handle_login),
        ft.TextButton("Need an account? Sign up", on_click=show_register)
    ], visible=False)

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[ft.Colors.ORANGE_100, ft.Colors.WHITE, ft.Colors.DEEP_ORANGE_50],
        ),
        content=ft.Column(
            controls=[
                ft.Container(expand=True),
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    border_radius=24,
                    padding=ft.padding.symmetric(horizontal=28, vertical=32),
                    shadow=ft.BoxShadow(spread_radius=0, blur_radius=30,
                                        color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 8)),
                    content=ft.Column([
                        username, email, password,
                        signup_buttons, login_buttons,
                    ]),
                    margin=ft.margin.symmetric(horizontal=20),
                ),
                ft.Container(expand=True),
            ],
            expand=True,
        )
    )