# Testing
***

## CI/CD

We use Github Actions to test our application for errors each time a commit occurs.
Github Actions uses the yml file to run each of the pytest within tests to check
that when code is updated it doesnt break the tests set out, allowing us to detect
easily if a piece of code has broken a test.

## How To Run Tests

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
   pytest src/tests
   ```

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
Unit testing done in test_auth_logic.py testing the logic of the functions is correct


| Test Class     | What it Tests                                                                                      |
|----------------|----------------------------------------------------------------------------------------------------|
| TestLogin      | Test that the login function checks each value before logging in the user                          |
| TestRegister   | Test that register function checks each value before committing to db with a new user              |
| TestCheckSetup | Tests that the check set up function works as intended and returns correct response                |
| TestSetupSave  | Test that setup saves properly, successfully checking that each vairable is valid before committing |

### Integration Testing
Integration testing is done within test_auth_integration which tests that the functions can be properly implemented with the db.

| Test Function                      | What it Tests                                                                                           |
|------------------------------------|---------------------------------------------------------------------------------------------------------|
| test_full_registration_integration | Test that user is entered into db by registration function and can then retrieved by the login function |




## Homepage Testing




### Unit Testing
Unit testing done in test_auth_logic.py testing the logic of the functions is correct

| Test Class    | What it Tests                                                                                |
|---------------|----------------------------------------------------------------------------------------------|
| TestHomeLogic | Tests the home functions including returning username, friends_activities and current streak |

##

## Activities Page Testing

### Unit Testing
Unit testing done in test_activities_logic.py testing the logic of the functions is correct

| Test Class              | What it Tests                                                                         |
|-------------------------|---------------------------------------------------------------------------------------|
| TestActivityLogging     | Tests that Activity function catches any issues and returns correct response          |
| TestPastActivityLogging | Tests that Past Activity function catches any issues and returns correct reponse      |
| TestActivityRetrieval   | Tests that retrieval function for activities returns activities or catches any issues |

### Integration Testing
Integration testing is done within test_activities_integration which tests that the functions can be properly implemented 
with the db.

| Test Function               | What it Tests                                                                               |
|-----------------------------|---------------------------------------------------------------------------------------------|
| test_activities_integration | Test that activities are successfully added into db and can then be retrieved without error |

## Nutrition Page Testing

### Unit Testing
Unit testing done in test_nutrition_logic.py testing the logic of the functions is correct

| Test Class          | What it Tests                                                                                       |
|---------------------|-----------------------------------------------------------------------------------------------------|
| TestFoodSearch      | Tests that fuzzy search logic works within function to return correct food values                   |
| TestSaveFoodLog     | Tests that saving foodlog catches any issues if found and protects errors from being commited to db |
| TestDailyStatsLogic | Tests that retrieve stats returns either correct values or default values if error occurs           |
| TestUserGoalsLogic  | Tests that retrieve goals returns either correct values or defaults values if error occurs          |

### Integration Testing
Integration testing is done within test_foodlog_integration.py which tests that the functions can be properly implemented 
with the db.

| Test Function            | What it Tests                                                                                   |
|--------------------------|-------------------------------------------------------------------------------------------------|
| test_foodlog_integration | Tests that foodlogs can be successfully added to the db and can then be retrieved without error |

## Social Page Testing
### Unit Testing
Unit testing done in test_social_logic.py testing the logic of the functions is correct

| Test Class                 | What it Tests                                                                                                  |
|----------------------------|----------------------------------------------------------------------------------------------------------------|
| TestFriendshipLogic        | Test that friends function works as intended, and that it doesnt cause any errors when invalid data is entered |
| TestSocialInteractionLogic | Test that the functions involving the posts and likes work as intended and dont cause any errors               |
| TestSocialFeedLogic        | Test that user feed returns as expected and correct response is returned                                       |


## Settings Page Testing
### Unit Testing
Unit testing done in test_settings_logic.py testing the logic of the functions is correct

| Test Class         | What it Tests                                                                                                                           |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| TestPasswordUpdate | Test that password update works as expected, returning the correct response when valid and stopping any errors being comitted to the db |
| TestGoalUpdate     | Test that goals are updated as expected and that any errors are prevented as expected                                                   |

