from datetime import date
from unittest.mock import patch
import pytest

from database.connection import connect
from nutrition.nutrition_services import retrieve_foodlogs,save_foodlog

@pytest.fixture
def db_cleanup():
    test_title = "Apple"
    yield test_title
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM foodlog WHERE title =%s",(test_title,))
    conn.commit()
    cur.close()
    conn.close()

@patch("nutrition.nutrition_services.notification")
def test_foodlog_intergration(mock_notification, db_cleanup):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = 1")
    cur.execute(
        "INSERT INTO users (id, username, email, password) "
        "VALUES (%s, %s, %s, %s)",
        (1, "FoodTester", "food@test.com", "dummypass1!")
    )
    conn.commit()
    test_title = db_cleanup
    calories = 200
    salts = 0
    proteins = 0.6
    success, message = save_foodlog(test_title, calories, salts, proteins,date.today(),"Snack",1)
    print(message)
    assert success is True
    assert message == "Successful"


    cur.execute("SELECT title,calories,salts,proteins FROM foodlog WHERE title =%s",(test_title,))
    row = cur.fetchone()
    assert row[0] == test_title
    assert row[1] == 200
    assert row[2] == 0
    assert row[3] == 0.6
    logs = retrieve_foodlogs(1)
    assert len(logs) == 1
    assert logs[0][0] == test_title

    cur.execute("DELETE FROM foodlog WHERE title =%s",(test_title,))
    conn.commit()
    cur.close()
    conn.close()

