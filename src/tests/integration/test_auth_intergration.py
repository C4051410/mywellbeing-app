from unittest.mock import patch

import pytest
from auth.auth_services import register_user, login_user
from database.connection import connect


@pytest.fixture
def db_cleanup():
    """Ensures the test user AND test email are wiped before and after."""
    test_user = "int_test_bob"
    test_email = "bob@integration.com"  # The email used in the test

    def cleanup():
        conn = connect()
        cur = conn.cursor()
        # Delete by both username and email to clear all possible conflicts
        cur.execute("DELETE FROM users WHERE username = %s OR email = %s", (test_user, test_email))
        conn.commit()
        cur.close()
        conn.close()

    cleanup()  # Clean before test
    yield test_user
    cleanup()  # Clean after test

def test_full_registration_flow(db_cleanup):
    """
    INTEGRATION TEST: Checks that the functions are properly integrated with the db
    Checks that a registration creates the user and that the user can log in with that account
    """
    #sets up data for test
    test_user = db_cleanup
    test_email = "bob@integration.com"
    test_pass = "SecurePass123!"

    with patch("auth.auth_services.resend"), \
            patch("auth.auth_services.notification"):
        #call on register to create an account
        success, message = register_user(test_user, test_email, test_pass)
        #check that success is true
        assert success is True,f"REGISTRATION FAILED! Message: {message}"

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