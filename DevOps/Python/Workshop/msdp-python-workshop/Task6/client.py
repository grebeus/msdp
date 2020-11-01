import logging
import utils


from hsm import HSM


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(message)s',
    )

    hsm = HSM()

    """
    Step 2.2. Monkey patch HSM.encrypt() method to measure encryption time with decorator
              implemented in utils module
    """
    ### Block implemented by student
    ### Block implemented by student

    for fruit in utils.tokens():
        logging.debug(f"'{fruit}' encrypted is '{hsm.encrypt(fruit).decode('ascii')}'\n")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(message)s',
    )

    main()