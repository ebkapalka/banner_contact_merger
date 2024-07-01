from typing import TYPE_CHECKING
import os

# Conditional import to avoid circular dependency issues
if TYPE_CHECKING:
    from bannerdriver.drivers.driver_base import BannerDriver

SCRIPT_NAMES = {
    "get_emails": "get_emails.js",
    "add_emails": "add_emails.js",
    "delete_emails": "delete_emails.js",
    "get_phone_numbers": "get_phone_numbers.js",
    "add_phone_numbers": "add_phone_numbers.js",
    "delete_phone_numbers": "delete_phone_numbers.js",
    "get_addresses": "get_addresses.js",
    "add_addresses": "add_addresses.js",
    "delete_addresses": "delete_addresses.js",
    "get_test_scores": "get_test_scores.js",
    "add_test_scores": "add_test_scores.js",
    "delete_test_scores": "delete_test_scores.js",
    # Add more scripts as needed
}


def execute_js(manager: "BannerDriver", script_name: str) -> None | str:
    """
    Executes a JavaScript file on the current page using Selenium WebDriver.
    :param manager: BannerDriver object
    :param script_name: Name of the JavaScript file to execute.
    :raises ValueError: If the script name is invalid.
    :raises FileNotFoundError: If the script file does not exist.
    :raises Exception: If there is an error reading or executing the script.
    :return: Result of the executed script or None.
    """
    driver = manager.get_driver()
    script_file = SCRIPT_NAMES.get(script_name)

    if not script_file:
        raise ValueError(f"Invalid script name '{script_name}'")
    if not os.path.isfile(script_file):
        raise FileNotFoundError(f"The script file '{script_file}' does not exist.")

    try:
        with open(script_file, 'r') as file:
            js_script = file.read()
    except Exception as e:
        print(type(e))
        raise Exception(f"Error reading the script file '{script_file}': {e}")
    try:
        result = driver.execute_script(js_script)
        return result
    except Exception as e:
        print(type(e))
        raise Exception(f"Error executing the script '{script_file}': {e}")


def switch_to_tab(tab_name: str) -> None:
    # TODO: write some JavaScript code to switch to a tab by name
    ...


def save_changes() -> None:
    ...
