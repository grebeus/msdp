import subprocess
import sqlite3
import csv
import logging
import os
import sys
import pathlib


BASH_FILE = "./create_db.sh"
DATABASE_NAME = "database.sqlite"
TABLE_NAME = "employees"
DATA_FILE = "data.csv"
DATABASE_DUMP_NAME = "database.dump.gz"


def main():
    """
    Step 1. Run bash script defined in `BASH_FILE` variable using subprocess to create the database and print to stdout execution output.
            You must provide filename with database to create (defined in `DATABASE_NAME` variable) as a first script argument.

            As a result, a database file with name defined in `DATABASE_NAME` variable should be created in current directory.

        Memo:
            * use subprocess.check_output() to launch bash script
            * output will return bytes that should be decoded before printing
    """
    try:
        ### Block implemented by student
        # output = <subprocess call of `BASH_FILE` with `DATABASE_NAME` argument>
        # logging.debug(<message with script output>)
        ### Block implemented by student
        output = subprocess.check_output([BASH_FILE, DATABASE_NAME]).decode()
        logging.debug(output)
    
    except subprocess.CalledProcessError as err:
        logging.error(f"Error running the database creating script, exit code={err.returncode}, output: '{err.output.decode().strip()}'")

    assert os.path.exists(DATABASE_NAME), "Database was not created, check the code again"

    sqliteConnection = None
    try:
        """
        Step 2. Connect to previously created database using the sqlite3 Python library.
                Get the `cursor` for the database.

            As a result you should have `sqlite3.Cursor` object, which you will reuse in the next steps.

            Memo:
                * make sure you connected to correct database, specified in `DATABASE_NAME` variable
        """
        ### Block implemented by student
        # sqliteConnection = <open sqlite connection to database defined in `DATABASE_NAME` variable, `sqlite3.Connection` object>
        sqliteConnection = sqlite3.connect(DATABASE_NAME)
        # cursor = <cursor from the `sqlite3.Connection` object>
        cursor = sqliteConnection.cursor()
        ### Block implemented by student
        logging.debug("Database connection was successful")

        with open(DATA_FILE) as fh:
            """
            Step 3.1. Create `csv.DictReader` object from opened `DATA_FILE`
            """
            ### Block implemented by student
            # csv_reader = <...>
            csv_reader = csv.DictReader(fh)

            ### Block implemented by student

            """
            Step 3.2. Insert the data from the data CSV file to the database using python library.

                Follow the next steps:
                    1. Transform `csv.DictReader.fieldnames` list from the CSV file to SQL compatible string:
                        ['LastName', 'FirstName', 'Title', 'BirthDate', ... ] -> "'LastName', 'FirstName', 'Title', ..."
                        As a result in `fieldnames` variable you should have string ready to use in SQL query.
                    2. For each row in the CSV file:
                        2.1. Transform row values from the CSV file to SQL compatible string:
                            {'LastName': 'Adams', 'FirstName': 'Andrew', 'Title': 'General Manager', ... } ->
                                "'Adams', 'Andrew', 'General Manager', ..."
                            As a result in `values` variable you should have string ready to use in SQL query.
                        2.1. Combine `fieldnames` and `values` variables in single SQL query:
                            "INSERT INTO <value from TABLE_NAME variable> (<content of your fieldnames variable>)
                                VALUES(<content of your values variable>);"
                            As a result in `query` variable you should have string with SQL query.
                        2.2. Execute the SQL query using the sqlite3 cursor created previously.
                        2.3. Print into stdout how many rows have been inserted.

                Memo:
                    * database changes are committed using database connection object, not cursor
                    * don't forget to close the cursor after injecting all rows
            """
            ### Block implemented by student
            # fieldnames = <SQL compatible string with field names>
            fieldnames = str(csv_reader.fieldnames)[1:-1]
            # iterate over rows from csv_reader
            for row in csv_reader:
                # values = <SQL compatible string with values to insert>
                values = str(list(row.values()))[1:-1]
                # query = <string with SQL query>
                # <execute the query>
                query = f"INSERT INTO {TABLE_NAME} ({fieldnames}) VALUES ({values})"
                # <commit changes to database>
                cursor.execute(query)
                sqliteConnection.commit()
                # logging.debug(<message with inserted rows count>)
                logging.debug(f"Inserted rows count - {cursor.rowcount}")
            ### Block implemented by student
            """
            Step 3.3. Query `TABLE_NAME` in order to find how many rows are in the table to validate results.
            
                As a result you should have number of rows in the `TABLE_NAME` table in `rows_inserted` variable.
            
                Memo:
                    * use following SQL query to count number of raws in the table:
                        SELECT count(*) FROM <value from TABLE_NAME variable>
                    * use fetchone() / fetchmany() / fetchall () cursor methods to get result
            """
            ### Block implemented by student
            # <execute sql query>
            # rows_inserted = <result from sql query>
            rows_inserted = cursor.execute(f"SELECT count(*) FROM {TABLE_NAME}").fetchone()[0]
            ### Block implemented by student

            assert rows_inserted == 8, "Wrong number of inserted rows, check the code again"
            """
            Step 3.4. Close the cursor
            """
            ### Block implemented by student
            cursor.close()
            # <close the cursor>
            ### Block implemented by student
    except sqlite3.Error as error:
        logging.error(f"Failed to insert data into sqlite table: {error}")
        sys.exit(1)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            logging.debug("The SQLite connection was closed")

    try:
        """
        Step 4. Dump database to gzip-compressed file using subprocess pipe.

            1. Use the sqlite3 cli to dump database content to pipe.
            2. Use gzip cli to compress content coming from stdin and write output to file handler opened beforehand.
            3. Use subprocess `Popen.communicate()` to link two processes together via pipe.

            Memo:
                * use `subprocess.Popen` constructor for subprocess creation,
                    it's a low level constructor which allows to customize subprocess execution as much as possible
                * you should write Python analog for the following cli command:
                    $ sqlite3 ${DATABASE_NAME} .dump | gzip -c > ${DATABASE_DUMP_NAME}

        """
        with open(DATABASE_DUMP_NAME, "bw") as dump_handler:
            pass
            ### Block implemented by student
            # p1 = <subprocess method call to execute sqlite3 binary with arguments and redurect stdout to pipe,
            p1 = subprocess.Popen(["sqlite3", DATABASE_NAME, ".dump"], stdout=subprocess.PIPE)

            # p2 = <subprocess method call to execute gzip binary, get stdin from `p1` stdout and redirect stdout to `dump_handler`
            p2 = subprocess.Popen(["gzip", "-c"], stdin=p1.stdout, stdout=dump_handler)
                        
            # link `p1` with `p2` together using `.communicate()`

            p2.communicate()
            ### Block implemented by student
        logging.debug(f"Dumped {DATABASE_NAME} to {DATABASE_DUMP_NAME}")
    except Exception as error:
        logging.error(f"Failed to dump database: {error}")
        sys.exit(1)

    assert os.path.exists(DATABASE_DUMP_NAME), "Database dump was not created, check the code again"
    assert int(pathlib.Path(DATABASE_DUMP_NAME).stat().st_size) > 50, "Database dump is empty, check the code again"


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(message)s',
    )

    main()
