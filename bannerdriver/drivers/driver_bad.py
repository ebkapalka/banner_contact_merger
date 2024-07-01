from bannerdriver.drivers.driver_base import BannerDriver

import time


class BadDriver(BannerDriver):
    """
    Driver to process the bad record
    """
    def main_loop(self) -> None:
        """
        Loop used for adding data to the bad record
        :return: None
        """
        driver = self.get_driver()
        while True:
            print("Bad")
            time.sleep(1)
