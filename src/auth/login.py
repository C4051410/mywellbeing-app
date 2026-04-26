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