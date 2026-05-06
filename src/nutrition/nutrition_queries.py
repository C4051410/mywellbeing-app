"""
    Nutrition Queries Layer
    Used to access the db and return the information
    retrieved
"""
from database.connection import connect

#commits foodlog to database
def commit_foodlog(food,calories,salts,proteins, fats, carbohydrates, date,mealtype,user_id):
    conn = connect()
    cur = conn.cursor()
    #query to store all the data under the correct user_id
    cur.execute(
        "INSERT INTO foodlog (title,calories,salts,proteins,fats,carbohydrates,date,mealtype,user_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)  ",
        (food, calories, salts, proteins, fats, carbohydrates, date, mealtype, user_id,))
    conn.commit()
    cur.close()
    conn.close()

#commits waterlog to db
def commit_waterlog(water,date,user_id):
    conn = connect()
    cur = conn.cursor()
    #query to store waterlog to correct user_id
    cur.execute("INSERT INTO waterlog (water,date,user_id) VALUES (%s,%s,%s)", (water,date, user_id,))
    conn.commit()
    cur.close()
    conn.close()

#retrieves foodlogs from db
def get_foodlog(user_id,date):
    conn = connect()
    cur = conn.cursor()
    #selects all rows from foodlog where user_id matches and is within a set time
    cur.execute(
        "SELECT title,calories,salts,proteins,fats,carbohydrates,mealtype,date FROM foodlog WHERE user_id = %s AND date > (%s) ORDER BY date DESC",
        (user_id, date))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    #returns all rows
    return rows

#retrieves waterlogs from db
def get_waterlog(user_id,date):
    conn = connect()
    cur = conn.cursor()
    #retrieve all rows from waterlog where user_id matches and is within set time
    cur.execute("SELECT water,date FROM waterlog WHERE user_id = %s AND date > (%s) ORDER BY date DESC",
                (user_id, date))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    # returns all rows
    return rows

#retrieves daily_stats
def get_daily_stats(user_id,date):
    conn = connect()
    cur = conn.cursor()
    #retrievs all foodlog stats from a user within a time
    cur.execute("SELECT calories,salts,proteins,fats,carbohydrates FROM foodlog WHERE user_id = %s AND date = %s",
                (user_id, date,))
    food_rows = cur.fetchall()
    #retrievs all waterlogs from a user within a time
    cur.execute("SELECT water FROM waterlog WHERE user_id = %s AND date = %s", (user_id,date,))
    water_rows = cur.fetchall()
    cur.close()
    conn.close()
    #return all rows
    return food_rows, water_rows

#gets users goals
def get_user_goals(user_id):
    conn = connect()
    cur = conn.cursor()
    #retrieve the goals from the specified user
    cur.execute("SELECT calorie_goal, salts_goal, proteins_goal,water_goal FROM user_stats WHERE user_id = %s",
                (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    #returns the row
    return row
