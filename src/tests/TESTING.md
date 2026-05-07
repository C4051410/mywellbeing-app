# Testing
***

## CI/CD

We use Github Actions to test our application for errors each time a commit occurs.
Github Actions uses the yml file to run each of the pytest within tests to check
that when code is updated it doesn't break the tests set out, allowing us to detect
easily if a piece of code has broken a test. E2E testing isn't completed due to the fact
that it would simply take too long to create the APK and open the emulator in GitHub,
it would not be practical to wait 15+ minutes to get the CI/CD back.

[.github/workflows/CSC2033_test.yml](.github/workflows/CSC2033_test.yml)

## How To Run Unit Tests

1.  **Create and Activate the Virtual Enviorment**:
    
   ```bash
   .\venv\Scripts\activate     # Windows
   ```
    
2.  **Download the Requirements**:

   ```bash
   pip install -r requirements.txt
   ```
3.  **Run The Tests**:
   ```bash
   pytest src/tests/unit
   ```

## How To Run Integration Tests
1.  **Create and Activate the Virtual Enviorment**:
    
   ```bash
   .\venv\Scripts\activate     # Windows
   ```
    
2.  **Download the Requirements**:

   ```bash
   pip install -r requirements.txt
   ```
3. **Download and Install PostgreSQL**

    Download At https://www.postgresql.org/download/windows/
    
    Set Up PostgresSQL and Create a Database using 
    [schema.sql](integration/schema.sql)
    
    run within integration: 
    ```bash
    psql -U postgres -d database_name -f source/to/schema.sql
    ```
    Add link to .env as DATABASE_URL to link the Database to connection.py
    postgresql://username:password@localhost:5432/database_name

    **WARNING, RUNNING TESTS RESULTS IN DATABASE BEING TRUNCATED
    CREATE SPECIAL DB FOR TESTING**

4. **Run the Tests**
   ```bash
   pytest src/tests/integration
   ```

## How To Run End 2 End Tests
1.  **Create and Activate the Virtual Enviorment**:
    
   ```bash
   .\venv\Scripts\activate     # Windows
   ```
    
2.  **Download the Requirements**:

   ```bash
   pip install -r requirements.txt
   ```
3. **Download and Install PostgreSQL**
    
    Follow the steps above, but use this link instead to connect to emulator
    postgresql://username:password@10.0.2.2:5432/database

4. **Install Emulator**
   Download At https://developer.android.com/studio
    
    Install emulator within and start running it
5. **Install Flutter SDK**
   Download At https://docs.flutter.dev/install/manual
6. **Install Node.js**
   Download At https://nodejs.org/en/download
7. **Install Appium**
    ```bash
    npm install -g appium
    appium driver install uiautomator2
    ```
8. **Check Android Emulator Running**
    ```bash
    adb devices
    ```   
    Check that it returns emulator-5554, if not, try and restart emulator
9. **Download APK**
    ```bash
    flet build apk
    ```
    Copy File from apk to Andorid Simulator
10. **Run Appium then Test**
    ```bash
    appium
    ```
    Then
    ```bash
    pytest src/tests/e2e
    ```

Testing results can be found in [report.html](report.html)
## End to End Testing
The end-to-end testing is done in one file, this is to simplify the task, as it requires the use
of external tools like android studio, and a constantly running emulator, Appium is also required 
to be running as well. The test was made with help from Appium Inspector, allowing us to view the 
details of objects. test_app_open is used to test that the application opens correctly.
All E2E testing is done in [test_e2e_appium.py](e2e/test_e2e_appium.py), different sections will be clearly labeled.

| End to End Tests | What it Tests                                                                                                                            |
|------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Login            | Tests that the user can successfully navigate and login and end up on the homepage                                                       |
| Activities       | Tests that the user can navigate to activities page, and create a new activity, and see the new activity                                 |
| Nutrition        | Tests that the user can navigate to the nutrition page and create a new food log, and see the new log                                    |
| Social           | Tests that the user can navigate to the social page and add a friend                                                                     |
| Settings         | Tests that the user can navigate to the settings page and log out of their account                                                       |
| Registration     | Tests that the user can successfully navigate and create a new account and end up on the homepage                                        |
| Setup            | Tests that the user can successfully navigate and enter all the required fields in the setup and end up on the homepage                  |
| Moderator        | Tests that the moderator is successfully logged into their page and that they can delete users posts                                     |
| Admin            | Tests that the admin is successfully logged into their page and that they can delete users accounts and also promote users to moderators |

We also conducted a [Google Lighthouse Search](e2e/GoogleLightHouseE2E.pdf) to find the performance of our application and how well it going between pages.
The tests are normally conducted on websites, so our tests maybe less accurate as it's based on an application.

## Login and Registration Testing

