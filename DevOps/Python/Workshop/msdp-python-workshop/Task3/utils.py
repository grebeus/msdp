import os
import tempfile
import shutil
import logging
import yaml


from datetime import datetime
from datetime import timedelta


def seed(suffix=None, prefix=None):
    root_dir = tempfile.mkdtemp(suffix, prefix)
    now = datetime.utcnow()

    logging.debug(f"seeding '{root_dir}'")
    for delta in range(0, 100):
        """
        Step 1. Construct `daily_dir` based on `now` (datetime object with current date) and `delta` (increment).
                Memo:
                    * `datetime` and `timedelta` objects support math operations
                    * `datetime` object has `strftime` method to convert object to string representation
                    * you can get `date` object from `datetime` object with `date()` method
                    * `date` object has `isoformat()` method to get properly fromatted string representation
                As a result:
                    * in `daily_dir` there should be a string like "2020-09-01"
                    * date in that string should be decreased by one day on each iteration
        """
        ### Block implemented by student
        # daily_dir = <difference between `now` and `timedelta` with "delta" days, converted to string "YYYY-MM-DD">
        ### Block implemented by student
        new_dir = os.path.join(root_dir, daily_dir)
        os.makedirs(new_dir)
        logging.debug(f"creating '{new_dir}'")

    return root_dir


def cleanup(dir):
    logging.debug(f"removing '{dir}'")
    shutil.rmtree(dir)


class Config(object):
    def __init__(self, config_file):
        self.config_file = config_file
        """
        Step 3.1.1. Read and parse yaml from `self.config_file` to `self.cfg` as Python dictionary
        """
        ### Block implemented by student
        # self.cfg = <dict constructed from yaml, loaded from `self.config_file`>
        ### Block implemented by student

    @property
    def verbose(self):
        """
        Step 3.1.2. Return value of `verbose` key from `self.cfg`. It is is not present, return False.
        """
        ### Block implemented by student
        # return <>
        ### Block implemented by student

    @property
    def monthly(self):
        """
        Step 3.1.3. Return value of `monthly` key located in `retention` dict from `self.cfg`. It is is not present, return 0.
        """
        ### Block implemented by student
        # return <>
        ### Block implemented by student

    @property
    def weekly(self):
        """
        Step 3.1.4. Return value of `weekly` key located in `retention` dict from `self.cfg`. It is is not present, return 0.
        """
        ### Block implemented by student
        # return <>
        ### Block implemented by student

    @property
    def daily(self):
        """
        Step 3.1.5. Return value of `daily` key located in `retention` dict from `self.cfg`. It is is not present, return 0.
        """
        ### Block implemented by student
        # return <>
        ### Block implemented by student
