from database.connection import connect

def get_user(user_id):
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