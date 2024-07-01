from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

from bannerdriver.functions_login import enter_credentials, handle_2fa, nav_to_login
from command_queue.sqlite import SQLiteManager


class BannerDriver:
    def __init__(self, username: str, password: str,
                 queue: SQLiteManager, env="prod", timeout=10):
        self.username = username
        self.password = password
        self.queue = queue
        self.env = env
        self.timeout = timeout
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = None

        nav_to_login(self)
        enter_credentials(self)
        handle_2fa(self)

    def get_driver(self) -> webdriver:
        """
        Get the Selenium WebDriver object
        :return: webdriver object
        """
        if not self.driver:
            self.driver = webdriver.Chrome(
                options=self.options)
        return self.driver


# grdSortest
