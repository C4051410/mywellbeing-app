import re
import bcrypt
from database.connection import connect

def register(username, full_name, password, email):
    # password validation
    regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if not re.search(regex, password):
        return "Password must have minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character"

    conn = connect()
    cur = conn.cursor()

    try:
        # check if email is already in use
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            if existing_user == email:
                return "Email already registered"

        # hash user password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12).decode("utf-8")).decode("utf-8")

        # insert row into database
        cur.execute("INSERT INTO users (username, full_name, password, email) VALUES (%s, %s, %s, %s)",(username, full_name, hashed_password, email))
        conn.commit()
        return "User registration successful"
    except Exception as e:
        conn.rollback()
        return "Error"

    finally:
        cur.close()
        conn.close()


