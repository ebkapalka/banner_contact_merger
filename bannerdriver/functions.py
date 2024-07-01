from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from bannerdriver.driver import BannerDriver


def enter_credentials(manager: BannerDriver):
    """
    Enter the username and password into the login form
    :param manager: BannerDriver object
    :return: None
    """
    driver = manager.get_driver()

    def _identify_error() -> str:
        """
        Identify any error message
        :return: text of the error message
        """
        try:
            login_form = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "login-form")))
            error_div = login_form.find_element(By.CLASS_NAME, "alert-danger")
            if error_div:
                return error_div.text
        except NoSuchElementException:
            return ""
        except TimeoutException:
            return ""
        return ""

    # Enter the username and password
    timeout = manager.timeout
    username = manager.username
    password = manager.password
    input_username = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, "username")))
    input_password = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, "password")))
    button_submit = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@name='_eventId_proceed']")))
    input_username.send_keys(username)
    input_password.send_keys(password)
    button_submit.click()

    if e := _identify_error():
        print(f"Error: {e}")
        driver.quit()
    WebDriverWait(driver, timeout).until(
        EC.title_is("Two-Factor Authentication"))


def handle_2fa(manager: BannerDriver, method="push"):
    """
    Handle the 2FA process
    :param manager: BannerDriver object
    :param method: "push", "sms", or "call"
    :return: None
    """
    driver = manager.get_driver()
    timeout = manager.timeout
    WebDriverWait(driver, timeout).until(
        EC.title_is("Two-Factor Authentication"))
    if method == "push":
        print("Please accept the push notification on your phone")
        xpath = "//button[text()='Send Me a Push ']"
        button = WebDriverWait(driver, 300).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        button.click()
    elif method == "sms":
        # TODO: Implement SMS 2FA
        ...
    elif method == "call":
        # TODO: Implement Call 2FA
        ...
    else:
        raise ValueError("Invalid 2FA method")

    # Wait for the user to complete the 2FA process
    WebDriverWait(driver, timeout).until(
        EC.title_is("Application Navigator"))
    print("Successfully logged in")
