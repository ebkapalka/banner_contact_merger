from selenium.common import (TimeoutException, NoSuchElementException,
                             StaleElementReferenceException)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import time


def nav_to_form(driver: webdriver, form: str, timeout=20) -> None:
    """
    Navigate to the specified form page
    :param driver: webdriver object
    :param form: form to navigate to
    :param timeout: timeout in seconds
    :return: None
    """
    env = _get_env(driver)
    form = form.upper().strip()
    driver.get(f"https://{env}.montana.edu/BannerAdmin?form={form}")
    selector = (By.XPATH, f"//h2[contains(text(), '{form}')]")
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(selector))
        print(f"Navigated to {form}")
        return
    except TimeoutException:
        print(f"Could not navigate to {form}")
        selector = (By.CLASS_NAME, "notifications-item-text")
        try:
            err_elem = driver.find_element(*selector)
            print(f"Error: {err_elem.text}")
        except NoSuchElementException:
            return


def get_current_form(driver: webdriver, timeout=5) -> str:
    """
    Get the current form name
    :param driver: webdriver object
    :param timeout: timeout in seconds
    :return: the name of the current form
    """
    try:
        selector = (By.XPATH, "(//h2[@class='workspace-title'])")
        elem = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(selector))
        form_name = elem.get_attribute("title").strip().split()[-4]
        return form_name
    except (IndexError, TimeoutException, NoSuchElementException):
        print(f"Could not identify current form")
    except Exception as e:
        print(f"Unknown error: {type(e)}")
        print(e)
    return ""


def enter_gid(driver: webdriver, gid: str, max_tries=10, timeout=10):
    """
    Enter the GID into the input box
    :param driver: webdriver object
    :param gid: gid to enter
    :param max_tries: maximum number of tries before giving up
    :param timeout: timeout in seconds
    :return: None
    """
    input_gid = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, "inp:key_block_id")))
    input_gid.clear()
    input_gid.send_keys(gid)

    try_count = 0
    while try_count < max_tries:
        try:
            button_go = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@title='Go (Alt+PageDown)']")))
            button_go.click()
            WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@title='Start Over (F5)']")))
            break
        except (TimeoutException, NoSuchElementException,
                StaleElementReferenceException):
            try_count += 1
            time.sleep(0.25)
    else:
        print("Entered GID")
        return
    print("Could not enter GID")


def _get_env(driver: webdriver) -> str:
    """
    Get the environment from the current URL
    :param driver: webdriver object
    :return: the current Banner environment
    """
    entire_url = driver.current_url
    base_url = entire_url.split("//")[1]
    return base_url.split('.')[0]