### Manual Testing
| Test ID | Test                   | Description                                                     | Result                                                                      | Reason                                                                  |
|:--------|:-----------------------|:----------------------------------------------------------------|:----------------------------------------------------------------------------|:------------------------------------------------------------------------|
| **MT1** | Valid Registration     | Test entering a user with a valid username, email and password. | Pass: Leads to user setup page                                              | Tests that account creation works                                       |
| **MT2** | Missing Fields         | Test that when fields are missing.                              | Pass: Page remains on registration and displays missing field text          | Test that all fields need to be entered                                 |
| **MT3** | Already Existing Users | Test when account already exists                                | Pass: Page remains on registration and displays account already exists text | Test that you cant create multiple accounts with same username or email |
| **MT4** | Valid login            | Test entering a user with a valid email and password            | Pass: Leads user to Homepage                                                | Test that you can log into an created account                           |
| **MT5** | Invalid Account Login  | Test that when account is missing during login                  | Pass: Page remains on login and displays account doesnt exists text         | Test that you can only log into an account that exists                  |

### Unit Testing
Unit testing done in [test_auth_logic.py](unit/test_auth_logic.py) testing the logic of the functions is correct


| Test Class     | What it Tests                                                                                      |
|----------------|----------------------------------------------------------------------------------------------------|
| TestLogin      | Test that the login function checks each value before logging in the user                          |
| TestRegister   | Test that register function checks each value before committing to db with a new user              |
| TestCheckSetup | Tests that the check set up function works as intended and returns correct response                |
| TestSetupSave  | Test that setup saves properly, successfully checking that each vairable is valid before committing |

### Integration Testing
Integration testing is done within [test_auth_integration.py](integration/test_auth_integration.py) 
which tests that the functions can be properly implemented with the db.

| Test Function                      | What it Tests                                                                                           |
|------------------------------------|---------------------------------------------------------------------------------------------------------|
| test_full_registration_integration | Test that user is entered into db by registration function and can then retrieved by the login function |



## Homepage Testing
### Manual Testing
| Test ID | Test            | Description                                                                  | Result                               | Reason                                   |
|:--------|:----------------|:-----------------------------------------------------------------------------|:-------------------------------------|:-----------------------------------------|
| **MT1** | Content Appears | Check that all content appears including name, activity, streak friends etc. | Pass: All content is displayed       | Tests that all content appears correctly |
| **MT2** | Web Link Works  | Check that clicking the link to the UN page works as intended                | Pass: When clicked, loads UN website | Tests that the link works when clicked   |



### Unit Testing
Unit testing done in [test_home_logic.py](unit/test_home_logic.py) testing the logic of the functions is correct

| Test Class    | What it Tests                                                                                |
|---------------|----------------------------------------------------------------------------------------------|
| TestHomeLogic | Tests the home functions including returning username, friends_activities and current streak |

### Integration Testing
Integration testing is done within [test_home_integration.py](integration/test_home_integration.py) 
which tests that the functions can be properly implemented with the db.

| Test Function         | What it Tests                                                                     |
|-----------------------|-----------------------------------------------------------------------------------|
| test_home_integration | Tests that user stats and friends activities are returned as expected from the db |
##

## Activities Page Testing
### Manual Testing
| Test ID | Test                 | Description                                                                                        | Result                                                                            | Reason                                          |
|:--------|:---------------------|:---------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:------------------------------------------------|
| **MT1** | Display Activities   | Check that the page displays the activities, and also when clicked goes into detail about activity | Pass: All activities and displayed and can be viewed in detail                    | Tests that activities are displayed to user     |
| **MT2** | Connect Strava       | Connect to strava API and make sure it displays the users activities from strava to our app        | Pass: Strava API works as intended and displays their activities with strava logo | Tests that strava API works as intended         |
| **MT3** | Create Activity      | Check that new activity can create activity that tracks them on activities like runs or cycles     | Pass: New activities successfully track users when they go on runs/walks          | Tests that new activities properly tracks users |
| **MT4** | Create Past Activity | Check that a past activity can be entered with a wide range of options like reps and distance      | Pass: Past activities can be logged successfully                                  |                                                 |
| **MT5** | Invalid Values       | Check that user cannot enter impossible details like negative numbers for distance or reps         | Pass: Text fields prevent impossible entries from being entered                   |                                                 |

### Unit Testing
Unit testing done in [test_activities_logic.py](unit/test_activities_logic.py) testing the logic of the functions is correct

| Test Class              | What it Tests                                                                         |
|-------------------------|---------------------------------------------------------------------------------------|
| TestActivityLogging     | Tests that Activity function catches any issues and returns correct response          |
| TestPastActivityLogging | Tests that Past Activity function catches any issues and returns correct reponse      |
| TestActivityRetrieval   | Tests that retrieval function for activities returns activities or catches any issues |

