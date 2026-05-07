"""
    Register Queries Layer
    Used to access the db and return the information
    retrieved
"""
import bcrypt
from database.connection import connect

#registers user into db
def register(username, email, password):
    conn = connect()
    try:
        cur = conn.cursor()
        #encrypts password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")
        # insert row into database
        cur.execute("INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s) RETURNING id",(username, hashed_password, email, "user"))
        #retrieves the users new id
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return user_id
    except Exception as e:
        conn.rollback()
        return str(e)

#check for existing user
def get_existing_user(username, email):
    conn = connect()
    try:
        cur = conn.cursor()
        #check for existing user, Cap Sensitive
        cur.execute("SELECT username FROM users WHERE username = %s", (username,))
        ex_username = cur.fetchone()
        #check for email, NOT Cap sensitive
        cur.execute("SELECT email FROM users WHERE LOWER(email) = LOWER(%s)", (email,))
        ex_email = cur.fetchone()
        cur.close()
        conn.close()
        #return if any existing users or email
        return  ex_username, ex_email
    except Exception as e:
        conn.close()
        return str(e)

def commit_setup(user_id, age, gender, height_cm, current_weight_kg, weight_goal_kg,
                 calorie_goal,salts_goal,protein_goal,fats_goal,carbs_goal,water_goal, weekly_activity_goal):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO user_stats (user_id,age,gender,height_cm,
                                    current_weight_kg,weight_goal_kg,
                                    calorie_goal,salts_goal,proteins_goal,water_goal,
                                    fats_goal,carbs_goal,
                                    weekly_activity_goal,current_streak,longest_streak)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s, %s, %s, %s)
            """,
            (user_id,age,gender,height_cm,current_weight_kg,weight_goal_kg,calorie_goal,
             salts_goal,protein_goal,water_goal,fats_goal,carbs_goal,weekly_activity_goal,1,1))
        conn.commit()
        cur.close()
        conn.close()
        return True

    except Exception as e:
        conn.rollback()
        conn.close()
        print(e)
        return False
