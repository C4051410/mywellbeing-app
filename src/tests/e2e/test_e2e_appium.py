import os
from pathlib import Path
import bcrypt
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from database.connection import connect
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    #used to create the options, including details about the emulator
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.automation_name = "UiAutomator2"
    #get the tests current files
    current_file = Path(__file__).resolve()
    #go to root node
    project_root = current_file.parents[3]
    #create the path to the apk
    apk_path = os.getenv("APK_PATH", str(project_root / "build" / "apk" / "mywellbeing.apk"))
    options.app = apk_path
    #creates the driver for the test
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    #waits until test finishes
    yield driver
    #quits driver after tests
    driver.quit()


@pytest.fixture
def seed_test_user():
    conn = connect()
    cur = conn.cursor()
    #creates and hashes passwords
    password = "Password1!"
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")
    try:
        #try and delete user if it exists
        cur.execute("DELETE FROM users WHERE email = %s", ("newuser@gmail.com",))
        conn.commit()
        #insert the new user into DB
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            ("NewUser", "newuser@gmail.com", hashed_password)
        )
        conn.commit()
        #get the users ID
        cur.execute("SELECT id FROM users WHERE email = %s", ("newuser@gmail.com",))
        user_id = cur.fetchone()[0]
        cur.execute("DELETE FROM user_stats WHERE user_id = %s", (user_id,))
        conn.commit()
        #go and insert their stats to move onto homepage
        cur.execute("""
                    INSERT INTO user_stats (user_id, age, gender, height_cm, current_weight_kg, weight_goal_kg, calorie_goal, salts_goal, proteins_goal, water_goal)
                    VALUES (%s, 25, 'Male', 180, 75, 70, 2000, 5, 150, 2000)
                """, (user_id,))
        conn.commit()
        #wait until the test is finished
        yield
    except Exception as e:
        print(f"DEBUG: Database seeding failed: {e}")
        conn.rollback()
        raise e
    finally:
        try:
            #try and reset the tables
            cur.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
            cur.execute("TRUNCATE TABLE user_stats RESTART IDENTITY CASCADE")
            conn.commit()
        except:
            pass
        cur.close()
        conn.close()


def test_app_open(driver):
    #this test that the app actually opens
    assert driver.current_package is not None




def test_e2e(driver,seed_test_user):
    """
        End 2 End Test: Check that the front end can properly operate with the backend
    """
    """
        Check that a user can log in using the front end objects and make it to the homepage
    """
    # Set a 10-second wait limit to allow for delays in loading
    wait = WebDriverWait(driver, 10)

    #look for the button to switch from registration to login
    switch_to_login = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Already have an account? Login"))
    )
    switch_to_login.click()

    #looks for the email text field on the page, using the Xpath collected using appium inspector
    email_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.EditText[1]")
    ))
    #click on the text field
    email_field.click()
    #enter the into the field the user email
    email_field.send_keys("newuser@gmail.com")

    #repeat the same as above but for password field
    pass_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.EditText[2]")
    ))
    pass_field.click()
    pass_field.send_keys("Password1!")

    # Finds the login button and clicks it
    login_btn = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Login")
    login_btn.click()

    #Check that it's actually gone to homepage by looking for welcome text
    assert wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Welcome NewUser!"))
    )