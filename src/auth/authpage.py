import flet as ft
from auth.register import register
from auth.login import login
from auth.auth_services import login_user, register_user, refresh_inactivity_timer


def authPage(on_login_success, on_register_success):
    message = ft.Text(color=ft.Colors.RED)
    # signup fields
    username = ft.TextField(label="Username")
    email = ft.TextField(label="Email")
    password = ft.TextField(label="Password", password=True)

    # fields only show on the signup page
    signup = [username]

    def handle_login(e):
        success,user = login_user(email.value, password.value)
        #logs in user if successful
        if success:
            #refreshes the inactivity timer used to send email notification
            refresh_inactivity_timer(user[0],user[1])
            on_login_success(user[0])
        #displays specific failed category
        else:
            message.value = user
            e.page.update()

    def handle_register(e):
        # registers users
        message.value = ""
        e.page.update()
        success,user = register_user(username.value,email.value, password.value)
        #successfully registers user if successful
        if success:
            on_register_success(user)
        #display specific failed category
        else:
            message.value = user
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
            username, email, password,
            signup_buttons, login_buttons, message
        ]))