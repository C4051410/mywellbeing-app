import flet as ft

def RegisterApp():
    login = ft.Text("Please enter your details")
    username = ft.TextField(label="Enter your username")
    password = ft.TextField(label="Enter your password", password=True, can_reveal_password=True)
    confirm_password = ft.TextField(label="Confirm your password",password=True, can_reveal_password=True)
    email = ft.TextField(label="Enter your email")
    age = ft.TextField(label="Enter your age",input_filter=ft.InputFilter(allow=True,regex_string="^[0-9]*$",replacement_string=""))

    return ft.Container(ft.Column([login, username, password,confirm_password,email,age]))