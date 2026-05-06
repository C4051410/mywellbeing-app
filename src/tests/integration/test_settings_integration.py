from unittest.mock import patch
import bcrypt
from database.connection import connect
from settings.settings_services import update_password, update_goals, delete_account, retrieve_notification_status, \
    update_notification_status


@patch("settings.settings_services.resend")
def test_settings_integration_flow(mock_resend):
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
        "INSERT INTO users (id, username, email, password, role,notification_status) "
        "VALUES (%s, %s, %s, %s, %s,%s)",
        (1, "SettingsUser", "set@test.com", hashed_old, "user",True)
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
    success_goal, msg_goal = update_goals(1, 2500, 3000,4)
    assert success_goal is True
    #check that the goals have been successfully updated in the db
    cur.execute("SELECT calorie_goal, water_goal, weekly_activity_goal FROM user_stats WHERE user_id = 1")
    row = cur.fetchone()
    assert row[0] == 2500
    assert row[1] == 3000
    assert row[2] == 4

    #try and retrieve the notification status and check its correct
    status = retrieve_notification_status(1)
    assert status is True
    #try and update the notification status and check it completed
    update_status = update_notification_status(1,status)
    assert update_status is True
    #check the db to see that the notification status has updated
    cur.execute("SELECT notification_status FROM users WHERE id = %s",(1,))
    row = cur.fetchone()
    assert row[0] == False

    #try and delete the account
    success_del, msg_del = delete_account(1)
    assert success_del is True

    #check that now user was removed from the db
    cur.execute("SELECT COUNT(*) FROM users")
    assert cur.fetchone()[0] == 0

    cur.close()
    conn.close()