### Integration Testing
Integration testing is done within [test_activities_integration.py](integration/test_activities_integration.py) 
which tests that the functions can be properly implemented with the db.

| Test Function               | What it Tests                                                                               |
|-----------------------------|---------------------------------------------------------------------------------------------|
| test_activities_integration | Test that activities are successfully added into db and can then be retrieved without error |

## Nutrition Page Testing
### Manual Testing
| Test ID | Test                     | Description                                                              | Result                                                       | Reason                                            |
|:--------|:-------------------------|:-------------------------------------------------------------------------|:-------------------------------------------------------------|:--------------------------------------------------|
| **MT1** | Display Logs             | Make sure that both food and water logs are displayed                    | Pass: Both are displayed appropriately, showing their detail | Tests that users can see their past entries       |
| **MT2** | Create Food log          | Make sure that users can enter food logs with all their details          | Pass: Users can enter the details about their food           | Tests that food logs can be successfully added    |
| **MT3** | Invalid Food log Values  | Make sure that users cannot enter invalid food log values like negatives | Pass: Text fields prevent erroneous data from being entered  | Test that food logs catches any errors with data  |
| **MT2** | Create Water log         | Make sure that users can enter water logs                                | Pass: Users can enter the details about their water          | Tests that water logs can be successfully added   |
| **MT3** | Invalid Water log Values | Make sure that users cannot enter invalid water log value like negatives | Pass: Text fields prevent erroneous data from being entered  | Test that water logs catches any errors with data |

### Unit Testing
Unit testing done in [test_nutrition_logic.py](unit/test_nutrition_logic.py) testing the logic of the functions is correct

| Test Class          | What it Tests                                                                                       |
|---------------------|-----------------------------------------------------------------------------------------------------|
| TestFoodSearch      | Tests that fuzzy search logic works within function to return correct food values                   |
| TestSaveFoodLog     | Tests that saving foodlog catches any issues if found and protects errors from being commited to db |
| TestDailyStatsLogic | Tests that retrieve stats returns either correct values or default values if error occurs           |
| TestUserGoalsLogic  | Tests that retrieve goals returns either correct values or defaults values if error occurs          |

### Integration Testing
Integration testing is done within [test_nutrition_integration.py](integration/test_nutrition_integration.py) 
which tests that the functions can be properly implemented with the db.

| Test Function              | What it Tests                                                                                    |
|----------------------------|--------------------------------------------------------------------------------------------------|
| test_nutrition_integration | Tests that food logs can be successfully added to the db and can then be retrieved without error |

## Social Page Testing
### Manual Testing
| Test ID | Test                      | Description                                                                           | Result                                                          | Reason                              |
|:--------|:--------------------------|:--------------------------------------------------------------------------------------|:----------------------------------------------------------------|:------------------------------------|
| **MT1** | Check Leaderboard         | Check that leaderboard is displayed properly and scores are displayed between friends | Pass: Users friends are displayed on leaderboard correctly      | Tests leaderboard works as intended |
| **MT2** | Check Friends Activities  | Make sure that firends activities are displayed                                       | Pass: Users friends activities are displayed                    | Tests activities are returned       |
| **MT3** | Check Like/Unlike Post    | Check that users can like/unlike their friends Posts                                  | Pass: Users can like a post and then unlike it                  | Tests likes work as intended        |
| **MT4** | Check Add/Delete Comments | Check users can comment on posts and then delete them                                 | Pass: Users can create comments about a post and then delete it | Tests comments work as intended     |
| **MT5** | Check Add/Remove Friends  | Check users can add and remove friends                                                | Pass: Users can add and remove friends                          | Tests friends work as intended      |

### Unit Testing
Unit testing done in [test_social_logic.py](unit/test_social_logic.py) testing the logic of the functions is correct

| Test Class                 | What it Tests                                                                                                  |
|----------------------------|----------------------------------------------------------------------------------------------------------------|
| TestFriendshipLogic        | Test that friends function works as intended, and that it doesnt cause any errors when invalid data is entered |
| TestSocialInteractionLogic | Test that the functions involving the posts and likes work as intended and dont cause any errors               |
| TestSocialFeedLogic        | Test that user feed returns as expected and correct response is returned                                       |

### Integration Testing
Integration testing is done within [test_social_integration.py](integration/test_social_integration.py)
which tests that the functions can be properly implemented with the db.

| Test Function           | What it Tests                                                                                              |
|-------------------------|------------------------------------------------------------------------------------------------------------|
| test_social_integration | Test that user can add friends, like and comment on posts and retrieve the leaderboard correctly in the db |


