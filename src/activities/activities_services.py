"""
    Activities Service Layer
    This file contains the business logic for the activities module.
    It sits between the UI and the database queries.
"""
from datetime import datetime
from plyer import notification
from activities.activity_queries import commit_activity, commit_past_activity, get_activities
from settings.settings_services import retrieve_notification_status


def save_activity(user_id,activity_type,distance_km,duration_seconds,start_date):
    """Save User Activities from map.py"""
    #make sure all fields are filled, have to do this to allow 0
    fields = [user_id,activity_type,distance_km,duration_seconds,start_date]
    if any(field is None for field in fields):
        return False
    #checks that user_id, distance and seconds are all of right type and > 0
    try:
        if int(user_id) < 0:
            return False
        elif float(distance_km) < 0:
            return False
        elif int(duration_seconds) < 0:
            return False
    except ValueError:
        return False
    #checks start_date is date format
    if not isinstance(start_date, datetime):
        return False
    #makes sure the date is not in the future
    if start_date > datetime.now():
        return False
    #makes sure the type is one of the three
    if activity_type not in ['Run','Cycle','Walk']:
        return False
    #commit activity to database
    commit_activity(user_id,activity_type,distance_km,duration_seconds,start_date)
    #check if notifications are enabled and tries to send if true
    if retrieve_notification_status(user_id):
        try:
            notification.notify(
                title="Activity Recorded Logged",
                message=f"{activity_type} Recorded",
                app_name="MyWellBeing"
            )
        except Exception as e:
            print(e)
    return True

def save_past_activity(user_id, title,calories,duration_seconds,reps,distance,start_date):
    """Save User Activities from past_activities.py"""
    #check that none of the values are None
    fields = [user_id,title,calories,reps,duration_seconds,distance,start_date]
    if any(field is None for field in fields):
        return False
    #make sure each value is the meets required type and > 0
    try:
        if int(user_id) < 0:
            return False
        elif int(calories) < 0:
            return False
        elif int(duration_seconds) < 0:
            return False
        elif int(reps) < 0:
            return False
        elif float(distance) < 0:
            return False
    except ValueError:
        return False
    #makes sure start_date is datetime
    if not isinstance(start_date, datetime):
        return False
    #makes sure start_date is not in future
    if start_date > datetime.now():
        return False
    #commits activity
    commit_past_activity(user_id,title,calories,duration_seconds,reps,distance,start_date)
    #check if notifications are enabled and tries to send if true
    if retrieve_notification_status(user_id):
        try:
            notification.notify(
                    title="Activity Recorded Logged",
                    message=f"{title} Recorded",
                    app_name="MyWellBeing"
            )
        except Exception as e:
            print(e)
    return True

def retrieve_activities(user_id):
    """retrieve all the users activities"""
    if not user_id:
        return []
    try:
        if int(user_id) < 0:
            return []
    except ValueError:
        return []
    activities = get_activities(user_id)
    return activities


