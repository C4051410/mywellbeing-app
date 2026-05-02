import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

@pytest.fixture
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.automation_name = "UiAutomator2"
    options.app = "E:/Pycharm_Projects/CSC2033-Project/build/apk/mywellbeing.apk"
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield driver
    driver.quit()

def test_app_open(driver):
    assert driver.current_package is not None


from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_interaction(driver):
    # Set a 10-second wait limit
    wait = WebDriverWait(driver, 10)

    # 1. Switch to Login View
    # Flet maps the text of the TextButton to the Accessibility ID
    switch_to_login = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Already have an account? Login"))
    )
    switch_to_login.click()

    # 2. Enter Email
    # Using 'Email' as the value because that is the 'label' in your ft.TextField
    email_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.EditText[1]")
    ))
    email_field.click()
    email_field.send_keys("newuser@gmail.com")

    # 3. Enter Password
    pass_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//android.widget.EditText[2]")
    ))
    pass_field.click()
    pass_field.send_keys("Password1!")

    # 4. Click the Login Button
    # Note: There are two buttons named "Login" in your code (the view switcher and the actual button)
    # Appium usually finds the visible one.
    login_btn = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Login")
    login_btn.click()

    # 5. Verify Login Success
    # Check for an element that only exists on the Home Screen (e.g., your NavBar)
    assert wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Welcome NewUser!"))
    )