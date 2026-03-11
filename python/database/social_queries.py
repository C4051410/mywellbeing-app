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