from command_queue.sqlite import SQLiteManager
from bannerdriver.driver import BannerDriver

import os


if __name__ == '__main__':
    banner_username = os.environ.get("BANNER_USERNAME")
    banner_password = os.environ.get("BANNER_PASSWORD")

    queue_db = "sqlite:///command_queue/db.sqlite"
    queue_good = SQLiteManager(queue_db, "worker_good")
    queue_bad = SQLiteManager(queue_db, "worker_bad")
    driver_good = BannerDriver(banner_username, banner_password, queue_good)
    driver_bad = BannerDriver(banner_username, banner_password, queue_bad)
