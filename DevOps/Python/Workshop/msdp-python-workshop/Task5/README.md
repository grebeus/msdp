# Task 5 (working with processes and exporting metrics in Prometheus format)

* [Theory](#theory)
    * [Psutil](#psutil)
        * [Process class](#process-class)
        * [Iterate over the list of the processes](#iterate-over-the-list-of-the-processes)
    * [Prometheus](#prometheus)
        * [Metrics format](#metrics-format)
        * [Client library](#client-library)
* [Narrative](#narrative)
* [Guide](#guide)
    * [Prerequisites](#prerequisites)
    * [Step 1 (simulate CPU workload and export metrics)](#step-1-simulate-cpu-workload-and-export-metrics)
    * [Step 2 (kill process)](#step-2-kill-process)
    * [Step 3 (evaluate results)](#step-3-evaluate-results)

## Theory

### Psutil

psutil (python system and process utilities) is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python.

It is useful mainly for:
* system monitoring
* limiting process resources
* the management of running processes.

#### Process class

`psutil.Process(pid=None)` class represents particular OS process. Class instance can be created by specifying process PID in the constructor arguments:
```
>>> proc = psutil.Process( os.getpid() )
>>> proc
psutil.Process(pid=18171, name='Python', status='running', started='21:46:44')
```

All the process information can be obtained using this class instance as well as it can be used for variety of actions on the process:
```
>>> list(proc.environ().keys())[:3]
['TERM_SESSION_ID', 'SSH_AUTH_SOCK', 'LC_TERMINAL_VERSION']

>>> proc.exe()
'/usr/local/Cellar/python@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/Resources/Python.app/Contents/MacOS/Python'

>>> proc.cwd()
'/Users/oleg/Library/Mobile Documents/com~apple~CloudDocs/projects/epam/msdp/msdp-python-workshop/Task5'

>>> proc.username()
'oleg'

>>> proc.cpu_times()
pcputimes(user=0.068518784, system=0.038996296, children_user=0.0, children_system=0.0)

>>> proc.kill()
[1]    18171 killed     python3
```

#### Iterate over the list of the processes

Use `psutil.process_iter(attrs=None)` to iterate over running processes, it yields a `psutil.Process` class instance for all running processes on the local machine.

Note:
* to speed up process info retrieval the list of `attrs` should be specified with needed attributes, in this case result will be stored as a `info` attribute attached to the returned Process instances:
```
>>> for proc in psutil.process_iter(attrs=['pid', 'name']):
        print(proc.info)
{'pid': 97289, 'name': 'docker-machine-d'}
{'pid': 97290, 'name': 'docker-machine-d'}
{'pid': 97291, 'name': 'kubectl'}
{'pid': 98548, 'name': 'Google Chrome'}
{'pid': 98603, 'name': 'Safari'}
{'pid': 97289, 'name': 'docker-machine-d'}
```

* some of attributes might be `None`, take that into account if you're planning to use them later in calculations:
```
>>> len([ 1 for proc in psutil.process_iter(attrs=['name', 'cpu_times']) if proc.info['cpu_times'] is None ])
202
>>> len([ 1 for proc in psutil.process_iter(attrs=['name', 'cpu_times']) if proc.info['cpu_times'] is not None ])
385
```

* depending on operation system (Linux of macOS), process names and actually executed binaries might have different values:
```
>>> """ macOS """
>>> [proc.info for proc in psutil.process_iter(attrs=['name', 'cmdline']) if "ython" in proc.info['name']]
[{'cmdline': ['/usr/local/Cellar/python@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/Resources/Python.app/Contents/MacOS/Python'], 'name': 'Python'}]

>>> """ Linux """
>>> [proc.info for proc in psutil.process_iter(attrs=['name', 'cmdline']) if "ython" in proc.info['name']]
[{'name': 'python3', 'cmdline': ['python3']}]
```

### Prometheus

#### Metrics format

Prometheus is one of the foundations of the cloud-native environment. It has become the de-facto standard for visibility in microservices environments.

Prometheus collects metrics from monitored targets by scraping metrics HTTP endpoints on these targets. Prometheus metrics should be exported using text-based, line-oriented format:
* lines are separated by a line feed character (`\n`)
* the last line must end with a line feed character
* empty lines are ignored.

A metric is composed by several fields:
* metric name
* any number of labels (can be 0), represented as a key-value array
* current metric value
* optional metric timestamp.

It can be as simple as:
```
cpu_time 1.4231235
```

or, can include all the mentioned components:
```
# HELP cpu_time Hold current process CPU consumption time
# TYPE cpu_time gauge
# This line should not be parsed by Prometheus
cpu_time{cmd="bash ./bucle.sh",id="bash_15947"}  17.608653552   1600716142000
```

Metric output is typically preceded with `# HELP` and `# TYPE` metadata lines. The `# HELP` string identifies the metric name and a brief description of it. The `# TYPE` string identifies the type of metric. If there’s no `# TYPE` before a metric, the metric is set to untyped. Everything else that starts with a # is parsed as a comment.

#### Client library

[prometheus_client](https://github.com/prometheus/client_python) is the official Python client for Prometheus. It has build-in web server and all the high-level methods for metrics dealing.

There are four types of metric are offered: Counter, Gauge, Summary and Histogram. See the documentation on [metric types](http://prometheus.io/docs/concepts/metric_types/) and [instrumentation best practices](https://prometheus.io/docs/practices/instrumentation/#counter-vs-gauge-summary-vs-histogram) on how to use them.

For this task we will use `Gauge` metric that can go up, down and allows to set a particular value:
```python
import prometheus_client
import time

prometheus_client.start_http_server(9999)

g_metric = prometheus_client.Gauge('metric_name',
                                   'Metric description',
                                   ['label1', 'label2'])

g_metric.labels('label1_value', 'label2_value').set(4.2)

while True:
    g_metric.labels('label1_value', 'label2_value').inc()
    time.sleep(1)
```

After launching the script, metric is available at HTTP endpoint:
```shell script
$ curl 127.0.0.1:9999 && sleep 2 && curl 127.0.0.1:9999

# HELP metric_name Metric description
# TYPE metric_name gauge
metric_name{label1="label1_value",label2="label2_value"} 15.2

# HELP metric_name Metric description
# TYPE metric_name gauge
metric_name{label1="label1_value",label2="label2_value"} 17.2
```

## Narrative

Process management is a pretty common operation, it includes:
* getting information about currently running processes
* launching and killing processes
* exporting collected information in different formats to external monitoring systems.

In this task you will be practicing processes management by creating a script that:
* launches script to simulate CPU workload
* exports CPU metrics for the processes subpart (only `python` and `bash` processes) on HTTP endpoint in Prometheus format
* kills CPU loading script.

This directory contains files you should use during task implementation:
* [Client script](client.py) - testing CLI script

## Guide

### Prerequisites

* make sure executable bit is set on [bucle.sh](bucle.sh):
```shell script
$ ls -la bucle.sh
-rw-r--r--  1 oleg  staff  562 Sep 11 12:17 bucle.sh

$ chmod +x bucle.sh

$ ls -la bucle.sh
-rwxr-xr-x  1 oleg  staff  562 Sep 11 12:17 bucle.sh
```

* create new virtual environment
* add following modules to requirements and install them:
    * `requests`
    * `prometheus_client`
    * `psutil`

### Step 1 (simulate CPU workload and export metrics)

Work in [client script](client.py) to:
1. Execute provided bash script to simulate CPU workload
2. Collect statistics regarding running `python` and `bash` processes - name, command line, summary of CPU usage
3. Update Prometheus metrics using collected data

### Step 2 (kill process)

Work in [client script](client.py) to:
1. Kill the process at 6th iteration

### Step 3 (evaluate results)

Check script output and note how `bucle.sh` process `CPU consumption time` metric changes over time:
* until the process is alive, its CPU consumption increases
* after the process was killed, its CPU consumption increase stopped, but Prometheus client still shows last consumption value.
