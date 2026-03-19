import re
import bcrypt
from database.connection import connect

def register(username, password, email):
    # TODO: (UI) add field level error messages next to each input
    # eg: username.error = "Please enter a username"
    if not all ([username, password, email]):
        return "All fields are required"

    # email validation
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, email):
        return "Please enter a valid email"

    # TODO: accept other special characters
    # password validation
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if not re.search(password_regex, password):
        return "Password must have minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character"

    conn = connect()
    cur = conn.cursor()

    try:
        # check if email is already in use
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            return "Email already registered"

        # hash user password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")

        # insert row into database
        cur.execute("INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s) RETURNING id",(username, hashed_password, email, "user"))
        user_id = cur.fetchone()[0]
        conn.commit()
        return (user_id,)
    except Exception as e:
        conn.rollback()
        return str(e)

    finally:
        cur.close()
        conn.close()


