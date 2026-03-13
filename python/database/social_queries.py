from database.connection import connect


def get_user_by_username(username):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, username, full_name FROM users WHERE username = %s",
            (username,)
        )
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def add_friend(user_id, friend_id):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO friends (id, user_id, friend_id)
            VALUES (gen_random_uuid(), %s, %s)
            """,
            (user_id, friend_id)
        )
        cur.execute(
            """
            INSERT INTO friends (id, user_id, friend_id)
            VALUES (gen_random_uuid(), %s, %s)
            """,
            (friend_id, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        cur.close()
        conn.close()


def remove_friend(user_id, friend_id):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM friends WHERE user_id = %s AND friend_id = %s",
            (user_id, friend_id)
        )
        cur.execute(
            "DELETE FROM friends WHERE user_id = %s AND friend_id = %s",
            (friend_id, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        cur.close()
        conn.close()


def get_friends(user_id):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT u.id, u.username, u.full_name
            FROM friends f
            JOIN users u ON f.friend_id = u.id
            WHERE f.user_id = %s
            ORDER BY u.username
            """,
            (user_id,)
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def get_friend_ids(user_id):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT friend_id FROM friends WHERE user_id = %s",
            (user_id,)
        )
        rows = cur.fetchall()
        return [row[0] for row in rows]
    finally:
        cur.close()
        conn.close()


def like_target(user_id, target_type, target_id):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO social_likes (id, target_type, target_id, user_id)
            VALUES (gen_random_uuid(), %s, %s, %s)
            """,
            (target_type, target_id, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        cur.close()
        conn.close()


def unlike_target(user_id, target_type, target_id):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            DELETE FROM social_likes
            WHERE user_id = %s AND target_type = %s AND target_id = %s
            """,
            (user_id, target_type, target_id)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        cur.close()
        conn.close()


def add_comment(user_id, target_type, target_id, content):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO social_comments (id, target_type, target_id, user_id, content)
            VALUES (gen_random_uuid(), %s, %s, %s, %s)
            """,
            (target_type, target_id, user_id, content)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        cur.close()
        conn.close()


def get_comments(target_type, target_id):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT c.id, c.user_id, u.username, c.content, c.created_at
            FROM social_comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.target_type = %s AND c.target_id = %s
            ORDER BY c.created_at DESC
            """,
            (target_type, target_id)
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def get_social_feed(user_id):
    """
    Retrieve recent activity (workouts & meals(foodlog)) from user's friends.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        # first retrieve friend IDs
        cur.execute(
            "SELECT friend_id FROM friends WHERE user_id = %s",
            (user_id,)
        )
        friend_rows = cur.fetchall()
        # convert rows into simple list of ids
        friend_ids = [row[0] for row in friend_rows]
        # if user has no friends return empty feed
        if not friend_ids:
            return []
        # convert to tuple for SQL IN clause
        friend_ids_tuple = tuple(friend_ids)
        # retrieve workout activities
        cur.execute(
            f"""
            SELECT
                'workout' AS activity_type,
                u.username,
                w.title,
                w.calories,
                w.id,
                w.user_id
            FROM workouts w
            JOIN users u ON w.user_id = u.id
            WHERE w.user_id IN %s
            ORDER BY w.id DESC
            LIMIT 5
            """,
            (friend_ids_tuple,)
        )
        workouts = cur.fetchall()
        # retrieve meal activities
        cur.execute(
            f"""
            SELECT
                'meal' AS activity_type,
                u.username,
                f.title,
                f.calories,
                f.id,
                f.user_id
            FROM foodlog f
            JOIN users u ON f.user_id = u.id
            WHERE f.user_id IN %s
            ORDER BY f.id DESC
            LIMIT 5
            """,
            (friend_ids_tuple,)
        )
        meals = cur.fetchall()
        # combine activities
        activity_feed = workouts + meals
        return activity_feed
    finally:
        cur.close()
        conn.close()


def get_leaderboard():
    """
    Retrieve top users based on total workout calories.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT
                u.username,
                SUM(w.calories) AS total_calories
            FROM workouts w
            JOIN users u ON w.user_id = u.id
            GROUP BY u.username
            ORDER BY total_calories DESC
            LIMIT 3
            """)
        leaderboard = cur.fetchall()
        return leaderboard
    finally:
        cur.close()
        conn.close()