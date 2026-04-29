import importlib
import os

import pytest
from unittest.mock import patch

# 1. Import the modules that are being mocked elsewhere
import database.connection
import auth.auth_services

# 2. Force a clean reload of these modules to wipe out any Mocks
importlib.reload(database.connection)
importlib.reload(auth.auth_services)

# 3. NOW import the functions you need for the test
from auth.auth_services import register_user,login_user
from database.connection import connect

@pytest.fixture(autouse=True)
def stop_all_mocks():
    """Force-stops any leaked mocks from unit tests."""
    patch.stopall() # This kills any 'MagicMock' leaked from other files
    yield
@pytest.fixture
def db_cleanup():
    """Wipes everything and PRINTS the DB URL for debugging."""
    test_user = "int_test_jobs"
    test_email = "bob@integration.com"

    # DEBUG: This will show up in the GitHub logs
    print(f"\n--- DEBUG: CONNECTING TO: {os.getenv('DATABASE_URL')} ---")

    def cleanup():
        try:
            conn = connect()
            cur = conn.cursor()
            # Wipe both to prevent the 'Already Exists' error
            cur.execute("DELETE FROM users WHERE username = %s OR email = %s", (test_user, test_email))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Cleanup failed: {e}")

    cleanup()
    yield test_user
    cleanup()


def test_full_registration_flow(db_cleanup):
    test_user = db_cleanup
    test_email = "bob@integration.com"
    test_pass = "SecurePass123!"

    with patch("auth.auth_services.resend"), \
            patch("auth.auth_services.notification"):
        success, message = register_user(test_user, test_email, test_pass)

        if not success:
            # IF IT FAILS, LET'S SEE WHAT'S ACTUALLY IN THE DB
            conn = connect()
            cur = conn.cursor()
            cur.execute("SELECT username, email FROM users")
            users = cur.fetchall()
            cur.close()
            conn.close()
            print(f"\n--- DATABASE CONTENTS: {users} ---")

        assert success is True, f"FAILED! Message: {message}"

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