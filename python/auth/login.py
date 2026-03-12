import bcrypt
from database.connection import connect

def login(email,password):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, username, full_name, email, password_hash FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        # if no user exists with that email, login fails
        if not user:
            return "Invalid email."

        # retrieve stored password
        stored_password = user[4].encode()

        # compare entered password with stored password
        if not bcrypt.checkpw(password.encode(), stored_password):
            return "Invalid password."

        # if password matches login is succesful
        # TODO: (UI) change it to redirect user to home page once logged in
        return user

    finally:
        cur.close()
        conn.close()