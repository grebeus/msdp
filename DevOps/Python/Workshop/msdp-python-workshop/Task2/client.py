import re
import requests
import sys
import logging


INPUT_FILE = "access.log"

API_URL = "http://localhost:5000"
TEST_ENDPOINT = "/task3/test"
BYTES_SERVED_CHECK_ENDPOINT = "/task3/check_bytes_served"
FAILED_RATE_CHECK_ENDPOINT = "/task3/check_failed_rate"


def main():
    # total number of bytes served from the log file
    bytes_served = 0
    # all the status codes from the log file
    status_codes = []

    """
    Step 1.1. Put your compiled regexp for status code and bytes getting into `status_regexp_pattern` variable
    """
    ### Block implemented by student
    # status_regexp_pattern = re.compile(<your regexp for status code and bytes served parsing>)
    status_regexp_pattern = re.compile("HTTP.+\" (?P<status_code>\d+) (?P<bytes>\d+) ")
    ### Block implemented by student
    with open(INPUT_FILE, "r") as logs:
        for line in logs:
            match = status_regexp_pattern.search(line)
            if match:
                status_codes.append(int(match.group("status_code")))
                bytes_served += int(match.group("bytes"))
            else:
                logging.warning("Not matched")

    """
        Step 1.2. Read and parse log records:
            * read `INPUT_FILE` line by line in context manager
            * test `status_regexp_pattern` on each line
            * if there is match with `status_regexp`:
                * add parsed `status_code` value to `status_codes` list
                * add parsed `bytes` value to `bytes_served` accumulator (int)
            * the code should raise warning (using logging.warning) if line is not matched with the regexp

            TODO: add samples for:
                * re.search + group()
    """
    ### Block implemented by student
    # open `INPUT_FILE` in context manager
        # for each line in input file
            # search for status_regexp_pattern in line
            # if there is match
                # append matched status code (converted to int) to `status_codes` list
                # increment `bytes_served` variable by value of bytes from current line
            # otherwise
                # print warning that line was not matched
    ### Block implemented by student

    logging.info(f"Bytes served: {bytes_served}")

    """
        Step 2.1. Calculate number of:
            * failed status codes (from 400 to 599, inclusive)
            * succeed status codes (all other)
    """
    failed_codes_count = 0
    succeed_codes_count = 0
    ### Block implemented by student
    # iterate over status_codes
        # when status code is in [400, 599] interval
            # increment failed_codes_count
        # otherwise
            # increment succeed_codes_count
    ### Block implemented by student

    for status_code in status_codes:
        if status_code >= 400 and status_code <600:
            failed_codes_count += 1
        else:
            succeed_codes_count += 1

    try:
        """
            Step 2.2. Calculate failed requests rate - what is the percentage of failed requests in the total (failed + succeed) requests number.
        """
        ### Block implemented by student
        #failed_rate = int(<your percentage formula>)+
        failed_rate = failed_codes_count / (failed_codes_count + succeed_codes_count)
        ### Block implemented by student
    except ZeroDivisionError:
        logging.error("Failed rate calculation failed, check the code again")
        sys.exit(1)
    logging.info(f"Failed rate: {failed_rate}%")

    assert api_check(TEST_ENDPOINT, {"it": "works"}) == 200, "Wrong API response, check api_check() code"
    """
        Step 3.2. Validate bytes served, using previously implemented `api_check()` with two arguments:
            1) endpoint, defined in `BYTES_SERVED_CHECK_ENDPOINT`
            2) payload, dict - {"bytes_served": <value from `bytes_served` variable>}
    """
    ### Block implemented by student
    # response_code = <your api_check() call>
    response_code = api_check(BYTES_SERVED_CHECK_ENDPOINT, {"bytes_served": bytes_served})

    ### Block implemented by student
    assert response_code == 200, "Bytes served value is wrong, check the code again"

    """
        Step 3.3. Validate failed requests rate, using previously implemented `api_check()` with two arguments:
            1) endpoint, defined in `FAILED_RATE_CHECK_ENDPOINT`
            2) payload, dict - {"failed_rate": <value from `failed_rate` variable>}
    """
    ### Block implemented by student
    # response_code = <your api_check() call>
    ### Block implemented by student
    assert response_code == 200, "Failed rate value is wrong, check the code again"

    logging.info("All API checks passed, you are good")


def api_check(endpoint, payload):
    """
    Step 3.1. Add requests post call in order to validate `payload` data at `endpoint` of `API_URL`.
              It should return integer with API returned status code.
    """
    pass
    ### Block implemented by student
    # response = <POST request to API endpoint with `payload` in data>
    # return <response HTTP code>
    response = requests.post(API_URL + endpoint, data=payload)
    return response.status_code

    ### Block implemented by student


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(message)s',
    )
    logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)

    main()
