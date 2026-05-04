import datetime

import pytest
from database.connection import connect
from home.home_services import retrieve_user_stats, retrieve_friends_activities
from datetime import date


@pytest.fixture
def db_home_setup():
    conn = connect()
    cur = conn.cursor()
    #remove all data from all tables involved and resets identity back to 1
    cur.execute("TRUNCATE TABLE users,user_stats,friends, workouts RESTART IDENTITY CASCADE")
    conn.commit()
    #run the test and wait
    yield
    #repeat step above
    cur.execute("TRUNCATE TABLE users, user_stats,friends, workouts RESTART IDENTITY CASCADE")
    conn.commit()
    cur.close()
    conn.close()


def test_home_integration(db_home_setup):
    """
    INTEGRATION TEST: Verifies database aggregation for streaks,
    daily calories, and friend activities.
    """
    conn = connect()
    cur = conn.cursor()
    today = date.today()

    #create the users required
    cur.execute(
        "INSERT INTO users (id, username, email, password, role) VALUES (%s, %s, %s, %s, %s), (%s, %s, %s, %s, %s)",
        (1, "MainUser", "main@test.com", "pass!", "user",
         2, "FriendUser", "friend@test.com", "pass!", "user")
    )

    #create the user stats needed for test
    cur.execute(
        "INSERT INTO user_stats (user_id, current_streak, longest_streak, calorie_goal) VALUES (%s, %s, %s, %s), (%s, %s, %s, %s)",
        (1, 5, 10, 2000,
         2, 1, 1, 2000)  # Friend needs a stats record to satisfy the JOIN
    )

    #insert two food logs
    cur.execute(
        "INSERT INTO foodlog (user_id, calories, date) VALUES (%s, %s, %s), (%s, %s, %s)",
        (1, 500, today,
         1, 300, today)
    )

    #create friendship between the two accounts
    cur.execute("INSERT INTO friends (user_id, friend_id) VALUES (%s, %s)",
                (1, 2))
    #create exercise for friend user
    cur.execute(
        "INSERT INTO workouts (user_id, title, activity_type, distance_km, duration, calories, start_date) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (2, "Evening Run", "Run", 5.0, datetime.timedelta(minutes=30), 400, today)
    )

    conn.commit()

    #retrive the users stats from the db
    stats = retrieve_user_stats(1)
    #check all stats are correct
    assert stats[0] == "MainUser" #username
    assert stats[1] == 5  #current streak
    assert stats[2] == 10 #longest streak
    assert stats[3] == 2000 #calorie goal
    assert stats[4] == 800  # daily caloire

    #retrieves your friends activities
    activities = retrieve_friends_activities(1, today)
    assert len(activities) == 1 # check one is returned
    assert activities[0][0] == "FriendUser" #check friends username
    assert activities[0][1] == "Evening Run" #check title is correct
    assert activities[0][2] == 1 #check streak
    assert activities[0][3] == "Run" #activity type
    assert activities[0][4] == 5 #distance
    assert activities[0][5] == datetime.timedelta(minutes=30) #duration
    assert activities[0][6] == 400 #calories

    cur.close()
    conn.close()