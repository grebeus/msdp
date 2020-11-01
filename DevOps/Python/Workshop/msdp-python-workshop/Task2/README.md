# Task 2 (parsing logs with regular expressions)

* [Theory](#theory)
    * [Regex](#regex)
    * [Collections most_common](#collections-most_common)
* [Narrative](#narrative)
* [Guide](#guide)
    * [Prerequisites](#prerequisites)
    * [Step 1 (parse log file to get stats)](#step-1-parse-log-file-to-get-stats)
        * [Memo](#memo)
    * [Step 2 (find out URL rates)](#step-2-find-out-url-rates)
    * [Step 3 (find out failed requests rate)](#step-3-find-out-failed-requests-rate)
    * [Step 4 (validate stats)](#step-4-validate-stats)
        * [Memo](#memo-1)

## Theory

#### Regex

A RegEx, or Regular Expression, is a sequence of characters that forms a search pattern.
RegEx can be used to check if a string contains the specified search pattern.

The built-in `re` module offers a set of functions that allows searching a string for a match:
* `re.findall()` - Returns a list containing all matches
* `re.search()`  - Returns a Match object if there is a match anywhere in the string

Match objects can address individual sub-matches of complex regular expressions.

```
>>> import re

>>> txt1 = "The rain in Spain"
>>> txt2 = "The snow in Montenegro"
>>> txt3 = "The fog in the Netherlands"

>>> re.findall("in", txt1)
['in', 'in', 'in']

>>> weather_re = re.compile("^The (?P<condition>[a-z]+) in (?P<country>\w+)$")
>>> match1 = weather_re.search(txt1)
>>> match2 = weather_re.search(txt2)

>>> match1
<re.Match object; span=(0, 17), match='The rain in Spain'>
>>> match1.groups()
('rain', 'Spain')
>>> match1.group("condition")
'rain'

>>> match2.groups()
('snow', 'Montenegro')
>>> match2.group("condition")
'snow'

>>> weather_re.search(txt3)
None
```

Special characters in patterns:
* `[]` operator -   (Ex: [0-9] matches any single decimal digit)
* dot (`.`) operator -  matches any character except a newline
* `^` operator - Anchors a match at the start of a string
* `$` operator - Anchors a match at the end of a string
* `*` operator - Matches zero or more repetitions
* `+` operator - Matches one or more repetitions

Full list of operators you can find in this [Regex cheatsheet](https://external-preview.redd.it/jZqQ4T-R9IX8XR9KEiViaRshCfY0Q_sMAIvg4rqH9QI.jpg?auto=webp&s=78de01a0c8aa8bf307e9a9084b1087980c606695)

Example of usage [topic](https://realpython.com/regex-python/)

## Narrative

You work on statistics collection script for web server. The script should:
* parse [nginx log](access.log) in order to find:
    * total amount of body bytes served
    * the most frequently visited URL
    * percentage of failed requests (status codes from 400 to 599) over successful requests (all other status codes)
* send values calculated on previous steps to external API in order to validate them.

The most frequently visited URL calculation should be done in two ways:
* manually
* using `most_common` method of `collections.Counter` class.

This directory contains files you should use during task implementation:
* [Client script](client.py) - testing CLI script
* [Nginx log file](access.log) - nginx log file example.

## Guide

### Prerequisites

* create new virtual environment
* add `requests` module to requirements and install it
* launch [API server](../API/)

### Step 1 (parse log file to get stats)

Work in [client script](client.py) to:
1. Create regexp for status code and bytes getting
2. Parse log file and collect stats

#### Memo

Nginx default row structure:
```
93.180.71.3 - - [17/May/2015:08:05:32 +0000] "GET /downloads/product_1 HTTP/1.1" 304 0 "-" "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"
<remote ip address> - - [<request date>] "<request method> <url> <status code> <body bytes transfered> "-" <requester http agent>
```

Regexp example to get status code (one of possible ways):
`\" (\d+) \d+ \"`

Use [regular expression debugger](https://regex101.com/) for testing your regexps before using in the code.

### Step 2 (find out failed requests rate)

Work in [client script](client.py) to:
1. Calculate number of failed and succeed status codes separately
2. Calculate failed requests rate

### Step 3 (validate stats)

Work in [client script](client.py) to:
1. Finish `api_check` function
2. Validate bytes served value
3. Validate failed requests rate value

#### Memo

* Check bytes served
```
curl --request POST 'http://localhost:5000/task3/check_bytes_served' \
     --form 'bytes_served=123456789'
```

* Check failed rate
```
curl --request POST 'http://localhost:5000/task3/check_failed_rate' \
     --form 'failed_rate=23'
```
