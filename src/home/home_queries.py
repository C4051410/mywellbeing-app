from database.connection import connect

#returns users username
def get_username(user_id):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row[0]
    #if connection fails returns None
    except Exception as e:
        conn.close()
        return None

#returns friends activities
def get_friends_activities(user_id,date):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT ON (u.username)
            u.username,w.title, us.current_streak
            FROM friends f
            JOIN users u ON f.friend_id = u.id
            JOIN workouts w on u.id = w.user_id
            JOIN user_stats us ON us.user_id = u.id
            WHERE f.user_id = %s AND w.start_date::date = %s
            ORDER BY u.username, w.id DESC
        """,(user_id,date,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    #return None if connection fails
    except Exception as e:
        conn.close()
        return None

def get_current_streaks(user_id):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT current_streak, longest_streak
            FROM user_stats 
            WHERE user_id = %s
        """,(user_id,))
        streaks = cur.fetchone()
        cur.close()
        conn.close()
        return streaks
    #return None if connection fails
    except Exception as e:
        conn.close()
        return None





