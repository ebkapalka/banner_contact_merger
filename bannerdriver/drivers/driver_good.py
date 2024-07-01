from bannerdriver.drivers.driver_base import BannerDriver

import time


class GoodDriver(BannerDriver):
    """
    Driver to process the good record
    """
    def main_loop(self) -> None:
        """
        Loop used for adding data to the good record
        :return: None
        """
        driver = self.get_driver()
        while True:
            # TODO: change database structure so this works
            command = self.queue.get_next_command(self.gid)
