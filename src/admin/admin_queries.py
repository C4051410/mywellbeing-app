from src.database.connection import connect

def retrieve_U(search_query=""):
    conn = connect()
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

def delete_U(user_id: int):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s",(user_id,))
    conn.commit()
    cur.close()

def make_M(user_id: int):
    conn = connect()
    cur = conn.cursor()
    cur.execute(" UPDATE users SET role = %s WHERE id = %s",("moderator", user_id,))
    conn.commit()
    cur.close()



