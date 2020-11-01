# Task 4 (dealing with databases and subprocesses)

* [Theory](#theory)
    * [SQLite](#sqlite)
        * [Open database](#open-database)
        * [Database connection](#database-connection)
        * [Database cursor](#database-cursor)
    * [Subprocess](#subprocess)
* [Narrative](#narrative)
* [Guide](#guide)
    * [Prerequisites](#prerequisites)
    * [Step 1 (create database by executing external script)](#step-1-create-database-by-executing-external-script)
    * [Step 2 (connect to database)](#step-2-connect-to-database)
    * [Step 3 (inject data from csv file to database)](#step-3-inject-data-from-csv-file-to-database)
    * [Step 4 (dump database to gzip-compressed file using subprocess pipe)](#step-4-dump-database-to-gzip-compressed-file-using-subprocess-pipe)
* [Additional materials](#additional-materials)

## Theory

### SQLite

[SQLite](https://www.sqlite.org/) is a C library that provides a lightweight disk-based database that does not require a separate server process. At it is file-based (the database consists of a single file on the disk), it makes it extremely portable and reliable. SQLite is meant to be great for both developing and testing and offers more than what is needed for development.

There is a build-in [sqlite3](https://docs.python.org/3/library/sqlite3.html) Python module to deal with SQLite databases.

#### Open database

As a first step it is required to open database from file and get object which represents database connection:
```
class sqlite3
    Methods:
        * connect(database_file_name) - open connection to the SQLite database file database and returns `sqlite3.Connection` object
```

#### Database connection

`sqlite3.Connection` controls:
* database cursors (control structure that enables traversal over the records in a database), which can be used to execute queries
* transactions - a sequence of operations performed (using one or more SQL statements) on a database as a single logical unit of work. The effects of all the SQL statements in a transaction can be either all committed (applied to the database) or all rolled back (undone from the database).

Use following methods for cursors and transactions management:
```
class sqlite3.Connection
    Methods:
        * cursor() - creates `cursor` and returns `sqlite3.Cursor` object
        * commit() - commits the current transaction
        * close() - closes the database connection. This does not automatically call commit().
```

Note:
* if you don’t call `commit()` after database changes, anything you did since the last call to `commit()` is not visible from other database connections
* if you just `close()` your database connection without calling `commit()` first, your changes will be lost!

#### Database cursor

Finally, with database cursor SQL statements can be executed:
```
class sqlite3.Cursor
    Attributes:
        * rowcount - returns the number of rows that are affected or selected by the latest executed SQL query.

    Methods:
        * execute(sql) - executes an SQL statement
        * fetchone() - fetches the next row of a query result set, returning a single sequence, or None when no more data is available
        * fetchall() - fetches all (remaining) rows of a query result, returning a list. An empty list is returned when no rows are available.
```

Example:
``` Python
import sqlite3
conn = sqlite3.connect('example.db')

c = conn.cursor()

c.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')

c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
print(f"Inserted rows count - {c.rowcount}")

conn.commit()

# Insecure: do this only when you trust you source
#           it makes your program vulnerable to an SQL injection attack
symbol = 'RHAT'
c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)
print(c.fetchone())

# Secure: do this instead in most cases (DB-API’s parameter substitution)
#         Put ? as a placeholder wherever you want to use a value,
#           and then provide a tuple of values as the second argument to the cursor’s execute() method
t = ('RHAT',)
c.execute('SELECT * FROM stocks WHERE symbol=?', t)
print(c.fetchone())

conn.close()
```

### Subprocess

The [subprocess](https://docs.python.org/3/library/subprocess.html) module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.

```
class subprocess
    Methods:
        * check_output([command, argument1, ...]): Run command with arguments and return its output.
            If the return code was non-zero it raises a CalledProcessError.
            The CalledProcessError object will have the return code in the `returncode` attribute
                and any output in the `output` attribute.
        * Popen([command, argument1, ...], stdin=, stdout=, stderr=): A class for flexible executing a command in a new process.
            It returns `subprocess.Popen` object.
            stdin/stdout/stderr arguments can be set to one of constants described below or
                another `subprocess.Popen` object stdin/stdout/stderr.

    Constants
        DEVNULL: Special value that indicates that os.devnull should be used
        PIPE:    Special value that indicates a pipe should be created
```

`subprocess.check_output` usage:
```
>>> import subprocess

>>> output = subprocess.check_output(["/bin/ls"])
>>> print(output.decode())
README.md
client.py
create_db.sh
data.csv

>>> subprocess.check_output(["/bin/ls", "/doesnotexist"])
ls: /doesnotexist: No such file or directory
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/Cellar/python@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/lib/python3.8/subprocess.py", line 411, in check_output
    return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
  File "/usr/local/Cellar/python@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/lib/python3.8/subprocess.py", line 512, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command '['/bin/ls', '/doesnotexist']' returned non-zero exit status 1.
```
Note:
* it returns command execution result as a binary
* it raises `subprocess.CalledProcessError` when command execution result is not zero.

`subprocess.Popen` usage and how to connect two subprocesses via `subprocess.PIPE`:
```
>>> import subprocess
>>> p1 = subprocess.Popen(["/bin/ls"], stdout=subprocess.PIPE)
>>> p2 = subprocess.Popen(["/usr/bin/grep", ".csv"], stdin=p1.stdout, stdout=subprocess.PIPE)
>>> output = p2.communicate()[0]
>>> print(output.decode())
data.csv
```

The above-mentioned code is Python equivalent of the following `bash` code:
```shell script
$ cd Task4
$ /bin/ls | /usr/bin/grep .csv
data.csv
```


## Narrative

There are a lot of moments when you will need to execute external commands from your Python code.
Using `subprocess` standard Python module is the most common approach to do that.

Another very common activity is data management when you need to:
* populate some database from file or external API
* get data from database and perform some actions based on what you got.

In this task you will be handling both activities by creating a script that:
* executes a given external bash script
* executes bash commands directly writen in the Python code
* populates database from CSV file.

This directory contains files you should use during task implementation:
* [Database creation script](create_db.sh) - script that will create the sqlite database and table
* [Employee data](data.csv) - coma separated CSV file with employee information
* [Client script](client.py) - testing CLI script.

## Guide

### Prerequisites

* make sure executable bit is set on [create_db.sh](create_db.sh):
```shell script
$ ls -la create_db.sh
-rw-r--r--  1 oleg  staff  562 Sep 11 12:17 create_db.sh

$ chmod +x create_db.sh

$ ls -la create_db.sh
-rwxr-xr-x  1 oleg  staff  562 Sep 11 12:17 create_db.sh
```

### Step 1 (create database by executing external script)

Work in [client script](client.py) to:
1. Execute bash script to create the database
2. Output result of the execution.

### Step 2 (connect to database)

Work in [client script](client.py) to:
1. Establish database connection using sqlite3 Python module
2. Open execution cursor for that database.

### Step 3 (inject data from csv file to database)

Work in [client script](client.py) to:
1. Open input CSV file as `csv.DictReader`
2. Insert the data from CSV file to the database using sqlite3 Python library
3. Validate inserted data by querying count of rows in the table
4. Close the database cursor.

### Step 4 (dump database to gzip-compressed file using subprocess pipe)

Work in [client script](client.py) to:
1. Dump database to gzip-compressed file using subprocess pipe.

## Additional materials

TODO: Add information on ORMs