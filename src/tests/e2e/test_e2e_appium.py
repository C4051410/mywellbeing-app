import os
import time
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
        cur.execute("DELETE FROM users WHERE email = %s", ("NewUserEmail@email.com",))
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
            cur.execute("TRUNCATE TABLE foodlog RESTART IDENTITY CASCADE")
            cur.execute("TRUNCATE TABLE workouts RESTART IDENTITY CASCADE")
            conn.commit()
        except:
            pass
        cur.close()
        conn.close()


def test_app_open(driver):
    #this test that the app actually opens
    assert driver.current_package is not None




def test_e2e_login(driver,seed_test_user):
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
    time.sleep(7)
    """
        Check that a user can log an activity by accessing the activities page
    """
    #find and click the activities option on the navbar
    activities_navbar = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Activities")
    activities_navbar.click()
    #check for an element only on activities
    assert wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID,"THIS WEEK'S TOTALS"))
    )
    #find and click the new activities button
    new_activity = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="New Activity")
    new_activity.click()
    #check that start button appears
    assert wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID,"START"))
    )
    #find and click the start button
    start_run = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="START")
    start_run.click()
    #used to click allow location permission when it pops up
    allow_button_id = "com.android.permissioncontroller:id/permission_allow_foreground_only_button"
    allow_button = wait.until(EC.element_to_be_clickable((AppiumBy.ID, allow_button_id)))
    allow_button.click()
    #wait 5 seconds
    time.sleep(5)
    #find and click the stop running button
    stop_run = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="PAUSE")
    stop_run.click()
    #check resume button appears
    assert wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID,"RESUME"))
    )
    #find and click finish button
    finish_run = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="FINISH")
    finish_run.click()
    #check that back on activities page it shows the new run log
    assert wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Run')]"))
    )
    time.sleep(7)
    """
        Check that a user can log an a nutrition food log by accessing the nutrition page
    """
    #find the nutrition option on the navbar and click it
    nutrition_navbar = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Nutrition")
    nutrition_navbar.click()
    #check activities page appears by checking for calories in page
    assert wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID,"Calories"))
    )
    #find and click the enter food button
    add_food = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Enter A Food")
    add_food.click()
    #find the enter value button and click it
    food_name = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.EditText[1]")
    ))
    food_name.click()
    #enter apple, this should auto fill the rest of the values
    food_name.send_keys("Apple")
    #finds and clicks the mealtype option
    mealtype = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.Button[2]")
    ))
    mealtype.click()
    #find the snack option and click it
    snack = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Snack")
    snack.click()
    time.sleep(2)
    #find and click the food log button and click it
    save_food = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="LOG FOOD")
    save_food.click()
    #make sure the food log appears back on the nutrition page
    assert wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Apple')]"))
    )
    time.sleep(7)
    """
        Test Social Page loads as intended and displays correct information
    """
    #find and click social page button on navbar
    social_navbar = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Social")
    social_navbar.click()
    #check that social page has loaded properly
    assert wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Track progress with friends"))
    )
    """
        Test Settings page loads as intended and displays correct information
    """
    #find and click the settings navbar button
    settings_navbar = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Settings")
    settings_navbar.click()
    #check that the settings page as been properly loaded
    assert wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Manage your account"))
    )
    #find the logout button on the setting page and click it
    logout_btn = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Logout\nSign out of your account")
    logout_btn.click()
    #check the user has been returned to the auth page for full circle testing.
    assert wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Register"))
    )

def test_e2e_register(driver,seed_test_user):
    """
        End 2 End Test: Specifically Tests the Register and Setup Pages
    """
    """
        Checks that you can register account on register page
    """
    #sets the wait time for the pages
    wait = WebDriverWait(driver, 10)
    #gets the username field and enter the username
    username_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.EditText[1]")
    ))
    username_field.click()
    username_field.send_keys("NewUser1")
    #gets the email field and enter the email
    email_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.EditText[2]")
    ))
    email_field.click()
    email_field.send_keys("NewUserEmail@email.com")
    #gets the password field and enter the password
    password_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.EditText[3]")
    ))
    password_field.click()
    password_field.send_keys("Password1!")
    #find the register button and click it
    login_btn = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Register")
    login_btn.click()
    #check that they have gone to the register page
    assert wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Set Up Your Profile"))
    )
    """
        Check that user can properly setup their account
    """
    #Repeat for all fields, get field, enter value or click on dropdown option
    age_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.EditText[1]")
    ))
    age_field.click()
    age_field.send_keys("20")
    gender_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.Button[1]")
    ))
    gender_field.click()
    male = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Male")
    male.click()
    height_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.EditText[2]")
    ))
    height_field.click()
    height_field.send_keys("185")
    current_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.EditText[3]")
    ))
    current_field.click()
    current_field.send_keys("80")
    target_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.EditText[4]")
    ))
    target_field.click()
    target_field.send_keys("70")
    salts_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.EditText[5]")
    ))
    salts_field.click()
    salts_field.send_keys("0.5")
    protein_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.EditText[6]")
    ))
    protein_field.click()
    protein_field.send_keys("20")
    water_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.EditText[7]")
    ))
    water_field.click()
    water_field.send_keys("1000")
    exercise_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.Button[2]")
    ))
    exercise_field.click()
    light_exercise = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Light: exercise 1-3 times/week")
    light_exercise.click()
    #used to scroll down page so they can reach button
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiScrollable(new UiSelector().scrollable(true)).scrollToEnd(10)')
    #find and click button
    finish_btn = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Continue")
    finish_btn.click()
    #check that on completion they are sent to home page
    assert wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Welcome NewUser1!"))
    )
    time.sleep(7)
    # find and click the settings navbar button
    settings_navbar = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Settings")
    settings_navbar.click()
    # check that the settings page as been properly loaded
    assert wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Manage your account"))
    )
    # find the logout button on the setting page and click it
    logout_btn = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Logout\nSign out of your account")
    logout_btn.click()
    # check the user has been returned to the auth page for full circle testing.
    assert wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Register"))
    )
