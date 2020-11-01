# Task 1 (API interaction, operations with encoded and compressed CSV files)

* [Theory](#theory)
    * [CSV files](#csv-files)
        * [Reading](#reading)
           * [csv.reader](#csvreader)
           * [csv.DictReader](#csvdictreader)
        * [Writing](#writing)
    * [Requests](#requests)
        * [Response](#response)
        * [HTTP basic auth](#http-basic-auth)
        * [Response headers](#response-headers)
    * [Base64 encoding](#base64-encoding)
    * [MD5 hash](#md5-hash)
* [Narrative](#narrative)
* [Guide](#guide)
    * [Prerequisites](#prerequisites)
    * [Step 1 (get report, parse csv, find out stats)](#step-1-get-report-parse-csv-find-out-stats)
    * [Step 2 (generate CSV report)](#step-2-generate-csv-report)
    * [Step 3 (validate CSV report)](#step-3-validate-csv-report)

## Theory

### CSV files
CSV (Comma Separated Values) is a simple file format used to store tabular data, such as a spreadsheet or database. The name `CSV` indicates the use of the comma to separate data fields. Nevertheless, the term `CSV` is widely used to refer a large family of formats, which differ in many ways:
* allow or require single or double quotation marks around some or all fields
* reserve the very first record as a header containing a list of field names
* field separators handling (such as space or semicolon)
* newline characters inside text fields

and so on, thus during CSV decoding you should know what CSV dialect your file was created with.

We will work with simple CSV format which:
* uses a comma to separate each specific data value
* reserves first row for a header with list of field names
* assumes absence of new lines inside data values
* does not use quotation for data values.

Here’s what that structure looks like:
```
name,department,birthday month
John Smith,Accounting,November
Erica Meyers,Information technology,March
```

There is a built-in Python module called `csv` for dealing with CSV data.

#### Reading

##### csv.reader

Reading from a CSV file is done using the `csv.reader` object. The CSV file is opened as a text file with Python’s built-in `open()` function, which returns a file object. Then it is passed to the `csv.reader`, which does the heavy lifting:
```python
with open('example.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        print(row)
```

The result of the code execution:
```
['name', 'department', 'birthday month']
['John Smith', 'Accounting', 'November']
['Erica Meyers', 'Information technology', 'March']
```

Note: the header (list of field names) is not handled separately by `csv.reader`, it just comes first during iteration and requires separate handing by your code if present.

##### csv.DictReader

Rather than deal with a list of individual string elements, CSV data can be read directly into a dictionary as well using `csv.DictReader`:
```python
with open('example.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    print(f"CSV header - {csv_reader.fieldnames}\n")
    for row in csv_reader:
        print(f"{row['name']} works in the {row['department']} department, and was born in {row['birthday month']}.")
```

The result of the code execution:
```
CSV header - ['name', 'department', 'birthday month']

John Smith works in the Accounting department, and was born in November.
Erica Meyers works in the Information technology department, and was born in March.
```

Note:
* `csv.DictReader` handles the header (list of field names) automatically and saves column names in `csv.DictReader.fieldnames`
* data values can be referred to separately by corresponding field names from the header.

#### Writing

CSV data can be populated into a file using a `csv.writer` object and its `writerow()` method:
```
with open('example.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['name', 'department', 'birthday month'])

    csv_writer.writerow(['John Smith', 'Accounting', 'November'])
    csv_writer.writerow(['Erica Meyers', 'IT', 'March'])
```

Similarly, data can be written out from a dictionary using `csv.DictWriter`:
```
with open('example.csv', mode='w') as csv_file:
    fieldnames = ['name', 'department', 'birthday month']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

    csv_writer.writerow({'name': 'John Smith', 'department': 'Accounting', 'birthday month': 'November'})
    csv_writer.writerow({'name': 'Erica Meyers', 'department': 'Information technology', 'birthday month': 'March'})
```

Note the difference with headers writing:
* with `csv.writer`, header is written manually as an ordinary row
* with `csv.DictWriter`, there are separate argument `fieldnames` and method `writeheader()`.


### Requests

The `requests` library is the de facto standard for making HTTP requests in Python. It abstracts the complexities of making requests behind an easy to use API so that you can focus on interacting with services and consuming data in your application.

Two of the most common HTTP methods are `GET` and `POST`. Both `GET` and `POST` methods are used to transfer data from client to server via HTTP protocol. Main difference between `POST` and `GET` methods are that `GET` carries request parameters appended in the URL string while `POST` carries request parameters in the message body.

GET request example:
```
>>> response = requests.get('https://www.google.com.ua/search?q=test')
>>> type(response)
<class 'requests.models.Response'>
```

POST request example:
```
>>> response = requests.post('https://httpbin.org/post', data={'key': 'value'})
>>> type(response)
<class 'requests.models.Response'>
```

Both methods return `requests.Response` object, which can be used to get all details about the HTTP response.

#### Response

Response content can be returned from the `requests.Response.text` field.
```
>>> response = requests.get('https://api.github.com/events')
>>> type(response.text)
<class 'str'>
>>> response.text[:100]
'[{"id":"13502579226","type":"CreateEvent","actor":{"id":62062856,"login":"ubelyse","display_login":"'
```

Also, there is a built-in JSON decoder `requests.Response.json()`, which returns the JSON object if the response content is JSON-formatted.
```
>>> response = requests.get('https://api.github.com/events')
>>> response.json()
...enormous output skipped...
>>> type(response.json())
<class 'list'>
```

#### HTTP basic auth

Many web services that require authentication accept HTTP Basic Auth. This is the simplest kind, and `Requests` supports it straight out of the box. Just create `requests.auth.HTTPBasicAuth` object with required username and password, and pass that object to `requests.get` or `requests.post` in `auth` argument:
```
>>> from requests.auth import HTTPBasicAuth
>>> requests.get('https://api.github.com/user', auth=HTTPBasicAuth('user', 'pass'))
<Response [200]>
```

#### Response headers

Server response headers can be accessed using `requests.Response.headers` dictionary field.
```
>>> response = requests.get('https://wordpress.com')
>>> response.headers.get('X-hacker')
"If you're reading this, you should visit automattic.com/jobs and apply to join the fun, mention this header."
```

### Base64 encoding

Base64 encoding is suitable for encoding binary data so that it can be safely sent by email, used as parts of URLs, or included as part of an HTTP POST request.

```
>> import os
>> import base64

>>> bytes = os.urandom(10)
>>> random_bytes = os.urandom(10)
>>> random_bytes
b'\xa36v{P\x7f\xedF\x96\xae'

>>> base64.b64encode(random_bytes).decode()
'ozZ2e1B/7UaWrg=='
```

Base64 is not an encryption mechanism, it is an encoding scheme. It is easily reversed, so it is a bad choice for protecting sensitive data:
```
>>> base64.b64decode(base64.b64encode(random_bytes)) == random_bytes
True
```

### MD5 hash

Cryptographic hashes are used in various computer programs in our day-to-day life. Some of the applications: digital signatures, message authentication codes, manipulation detection, fingerprints, checksums (message integrity check), hash tables, password storage and much more. Hashing is also used in sending messages over the network for security or storing messages in databases.

The Python standard library includes a module called `hashlib`, which contains most of the popular hashing algorithms.

Functions associated:
* `str.encode()` - converts the string to bytes to be acceptable by hash function
* `hashlib.md5()` - returns an MD5 object
* `hashlib.md5().digest()` - returns the MD5 hash in **byte format**
* `hashlib.md5().hexdigest()` - returns the MD5 hash as a string in **hexadecimal format**.

```
>>> import hashlib

>>> """ Input string in ASCII encoding """
>>> input_str = 'Hello, Python!'

>>> """ Encoded to bytes representation of input string """
>>> input_bytes = input_str.encode()
>>> input_bytes
b'Hello, Python!'

>>> """ MD5 hash calculation """
>>> hash_obj = hashlib.md5(input_bytes)

>>> """ Raw digest of the MD5 hash """
>>> hash_obj.digest()
b'\xa0\xafx\x10\xeb_\xcb\x84\xc70\xf8Q6\x1d\xe0j'

>>> """ HEX digest of the MD5 hash """
>>> hash_obj.hexdigest()
'a0af7810eb5fcb84c730f851361de06a'
```


## Narrative

On a regular basis you work with CSV-based transactions statistics report, generated by external system and accessible via basic auth protected API. Alongside with the report, API returns in `checksum` header `md5` hash of the report content to guarantee report consistency.
Based on that report you need to calculate additional statistics values and send them to another external API system in CSV format.
You decided to automate the process and create a script for automatic downloading base report, calculating required parameters and sending report back.

The script should:
* request and parse base64-encoded gzip-compressed CSV report (format is described below), from external, basic auth protected, API
* validate report by comparing actual `md5` hash of the report content with the value provided in `checksum` header in API response
* find in the report values of:
    * the highest `90 Percent` average time
    * the highest fail rate (`Fail` / `Pass` ratio)
* create CSV report based on found `transaction names` and `corresponding values` (format described below)
* send back to external API base64-encoded gzip-compressed generated CSV report

This directory contains files you should use during task implementation:
* [Client script](client.py) - testing CLI script

## Guide

### Prerequisites

* launch [API server](../API/)
* create [new virtual environment](https://git.epam.com/Oleh_Palii/msdp-python-workshop#create-virtual-env)
* add `requests` module to requirements and install it

### Step 1 (get report, parse csv, find out stats)

Work in [client script](client.py) to:
1. Get CSV report from API server
2. Validate checksum of report
3. Decode and parse CSV data, find out required stats based on parsed data:
    * the highest `90 Percent` average time
    * the highest fail rate (`Fail` / `Pass` ratio)
4. Round stats values to 2 precision after the decimal point.

Input CSV report structure:
```
Transaction Name,Minimum,Average,Maximum,Std. Deviation,90 Percent,Pass,Fail,Stop
Logout_Operator,0.001,0.02,0.1,1.1,0.5,2221,2,0
...
```

### Step 2 (generate CSV report)

Work in [client script](client.py) to:
1. Generate CSV report using stats collected on previous step

Output CSV report structure:
```
N,Value
1,Max_90_Percent_value
2,Max_Fail_rate_value
```

### Step 3 (validate CSV report)

Work in [client script](client.py) to:
1. Post generated CSV report to API server
