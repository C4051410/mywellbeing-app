from home.home_queries import get_friends_activities, get_current_streaks, get_username

#gets username
def retrieve_username(user_id):
    #if user_id is empty return default name
    if not user_id:
        return "DefaultUsername"
    #returns default name if not int or < 0
    try:
        if int(user_id) < 0:
            return "DefaultUsername"
    except ValueError:
        return "DefaultUsername"
    username = get_username(user_id)
    #if username not None return username
    if username:
        return username
    #else return default
    else:
        return "DefaultUsername"

#gets friends activities
def retrieve_friends_activities(user_id,date):
    activity_rows = get_friends_activities(user_id,date)
    #if activity rows isnt None return rows
    if activity_rows:
        return activity_rows
    #else return empty list
    else:
        return []

#gets streaks
def retrieve_current_streaks(user_id):
    streaks = get_current_streaks(user_id)
    #if streaks are not None return rows
    if streaks:
        return streaks
    #else return a default [0,0] to avoid crash
    else:
        return [0,0]