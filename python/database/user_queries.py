from database.connection import connect
from datetime import date, timedelta

# retrieve user by id
# to be called by the homepage to load user data
def get_user(user_id):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT u.id, u.username, u.full_name, u.email, u.role,us.steps_today, us.calories_today, 
        us.current_streak, us.longest_streak, us.last_active, us.calorie_goal, us.weight_goal, us.current_weight, 
        us.height FROM users u LEFT JOIN user_stats us ON us.user_id = u.id WHERE u.id = %s """, (user_id,))
        return cur.fetchone()
    except Exception as e:
        return str(e)
    finally:
        cur.close()
        conn.close()

# create stats row for new users
def user_stats(user_id):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""INSERT INTO user_stats (user_stats_id ,user_id) VALUES (gen_random_uuid(), %s)""", (user_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        cur.close()
        conn.close()

# updates daily streak
# needs to be called everytime the user logs an activity
def user_streak(user_id):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT current_streak, longest_streak, last_active FROM user_stats WHERE user_id = %s", (user_id,))

        stats = cur.fetchone()
        current_streak, longest_streak, last_active = stats
        today = date.today()
        yesterday = today - timedelta(days=1)

        # if user already logged activity, do nothing
        if last_active == today:
            return
        # if user logged activity yesterday and today, streak goes up
        elif last_active == yesterday:
            current_streak =+ 1
        # if user has not logged activity before yesterday, streak resets
        else:
            streak = 1

        longest_streak = max(current_streak, longest_streak)

        cur.execute("""UPDATE user_stats SET current_streak = %s, longest_streak = %s, last_active = %s WHERE 
        user_id = %s""", (current_streak, longest_streak, today, user_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        cur.close()
        conn.close()
    return streak

def user_steps(user_id):
    # retrieve step count from phone/watch
    return

def user_calories(user_id):
    # updates users daily calories
    # to be called each time user logs a meal or food item
    return