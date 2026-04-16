from database.connection import connect

def save_foodlog(food,calories,salts,proteins,date,mealtype,user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO foodlog (title,calories,salts,proteins,date,mealtype,user_id) VALUES (%s,%s,%s,%s,%s,%s,%s)  ",
        (food, calories, salts, proteins, date, mealtype, user_id,))
    conn.commit()
    cur.close()
    conn.close()

def save_waterlog(water,date,user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO waterlog (water,date,user_id) VALUES (%s,%s,%s)", (water,date, user_id,))
    conn.commit()
    cur.close()
    conn.close()

def retrieve_foodlog(user_id,date):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT title,calories,salts,proteins,mealtype,date FROM foodlog WHERE user_id = %s AND date > (%s) ORDER BY date DESC",
        (user_id, date))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def retrieve_waterlog(user_id,date):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT water,date FROM waterlog WHERE user_id = %s AND date > (%s) ORDER BY date DESC",
                (user_id, date))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def retrieve_daily_stats(user_id,date):
    total_c = 0
    total_s = 0.0
    total_p = 0.0
    total_w = 0
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT calories,salts,proteins FROM foodlog WHERE user_id = %s AND date = %s",
                (user_id, date,))
    rows = cur.fetchall()
    for data in rows:  # retrieves stats from today and totals them
        total_c = total_c + data[0]
        total_s = total_s + data[1]
        total_p = total_p + data[2]
    cur.execute("SELECT water FROM waterlog WHERE user_id = %s AND date = %s", (user_id,date,))
    rows = cur.fetchall()
    for data in rows:  # find total water from today
        total_w = total_w + data[0]
    cur.close()
    conn.close()

    return total_c,total_s,total_p,total_w


def retrieve_user_goals(user_id):
    goal_c = 1
    goal_s = 1.0
    goal_p = 1.0
    goal_w = 1
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT calorie_goal, salts_goal, proteins_goal,water_goal FROM user_stats WHERE user_id = %s",
                (user_id,))
    rows = cur.fetchall()
    for data in rows:
        goal_c = data[0]
        goal_s = data[1]
        goal_p = data[2]
        goal_w = data[3]
    cur.close()
    conn.close()
    return goal_c, goal_s, goal_p, goal_w
