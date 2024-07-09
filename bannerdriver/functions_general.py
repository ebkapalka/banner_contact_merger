from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
import time

from bannerdriver.drivers.driver_base import BannerDriver


def update_input_value_legacy(driver: WebDriver | BannerDriver, input_element: WebElement, new_text: str):
    """
    Update the value of an input element in a Banner form.
    :param driver: webdriver object
    :param input_element: the input element to update
    :param new_text: new text to enter into the input element
    :return: None
    """
    driver = get_driver(driver)
    switch_iframe(driver)
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


def update_input_value(driver: WebDriver | BannerDriver, input_element: WebElement, new_text: str):
    """
    Update the value of an input element in a Banner form using JavaScript only.
    :param driver: webdriver object
    :param input_element: the input element to update
    :param new_text: new text to enter into the input element
    :return: None
    """
    driver = get_driver(driver)
    switch_iframe(driver)
    element_type = driver.execute_script(
        "return arguments[0].parentElement.getAttribute('data-widget')",
        input_element
    )

    if element_type == 'checkbox':
        should_check = new_text.lower() in ['true', 'checked']
        driver.execute_script("""
            var inputElement = arguments[0];
            var shouldCheck = arguments[1];
            var maxAttempts = 100;

            function updateCheckbox() {
                var isChecked = inputElement.getAttribute('aria-checked') === 'true';
                if (isChecked !== shouldCheck && maxAttempts > 0) {
                    inputElement.click();
                    maxAttempts--;
                    setTimeout(updateCheckbox, 100);
                } else if (maxAttempts === 0) {
                    console.error("Checkbox state did not update after 100 attempts");
                }
            }

            updateCheckbox();
        """, input_element, should_check)
    else:
        driver.execute_script("""
            var inputElement = arguments[0];
            var newValue = arguments[1];
            var maxAttempts = 100;

            function updateInput() {
                // Clear the input value
                inputElement.value = '';

                // Set the new value
                inputElement.value = newValue;

                // Trigger the input and change events
                inputElement.dispatchEvent(new Event('input', { bubbles: true }));
                inputElement.dispatchEvent(new Event('change', { bubbles: true }));

                // Function to simulate pressing Enter
                var event = new KeyboardEvent('keydown', {
                    bubbles: true,
                    cancelable: true,
                    key: 'Enter',
                    code: 'Enter',
                    keyCode: 13
                });
                inputElement.dispatchEvent(event);

                // Check if the title attribute matches the new value
                if (inputElement.title !== newValue && maxAttempts > 0) {
                    maxAttempts--;
                    setTimeout(updateInput, 100);  // Retry after 100ms
                } else if (maxAttempts === 0) {
                    console.error("Title attribute did not update after 100 attempts");
                }
            }

            updateInput();
        """, input_element, new_text)


def extract_input_values(driver: WebDriver | BannerDriver) -> dict[str, tuple[WebElement, str]]:
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
                var button = div.querySelector(':scope > button');
                if (label && (input || button)) {
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
                        data[labelKey] = {element: button, value: inputValue};
                    } else {
                        inputValue = input.value;
                        data[labelKey] = {element: input, value: inputValue};
                    }
                }
            }
        });
        return data;
    })();
    """
    driver = get_driver(driver)
    switch_iframe(driver)
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
    driver = get_driver(driver)
    switch_iframe(driver)
    return driver.execute_script(script)


def save_changes(driver: WebDriver | BannerDriver) -> None:
    """
    Clicks the 'Save' button on a Banner form.
    :param driver: webdriver or BannerDriver object
    :return: None
    """
    try:
        driver = get_driver(driver)
        switch_iframe(driver)
        save_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "save-bt"))
        )
        save_button.click()
    except Exception as e:
        print(f"An error occurred: {e}")


def get_driver(driver: WebDriver | BannerDriver) -> WebDriver:
    """
    Get the Selenium WebDriver object
    :return: webdriver object
    """
    if isinstance(driver, WebDriver):
        return driver
    return driver.get_driver()


def switch_iframe(driver: WebDriver | BannerDriver, frame_id="bannerHS") -> None:
    """
    Switch to the iframe containing the Banner form
    :param driver: webdriver or BannerDriver object
    :param frame_id: ID of the iframe, default is 'bannerHS'
    :return: None
    """
    driver = get_driver(driver)
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
