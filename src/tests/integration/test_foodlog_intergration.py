from datetime import date
from unittest.mock import patch
import pytest

from database.connection import connect
from nutrition.nutrition_services import retrieve_foodlogs,save_foodlog

#used to clean db whether tests completes or fails
@pytest.fixture
def db_cleanup():
    #used to wait for other function to finish before returning
    test_title = "Apple"
    yield test_title
    conn = connect()
    cur = conn.cursor()
    #deletes foodlog or user if they exist
    cur.execute("DELETE FROM foodlog WHERE title =%s",(test_title,))
    cur.execute("DELETE FROM users WHERE id = 1")
    conn.commit()
    cur.close()
    conn.close()

@patch("nutrition.nutrition_services.notification")
def test_foodlog_intergration(mock_notification, db_cleanup):
    """
    INTEGRATION TEST: Checks that functions are properly integrated with db
    Checks that foodlog can be successfully saved and retrieved from a user in the db
    """
    conn = connect()
    cur = conn.cursor()
    #inserts user to solve foreign key issue
    cur.execute(
        "INSERT INTO users (id, username, email, password) "
        "VALUES (%s, %s, %s, %s)",
        (1, "FoodTester", "food@test.com", "dummypass1!")
    )
    conn.commit()
    #used to call cleanup when function successeds or fails
    test_title = db_cleanup
    #tests values including 0 and floats
    calories = 200
    salts = 0
    proteins = 0.6
    #call function which should save to db using query tools
    success, message = save_foodlog(test_title, calories, salts, proteins,date.today(),"Snack",1)
    #check it was successful and it returns correct message
    assert success is True
    assert message == "Successful"

    #check that data is actually in the database by using query
    cur.execute("SELECT title,calories,salts,proteins FROM foodlog WHERE title =%s",(test_title,))
    row = cur.fetchone()
    #make sure results match
    assert row[0] == "Apple"
    assert row[1] == 200
    assert row[2] == 0
    assert row[3] == 0.6
    #try and retrieve the foodlogs for that user
    logs = retrieve_foodlogs(1)
    #check only the single log returns with right name
    assert len(logs) == 1
    assert logs[0][0] == test_title
    #cleans db to protect it from errors
    cur.execute("DELETE FROM foodlog WHERE title =%s",(test_title,))
    cur.execute("DELETE FROM users WHERE id = 1")
    conn.commit()
    cur.close()
    conn.close()

