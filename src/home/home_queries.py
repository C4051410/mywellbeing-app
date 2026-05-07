"""
    Home Queries Layer
    Used to access the db and return the information
    retrieved
"""
from datetime import date

from database.connection import connect

#returns users username
def get_user_stats(user_id):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT u.username,
            us.current_streak,
            us.longest_streak,
            us.calorie_goal,
            COALESCE(SUM(CASE WHEN fl.date = %s THEN fl.calories ELSE 0 END), 0) AS daily_calories
            FROM users u
            LEFT JOIN user_stats us ON us.user_id = u.id
            LEFT JOIN foodlog fl ON fl.user_id = u.id
            WHERE u.id = %s
            GROUP BY u.username, us.current_streak, us.longest_streak,us.calorie_goal
        """, (date.today(), user_id))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row
    #if connection fails returns None
    except Exception as e:
        conn.close()
        print(e)
        return None

#returns friends activities
def get_friends_activities(user_id,date):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT ON (u.username)
                u.username, w.title, us.current_streak,
                w.activity_type, w.distance_km, w.duration, w.calories
            FROM friends f
            JOIN users u ON f.friend_id = u.id
            JOIN workouts w ON u.id = w.user_id
            JOIN user_stats us ON us.user_id = u.id
            WHERE f.user_id = %s AND w.start_date::date = %s
            ORDER BY u.username, w.id DESC
        """, (user_id, date,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    #return None if connection fails
    except Exception:
        conn.close()
        return None






