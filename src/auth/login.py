import bcrypt
from database.connection import connect
from plyer import notification
from pygments.filter import apply_filters


def login(email,password):
    conn = connect()
    try:
        cur = conn.cursor()
        #gets information needed to log in
        cur.execute("SELECT id, username, email, password FROM users WHERE LOWER(email) = LOWER(%s)", (email,))
        user = cur.fetchone()
        return user
    except Exception as e:
        return str(e)

def get_user_setup(user_id):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM user_stats WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
    except Exception as e:
        conn.close()
        return str(e)

def get_last_email(user_id):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("SELECT last_scheduled_email_id FROM users WHERE user_id = %s", (user_id,))
        email = cur.fetchone()
        cur.close()
        conn.close()
        return email[0]
    except Exception as e:
        conn.close()
        return str(e)

def commit_last_email(user_id,email_id):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE users SET last_scheduled_email_id = %s WHERE id = %s", (email_id,user_id,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        conn.close()
        return str(e)