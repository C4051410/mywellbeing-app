from database.connection import connect

def retrieve_users_admin(search_query=""):
    conn = connect()
    try:
        cur = conn.cursor()
        query = "SELECT username, email, role, id FROM users WHERE role != %s"
        params = ["admin"]
        if search_query:
            query += " AND username LIKE %s"
            params.extend([f"%{search_query}%",])
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()

def delete_users_admin(user_id: int):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s",(user_id,))
        conn.commit()
        cur.close()
    except Exception as e:
        conn.rollback()
        print(e)

def make_moderators_admin(user_id: int):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute(" UPDATE users SET role = %s WHERE id = %s",("moderator", user_id,))
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()



