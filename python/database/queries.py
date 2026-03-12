from database.connection import connect

def get_user(user_id):
    '''Retrieves user's data and other associated information from user table using their id'''
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """SELECT u.id, u.username, u.email, u.role, us.age, us.gender, us.height_cm,
            us.current_weight_kg, us.weight_goal_kg, us.calorie_goal, us.current_streak,
            us.longest_streak, us.last_active, us.steps_today
            FROM users u
            LEFT JOIN user_stats us ON us.user_id = u.id
            WHERE u.id = %s""",
            (user_id,)
        )
        return cur.fetchone()

    finally:
        cur.close()
        conn.close()

def save_setup(user_id, age, gender, height_cm, current_weight_kg, weight_goal_kg, calorie_goal):
    '''Saves the user's profile setup information to user_stats table '''
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
                "INSERT INTO user_stats (user_id, age, gender, height_cm, current_weight_kg, weight_goal_kg, "
                "calorie_goal) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (user_id, age, gender, height_cm, current_weight_kg, weight_goal_kg, calorie_goal))
        conn.commit()
        return "Setup saved"

    except Exception as e:
        conn.rollback()
        return str(e)

    finally:
        cur.close()
        conn.close()