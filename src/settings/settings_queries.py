"""
    Settings Queries Layer
    Used to access the db and return the information
    retrieved
"""
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


def commit_update_goals(user_id, calorie_goal, water_goal, weekly_activity_goal):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""
                    UPDATE user_stats 
                    SET calorie_goal = %s, water_goal = %s, weekly_activity_goal = %s
                    WHERE user_id = %s""",
                    (calorie_goal, water_goal, weekly_activity_goal, user_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(e)
        return False
    finally:
        cur.close()
        conn.close()

def get_notification_status(user_id):
    #connect to database
    conn = connect()
    cur = conn.cursor()
    try:
        #try adn retrieve the status from the users_id
        cur.execute("SELECT notification_status FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        #check it's not None
        if row is None:
            return True
        else:
            return row[0]
    #used if their was an issue with connection
    except Exception as e:
        print(e)
        conn.close()
        return True

def commit_notification_status(user_id, notification_status):
    #connect to database
    conn = connect()
    cur = conn.cursor()
    try:
        #try and update the notification status of the user_id with new notification status
        cur.execute("UPDATE users SET notification_status = %s WHERE id = %s", (notification_status,user_id))
        conn.commit()
        cur.close()
        conn.close()
    #used if there is an issue with the connection
    except Exception as e:
        conn.rollback()
        print(e)
        conn.close()

def delete_user_account_db(user_id):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(e)
        return str(e)
    finally:
        cur.close()
        conn.close()

