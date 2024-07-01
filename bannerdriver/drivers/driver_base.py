from abc import ABC, abstractmethod
from selenium import webdriver

from bannerdriver.functions_login import enter_credentials, handle_2fa, nav_to_login
from command_queue.sqlite import SQLiteManager


class BannerDriver(ABC):
    def __init__(self, username: str, password: str, name: str,
                 queue: SQLiteManager, env="prod", timeout=10):
        self.username = username
        self.password = password
        self.name = name
        self.queue = queue
        self.env = env
        self.timeout = timeout
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('--headless')
        self.driver = None

        nav_to_login(self, timeout=300)
        enter_credentials(self, timeout=300)
        handle_2fa(self, timeout=300)

    def get_driver(self) -> webdriver:
        """
        Get the Selenium WebDriver object
        :return: webdriver object
        """
        if not self.driver:
            self.driver = webdriver.Chrome(
                options=self.options)
        return self.driver

    @abstractmethod
    def main_loop(self) -> None:
        """
        Main loop for the BannerDriver
        :return: None
        """
        pass
