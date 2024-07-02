from bannerdriver.functions_general import extract_input_values, switch_to_tab
from bannerdriver.navigation import nav_to_form, enter_gid
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
        nav_to_form(self, "SPAIDEN")
        enter_gid(self, self.gid)
        switch_to_tab(self, "Address")
        v = extract_input_values(self)
        print(v)
        time.sleep(300)

    # while True:
        #     # TODO: change database structure so this works
        #     command = self.queue.get_next_command(self.gid)
