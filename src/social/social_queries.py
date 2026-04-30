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
    Add a like to a workout.
    The user can only like the same target once.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO social_likes (target_type, target_id, user_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, target_type, target_id) DO NOTHING
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
    Remove a like from a workout (target).
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

def has_user_liked(user_id, target_type, target_id):
    """
    Return True if the user has liked the target.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT 1 FROM social_likes
            WHERE user_id = %s AND target_type = %s AND target_id = %s
            LIMIT 1
            """,
            (user_id, target_type, target_id)
        )
        return cur.fetchone() is not None
    finally:
        cur.close()
        conn.close()

def count_likes(target_type, target_id):
    """
    Return the number of likes for one target.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT COUNT(*) FROM social_likes
            WHERE target_type = %s AND target_id = %s
            """,
            (target_type, target_id)
        )
        return cur.fetchone()[0]
    finally:
        cur.close()
        conn.close()


def add_comment(user_id, target_type, target_id, content):
    """
    Add a comment to a workout (target).
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO social_comments (target_type, target_id, user_id, content)
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

def count_comments(target_type, target_id):
    """
    Return the number of comments for one target.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT COUNT(*) FROM social_comments
            WHERE target_type = %s AND target_id = %s
            """,
            (target_type, target_id)
        )
        return cur.fetchone()[0]
    finally:
        cur.close()
        conn.close()

def get_comments(target_type, target_id):
    """
    Retrieve comments for a workout (target).
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

def delete_comment(comment_id, user_id):
    """
    Delete comment if it belongs to the current user.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            DELETE FROM social_comments
            WHERE id = %s AND user_id = %s
            """,
            (comment_id, user_id)
        )
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        cur.close()
        conn.close()

# Social feed
def get_social_feed(user_id):
    """
    Retrieve recent workout activity from user's friends.
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
                COALESCE(w.calories, 0) AS calories,
                w.id,
                w.user_id,
                COALESCE(w.duration_seconds, 0) AS duration_seconds,
                w.start_date
            FROM workouts w
            JOIN users u ON w.user_id = u.id
            WHERE w.user_id = ANY(%s)
            ORDER BY w.start_date DESC NULLS LAST, w.id DESC
            LIMIT 6
            """,
            (friend_ids,)
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def get_leaderboard(user_id):
    """
    Retrieve a weekly leaderboard for the current user and their friends.
    Score is calculated based on a combination of calories, distance and duration..
    TODO: upgrade to a more accurate weekly relative effort score
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            WITH friend_group AS (
                SELECT friend_id AS member_id
                FROM friends
                WHERE user_id = %s

                UNION

                SELECT %s AS member_id
            ),
            weekly_workouts AS (
                SELECT
                    user_id,
                    COALESCE(SUM(calories), 0) AS total_calories,
                    COALESCE(SUM(distance_km), 0) AS total_distance,
                    COALESCE(SUM(duration_seconds), 0) AS total_seconds
                FROM workouts
                WHERE start_date >= date_trunc('week', CURRENT_DATE)
                GROUP BY user_id
            )
            SELECT
                u.id,
                u.username,
                CAST(
                    COALESCE(ww.total_calories, 0)
                    + COALESCE(ww.total_distance, 0) * 100
                    + COALESCE(ww.total_seconds, 0) / 60
                    AS INTEGER
                ) AS total_points
            FROM friend_group fg
            JOIN users u ON u.id = fg.member_id
            LEFT JOIN weekly_workouts ww ON ww.user_id = u.id
            ORDER BY total_points DESC, u.username ASC
            """,
            (user_id, user_id)
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()