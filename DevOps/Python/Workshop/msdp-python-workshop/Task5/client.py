import psutil
import requests
import logging
import prometheus_client
import subprocess
import time
import contextlib


BUCLE_FILE = "./bucle.sh"

PROMETHEUS_PORT = 9999
UPDATE_PERIOD   = 3


def bucle_launch():
    """
    Step 1.1. Run bash script defined in `BUCLE_FILE` variable using subprocess to start an infinite loop process.
              The process has to run in the background, that means that your python script should continue running after
              you execute the bash file.

            As a result, you should have a running process with `BUCLE_FILE` in command line arguments.
        Memo:
            * use `subprocess.Popen()` to launch bash script
            * use `logging.*` to log message
    """
    ### Block implemented by student
    # log message regarding launching BUCLE_FILE
    # Execute bash file in the background: <subprocess call of `BUCLE_FILE`>
    ### Block implemented by student


def processes():
    # list to populate with the running processes information
    proc_objects = []
    # labels for the attributes that are going to be requested
    labels = ['pid', 'name', 'cmdline', 'cpu_times']

    """
    Step 1.2. Filter `python` and `bash` processes from the list of all the running processes.

        Follow the next steps:
            1. Use `psutil.process_iter(attrs=labels)` to get a list of all the processes running
            2. Iterate over the list of the running processes
            3. If it is `python` of `bash` process (check proc.info['name'] for strings like "python" and "bash"),
                 add `proc.info` to `proc_objects`.

        Note:
            * depending on OS (macOS or Linux) process names can:
                * start from capital letter
                * have python version (3, 3.7, 3.8) in the end

        As a result `proc_objects` list should contain dictionaries with `python` and `bash` processes running currently on the system.
    """
    ### Block implemented by student
    # for all running processes
        # when it is python or bash process
            # add process info to `proc_objects`
    ### Block implemented by student

    return proc_objects


def main():
    prometheus_client.start_http_server(PROMETHEUS_PORT)
    logging.info(f"Prometheus exporter started at http://127.0.0.1:{PROMETHEUS_PORT}")

    CPU_TIME = prometheus_client.Gauge('cpu_time',
                                       'Hold current process CPU consumption time',
                                       ['id', 'cmd'])

    for counter in range(10):
        """
        Step 1.3. Update Prometheus metrics in a loop

            Complete the next steps in the loop:
                1. For each process from the function implemented in step 1.2,
                    update `CPU_TIME` `Gauge` metric labeled with:
                        a) `id` formed by combining `proc['name']` and `proc['pid']` ("name_pid" format)
                        b) `cmd` formed by joining `proc['cmdline']` list values with " " (space) separator
                    with *sum* of `proc['cpu_times'].system` and `proc['cpu_times'].user` values
                2. Sleep for UPDATE_PERIOD
                3. Perform HTTP GET request to Prometheus endpoint and print its content to stdout.
        """
        for proc in processes():
            pass
            ### Block implemented by student
            # set labeled cpu times value in `CPU_TIME`
            ### Block implemented by student
        ### Block implemented by student
        # sleep for an `UPDATE_PERIOD`
        # log HTTP Get request result to Prometheus endpoint
        ### Block implemented by student

        """
        Step 2.2. Kill bucle process when counter equals to `6` using function implemented in step 2.1.
        """
        ### Block implemented by student
        # it it is the 6th iteration
            # use bucle_kill() function to kill the bucle processes
        ### Block implemented by student


def bucle_kill():
    for proc in psutil.process_iter(['cmdline']):
        cmdline = proc.info.get("cmdline")
        if cmdline is None:
            continue
        if BUCLE_FILE in cmdline:
            logging.info(f"Killing {proc}")
            try:
                proc.kill()
            except Exception:
                logging.exception(f"Failed to handle {proc}")


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(message)s',
    )
    logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)

    # disable default process metrics
    for name in list(prometheus_client.REGISTRY._names_to_collectors.values()):
        with contextlib.suppress(KeyError):
            prometheus_client.REGISTRY.unregister(name)

    bucle_launch()
    bucle_launch()

    main()

    bucle_kill()