from admin.admin_queries import get_admin, get_users_admin, delete_users_admin, update_moderators_admin


def check_admin(user_id):
    #checks admin is not empty
    if not user_id:
        return False
    #checks value is an int and is greater than 0
    try:
        if int(user_id) < 0:
            return False
    except ValueError as e:
        return False
    #retrieves user role from db
    admin = get_admin(user_id)
    #if role is admin, return true, else false
    if admin == "admin":
        return True
    else:
        return False

def retrieve_users_admin(search_query):
    rows = get_users_admin(search_query)
    #if rows are empty, return empty list
    if not rows:
        return []
    #else returns the rows
    else:
        return rows

def remove_users_admin(user_id):
    #checks its not empty
    if not user_id:
        return False
    #checks value isnt less than 0 or not an int
    try:
        if int(user_id) < 0:
            return False
    except ValueError as e:
        return False
    #deletes user and returns True
    delete_users_admin(user_id)
    return True

def make_moderators_admin(user_id):
    if not user_id:
        return False
    try:
        if int(user_id) < 0:
            return False
    except ValueError as e:
        return False
    update_moderators_admin(user_id)
    return True