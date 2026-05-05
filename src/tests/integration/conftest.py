# src/tests/conftest.py
import pytest
from database.connection import connect

@pytest.fixture(autouse=True)
def db_wipe():
    """
    Automatically runs before every test to ensure a clean, responsive DB.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        #terminate any connections that maybe accidently open
        cur.execute("""
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname = current_database()
                      AND pid <> pg_backend_pid();
                """)
        # Clear all tables involved in integration tests
        cur.execute("""
            TRUNCATE TABLE 
                users, user_profiles, user_stats, workouts, 
                foodlog, waterlog, friends, social_likes, 
                social_comments, strava_connections 
            RESTART IDENTITY CASCADE
        """)
        conn.commit()
    finally:
        cur.close()
        conn.close()