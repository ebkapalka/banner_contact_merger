from bannerdriver.drivers.driver_good import GoodDriver
from bannerdriver.drivers.driver_bad import BadDriver
from command_queue.sqlite import SQLiteManager

import multiprocessing
import os


def start_good_worker(username: str, password: str, db_uri: str, gid: str, env: str) -> None:
    """
    Start the worker to process the good gid record
    :param username: username for Banner login
    :param password: password for Banner login
    :param db_uri: uri for the command queue database
    :param gid: GID of the good student record
    :param env: 'prod' or 'test', depending on the environment
    :return: None
    """
    queue = SQLiteManager(db_uri, worker_name="good")
    worker = GoodDriver(username, password, queue, gid, env)
    worker.main_loop()


def start_bad_worker(username: str, password: str, db_uri: str, gid: str, env: str) -> None:
    """
    Start the worker to process the bad gid record
    :param username: username for Banner login
    :param password: password for Banner login
    :param db_uri: uri for the command queue database
    :param gid: GID of the bad student record
    :param env: 'prod' or 'test', depending on the environment
    :return: None
    """
    queue = SQLiteManager(db_uri, worker_name="bad")
    worker = BadDriver(username, password, queue, gid, env)
    worker.main_loop()


if __name__ == '__main__':
    good_gid = '-02179809'
    bad_gid = '-02179899'
    queue_db_uri = "sqlite:///command_queue/db.sqlite"
    environment = os.environ.get("BANNER_ENV", 'prod')
    banner_username = os.environ.get("BANNER_USERNAME")
    banner_password = os.environ.get("BANNER_PASSWORD")

    good_process = multiprocessing.Process(target=start_good_worker,
                                           args=(banner_username,
                                                 banner_password,
                                                 queue_db_uri,
                                                 good_gid,
                                                 environment))
    bad_process = multiprocessing.Process(target=start_bad_worker,
                                          args=(banner_username,
                                                banner_password,
                                                queue_db_uri,
                                                bad_gid,
                                                environment))
    good_process.start()
    bad_process.start()
    good_process.join()
    bad_process.join()
