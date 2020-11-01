# Task 3 (date/time and filesystem operations, yaml parsing and command-line arguments usage)

* [Theory](#theory)
    * [Date operations](#date-operations)
    * [Filesystem operations](#filesystem-operations)
    * [Lists and dicts](#lists-and-dicts)
        * [Lists sorting, indexing and slicing](#lists-sorting-indexing-and-slicing)
        * [Safe dictionary indexing](#safe-dictionary-indexing)
    * [Reading text files](#reading-text-files)
* [Narrative](#narrative)
* [Guide](#guide)
    * [Prerequisites](#prerequisites)
    * [Step 1 (fix seeding function)](#step-1-fix-seeding-function)
    * [Step 2 (implement retention)](#step-2-implement-retention)
    * [Step 3 (leverage config file)](#step-3-leverage-config-file)
    * [Step 4 (leverage command-line arguments)](#step-4-leverage-command-line-arguments)

## Theory

### Date operations

There are several classes in Python to work with date and time, but the most common to use are:
* `datetime.datetime`, it represents a combination of a date and a time
* `datetime.timedelta`, a duration expressing the difference between two date, time, or datetime instances.

```
class datetime.datetime
    Attributes: year, month, day, etc.

    Methods:
        * now() / utcnow() - Return the current local / UTC date and time
        * date() - return date object with same year, month and day
        * isoformat() - return a string representing the date and/or time in ISO 8601 format
        * weekday() - return the day of the week as an integer, where Monday is 0 and Sunday is 6
        * strftime(format) - return a string representing the date and time, controlled by an explicit format string
        * strptime(date_string, format) - return a datetime corresponding to date_string, parsed according to format

    strftime() and strptime() format codes:
        * %Y - year with century as a decimal number
        * %m - month as a zero-padded decimal number
        * %d - day of the month as a zero-padded decimal number

class datetime.timedelta(weeks=0, days=0, ..., minutes=0, ...)
```

How to get current date/time and access different properties:
```
>>> datetime.utcnow()
datetime.datetime(2020, 9, 4, 16, 17, 45, 674647)
>>> datetime.utcnow().day
4
>>> datetime.utcnow().weekday()
3
```

Timedelta objects support additions and subtractions with datetime objects:
```
>>> datetime.utcnow() - timedelta(minutes=60)
datetime.datetime(2020, 9, 4, 14, 48, 35, 908453)

>>> (datetime.utcnow() - timedelta(minutes=60)).date().isoformat()
'2020-09-04'

>>> (datetime.utcnow() - timedelta(minutes=60)).strftime("%Y")
'2020'
```

### Filesystem operations

```
os.listdir(path='.') - return a list containing the names of the entries in the directory given by path.
                       The list does not include the special entries '.' and '..'.

os.walk(top) - generate the file names in a directory tree by walking the tree either top-down or bottom-up.

os.rmdir(path) - remove empty directory

shutil.rmtree(path) - delete an entire directory tree
```

### Lists and dicts

#### Lists sorting, indexing and slicing

```
>>> array = [3, 2, 6, 5, 1, 10, 9, 7, 8, 4]

>>> """ return sorted array *copy* """
>>> sorted(array)
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

>>> """ sorts list *in-place* """
>>> array.sort()
>>> array
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

>>> """ get list *copy* with slicing """
>>> array[:]
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

>>> """ get single element (from the beginning) """
>>> array[3]
4
>>> """ get single element (from the end) """
>>> array[-3]
8

>>> """ get sublist (second index ommited -> till the end) """
>>> array[5:]
[6, 7, 8, 9, 10]
>>> """ get sublist (first index ommited -> from the beginning) """
>>> sorted(array)[:4]
[1, 2, 3, 4]

>>> """ get sublist (positive indexes) """
>>> array[5:8]
[6, 7, 8]
>>> """ get sublist (first negative index -> start from the end, second index ommited -> till the end) """
>>> array[-3:]
[8, 9, 10]
```

#### Safe dictionary indexing

Check if element exists before accessing:
```
if k in d:
    value = d[k]
else:
    value = default_value
```

Ask forgiveness not permission:
```
try:
    value = d[k]
except KeyError:
    value = default_value
```

The shortest and simplest way is to use build-in method:
```
value = d.get(k, default_value)
```

### Reading text files

Reading whole file at once (can be memory-heavy) using context manager:
```python
with open(filename, "rt") as fh:
    content = fh.read()
    print(content)
```

Reading file line by line using context manager:
```python
with open(filename, "rt") as fh:
    for line in fh:
        print(line)
```

Reading whole file at once with file explicit `open` and `close`:
```python
fh = open(filename, "rt")
content = fh.read()
print(content)
fh.close()
```

Reading whole file at once, closing file with garbage collection (CPython). **Bad practice, do not use such code**:
```python
content = open(filename, "rt").read()
print(content)
```

### Reading YAML

YAML is a human friendly **data serialization** standard for all programming languages. It can be used to serialize (represent) internal Python structures (some of them) in text as vice versa. The most common usage case is storing configuration for your scripts in YAML files.

Parsing YAML using [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)
```
>>> import yaml

>>> config = {'count': 5, 'day': 'Mon', 'opts': ['first', 'second']}

>>> config_yaml = yaml.safe_dump(config)
>>> type(config_yaml)
<class 'str'>
>>> print(config_yaml)
count: 5
day: Mon
opts:
- first
- second

>> config_dict = yaml.safe_load(config_yaml)
>>> type(config_dict)
<class 'dict'>
>>> print(config_dict)
{'count': 5, 'day': 'Mon', 'opts': ['first', 'second']}
```

Note: It is not safe to call `yaml.load()` with any data received from an untrusted source! `yaml.load()` is as powerful enough to call any Python function. Use `yaml.safe_*()` functions instead.


## Narrative

You work on backups retention script, which walks through directory with predefined structure and removes outdated backup directories. Backup directory represents one-level structure with directories named using `YYYY-MM-DD` pattern, one directory per day, i.e.:
```
/
├── YYYY-MM-DD
├── YYYY-MM-DD
  ...
├── YYYY-MM-DD
```

The script should keep only:
* 5 most recent daily backups
* 4 most recent weekly backups (taken on Sundays)
* 2 most recent monthly backups (taken on the 1st day of a month)

all other folder should be deleted.

This directory contains files you should use during task implementation:
* [Client script](client.py) - testing CLI script
* [Utility module](utils.py) - Python library with user-defined code
* [Configuration file](config.yaml) - yaml to configure script parameters.

## Guide

### Prerequisites

* create new virtual environment
* add `pyyaml` module to requirements and install it

### Step 1 (fix seeding function)

Work in [utility module](utils.py) to:
1. Implement missing line in `seed` function. This function is used to fill initial directory structure you will work with.

### Step 2 (implement retention)

Work in [client script](client.py) to:
1. Get the list of currently present backup directories
2. Sort directories by monthly (taken on the 1st day of a month), weekly (taken on Sundays), daily (all other) categories
3. Prepare the list of directories to remove

Use hardcoded retention params for each category.

### Step 3 (leverage config file)

1. Finish `Config` class in [utility module](utils.py) which represents yaml config as Python object
2. Work in [client script](client.py) to read backup retention params from hardcoded [config file](config.yaml).
3. Replace hardcoded retention params with values from config
4. Replace hardcoded logging level in `logging.basicConfig` according to `verbose` param from config.

### Step 4 (leverage command-line arguments)

Work in [client script](client.py) to:
1. Use command-line arguments to pass config file name with backup retention params.
