import re

import bcrypt
from plyer import notification

from auth.login import login, get_user_setup
from auth.register import register, get_existing_user


def login_user(email, password):
    #checks fields arent empty
    if not all([email, password]):
        return False, "Please Enter All Fields"
    email = email.lower()
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    #checks email is valid email format
    if not re.match(email_regex, email):
        return False, "Invalid Email"
    #attempts to log user in
    user = login(email, password)
    #checks user exists
    if not user:
        return False, "User Not Found"
    stored_password = user[3].encode()
    #check password matches
    if not bcrypt.checkpw(password.encode(), stored_password):
        return False, "Invalid Password"
    #tries to send email
    try:
        notification.notify(
            title="Login Successful",
            message=f"Welcome Back {user[1]}",
            app_name="MyWellBeing",
        )
    except Exception as e:
        print(e)
    #return true with user data
    return True,user

def register_user(username,email, password):
    #checks all fields have been entered
    if not all([username,email, password]):
        return False, "Please Enter All Fields"
    email = email.lower()
    #check email is correct format
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, email):
        return False, "Please enter a valid email"
    #cehcks passwords greater than 8 characters
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    #check password contains at least 1 uppercase, lowercase, number, and special character
    if not re.search(password_regex, password):
        return False, "Password must at least one uppercase letter, one lowercase letter, one number and one special character"
    #checks for existing users
    existing_user,existing_email = get_existing_user(username, email)
    #checks if user exists already
    if existing_user:
        return False, "User Already Exists"
    #checks if email exists already
    if existing_email:
        return False, "Email Already Exists"
    #register user
    user_id = register(username, email, password)
    #try and send email
    try:
        notification.notify(
            title="Registration Successful",
            message="Account Created Successfully",
            app_name="MyWellBeing",
        )
    except Exception as e:
        print(e)
    #return true with user data
    return True,user_id


def check_setup_complete(user_id):
    if not user_id:
        return False
    try:
        if int(user_id) < 0:
            return False
    except ValueError:
        return False
    setup = get_user_setup(user_id)
    if not setup:
        return False
    return True


