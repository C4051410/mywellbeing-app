from unittest.mock import patch

import pytest
from auth.auth_services import register_user, login_user
from database.connection import connect


@pytest.fixture
def db_cleanup():
    """Ensures the test user is removed even if the test fails."""
    test_user = "int_test_bob"
    #used to return username for registration, wait to complete rest until function is returned
    yield test_user
    #cleans db if tests fails
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = %s", (test_user,))
    conn.commit()
    cur.close()
    conn.close()

@patch("auth.auth_services.notification")
@patch("auth.auth_services.resend")
def test_full_registration_flow(mock_resend,mock_notification,db_cleanup):
    """
    INTEGRATION TEST: Checks that the functions are properly integrated with the db
    Checks that a registration creates the user and that the user can log in with that account
    """
    #sets up data for test
    test_user = db_cleanup
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


    #cleans up db after testing is complete
    cur.execute("DELETE FROM users WHERE username = %s", (test_user,))
    conn.commit()
    cur.close()
    conn.close()