from datetime import datetime
from unittest.mock import patch
import pytest
from activities.activities_services import save_activity,save_past_activity,retrieve_activities
from database.connection import connect

@pytest.fixture
def db_cleanup():
    #used to clean db whether test fails or not
    test_duration = 60
    yield test_duration
    conn = connect()
    cur = conn.cursor()
    #deletes all record that could be remaining
    cur.execute("DELETE FROM workouts WHERE duration_seconds =%s", (test_duration,))
    cur.execute("DELETE FROM users WHERE id = %s", (2,))
    conn.commit()
    cur.close()
    conn.close()

@patch('activities.activities_services.notification')
def test_activities_integration(mock_notification,db_cleanup):
    """
    INTEGRATION TEST: Checks that functions are properly integrated with db
    Checks that activities_services, current and past, save properly from db and can be retrieved
    """
    conn = connect()
    cur = conn.cursor()
    #inserts a user to deal with foreign key issues
    cur.execute(
        "INSERT INTO users (id, username, email, password) "
        "VALUES (%s, %s, %s, %s)",
        (2, "ActTester", "act@test.com", "dummypass1!")
    )
    conn.commit()
    #define the elements needed in activity
    type = "Run"
    distance_km = 1.5
    test_duration = db_cleanup
    #try and save activity to database
    success = save_activity(2,type,distance_km,test_duration,datetime.today())
    #check it returns successful
    assert success is True
    #try and retrieve the activity to check values are correct
    cur.execute("SELECT user_id,title,distance_km,duration_seconds FROM workouts WHERE user_id =%s", (2,))
    row = cur.fetchone()
    #check values match up to the expected
    assert row[0] == 2
    assert row[1] == "Run"
    assert row[2] == 1.5
    assert row[3] == 60
    #create values that can be used in past_activities
    title = "Pushups"
    calories = 200
    reps = 20
    #try and save the past activity, including empty values stored as 0
    success = save_past_activity(2,title,calories,test_duration,reps,0,datetime.today())
    #check that it returns successful
    assert success is True
    #try and retrieve the past activity to check values stored correctly
    cur.execute("SELECT user_id,activity_type,reps,duration_seconds,distance_km from workouts WHERE title = %s", (title,))
    row = cur.fetchone()
    #check that values are stored correctly
    assert row[0] == 2
    assert row[1] == "Workout"
    assert row[2] == 20
    assert row[3] == 60
    assert row[4] == 0
    #try and retrieve both sets of activities using retrieve
    activities = retrieve_activities(2)
    #check that both activities return
    assert len(activities) == 2
    #check the type of each is correct, in correct order, more recent one first
    assert activities[0][1] == "Workout"
    assert activities[1][1] == "Run"
    #deletes record to keep db clean
    cur.execute("DELETE FROM workouts WHERE user_id = %s", (2,))
    cur.execute("DELETE FROM users WHERE id = %s", (2,))


