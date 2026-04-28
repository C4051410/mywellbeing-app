import os
import re

import bcrypt
import resend
from plyer import notification

from auth.login import login, get_user_setup, get_last_email, commit_last_email
from auth.register import register, get_existing_user, commit_setup
from database.connection import email_key
current_dir = os.path.dirname(__file__)

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
    #gets api keys
    resend.api_key = email_key()
    #uses the test email, as we dont have the costs to buy domain
    #on deployment, would remove this and use email
    test_email = "m.austoni2@newcastle.ac.uk"
    try:
        #gets html to be used in email
        template_path = os.path.join(current_dir, "welcome.html")
        html_body = load_template(template_path, username)
        #sends emails
        resend.Emails.send({
            "from": "MyWellBeing <reminder@resend.dev>",
            "to": [test_email],
            "subject": "Welcome to MyWellBeing",
            "html": html_body,
        })
    #catches any issues
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

def save_setup(user_id, age, gender, height_cm, current_weight_kg, weight_goal_kg, calorie_goal,salts_goal,protein_goal,water_goal):
    fields = [user_id, age, gender, height_cm, current_weight_kg, weight_goal_kg, calorie_goal,salts_goal,protein_goal,water_goal]
    if any(field is None for field in fields):
        return False
    try:
        if int(user_id) < 0:
            return False
        if int(age) < 0:
            return False
        if int(height_cm) < 0:
            return False
        if float(current_weight_kg) < 0:
            return False
        if float(weight_goal_kg) < 0:
            return False
        if int(calorie_goal) < 0:
            return False
        if float(salts_goal) < 0:
            return False
        if float(protein_goal) < 0:
            return False
        if int(water_goal) < 0:
            return False
    except ValueError:
        return False
    commit_setup(user_id, age, gender, height_cm, current_weight_kg, weight_goal_kg, calorie_goal,salts_goal,protein_goal,water_goal)
    return True

def load_template(file_path, username):
    with open(file_path, 'r') as file:
        content = file.read()
    # Replace the placeholder with the actual variable
    return content.replace("{{username}}", username)