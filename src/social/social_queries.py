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



def get_interaction_stats(user_id, target_ids, target_type="workout"):
    """
    Fetch like counts, user-liked status, and comment counts
    """
    if not target_ids:
        return {}

    conn = connect()
    cur = conn.cursor()
    try:
        """
            Crates a table of posts that displays the posts likes, comments
            and whether the user has liked the post
        """
        cur.execute(
            """
            SELECT
                t.target_id,
                COUNT(DISTINCT l.id) AS like_count,
                BOOL_OR(l.user_id = %s)  AS liked_by_user,
                COUNT(DISTINCT c.id)  AS comment_count
            FROM unnest(%s::int[]) AS t(target_id)
            LEFT JOIN social_likes    l ON l.target_type = %s AND l.target_id = t.target_id
            LEFT JOIN social_comments c ON c.target_type = %s AND c.target_id = t.target_id
            GROUP BY t.target_id
            """,
            (user_id, target_ids, target_type, target_type)
        )
        rows = cur.fetchall()
        #converts the rows into a dictionary and returns it
        return {
            row[0]: {
                "like_count":     int(row[1]),
                "liked_by_user":  bool(row[2]),
                "comment_count":  int(row[3])
            }
            #goes through each row
            for row in rows
        }
    except Exception as e:
        print(e)
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
    Scoring:
    - goal completion score based on weekly activity goal
    - current streak bonus
    If weekly activity goal is 0, then the completion score is 0
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
                    COUNT(*) AS weekly_completed
                FROM workouts
                WHERE start_date >= date_trunc('week', CURRENT_DATE)
                GROUP BY user_id
            )
            SELECT
                u.id,
                u.username,
                CAST(
                    (
                        CASE
                            -- A goal of 0 means no weekly completion score
                            WHEN COALESCE(us.weekly_activity_goal, 0) <= 0 THEN 0
                            ELSE ROUND(
                                LEAST(COALESCE(ww.weekly_completed, 0)::numeric
                                    / NULLIF(us.weekly_activity_goal, 0),1.0) * 1000
                            )
                        END
                    )
                    + LEAST(COALESCE(us.current_streak, 0), 7) * 50
                    AS INTEGER
                ) AS total_points
            FROM friend_group fg
            JOIN users u ON u.id = fg.member_id
            LEFT JOIN user_stats us ON us.user_id = u.id
            LEFT JOIN weekly_workouts ww ON ww.user_id = u.id
            ORDER BY total_points DESC, u.username ASC
            """,
            (user_id, user_id)
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()