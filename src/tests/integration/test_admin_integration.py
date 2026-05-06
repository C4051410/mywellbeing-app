from database.connection import connect
from admin.admin_services import retrieve_users_admin, delete_users_admin, make_moderators_admin, remove_users_admin

def test_admin_integration():
    """
    INTEGRATION TEST: Checks that the functions are properly integrated with the db
    Check that admin_services properly retrieve users, and can delete and make mods in the db
    """
    conn = connect()
    cur = conn.cursor()
    #remove everything from table as backup
    cur.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
    #insert two users into users for testing
    cur.execute(
        "INSERT INTO users (id, username, email, password, role) VALUES (%s, %s, %s, %s, %s), (%s, %s, %s, %s, %s)",
        (1, "UserTester", "act@test.com", "dummypass1!", "user",
         2, "ModTester", "mod@test.com", "Dummypass1!", "moderator")
    )
    #commit users
    conn.commit()
    #try retrieve users to test they return all users
    users = retrieve_users_admin("")
    assert len(users) == 2 #make sure 2 users are returned
    assert users[0][3] == 1 #check id is 1
    assert users[1][3] == 2 #check id is 2
    #now check that the search query works as intended
    single_user = retrieve_users_admin("User")
    assert len(single_user) == 1 #make sure 1 user is returned
    assert single_user[0][3] == 1 #make sure its the correct user
    #try and remove the user with id == 2
    remove_users_admin(2)
    #use select to check the db for users
    cur.execute("SELECT username,email,role,id FROM users")
    row = cur.fetchone()
    #check that the correct user is returned
    assert row[0] == "UserTester"
    assert row[2] == "user"
    #try and make the user the moderator
    make_moderators_admin(1)
    cur.execute("SELECT username,email,role,id FROM users")
    row = cur.fetchone()
    assert row[0] == "UserTester" #checks that it's the same user as above
    assert row[2] == "moderator" #check that the user has been updated to moderator
    #delete the table to clear it for next test
    cur.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
    conn.commit()
    cur.close()
    conn.close()

