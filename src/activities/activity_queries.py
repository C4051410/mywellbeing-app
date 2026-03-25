from database.connection import connect
from database.connection import connect

def save_activity(user_id, activity_type, distance_km, duration_seconds, start_date, source="manual"):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO workouts (user_id, source, activity_type, distance_km, start_date, "
                "duration_seconds, title, duration) VALUES (%s, %s, %s, %s, %s, %s, %s, (%s || ' seconds')::interval)",
                (user_id, source, activity_type, distance_km, start_date, duration_seconds, activity_type, duration_seconds))
    conn.commit()
    cur.close()
    conn.close()

def get_activities(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT activity_type, distance_km, start_date, duration_seconds, source FROM workouts "
                "WHERE user_id = %s ORDER BY start_date DESC NULLS LAST, id DESC", (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


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