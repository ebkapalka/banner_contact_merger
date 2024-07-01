from bannerdriver.drivers.driver_base import BannerDriver


class GoodDriver(BannerDriver):
    def main_loop(self) -> None:
        """
        Loop used for adding data to the good record
        :return: None
        """
        driver = self.get_driver()
        while True:
            # Do something
            pass
