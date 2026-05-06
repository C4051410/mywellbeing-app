from unittest.mock import patch
from database.connection import connect
from social.social_service import (
    add_friend_by_username,
    like_item,
    comment_on_item,
    get_social_overview,
    list_friends,
    unlike_item,
    delete_comment_item,
    remove_friend_by_id,
    list_comments
)
@patch("social.social_service.retrieve_notification_status")
@patch("social.social_service.resend")
def test_social_integration_flow(mock_resend,mock_retrieve_notification_status):
    """
    INTEGRATION TEST: Verifies friend management, interactions, and feed logic
    can be stored and retrieved from the db.
    """
    conn = connect()
    cur = conn.cursor()

    #create 3 users, user, users friend and a random account
    cur.execute(
        "INSERT INTO users (id, username, email, password, role) VALUES (%s, %s, %s, %s, %s), (%s, %s, %s, %s, %s), (%s, %s, %s, %s, %s)",
        (1, "MainUser", "main@test.com", "pass!", "user",
         2, "FriendUser", "friend@test.com", "pass!", "user",
         3, "StrangerUser", "stranger@test.com", "pass!", "user")
    )

    #create an exercise for the users friend
    cur.execute(
        "INSERT INTO workouts (id, user_id, title, calories, start_date) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)",
        (100, 2, "Friend's Morning Run", 500)
    )
    conn.commit()

    #test that friends actually work
    add_result = add_friend_by_username(1, "FriendUser")
    assert add_result == "Friend added successfully"

    #check that friends have been added successfully, user to friend and friend to user
    cur.execute("SELECT COUNT(*) FROM friends")
    assert cur.fetchone()[0] == 2
    #check friends appear in friends list
    friends = list_friends(1)
    assert len(friends) == 1

    #try and like a post
    like_res = like_item(1, "workout", 100,2)
    assert like_res == "Liked successfully"

    #try and leave a comment on a post
    comment_res = comment_on_item(1, "workout", 100, "Great run!",2)
    assert comment_res == "Comment added successfully"
    #check list comments contains the comment
    comments = list_comments("workout", 100)
    assert len(comments) == 1
    #check like actually saves to db
    cur.execute("SELECT COUNT(*) FROM social_likes")
    assert cur.fetchone()[0] == 1
    #check comment actually saved to db
    cur.execute("SELECT COUNT(*) FROM social_comments")
    assert cur.fetchone()[0] == 1




    #try and retrieve all posts and leaderboard
    overview = get_social_overview(1)

    #check that the user comment and likes have been added correctly
    assert len(overview["activity"]) == 1
    post = overview["activity"][0]
    assert post["username"] == "FriendUser"
    assert post["like_count"] == 1
    assert post["liked_by_user"] is True
    assert post["comment_count"] == 1

    #check that only the relevant users appear in the leaderboard
    leaderboard_usernames = [entry["username"] for entry in overview["leaderboard"]]
    assert "MainUser" in leaderboard_usernames
    assert "FriendUser" in leaderboard_usernames
    assert "StrangerUser" not in leaderboard_usernames

    #check that unlike works
    unlike_res = unlike_item(1, "workout", 100)
    assert unlike_res == "Like removed successfully"
    #check that delete comment works
    del_comment = delete_comment_item(1,1)
    assert del_comment == "Comment deleted successfully"
    #check both are removed from the db
    cur.execute("SELECT COUNT(*) FROM social_likes")
    assert cur.fetchone()[0] == 0
    cur.execute("SELECT COUNT(*) FROM social_comments")
    assert cur.fetchone()[0] == 0

    remove_friend = remove_friend_by_id(1,2)
    assert remove_friend == "Friend removed successfully"
    cur.execute("SELECT COUNT(*) FROM friends")
    assert cur.fetchone()[0] == 0

    cur.close()
    conn.close()