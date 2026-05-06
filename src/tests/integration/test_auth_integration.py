from unittest.mock import patch
from auth.auth_services import register_user, login_user, check_setup_complete,save_setup
from database.connection import connect


@patch("auth.auth_services.notification")
@patch("auth.auth_services.resend")
def test_full_registration_integration(mock_resend,mock_notification):
    """
    INTEGRATION TEST: Checks that the functions are properly integrated with the db
    Checks that a registration creates the user and that the user can log in with that account
    """
    #sets up data for test
    test_user = "int_test_bob"
    test_email = "bob@integration.com"
    test_pass = "SecurePass123!"

    #call on register to create an account
    success, message = register_user(test_user, test_email, test_pass)
    #check that success is true
    assert success is True

    #check that values are actually stored in db
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email FROM users WHERE username = %s", (test_user,))
    row = cur.fetchone()
    #checks row isnt empty
    assert row is not None
    #checks username matches db
    assert row[1] == test_user
    #checks email matches db
    assert row[2] == test_email
    #check id matches users
    assert row[0] == message

    #tries and logs in
    success, message = login_user(test_email, test_pass)
    #checks login was successful
    assert success is True
    #check id username matches current user
    assert message[1] == test_user
    #check that the user hasn't been set up
    setup = check_setup_complete(message[0])
    assert setup is False
    #try and complete the setup
    complete =  save_setup(message[0],20,"Male",185,
                           85,75,2000,
                           2,50,1000,4)
    assert complete is True
    #check that setup was complete
    cur.execute("SELECT user_id FROM user_stats WHERE user_id = %s", (message[0],))
    row = cur.fetchone()
    assert row is not None
    #check that now set up is recognised
    setup = check_setup_complete(message[0])
    assert setup is True

    #cleans up db after testing is complete
    cur.execute("DELETE FROM users WHERE username = %s", (test_user,))
    conn.commit()
    cur.close()
    conn.close()