from selenium.webdriver.remote.webdriver import WebDriver
import os

from bannerdriver.functions_general import switch_iframe, get_driver

SCRIPT_NAMES = {
    "get_emails": "bannerdriver/js_scripts/get_emails.js",
    "add_emails": "bannerdriver/js_scripts/add_emails.js",
    "delete_emails": "bannerdriver/js_scripts/delete_emails.js",
    "get_phone_numbers": "bannerdriver/js_scripts/get_phone_numbers.js",
    "add_phone_numbers": "bannerdriver/js_scripts/add_phone_numbers.js",
    "delete_phone_numbers": "bannerdriver/js_scripts/delete_phone_numbers.js",
    "get_addresses": "bannerdriver/js_scripts/get_addresses.js",
    "add_addresses": "bannerdriver/js_scripts/add_addresses.js",
    "delete_addresses": "bannerdriver/js_scripts/delete_addresses.js",
    "get_test_scores": "bannerdriver/js_scripts/get_test_scores.js",
    "add_test_scores": "bannerdriver/js_scripts/add_test_scores.js",
    "delete_test_scores": "bannerdriver/js_scripts/delete_test_scores.js",
    "delete_alt_ids": "bannerdriver/js_scripts/delete_alt_ids.js",
    # Add more scripts as needed
}
script_cache = {}  # Cache for the content of JavaScript files


def load_js_scripts(script_names):
    """
    Load and cache JavaScript files into memory.
    :param script_names: Dictionary of script names and file paths.
    """
    for name, path in script_names.items():
        if not os.path.isfile(path):
            raise FileNotFoundError(f"The script file '{path}' does not exist.")
        try:
            with open(path, 'r') as file:
                script_cache[name] = file.read()
        except Exception as e:
            print(type(e))
            raise Exception(f"Error reading the script file '{path}': {e}")


def execute_js(driver, script_name, *args):
    """
    Executes a cached JavaScript file on the current page using Selenium WebDriver.
    :param driver: webdriver object
    :param script_name: Name of the cached JavaScript script to execute.
    :param args: Arguments to pass to the JavaScript function.
    :raises ValueError: If the script name is invalid.
    :return: Result of the executed script or None.
    """
    driver = get_driver(driver)
    switch_iframe(driver)
    js_script = script_cache.get(script_name)

    if not js_script:
        raise ValueError(f"Invalid script name '{script_name}'")

    try:
        js_code = f"return {js_script};"
        result = driver.execute_script(js_code, *args)
        return result
    except Exception as e:
        print(type(e))
        raise Exception(f"Error executing the script '{script_name}': {e}")


# Load all JavaScript scripts into the cache
load_js_scripts(SCRIPT_NAMES)
