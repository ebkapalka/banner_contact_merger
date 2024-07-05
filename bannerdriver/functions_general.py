from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
import time
import os

from bannerdriver.drivers.driver_base import BannerDriver

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


def execute_js(driver: WebDriver | BannerDriver, script_name: str) -> None | str:
    """
    Executes a JavaScript file on the current page using Selenium WebDriver.
    :param driver: webdriver or BannerDriver object
    :param script_name: Name of the JavaScript file to execute.
    :raises ValueError: If the script name is invalid.
    :raises FileNotFoundError: If the script file does not exist.
    :raises Exception: If there is an error reading or executing the script.
    :return: Result of the executed script or None.
    """
    driver = _get_driver(driver)
    _switch_iframe(driver)
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
        # this is apparently synchronous
        result = driver.execute_script(js_script)
        return result
    except Exception as e:
        print(type(e))
        raise Exception(f"Error executing the script '{script_file}': {e}")


def update_input_value_legacy(driver, input_element, new_text):
    """
    Update the value of an input element in a Banner form.
    :param driver: webdriver object
    :param input_element: the input element to update
    :param new_text: new text to enter into the input element
    :return: None
    """
    driver = _get_driver(driver)
    _switch_iframe(driver)
    element_type = driver.execute_script(
        "return arguments[0].parentElement.getAttribute('data-widget')",
        input_element
    )

    if element_type == 'checkbox':
        is_checked = driver.execute_script("return arguments[0].checked", input_element)
        should_check = new_text.lower() in ['true', 'checked']
        if is_checked != should_check:
            driver.execute_script("arguments[0].click()", input_element)
    else:
        # Clear and set the input value with JavaScript
        driver.execute_script("""
            arguments[0].value = '';
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, input_element, new_text)

        # Simulate pressing Enter to save the value
        actions = ActionChains(driver)
        actions.move_to_element(input_element).click()
        actions.send_keys(Keys.RETURN)
        actions.perform()
        time.sleep(0.5)


def update_input_value(driver, input_element, new_text):
    """
    Update the value of an input element in a Banner form using JavaScript only.
    :param driver: webdriver object
    :param input_element: the input element to update
    :param new_text: new text to enter into the input element
    :return: None
    """
    driver = _get_driver(driver)
    _switch_iframe(driver)

    element_type = driver.execute_script(
        "return arguments[0].parentElement.getAttribute('data-widget')",
        input_element
    )

    if element_type == 'checkbox':
        is_checked = driver.execute_script("return arguments[0].checked", input_element)
        should_check = new_text.lower() in ['true', 'checked']
        if is_checked != should_check:
            driver.execute_script("arguments[0].click()", input_element)
    else:
        # Use JavaScript to clear and set the input value, simulate pressing Enter, and wait for title attribute update
        driver.execute_script("""
            var inputElement = arguments[0];
            var newValue = arguments[1];

            // Clear the input value
            inputElement.value = '';

            // Function to simulate typing each character
            function simulateTyping(input, value) {
                input.value = value;
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
                input.blur();
            }

            // Function to simulate pressing Enter
            function simulateEnter(input) {
                var event = new KeyboardEvent('keydown', {
                    bubbles: true,
                    cancelable: true,
                    key: 'Enter',
                    code: 'Enter',
                    keyCode: 13
                });
                input.dispatchEvent(event);
            }

            // Set the new value and simulate typing and pressing Enter
            simulateTyping(inputElement, newValue);
            simulateEnter(inputElement);

            return new Promise(function(resolve, reject) {
                var maxAttempts = 50;  // maximum number of polling attempts
                var attempts = 0;
                var interval = setInterval(function() {
                    if (inputElement.title === newValue) {
                        clearInterval(interval);
                        resolve();
                    }
                    attempts++;
                    if (attempts >= maxAttempts) {
                        clearInterval(interval);
                        reject(new Error("Title attribute did not update"));
                    }
                }, 100);  // polling interval in milliseconds
            });
        """, input_element, new_text)

        # Wait for the promise to resolve
        driver.execute_async_script("""
            var callback = arguments[arguments.length - 1];
            var inputElement = arguments[0];
            var newValue = arguments[1];
            var maxAttempts = 50;
            var attempts = 0;
            var interval = setInterval(function() {
                if (inputElement.title === newValue) {
                    clearInterval(interval);
                    callback();
                }
                attempts++;
                if (attempts >= maxAttempts) {
                    clearInterval(interval);
                    callback(new Error("Title attribute did not update"));
                }
            }, 100);
        """, input_element, new_text)


def extract_input_values(driver):
    """
    Extract the values of all input elements in a Banner form.
    :param driver: webdriver object
    :return: dict of label text to a tuple (input element, input value)
    """
    script = """
    return (function() {
        function isVisible(element) {
            var style = window.getComputedStyle(element);
            return style && style.display !== 'none' && style.visibility !== 'hidden' && element.offsetWidth > 0 && element.offsetHeight > 0;
        }
        var divs = document.querySelectorAll('div[data-widget="textinput"], div[data-widget="datefield"], div[data-widget="checkbox"]');
        var data = {};
        var labelCount = {};
        divs.forEach(function(div) {
            if (isVisible(div)) {
                var label = div.querySelector(':scope > label');
                var input = div.querySelector(':scope > input');
                if (label && input) {
                    var labelText = label.innerText.trim();
                    if (labelCount[labelText] === undefined) {
                        labelCount[labelText] = 0;
                    }
                    labelCount[labelText]++;
                    var labelKey = labelText;
                    if (labelCount[labelText] > 1) {
                        labelKey = labelText + '_' + labelCount[labelText];
                    }
                    var inputValue;
                    if (div.getAttribute('data-widget') === 'checkbox') {
                        inputValue = input.checked ? 'checked' : 'unchecked';
                    } else {
                        inputValue = input.value;
                    }
                    data[labelKey] = {element: input, value: inputValue};
                }
            }
        });
        return data;
    })();
    """
    driver = _get_driver(driver)
    _switch_iframe(driver)
    result = driver.execute_script(script)
    return result


def switch_to_tab(driver: WebDriver | BannerDriver, tab_name: str, timeout=10) -> bool:
    """
    Switches to a tab in a Banner form.
    :param driver: webdriver object
    :param tab_name: tab name to switch to
    :param timeout: maximum time to wait for the tab to switch
    :return: true if the tab was switched to, false otherwise
    """
    script = f"""
    return (async function() {{
        function switchToTab(tabName) {{
            try {{
                var tabLists = document.querySelectorAll('ul[role="tablist"]');
                var tabList = null;
                for (var i = 0; i < tabLists.length; i++) {{
                    if (tabLists[i].offsetParent !== null) {{
                        tabList = tabLists[i];
                        break;
                    }}
                }}
                if (!tabList) return null;
    
                var tabs = tabList.getElementsByTagName('li');
                for (var i = 0; i < tabs.length; i++) {{
                    var anchor = tabs[i].querySelector('a.ui-tabs-anchor');
                    if (anchor && anchor.textContent.trim() === tabName) {{
                        anchor.click();
                        return anchor;
                    }}
                }}
                return null;
            }} catch (e) {{
                console.error('Error accessing tab content:', e);
                return null;
            }}
        }}
    
        var defaultTabName = '{tab_name}';
        var anchor = switchToTab(defaultTabName);
        if (!anchor) return false;

        var startTime = performance.now();
        while (performance.now() - startTime < {timeout} * 1000) {{
            if (anchor.getAttribute('aria-selected') === 'true') {{
                return true;
            }}
            await new Promise(resolve => setTimeout(resolve, 100));
        }}
        return false;
    }})();
    """
    driver = _get_driver(driver)
    _switch_iframe(driver)
    return driver.execute_script(script)


def save_changes(driver: WebDriver | BannerDriver) -> None:
    """
    Clicks the 'Save' button on a Banner form.
    :param driver: webdriver or BannerDriver object
    :return: None
    """
    try:
        driver = _get_driver(driver)
        _switch_iframe(driver)
        save_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "save-bt"))
        )
        save_button.click()
    except Exception as e:
        print(f"An error occurred: {e}")


def _get_driver(driver: WebDriver | BannerDriver) -> WebDriver:
    """
    Get the Selenium WebDriver object
    :return: webdriver object
    """
    if isinstance(driver, WebDriver):
        return driver
    return driver.get_driver()


def _switch_iframe(driver: WebDriver | BannerDriver, frame_id="bannerHS") -> None:
    """
    Switch to the iframe containing the Banner form
    :param driver: webdriver or BannerDriver object
    :param frame_id: ID of the iframe, default is 'bannerHS'
    :return: None
    """
    driver = _get_driver(driver)
    try:
        current_frame = driver.execute_script(
            "return window.frameElement ? "
            "window.frameElement.id : null;")
        if current_frame == frame_id:
            return
        iframe = driver.find_element(By.ID, frame_id)
        driver.switch_to.frame(iframe)
    except:
        driver.switch_to.default_content()
