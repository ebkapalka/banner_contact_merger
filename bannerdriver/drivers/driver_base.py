from abc import ABC, abstractmethod
from selenium import webdriver

from bannerdriver.functions_login import enter_credentials, handle_2fa, nav_to_login
from command_queue.sqlite import SQLiteManager


class BannerDriver(ABC):
    def __init__(self, username: str, password: str,
                 queue: SQLiteManager, gid: str, env="prod",
                 timeout=10):
        self.username = username
        self.password = password
        self.queue = queue
        self.gid = gid
        self.env = env
        self.timeout = timeout

        # disable autofill prompt
        self.options = webdriver.ChromeOptions()
        prefs = {
            'profile.default_content_setting_values.automatic_downloads': 1,
            'profile.password_manager_enabled': False,
            'credentials_enable_service': False,
            'autofill.profile_enabled': False,
        }
        self.options.add_experimental_option('prefs', prefs)
        self.options.add_argument("--disable-save-password-bubble")
        self.options.add_argument("--disable-autofill-keyboard-accessory-view")
        self.options.add_argument("--disable-prompt-on-repost")
        self.options.add_argument("--disable-autofill")

        # initialize the driver and log in
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
