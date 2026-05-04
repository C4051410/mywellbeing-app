from home.home_queries import get_friends_activities, get_user_stats

#gets username
def retrieve_user_stats(user_id):
    #if user_id is empty return default name
    if not user_id:
        return ["DefaultUsername",1,1,0,1]
    #returns default name if not int or < 0
    try:
        if int(user_id) < 0:
            return ["DefaultUsername",1,1,0,1]
    except ValueError:
        return ["DefaultUsername",1,1,0,1]
    user_stats = get_user_stats(user_id)
    #if username not None return username
    if user_stats:
        return user_stats
    #else return default
    else:
        return ["DefaultUsername",1,1,0,1]

#gets friends activities
def retrieve_friends_activities(user_id,date):
    activity_rows = get_friends_activities(user_id,date)
    #if activity rows isnt None return rows
    if activity_rows:
        return activity_rows
    #else return empty list
    else:
        return []