## Settings Page Testing
### Manual Testing
| Test ID | Test                | Description                                                                                                 | Result                                             | Reason                                                  |
|:--------|:--------------------|:------------------------------------------------------------------------------------------------------------|:---------------------------------------------------|:--------------------------------------------------------|
| **MT1** | Change Password     | Check that users can change their password                                                                  | Pass: Users can change their password              | Tests that password updates when changed                |
| **MT2** | Invalid Password    | Check that users cant change their password to an invalid password, like missing special characters or caps | Pass: Text fields catch when passwords are invalid | Tests that password doesnt update when invalid          |
| **MT3** | Change Goals        | Check that users can change their goals                                                                     | Pass: Users can change their goals                 | Tests that goals change when updated                    |
| **MT4** | Invalid Goals       | Check that users cant change their goals to invalid options like negative numbers                           | Pass: Text fields catch when goals are invalid     | Tests that goals dont update when change is invalid     |
| **MT5** | Delete Account      | Check that users can delete their own account in the settings page                                          | Pass: Users are deleted when confirmed             | Tests that user can delete their own account            |
| **MT6** | Change Notification | Check that users can change their notification settings                                                     | Pass: Users can chang their notification setting   | Tests that users can change their notification settings |

### Unit Testing
Unit testing done in [test_settings_logic.py](unit/test_settings_logic.py) testing the logic of the functions is correct

| Test Class             | What it Tests                                                                                                                           |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| TestPasswordUpdate     | Test that password update works as expected, returning the correct response when valid and stopping any errors being comitted to the db |
| TestGoalUpdate         | Test that goals are updated as expected and that any errors are prevented as expected                                                   |
| TestNotificationStatus | Test that notification status is changed as expected and catches any errors                                                             |
| TestDeleteUserAccount  | Test that delete account works as intended and that it catches any errors                                                               |

### Integration Testing
Integration testing is done within [test_settings_integration.py](integration/test_settings_integration.py)
which tests that the functions can be properly implemented with the db.

| Test Function             | What it Tests                                                                                                  |
|---------------------------|----------------------------------------------------------------------------------------------------------------|
| test_settings_integration | Test that user can update their passwords and user goals, and that they can delete there account within the db |


## Admin Page Testing

### Manual Testing
| Test ID | Test           | Description                                                  | Result                                                       | Reason                                                  |
|:--------|:---------------|:-------------------------------------------------------------|:-------------------------------------------------------------|:--------------------------------------------------------|
| **MT1** | Search Users   | Check that admin can search for a specific user or moderator | Pass: Search Bar works as intended and returns specific user | Tests that admin can return a specific user             |
| **MT2** | Delete User    | Check that admin can delete a user or moderator              | Pass: Admin can delete a specific user                       | Tests the admin power of deleting account               |
| **MT3** | Make Moderator | Check that an admin can turn a normal user into a moderator  | Pass: Admin can make a normal user into a moderator          | Tests the admin power of creating a moderator of a user |

### Unit Testing
Unit testing done in [test_admin_logic.py](unit/test_admin_logic.py) testing the logic of the functions is correct

| Test Class           | What it Tests                                                        |
|----------------------|----------------------------------------------------------------------|
| TestCheckAdmin       | Test that the checking the admin role returns the correct response   |
| TestRetrieveUsers    | Test that the users are returned as intended                         |
| TestRemoveUsers      | Test that the delete user works for deleting users from the DB       |
| TestUpdateModerators | Test that users can have their role changed from users to moderators |

### Integration Testing
Integration testing is done within [test_admin_integration.py](integration/test_admin_integration.py) 
which tests that the functions can be properly implemented with the db.

| Test Function          | What it Tests                                                                                                                 |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| test_admin_integration | Test that admin can retrieve all users and moderator and can change them to a moderator and can also delete users from the db |


## Moderator Page Testing

### Manual Testing
| Test ID | Test         | Description                                          | Result                                           | Reason                                        |
|:--------|:-------------|:-----------------------------------------------------|:-------------------------------------------------|:----------------------------------------------|
| **MT1** | Search Users | Check that moderators can search for a specific user | Pass: Search feature returns the specific user   | Tests that moderators can find specific users |
| **MT1** | Delete Post  | Check that moderators can delete a post              | Pass: Delete feature remove the post from the DB | Tests that moderators can delete posts        |

### Unit Testing
Unit testing done in [test_moderators_logic.py](unit/test_moderators_logic.py) testing the logic of the functions is correct

| Test Class         | What it Tests                                                          |
|--------------------|------------------------------------------------------------------------|
| TestCheckModerator | Test that the checking the moderator role returns the correct response |
| TestRetrievePosts  | Test that the posts are returned as intended                           |
| TestRemovePosts    | Test that the delete posts removes them from the database              |

### Integration Testing
Integration testing is done within [test_moderator_integration.py](integration/test_moderator_integration.py) 
which tests that the functions can be properly implemented with the db.

| Test Function              | What it Tests                                                                 |
|----------------------------|-------------------------------------------------------------------------------|
| test_moderator_integration | Test that the moderator can retrieve users posts, and delete them from the db |

