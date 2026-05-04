import pytest
from database.connection import connect
from moderator.moderator_services import retrieve_posts_moderator, remove_posts_moderator

def test_moderator_integration():
    """
    INTEGRATION TEST: Verifies that the moderator service correctly
    retrieves and deletes posts from both foodlog and workouts within the db.
    """
    conn = connect()
    cur = conn.cursor()

    #create 2 users in the db
    cur.execute(
        "INSERT INTO users (id, username, email, password, role) VALUES (%s, %s, %s, %s, %s),"
        "(%s, %s, %s, %s, %s)",
        (1, "FirstOwner", "1owner@test.com", "Pass1123!", "user",
         2, "SecondOwner","2owner@test.com","Pass1123!","user")
    )

    #create two separate food logs, one for each user
    cur.execute("INSERT INTO foodlog (id, user_id, title) VALUES (%s, %s, %s),"
                "(%s, %s, %s)",
                (10, 1, "Healthy Salad",
                 11,2,"Burger"))
    #create two separate workouts, one for each user
    cur.execute("INSERT INTO workouts (id, user_id, title) VALUES (%s, %s, %s),"
                "(%s, %s, %s)",
                (20, 1, "Gym Session",
                 21,2,"Run"))
    conn.commit()

    #retrieve the 4 posts from the database
    posts = retrieve_posts_moderator("")
    assert len(posts) == 4

    #check that the search filter only returns specific users posts
    search_results = retrieve_posts_moderator("First")
    assert len(search_results) == 2
    assert search_results[0][1] == "FirstOwner"

    #try and delete a post from the db
    delete_result = remove_posts_moderator(10, "food")
    assert delete_result is True

    #check within the database that post is gone
    cur.execute("SELECT COUNT(*) FROM foodlog WHERE id = 10")
    assert cur.fetchone()[0] == 0
    #check the other remaining 3 posts remain
    posts = retrieve_posts_moderator("")
    assert len(posts) == 3

    cur.close()
    conn.close()