import bcrypt
from database.connection import connect

#used to retrieve password
def retrieve_current_password(user_id):
    conn = connect()
    cur = conn.cursor()
    #tries to retrieve password
    try:
        cur.execute("SELECT password FROM users WHERE id = %s", (user_id,))
        password = cur.fetchone()[0].encode()
        conn.close()
        return password
    #if error occurs rollsback
    except Exception as e:
        conn.rollback()
        print(e)
        conn.close()


def commit_update_password(user_id, new_password):
    """
    Updates the user's password in the database.
    Hashes the password with bcrypt (NRF7) before storage
    """
    conn = connect()
    cur = conn.cursor()
    try:
        # Generate salt and hash
        hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')

        cur.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_pw, user_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        cur.close()
        conn.close()


def update_goals(user_id, goals):
    return