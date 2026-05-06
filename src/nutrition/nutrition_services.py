"""
    Nutrition Service Layer
    This file contains the business logic for the nutrition module.
    It sits between the UI and the database queries.
"""
import difflib
from datetime import date, timedelta
from plyer import notification

from nutrition.nutrition_queries import get_foodlog, get_waterlog, commit_foodlog, commit_waterlog, \
    get_daily_stats, get_user_goals
from settings.settings_services import retrieve_notification_status


#retrieves recent foodlogs
def retrieve_foodlogs(user_id):
    #used to find 48 hours ago
    two_days = date.today() - timedelta(days=2)
    #returns all foodlogs within 48 hour
    foodlogs = get_foodlog(user_id, two_days)
    if foodlogs:
        return foodlogs
    #returns empty array if empty
    else:
        return []

#same logic as above but for water
def retrieve_waterlogs(user_id):
    two_days = date.today() - timedelta(days=2)
    waterlogs = get_waterlog(user_id, two_days)
    if waterlogs:
        return waterlogs
    else:
        return []

#used to search a db of food
def search_food_db(search_query,food_db):
    query = search_query
    #if query is within the db
    if query in food_db:
        #returns with match_type so it knows if its exact or suggestion, and returns the result
        return "exact", food_db[query]
    #if at least 3 letters in the query match, go onto suggestion
    if len(query) > 2:
        #tries to find a close match within the db
        matches = difflib.get_close_matches(query,list(food_db.keys()),n=1,cutoff=0.6)
        #if match is returned
        if matches:
            #retruns match_type and the name of match
            return "suggestion",matches[0]
    #else returns None as not close
    return None,None

#saves entered foodlogs
def save_foodlog(food, calories, salts, proteins,fats,carbohydrates,date,mealtype,user_id):
    #returns false and message if not all fields are entered
    fields = [food,calories,salts,proteins,fats,carbohydrates,date,mealtype,user_id]
    if any(field is None for field in fields):
        return False, "All Fields Required"
    #tests for if user enters something not a number
    try:
        # if the value is negative return false and message
        if float(calories) < 0 or float(salts) < 0 or float(proteins) < 0:
            return False, "Values Cannot be Negative"
    except Exception as e:
        #returns false and message
        return False, str(e)
    #food is safe to enter so commits to db
    commit_foodlog(food,calories,salts,proteins,fats,carbohydrates,date,mealtype,user_id)
    #checks if notifications are enabled, then tries to send one
    if retrieve_notification_status(user_id):
        try:
            notification.notify(
                title="Food Log Logged",
                message=f"{food} Recorded",
                app_name="MyWellBeing"
            )
        except Exception as e:
            #print if error arises
            print(e)
        # returns True and Success message
    return True, "Successful"

#same as above but for water
def save_waterlog(water,date,user_id):
    if not all([water,date,user_id]):
        return False, "All Fields Required"
    try:
        if float(water) <= 0:
            return False, "Values Cannot be Negative or 0"
    except Exception as e:
        return False, str(e)
    commit_waterlog(water,date,user_id)
    #checks if notifications are enabled and then tries to send
    if retrieve_notification_status(user_id):
        try:
            notification.notify(
                title="Water Logged",
                message=f"{water}ml Recorded",
                app_name="MyWellBeing"
            )
        except Exception as e:
            print(e)
    return True, "Successful"

#used to retrieve daily stats
def retrieve_daily_stats(user_id,date):
    #defaults all stats to 0
    total_f=0.0
    total_carbs=0.0
    total_c = 0
    total_s = 0.0
    total_p = 0.0
    total_w = 0
    #gets food and water stats from db
    food_stats, water_stat  = get_daily_stats(user_id,date)
    #makes sure its not empty
    if food_stats:
        #goes through all rows
        for data in food_stats:
            #checks if not none before adding
            calories, salts, proteins, fats, carbs = data
            if calories is not None:
                total_c += calories
            if salts is not None:
                total_s += salts
            if proteins is not None:
                total_p += proteins
            if fats is not None:
                total_f += fats
            if carbs is not None:
                total_carbs += carbs

    #same with water
    if water_stat:
        for data in water_stat:
            total_w += data[0]
    #returns all values
    return total_c, total_s, total_p, total_f, total_carbs, total_w
def retrieve_user_goals(user_id):
    #defaults all values
    goal_f=50
    goal_carbs=200
    goal_c = 1
    goal_s = 1.0
    goal_p = 100.0
    goal_w = 1
    #retrievs all goals from db
    goals = get_user_goals(user_id)
    #checks its not empty
    if goals:
        #checks if not empty or less than 0, ZeroDivideError check
        if goals[0] is not None and goals[0] > 0:
            goal_c = goals[0]
        if goals[1] is not None and goals[1] > 0:
            goal_s = goals[1]
        if goals[2] is not None and goals[2] > 0:
            goal_p = goals[2]
        if goals[3] is not None and goals[3] > 0:
            goal_w = goals[3]
    #returns all values
    return goal_c, goal_s, goal_p, goal_f, goal_carbs, goal_w






