from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver


class BannerDriver:
    def __init__(self, username: str, password: str, env="prod", timeout=10):
        self.username = username
        self.password = password
        self.env = env
        self.timeout = timeout
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = None

        self._nav_to_login()
        self._enter_credentials()
        self._handle_2fa()

    def get_driver(self) -> webdriver:
        """
        Get the Selenium WebDriver object
        :return: webdriver object
        """
        return self.driver

    def _nav_to_login(self):
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(f"https://{self.env}banner.montana.edu/"
                        "applicationNavigator/seamless")
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located((By.ID, "username")))
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located((By.ID, "password")))

    def _enter_credentials(self):
        """
        Enter the username and password into the login form
        :return: None
        """

        def _identify_error() -> str:
            """
            Identify any error message
            :return: text of the error message
            """
            try:
                login_form = WebDriverWait(self.driver, 1).until(
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
        input_username = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located((By.ID, "username")))
        input_password = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located((By.ID, "password")))
        button_submit = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='_eventId_proceed']")))
        input_username.send_keys(self.username)
        input_password.send_keys(self.password)
        button_submit.click()

        if e := _identify_error():
            print(f"Error: {e}")
            self.driver.quit()
        WebDriverWait(self.driver, self.timeout).until(
            EC.title_is("Two-Factor Authentication"))

    def _handle_2fa(self, method="push"):
        """
        Handle the 2FA process
        :param method: "push", "sms", or "call"
        :return: None
        """
        WebDriverWait(self.driver, self.timeout).until(
            EC.title_is("Two-Factor Authentication"))
        if method == "push":
            print("Please accept the push notification on your phone")
            xpath = "//button[text()='Send Me a Push ']"
            button = WebDriverWait(self.driver, 300).until(
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
        WebDriverWait(self.driver, self.timeout).until(
            EC.title_is("Application Navigator"))
        print("Successfully logged in")


# grdSortest
