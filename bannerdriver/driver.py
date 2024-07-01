from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

from bannerdriver.functions import enter_credentials, handle_2fa


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
        enter_credentials(self)
        handle_2fa()

    def get_driver(self) -> webdriver:
        """
        Get the Selenium WebDriver object
        :return: webdriver object
        """
        if not self.driver:
            self.driver = webdriver.Chrome(
                options=self.options)
        return self.driver

    def _nav_to_login(self):
        driver = self.get_driver()
        driver.get(f"https://{self.env}banner.montana.edu/"
                        "applicationNavigator/seamless")
        WebDriverWait(driver, self.timeout).until(
            EC.visibility_of_element_located((By.ID, "username")))
        WebDriverWait(driver, self.timeout).until(
            EC.visibility_of_element_located((By.ID, "password")))
# grdSortest
