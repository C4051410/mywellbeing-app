from database.connection import connect
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
