from command_queue.sqlite import SQLiteManager
from bannerdriver.driver import BannerDriver

import threading
import os


def create_and_run_driver(name: str, db_uri: str):
    """
    Create and run a BannerDriver instance
    :param name: Name of the worker
    :param db_uri: URI of the SQLite database
    :return: None
    """
    queue = SQLiteManager(db_uri, name)
    banner_username = os.environ.get("BANNER_USERNAME")
    banner_password = os.environ.get("BANNER_PASSWORD")
    BannerDriver(banner_username, banner_password, name, queue)


if __name__ == '__main__':
    queue_db = "sqlite:///command_queue/db.sqlite"
    name_good = "worker_good"
    name_bad = "worker_bad"

    thread_good = threading.Thread(target=create_and_run_driver, args=(name_good, queue_db))
    thread_bad = threading.Thread(target=create_and_run_driver, args=(name_bad, queue_db))
    thread_good.start()
    thread_bad.start()
    thread_good.join()
    thread_bad.join()
