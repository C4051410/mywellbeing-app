from datetime import date, timedelta
from database.connection import connect

def retrieve_streak(user_id):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT current_streak,longest_streak,last_active
            FROM user_stats
            WHERE user_id = %s
        
        """,(user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row
    except Exception as e:
        conn.close()
        print(e)

def update_streak(user_id):
    conn = connect()
    try:
        cur = conn.cursor()
        today = date.today()
        yesterday = today - timedelta(days=1)
        streak = retrieve_streak(user_id)
        if streak is None:
            return
        current_s, longest_s, last_active = streak
        if longest_s == 0:
            longest_s = 1
        if last_active == today:
            cur.close()
            conn.close()
            return
        elif last_active == yesterday:
            current_s = current_s + 1
            if current_s >= longest_s:
                longest_s = current_s
            cur.execute("""
            UPDATE user_stats
            SET current_streak = %s, longest_streak = %s, last_active = %s
            WHERE user_id = %s
            """,(current_s,longest_s,today,user_id))
            conn.commit()
            cur.close()
            conn.close()
            return
        else:
            cur.execute("""
            UPDATE user_stats
            SET current_streak = %s, last_active =%s
            WHERE user_id = %s
            """,(1,today,user_id))
            conn.commit()
            cur.close()
            conn.close()
            return
    except Exception as e:
        conn.rollback()
        conn.close()
        print(e)


def commit_activity(user_id, activity_type, distance_km, duration_seconds, start_date, source="manual"):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO workouts (user_id, source, activity_type, distance_km, start_date, "
                    "duration_seconds, title, duration) VALUES (%s, %s, %s, %s, %s, %s, %s, (%s || ' seconds')::interval)",
                    (user_id, source, activity_type, distance_km, start_date, duration_seconds, activity_type, duration_seconds))
        conn.commit()
        cur.close()
        conn.close()
        update_streak(user_id)
        return
    except Exception as e:
        conn.rollback()
        conn.close()
        print(e)




def commit_past_activity(user_id, title,calories,duration_seconds,reps,distance,start_date, source="manual",activity_type="Workout"):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO workouts (user_id,source,title,activity_type,calories,duration_seconds,reps,distance_km,start_date,duration) VALUES (%s, %s, %s, %s,%s, %s,%s,%s, %s, (%s || ' seconds')::interval)",
                    (user_id, source, title,activity_type, calories, duration_seconds, reps, distance, start_date,duration_seconds))
        conn.commit()
        cur.close()
        conn.close()
        update_streak(user_id)
    except Exception as e:
        conn.rollback()
        conn.close()
        print(e)

def get_activities(user_id):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("SELECT title,activity_type, distance_km, start_date, duration_seconds,calories,reps, source FROM workouts "
                    "WHERE user_id = %s ORDER BY start_date DESC NULLS LAST, id DESC", (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        conn.close()
        print(e)


def save_tokens_for_user(user_id, token_data):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO strava_connections (
            user_id,
            strava_athlete_id,
            access_token,
            refresh_token,
            expires_at
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (user_id)
        DO UPDATE SET
            strava_athlete_id = EXCLUDED.strava_athlete_id,
            access_token = EXCLUDED.access_token,
            refresh_token = EXCLUDED.refresh_token,
            expires_at = EXCLUDED.expires_at
    """, (
        user_id,
        token_data["athlete"]["id"],
        token_data["access_token"],
        token_data["refresh_token"],
        token_data["expires_at"]
    ))

    conn.commit()
    cur.close()
    conn.close()

def load_tokens_for_user(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT access_token, refresh_token, expires_at, strava_athlete_id
        FROM strava_connections
        WHERE user_id = %s
    """, (user_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "access_token": row[0],
        "refresh_token": row[1],
        "expires_at": row[2],
        "strava_athlete_id": row[3],
    }