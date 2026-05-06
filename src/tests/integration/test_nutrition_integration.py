from datetime import date
from unittest.mock import patch
from database.connection import connect
from nutrition.nutrition_services import retrieve_foodlogs, save_foodlog, save_waterlog, retrieve_waterlogs, \
    retrieve_daily_stats, retrieve_user_goals


@patch("nutrition.nutrition_services.notification")
def test_nutrition_integration(mock_notification, ):
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
    cur.execute(
        "INSERT INTO user_stats (user_id,calorie_goal,salts_goal,"
        "proteins_goal,water_goal) VALUES (%s, %s, %s, %s, %s)",
        (1,2000,4,50,3000))
    conn.commit()
    #used to call cleanup when function successeds or fails
    test_title = "Apple"
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
    foodlogs = retrieve_foodlogs(1)
    #check only the single log returns with right name
    assert len(foodlogs) == 1
    assert foodlogs[0][0] == test_title
    #try and insert the waterlog
    success, message = save_waterlog(1000,date.today(),1)
    #check it returns successfully
    assert success is True
    assert message == "Successful"
    #try and retrieve water log from the db
    cur.execute("SELECT water FROM waterlog WHERE user_id =%s",(1,))
    row = cur.fetchone()
    #check its correct
    assert row[0] == 1000
    #check that water log retrieve works as intended
    waterlogs = retrieve_waterlogs(1)
    assert len(waterlogs) == 1
    assert waterlogs[0][0] == 1000
    #retrieve the total values of the stats
    total_c, total_s, total_p, total_w = retrieve_daily_stats(1,date.today())
    #check all the stats match up
    assert total_c == 200
    assert total_s == 0
    assert total_p == 0.6
    assert total_w == 1000
    #retrieve the users goal
    goal_c, goal_s, goal_p, goal_w = retrieve_user_goals(1)
    #check that values match up
    assert goal_c == 2000
    assert goal_s == 4
    assert goal_p == 50
    assert goal_w == 3000
    #cleans db to protect it from errors
    cur.execute("DELETE FROM foodlog WHERE title =%s",(test_title,))
    cur.execute("DELETE FROM users WHERE id = 1")
    conn.commit()
    cur.close()
    conn.close()

