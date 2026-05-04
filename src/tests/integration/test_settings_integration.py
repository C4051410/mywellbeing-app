from unittest.mock import patch
import pytest
import bcrypt
from database.connection import connect
from settings.settings_services import update_password, update_goals, delete_account


@pytest.fixture
def db_settings_setup():
    conn = connect()
    cur = conn.cursor()
    #delet all users that could be remaining in the db
    cur.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
    conn.commit()
    #wait till testing is finished
    yield
    #delete any users that could be remaining
    cur.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
    conn.commit()
    cur.close()
    conn.close()

@patch("auth.auth_services.resend")
def test_settings_integration_flow(db_settings_setup):
    """
    INTEGRATION TEST: Verifies that settings page correctly updates
    password hashing, goal updates, and deletion in the db.
    """
    conn = connect()
    cur = conn.cursor()
    #hash password so it works correctly
    original_password = "OldPass1!"
    hashed_old = bcrypt.hashpw(original_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    #insert user into db
    cur.execute(
        "INSERT INTO users (id, username, email, password, role) VALUES (%s, %s, %s, %s, %s)",
        (1, "SettingsUser", "set@test.com", hashed_old, "user")
    )
    #Insert stats for user so it can be successfully updated
    cur.execute("INSERT INTO user_stats (user_id, calorie_goal, water_goal) VALUES (1, 2000, 2000)")
    conn.commit()

    #try and update password to new password
    success, msg = update_password(1, "OldPass1!", "NewPass1!", "NewPass1!")
    assert success is True
    assert msg == "Password Updated"

    #retrieve password and check its updated to new password in db
    cur.execute("SELECT password FROM users WHERE id = 1")
    new_hashed_pw = cur.fetchone()[0].encode('utf-8')
    assert new_hashed_pw != hashed_old.encode('utf-8')
    assert bcrypt.checkpw("NewPass1!".encode('utf-8'), new_hashed_pw)

    #try and update goals
    success_goal, msg_goal = update_goals(1, 2500, 3000)
    assert success_goal is True
    #check that the goals have been successfully updated in the db
    cur.execute("SELECT calorie_goal, water_goal FROM user_stats WHERE user_id = 1")
    row = cur.fetchone()
    assert row[0] == 2500
    assert row[1] == 3000

    #try and delete the account
    success_del, msg_del = delete_account(1)
    assert success_del is True

    #check that now user was removed from the db
    cur.execute("SELECT COUNT(*) FROM users")
    assert cur.fetchone()[0] == 0

    cur.close()
    conn.close()