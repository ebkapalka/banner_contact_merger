from bannerdriver.functions_general import extract_input_values, switch_to_tab, update_input_value
from bannerdriver.navigation import nav_to_form, enter_gid
from bannerdriver.drivers.driver_base import BannerDriver

from pprint import pprint
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
        nav_to_form(self, "SPAIDEN")
        enter_gid(self, self.gid)
        switch_to_tab(self, "Address")
        v = extract_input_values(self)
        pprint(v)
        # time.sleep(10)

        update_input_value(self, v["Street Line 1"]['element'], "this is some text")
        update_input_value(self, v["Street Line 2"]['element'], "this is some text")
        update_input_value(self, v["Street Line 3"]['element'], "this is some text")
        update_input_value(self, v["City"]['element'], "this is some text")
        update_input_value(self, v["State or Province"]['element'], "CA")
        # update_input_value(self, "ZIP or Postal Code", "12345")
        # update_input_value(self, "Area Code", "123")
        # update_input_value(self, "Phone Number", "4567890")
        # update_input_value(self, v["Address Verified"]['element'], "true")
        # update_input_value(self, "Address Type", "Mailing")
        update_input_value(self, v["From Date"]['element'], "01/22/1997")
        # update_input_value(self, "Nonexistent Field", "some text")
        # update_input_value(self, "Skip Address Verify", "some text")
        v = extract_input_values(self)
        print("Updated values")
        pprint(v)
        time.sleep(3000)

    # while True:
        #     # TODO: change database structure so this works
        #     command = self.queue.get_next_command(self.gid)
