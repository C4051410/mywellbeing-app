from database.connection import connect

def get_users_admin(search_query=""):
    #connects to database
    conn = connect()
    #uses try to catch for errors
    try:
        cur = conn.cursor()
        #query used to returns users
        query = "SELECT username, email, role, id FROM users WHERE role != %s"
        #used to make it so admins don't appear
        params = ["admin"]
        #used for if user searches for specific user
        if search_query:
            query += " AND username LIKE %s"
            params.extend([f"%{search_query}%",])
        #execute query
        cur.execute(query, tuple(params))
        #return all results
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print(e)
        conn.close()

def delete_users_admin(user_id: int):
    conn = connect()
    try:
        cur = conn.cursor()
        #delete user using their id
        cur.execute("DELETE FROM users WHERE id = %s",(user_id,))
        conn.commit()
        cur.close()
    except Exception as e:
        #undos any actions if error occurred
        conn.rollback()
        print(e)

def update_moderators_admin(user_id: int):
    conn = connect()
    try:
        cur = conn.cursor()
        #update their role from user to moderator
        cur.execute(" UPDATE users SET role = %s WHERE id = %s",("moderator", user_id,))
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()

def get_admin(user_id):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE id = %s",(user_id,))
        user = cur.fetchone()[0]
        return user
    except Exception as e:
        print(e)
        return None



