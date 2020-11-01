import requests
import requests.auth
import base64
import hashlib
import csv
import gzip
import io
import logging


API_URL = "http://localhost:5000"
API_USERNAME = "username"
API_PASSWORD = "password"

REPORT_GET_ENDPOINT  = "/task1/report_get"
REPORT_POST_ENDPOINT = "/task1/report_post"


def main():
    """
    Step 1.1. Perform GET query to basic auth protected `REPORT_GET_ENDPOINT` on `API_URL` server.
              Username and password for authentication are defined in `API_USERNAME` and `API_PASSWORD` variables.

              As a result `response` should contain requests.Response Object.
    """
    ### Block implemented by student
    # response = "<requests.Response Object>"

    response = requests.get(API_URL + REPORT_GET_ENDPOINT, auth=requests.auth.HTTPBasicAuth(API_USERNAME, API_PASSWORD))

    ### Block implemented by student
    assert response.status_code == 200, f"Wrong API response '{response.status_code} / {response.reason}', check the code again"
    logging.info("GET request was performed successfully")

    """
    Step 1.2. Assign 'checksum' header value from `response` to `content_checksum` variable
    """
    ### Block implemented by student
    # content_checksum = "<'checksum' header value>"

    content_checksum = response.headers.get('checksum')
    # logging.info(f"response.header:{response.headers}")
    # logging.info(f"content_checksum:{content_checksum}")

    ### Block implemented by student
    assert content_checksum == hashlib.md5(response.content).hexdigest(), "Wrong content checksum, check the code again"
    logging.info("Content checksum is correct")

    """
    Step 1.3. Decode response content.

        As a result you should assign `content_gzip_decompressed_str`.

        The sequence should be following:
            1. Decode base64 content response
            2. Decompress gziped data with `gzip.decompress()`
            3. Convert bytes to str

        Memo:
            * content is gzip compressed and then base64 encoded
            * `base64.b64decode` accepts bytes and returns bytes
            * `gzip.decompress` accepts bytes and returns bytes
            * use `string.decode()` to convert bytes to str
    """
    ### Block implemented by student
    # content_base64_decoded_bytes = <decode response content from base64 to gziped bytes>
    # content_gzip_decompressed_bytes = <decompress gziped bytes to content bytes>
    # content_gzip_decompressed_str = <decode content bytes to a string>

    content_base64_decoded_bytes = base64.b64decode(response.content)
    # logging.debug(content_base64_decoded_bytes)
    content_gzip_decompressed_bytes = gzip.decompress(content_base64_decoded_bytes)
    # logging.debug(content_gzip_decompressed_bytes)
    content_gzip_decompressed_str = content_gzip_decompressed_bytes.decode()
    # logging.debug(content_gzip_decompressed_str)
    ### Block implemented by student

    assert isinstance(content_gzip_decompressed_str, str), "Wrong content type, check the code again"
    # logging.debug(f"Response content:\n{content_gzip_decompressed_str}")

    """
    Step 1.4. Parse response content as CSV data, find out required stats based on parsed data.

        As a result you should assign 2 below defined variables (data_*_value) with corresponding values:
            1.2. `data_percent_90_value` - the highest `90 Percent` value
            2.2. `data_fail_rate_value` - the highest fail rate (`Fail` / `Pass` ratio) value.

        The sequence should be following:
            1. Create a CSV DictReader from `io.StringIO` object
            2. Read CSV line by line
            3. If `90 Percent` value is greater than current `data_percent_90_value`:
                * assign new `90 Percent` value to `data_percent_90_value` variable
            4. If `Fail` / `Pass` ratio is greater than current `data_fail_rate_value`:
                * assign new `Fail` / `Pass` ratio to `data_fail_rate_value` variable

        Memo:
            * In order to avoid storing content in temporary file `io.StringIO` is used as in-memory buffer
            * `csv.DictReader` accepts string, that's why use `io.StringIO`, not `io.BytesIO`
            * all values from CSV are string, use `float()` before performing any divisions/subtractions/comparisons
    """
    # value with the highest "90 Percent" average time
    data_percent_90_value = 0

    # value with the highest fail rate (`Fail` / `Pass` ratio)
    data_fail_rate_value = 0

    with io.StringIO(content_gzip_decompressed_str) as csv_handler:
        pass
        ### Block implemented by student
        # csv_reader = <create csv dict reader from StringIO object>
        # print column names

        csv_reader = csv.DictReader(csv_handler)
        # logging.info(csv_reader.fieldnames)
        # for each row from csv reader
        for indx, row in enumerate(csv_reader):
            # logging.debug(row['90 Percent'])
            p90 = float(row['90 Percent'])
            if p90 > data_percent_90_value:
                data_percent_90_value = p90

                fail_rate = float(row['Fail'])
                pass_rate = float(row['Pass'])
                rate = fail_rate / pass_rate

                if rate > data_fail_rate_value:
                    data_fail_rate_value = rate

        # logging.debug(f"{indx+1} lines")
            # get "90 Percent" value
            # if it is greater than current `data_percent_90_value`
                # store new "90 Percent" value

            # get ("Fail" / "Pass") value
            # if it is greater than current `data_fail_rate_value`
                # store new ("Fail" / "Pass") value

        # print how many lines were processed from csv reader
        ### Block implemented by student

    """
    Step 1.5. Round each data_*_value to 2 precision after the decimal point, using round() build-in function
    """
    ### Block implemented by student
    # data_percent_90_value = <...>
    # data_fail_rate_value = <...>
    data_percent_90_value = round(data_percent_90_value, 2)
    data_fail_rate_value = round(data_fail_rate_value, 2)
    ### Block implemented by student

    logging.info(f"The highest 90 percent average time is {data_percent_90_value}")
    logging.info(f"The highest fail rate is {data_fail_rate_value}")

    fieldnames = ['N', 'Value']
    """
    Step 2. Generate in-memory CSV report using `csv.DictWriter` with fieldnames defined above.

        Memo:
            * CSV report should have header with field names
            * CSV columns:
                * 'N' - sequence number, starting from 1
                * 'Value' - data_*_value value
            * CSV rows order:
                1. `90 Percent`
                2. `Fail` / `Pass` ratio
            * Each write to `io.StringIO` object moves stream position to the end of stream, so:
                * Use `seek(0)` method to move stream position to the beginning
                * Use `read()` method to get CSV content as string
                * Use `encode()` method to convert string to bytes

        As a result you should get binary CSV report in `content` variable.
    """
    ### Block implemented by student
    # start with empty StringIO in a context manager
    with io.StringIO() as csv_handler:
        writer = csv.DictWriter(csv_handler, fieldnames=fieldnames)

        # create StringIO csv dict writer with field names from `fieldnames`

        # write header
        writer.writeheader()

        # write two rows:
        #   1. the highest `90 Percent` value
        #   2. the highest `Fail`/`Pass` value
        writer.writerow({'N': '1', 'Value': data_percent_90_value})
        writer.writerow({'N': '2', 'Value': data_fail_rate_value})
        
        csv_handler.seek(0)
        # seek to 0 position in StringIO
        # content = <csv_handler content encoded to bytes>
        content = csv_handler.read().encode()
        # logging.debug(content)

    ### Block implemented by student

    logging.info(f"Generated report:\n{content.decode()}")

    """
    Step 3. Perform POST query to basic auth protected REPORT_POST_ENDPOINT on API_URL server.
            Username and password for authentication are defined in `API_USERNAME` and `API_PASSWORD` variables.
            Send gzip compressed and then base64 encoded `content` as data.

            As a result `response` should contain requests.Response Object.
    """
    ### Block implemented by student
    # response_post = "<requests.Response Object>"
    response_post = requests.post(
        API_URL + REPORT_POST_ENDPOINT, 
        auth=requests.auth.HTTPBasicAuth(API_USERNAME, API_PASSWORD),
        data=base64.b64encode(gzip.compress(content)))

    ### Block implemented by student
    assert response_post.status_code == 200, f"Wrong API response '{response.status_code} / {response.reason}', check the code again"
    logging.info("API check passed, you are good")


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(message)s',
    )
    logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)

    main()
