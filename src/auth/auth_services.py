import os
import re
import json
import bcrypt
import resend
from plyer import notification
from auth.login import login, get_user_setup,get_last_email,commit_last_email
from auth.register import register, get_existing_user, commit_setup
from database.connection import email_key
from settings.settings_services import retrieve_notification_status

#find the current directory of this file
CURRENT_DIR = os.path.dirname(__file__)
#gets API key
resend.api_key = email_key()

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
    #checks whether user has notifications enabled before trying to send notification
    if retrieve_notification_status(user[0]):
        try:
            notification.notify(
                title="Login Successful",
                message=f"Welcome Back {user[1]}",
                app_name="MyWellBeing",
            )
        except Exception as e:
            pass
    #return true with user data
    return True,user

def register_user(username,email, password):
    #checks all fields have been entered
    if not all([username,email, password]):
        return False, "Please Enter All Fields"
    username.isspace()
    if " " in username:
        return False, "Username must not contain space"
    #check email is correct format
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, email):
        return False, "Please enter a valid email"
    #cehcks passwords greater than 8 characters
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    #check password contains at least 1 uppercase, lowercase, number, and special character, also prevents white space
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
    try:
        notification.notify(
            title="Registration Successful",
            message="Account Created Successfully",
            app_name="MyWellBeing",
        )
    except Exception as e:
        print(e)
    #uses the test email, as we dont have the costs to buy domain
    #on deployment, would remove this and use email
    test_email = "m.austoni2@newcastle.ac.uk"
    try:
        #gets html to be used in email
        template_path = os.path.join(CURRENT_DIR, "welcome.html")
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
        pass
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

def save_setup(user_id, age, gender, height_cm, current_weight_kg, weight_goal_kg, calorie_goal,salts_goal,protein_goal,water_goal,weekly_activity_goal):
    fields = [user_id, age, gender, height_cm, current_weight_kg, weight_goal_kg, calorie_goal,salts_goal,protein_goal,water_goal,weekly_activity_goal]
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
        if int(weekly_activity_goal) < 0:
            return False
    except ValueError:
        return False
    commit_setup(user_id, age, gender, height_cm, current_weight_kg, weight_goal_kg, calorie_goal,salts_goal,protein_goal,water_goal,weekly_activity_goal)
    return True

def load_template(file_path, username):
    with open(file_path, 'r') as file:
        content = file.read()
    # Replace the placeholder with the actual variable
    return content.replace("{{username}}", username)


def refresh_inactivity_timer(user_id,username):
    #gets last email ready to be sent
    old_email_id = get_last_email(user_id)
    #if the email exists, try and cancel it being sent using its id
    if old_email_id:
        try:
            resend.Emails.cancel(old_email_id)
        except Exception:
            pass
    if retrieve_notification_status(user_id):
        try:
            template_path = os.path.join(CURRENT_DIR, "reminder.html")
            html_body = load_template(template_path, username)
            test_email = "m.austoni2@newcastle.ac.uk"
            #send to user in 20 hours time
            sent_email = resend.Emails.send({
                "from": "MyWellBeing <reminders@resend.dev>",
                "to": test_email,
                "subject": "We miss you!",
                "html":html_body,
                "scheduled_at": "in 20 hours",
            })
            #store the last email id in the db
            commit_last_email(user_id, sent_email["id"])

        except Exception as e:
            print(f"Error scheduling email: {e}")

#create the file called .user_session to store the users detail when logged in
SESSION_FILE = os.path.join(CURRENT_DIR, ".user_session")

def save_session(user_id):
    #try and write the users name into the file
    try:
        with open(SESSION_FILE, "w") as file:
            json.dump({"user_id": user_id}, file)
    except Exception as e:
        print(f"Error saving session: {e}")

#used to find and load the user session
def load_session():
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "r") as file:
                data = json.load(file)
                #returns the users id
                return data.get("user_id")
    except Exception as e:
        print(f"Error loading session: {e}")
        return None
#used to clear the json file when logging out
def clear_session():
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
    except Exception as e:
        print(f"Error removing session: {e}")

