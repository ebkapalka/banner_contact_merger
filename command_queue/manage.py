from sqlalchemy import create_engine
from datetime import datetime
import shutil
import glob
import os

from .sqlite_manager import SQLiteManager
from .models import Base


def create_database(db_path):
    """
    Create the database if it does not exist.
    :param db_path: path to the database file
    :return: None
    """
    if not os.path.exists(db_path):
        engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(engine)
    else:
        temp = SQLiteManager(f"sqlite:///{db_path}", "temp")
        temp.clean_commands()
        print(f"Database already exists at {db_path}")


def backup_database(db_path: str, backup_dir: str, max_backups=10):
    """
    Create a backup of the database.
    :param db_path: path to the database file
    :param backup_dir: path to the directory where the backups will be stored
    :param max_backups: maximum number of backups to keep
    :return: None
    """
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Create timestamp
    timestamp = generate_timestamp()
    backup_path = os.path.join(backup_dir, f'db_{timestamp}.sqlite')

    # perform backup
    shutil.copy2(db_path, backup_path)
    print(f"Backup created at {backup_path}")

    # remove old backups
    backups = glob.glob(os.path.join(backup_dir, 'db_*.sqlite'))
    backups.sort(key=lambda x: os.path.getmtime(x))
    while len(backups) > max_backups:
        os.remove(backups.pop(0))
        print("Removed an old backup.")


def generate_timestamp(date_time: datetime = None,
                       timestamp_format: str = "%Y%m%d%H%M%S") -> str:
    """
    Generate a timestamp in the specified format.
    :param date_time: datetime object
    :param timestamp_format: format for the timestamp
    :return: timestamp string
    """
    if not date_time:
        date_time = datetime.now()
    return date_time.strftime(timestamp_format)
