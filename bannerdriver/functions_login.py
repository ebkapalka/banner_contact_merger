from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from typing import TYPE_CHECKING
import time

# ridiculous hack to get around circular imports
if TYPE_CHECKING:
    from bannerdriver.drivers.driver_base import BannerDriver


def nav_to_login(manager: "BannerDriver", timeout: int | None = None):
    """
    Navigate to the login page
    :param manager: BannerDriver object
    :param timeout: timeout in seconds
    """
    driver = manager.get_driver()
    if not timeout:
        timeout = manager.timeout
    env = manager.env
    driver.get(f"https://{env}banner.montana.edu/"
               "applicationNavigator/seamless")
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, "username")))
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, "password")))


def enter_credentials(manager: "BannerDriver", timeout: int | None = None):
    """
    Enter the username and password into the login form
    :param manager: BannerDriver object
    :param timeout: timeout in seconds
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
    if not timeout:
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
        EC.title_is("Duo Security"))


def handle_2fa(manager: "BannerDriver", timeout: int | None = None):
    """
    Handle the 2FA process
    :param manager: BannerDriver object
    :param method: "push", "sms", or "call"
    :param timeout: timeout in seconds
    :return: None
    """
    driver = manager.get_driver()
    if not timeout:
        timeout = manager.timeout
    # trust the browser
    btn_trust = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.ID, "trust-browser-button")))
    btn_trust.click()

    # Wait for the user to complete the 2FA process
    WebDriverWait(driver, timeout).until(
        EC.title_is("Application Navigator"))
    print("Successfully logged in")
