from database.connection import connect

def register(username, full_name, password, email):
    conn = connect()
    cur = conn.cursor()
    try:
        # insert row into database
        cur.execute("INSERT INTO users (username, full_name, password, email) VALUES (%s, %s, %s, %s)",(username, full_name, password, email))
        conn.commit()
        return "User registration successful"
    except Exception as e:
        conn.rollback()
        return "Error"

    finally:
        cur.close()
        conn.close()
