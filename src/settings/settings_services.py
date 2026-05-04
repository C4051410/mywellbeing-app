import os
import re

import bcrypt

from settings.settings_queries import commit_update_password, retrieve_current_password, commit_update_goals, \
    get_notification_status, commit_notification_status, delete_user_account_db
import resend
current_dir = os.path.dirname(__file__)
#used to check password is okay to update
def update_password(user_id,current_password, new_password,confirm_password):
    #makes sure all fields are returned
    if not all([user_id,current_password, new_password, confirm_password]):
        return False, "All Fields Required"
    #retrieves users stored password
    stored_password = retrieve_current_password(user_id)
    #checks current password is correct
    if not bcrypt.checkpw(current_password.encode("utf-8"), stored_password):
        return False, "Current Password Incorrect"
    #makes sure new password isnt same as old
    if current_password == new_password:
        return False, "New Password Cant Be Same as Old"
    #makes sure the confirm password is the same
    if new_password != confirm_password:
        return False, "Password Do Not Match"
    #makes sure password is longer then 8 characters
    if len(new_password) < 8:
        return False, "Password must be at least 8 characters long"
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    #makes sure password contains upper,lower and special
    if not re.search(password_regex, new_password):
        return False, "Password must contain at least 1 Uppercase,lowercase and special character"
    #commits password update if true
    commit_update_password(user_id, new_password)
    return True, "Password Updated"

def update_goals(user_id, calorie_goal, water_goal, weekly_activity_goal):
    #if some values empty retun false
    if not all([user_id, calorie_goal, water_goal, weekly_activity_goal]):
        return False, "All Fields Required"
    try:
        #if values are less then 0 return false
        if float(calorie_goal) < 0 or float(water_goal) < 0:
             return False, "Calories and Water Must Be Greater Than 0"
        if int(weekly_activity_goal) < 0 or int(weekly_activity_goal) > 7:
            return False, "Weekly Activity Goal Must Be Between 0 and 7"
    #if of wrong type return false
    except ValueError as e:
        return False, "Invalid Value"
    #commit changes
    success = commit_update_goals(user_id, calorie_goal, water_goal, weekly_activity_goal)
    #return true
    if success:
        return True, "Goals Updated"
    else:
        return False, "Failed to Update Goals"

def retrieve_notification_status(user_id):
    #check that user id is not None or invalid type
    if not user_id:
        return False
    try:
        if int(user_id) < 0:
            return False
    except ValueError:
        return False
    #gets the notification status from db
    status = get_notification_status(user_id)
    #if it's not None return the status
    if status:
        return status
    else:
        return False

def update_notification_status(user_id, notification_status):
    #check that user_id or notification are not None
    if user_id is None or notification_status is None:
        return False
    # check user_id is valid
    try:
        if int(user_id) < 0:
            return False
    except ValueError:
        return False
    #saves updates status to db
    commit_notification_status(user_id, not notification_status)
    return True
def delete_account(user_id):
    # Validates ID integrity before dropping an account
    if not user_id:
        return False, "Invalid User Id"
    try:
        if int(user_id) < 0:
            return False, "Invalid User Id"
    except ValueError:
        return False, "Invalid Value"

    result = delete_user_account_db(user_id)
    if result is True:
        #try and send account deletion email
        try:
            #uses this email due to API costs, would be changed on deployment
            email = "m.austoni2@newcastle.ac.uk"
            #get the email content from the directory
            template_path = os.path.join(current_dir, "goodbye.html")
            with open(template_path) as file:
                content = file.read()
            html_body = content
            #send the email using Resend API
            resend.Emails.send({
                "from": "MyWellBeing <reminder@resend.dev>",
                "to": email,
                "subject": "Were Sorry to See You Leave",
                "html": html_body,
            })
        except Exception as e:
            print(e)
        return True, "Account Deleted Successfully"
    else:
        return False, "Failed to Delete Account"
