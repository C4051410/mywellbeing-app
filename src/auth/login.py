import bcrypt
from database.connection import connect
from plyer import notification
from pygments.filter import apply_filters


def login(email,password):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, username, email, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        # if no user exists with that email, login fails
        if not user:
            return "Invalid email."

        # retrieve stored password
        stored_password = user[3].encode()

        # compare entered password with stored password
        if not bcrypt.checkpw(password.encode(), stored_password):
            return "Invalid password."

        # if password matches login is succesful
        # TODO: (UI) change it to redirect user to home page once logged in
        notification.notify(
            title="Login Successful",
            message=f"Welcome Back {user[1]}",
            app_name="MyWellBeing",
        )
        return user

    finally:
        cur.close()
        conn.close()