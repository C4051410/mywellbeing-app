from moderator.moderator_queries import get_posts_moderators, get_mod, delete_posts_moderator


def check_mod(user_id):
    #check admin is not empty
    if not user_id:
        return False
    #check value is in and > 0
    try:
        if int(user_id) < 0:
            return False
    except ValueError:
        return False
    #retrieve role from db
    mod = get_mod(user_id)
    #check role is moderator
    if mod == "moderator":
        return True
    else:
        return False

def retrieve_posts_moderator(search_query):
    #get rows from db
    rows = get_posts_moderators(search_query)
    #of rows are empty return empty list
    if not rows:
        return []
    #else return the rows
    else:
        return rows

def remove_posts_moderator(user_id,source):
    #check id isnt empty
    if not user_id:
        return False
    #check id is int and > 0
    try:
        if int(user_id) < 0:
            return False
    except ValueError:
        return False
    try:
        if str(source) != "food" or str(source) != "work":
            return False
    except ValueError:
        return False

    delete_posts_moderator(user_id,source)
    return True
