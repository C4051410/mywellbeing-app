import re

import bcrypt

from settings.settings_queries import commit_update_password, retrieve_current_password, commit_update_goals, \
    get_notification_status, commit_notification_status


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

def update_goals(user_id, calorie_goal,water_goal):
    #if some values empty retun false
    if not all([user_id, calorie_goal, water_goal]):
        return False, "All Fields Required"
    try:
        #if values are less then 0 return false
         if float(calorie_goal) < 0 or float(water_goal) < 0:
             return False, "Calories and Water Must Be Greater Than 0"
    #if of wrong type return false
    except ValueError as e:
        return False, "Invalid Value"
    #commit changes
    commit_update_goals(user_id,calorie_goal,water_goal)
    #return true
    return True, "Goals Updated"

def retrieve_notification_status(user_id):
    if not user_id:
        return False
    try:
        if int(user_id) < 0:
            return False
    except ValueError:
        return False
    status = get_notification_status(user_id)
    if status:
        return status
    else:
        return False

def update_notification_status(user_id, notification_status):
    if user_id is None or notification_status is None:
        return False
    try:
        if int(user_id) < 0:
            return False
    except ValueError:
        return False
    commit_notification_status(user_id, not notification_status)
    return True