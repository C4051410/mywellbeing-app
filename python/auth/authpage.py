import flet as ft
from auth.register import register
from auth.login import login

def authPage(on_login_success):
    message = ft.Text()
    # signup fields
    username = ft.TextField(label="Username")
    fullname = ft.TextField(label="Full Name")
    email = ft.TextField(label="Email")
    password = ft.TextField(label="Password", password=True)

    # fields only show on the signup page
    signup = [username, fullname]

    def handle_login(e):
        # logs in users
        logged_in = login(email.value, password.value)
        if isinstance(logged_in, tuple):
            on_login_success(logged_in[0])
        else:
            message.value = str(logged_in)
            e.page.update()

    def handle_register(e):
        # registers users
        registered = register(username.value, fullname.value, password.value, email.value)
        message.value = str(registered)
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
        content=ft.Column([
            username, fullname, email, password,
            signup_buttons, login_buttons, message
        ]))