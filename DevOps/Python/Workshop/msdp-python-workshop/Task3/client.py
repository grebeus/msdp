import logging
import utils
import os
import shutil
import argparse


from datetime import datetime


def main():
    """
    Step 4. Add "--config" command-line argument support using `argparse` module and leverage it for config parsing
    """
    ### Block implemented by student
    # parser = <argparse.ArgumentParser class instance>
    # <add `--config` argument support>

    # args = <parse supplied cmd arguments>
    ### Block implemented by student

    """
    Step 3.2. Use `Config` class from `utils` module to parse yaml config to Python object
    """
    ### Block implemented by student
    #cfg = <utils.Config class instance with hardcoded "config.yaml" config value>
    ### Block implemented by student

    """
    Step 3.4. Set logging level to `DEBUG` if verbose param is set to True, set it to `INFO` otherwise
    """
    logging.basicConfig(
        ### Block implemented by student
        #level=<condition based on `verbose` config param>,
        ### Block implemented by student
        level=logging.DEBUG,
        format='%(message)s',
    )

    root_dir = utils.seed(prefix="task2-")
    logging.debug(root_dir)

    # list with the monthly (created at the 1st day of the month) directories
    monthly = []
    # list with the weekly (created on Sundays) directories
    weekly = []
    # list with all other directories
    daily = []

    """
    Step 2.1. Put list with `root_dir` contents into `dirs` variable
    """
    ### Block implemented by student
    #dirs = <list root_dir>
    dirs = os.listdir(path=root_dir)

    ### Block implemented by student
    for dir_name in dirs:
        """
        Step 2.2. Sort directories by monthly, weekly and daily categories.
                  Memo:
                    * `datetime` class has `strptime` method to convert string to datetime object
                    * `datetime` object has properties and methods to get day and weekday:
        """
        ### Block implemented by student
        # dir_date = <convert string to datetime objects>
        #if <check if it is the 1st day of the month>:
            # append `dir_name` to `monthly` list
        #elif <check if it is Sunday>:
            # append `dir_name` to `weekly` list
        # otherwise
            # append `dir_name` to `daily` list
        ### Block implemented by student

    """
    Step 2.3. Remove from `dirs` list all the directories we want to keep.
              Memo:
                * sorting of monthly, weekly and daily lists will put directories in ascending order
                * the fastest way to filter list (to keep only directories you want to remove) is slicing (negative should do the trick in that case)
    """
    ### Block implemented by student
    #for dir in <monthly list slice with 2 the most recent dirs removed>:
        logging.debug(f"keeping monthly {dir}")
        dirs.remove(dir)
    #for dir in <weekly list slice with 4 the most recent dirs removed>:
        logging.debug(f"keeping weekly {dir}")
        dirs.remove(dir)
    #for dir in <daily list slice with 5 the most recent dirs removed>:
        logging.debug(f"keeping daily {dir}")
        dirs.remove(dir)
    ### Block implemented by student

    for dir in dirs:
        logging.debug(f"removing {dir}")
        shutil.rmtree(
            os.path.join(root_dir, dir)
        )

    utils.cleanup(root_dir)

if __name__ == "__main__":
    main()