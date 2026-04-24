from datetime import date, timedelta

from database.connection import connect

def get_user(user_id):
    '''Retrieves a dict object of the user's data and other associated information from user table using their id'''
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """SELECT u.id, u.username, u.email, u.role, us.age, us.gender, us.height_cm,
            us.current_weight_kg, us.weight_goal_kg, us.calorie_goal, us.current_streak,
            us.longest_streak, us.last_active, us.steps_today,us.salts_goal,us.proteins_goal,us.water_goal
            FROM users u
            LEFT JOIN user_stats us ON us.user_id = u.id
            WHERE u.id = %s""",
            (user_id,)
        )
        return cur.fetchone()

    finally:
        cur.close()
        conn.close()

def save_setup(user_id, age, gender, height_cm, current_weight_kg, weight_goal_kg, calorie_goal,salts_goal,protein_goal,water_goal):
    '''Saves the user's profile setup information to user_stats table '''
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
                "INSERT INTO user_stats (user_id, age, gender, height_cm, current_weight_kg, weight_goal_kg, "
                "calorie_goal,salts_goal,proteins_goal,water_goal,current_streak,longest_streak) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s,%s,%s,%s)",
                (user_id, age, gender, height_cm, current_weight_kg, weight_goal_kg, calorie_goal,salts_goal,protein_goal,water_goal,1,1))
        conn.commit()
        return "Setup saved"

    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        cur.close()
        conn.close()

def user_streak(user_id):
    '''Updates users daily streak - needs to be called everytime the user logs an activity'''
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
            current_streak = 1

        longest_streak = max(current_streak, longest_streak)

        cur.execute("""UPDATE user_stats SET current_streak = %s, longest_streak = %s, last_active = %s WHERE 
        user_id = %s""", (current_streak, longest_streak, today, user_id))
        conn.commit()
        return current_streak

    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        cur.close()
        conn.close()

def check_admin(user_id):
    conn = connect()
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE id = %s",(user_id,))
        user = cur.fetchone()
        if user is None or user[0] != "admin":
            return False
        else:
            return True


def check_mod(user_id):
    conn = connect()
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE id = %s",(user_id,))
        user = cur.fetchone()
        if user is None or user[0] != "moderator":
            return False
        else:
            return True
