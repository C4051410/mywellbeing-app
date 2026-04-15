from database.connection import connect

# User lookup
def get_user_by_username(username):
    """
    Find a user by username.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, username, email FROM users WHERE username = %s",
            (username,)
        )
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

def get_user_by_id(user_id):
    """
    Retrieve a user by id.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, username, email FROM users WHERE id = %s",
            (user_id,)
        )
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

# Friend management
def add_friend(user_id, friend_id):
    """
    Create a mutual friendship.
    """
    # Prevent user to add themselves
    if str(user_id) == str(friend_id):
        return "You cannot add yourself"
    conn = connect()
    cur = conn.cursor()
    try:
        # Insert the two direction of the friendship
        cur.execute(
            """
            INSERT INTO friends (user_id, friend_id)
            VALUES (%s, %s)
            ON CONFLICT (user_id, friend_id) DO NOTHING
            """,
            (user_id, friend_id)
        )
        cur.execute(
            """
            INSERT INTO friends (user_id, friend_id)
            VALUES (%s, %s)
            ON CONFLICT (user_id, friend_id) DO NOTHING
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
    """
    Remove a mutual friendship.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        # Delete both directions of the friendship in one query
        cur.execute(
            """
            DELETE FROM friends
            WHERE (user_id = %s AND friend_id = %s)
               OR (user_id = %s AND friend_id = %s)
            """,
            (user_id, friend_id, friend_id, user_id)
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
    """
    Retrieve all friends for the given user.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT u.id, u.username, u.email
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
    """
    Retrieve only the friend ids for the given user.
    Useful when building the social activity feed.
    """
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

# Likes and comments
def like_target(user_id, target_type, target_id):
    """
    Add a like to a workout or meal.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO social_likes (id, target_type, target_id, user_id)
            VALUES (%s, %s, %s)
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
    """
    Remove a like from a workout or meal.
    """
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
    """
    Add a comment to a workout or meal.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO social_comments (id, target_type, target_id, user_id, content)
            VALUES (%s, %s, %s, %s)
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
    """
    Retrieve comments for a workout or meal.
    """
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

# Social feed
def get_social_feed(user_id):
    """
    Retrieve recent activity (workouts & meals(foodlog)) from user's friends.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT friend_id FROM friends WHERE user_id = %s",
            (user_id,)
        )
        friend_rows = cur.fetchall()
        friend_ids = [row[0] for row in friend_rows]

        # If user has no friends return empty feed
        if not friend_ids:
            return []

        # Retrieve workout activities
        cur.execute(
            """
            SELECT 'workout' AS activity_type,
                   u.username,
                   w.title,
                   w.calories,
                   w.id,
                   w.user_id
            FROM workouts w
                     JOIN users u ON w.user_id = u.id
            WHERE w.user_id = ANY (%s)
            ORDER BY w.id DESC LIMIT 5
            """,
            (friend_ids,)
        )
        workouts = cur.fetchall()

        # Retrieve meal activities
        cur.execute(
            """
            SELECT 'meal' AS activity_type,
                   u.username,
                   f.title,
                   f.calories,
                   f.id,
                   f.user_id
            FROM foodlog f
                     JOIN users u ON f.user_id = u.id
            WHERE f.user_id = ANY (%s)
            ORDER BY f.id DESC LIMIT 5
            """,
            (friend_ids,)
        )
        meals = cur.fetchall()
        # Combine activities
        # Sort by target id descending as a temporary approximation of recency
        activity_feed = workouts + meals
        activity_feed.sort(key=lambda row: row[4], reverse=True)
        return activity_feed[:6]
    finally:
        cur.close()
        conn.close()


def get_leaderboard(user_id):
    """
    Retrieve a leaderboard for the current user and their friends.
    For now, score is based on total workout calories.
    TODO: upgrade to a more accurate weekly relative effort score
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            WITH friend_group AS (SELECT friend_id AS member_id
                                  FROM friends
                                  WHERE user_id = %s

                                  UNION

                                  SELECT %s AS member_id)
            SELECT u.id,
                   u.username,
                   COALESCE(SUM(w.calories), 0) AS total_points
            FROM friend_group fg
                     JOIN users u ON u.id = fg.member_id
                     LEFT JOIN workouts w ON w.user_id = u.id
            GROUP BY u.id, u.username
            ORDER BY total_points DESC, u.username ASC
            """,
            (user_id, user_id)
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()