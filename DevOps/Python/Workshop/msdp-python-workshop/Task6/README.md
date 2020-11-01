# Task 6 (practical decorators)

* [Theory](#theory)
    * [Decorators overview](#decorators-overview)
    * [Decorators in practice](#decorators-in-practice)
    * [Monkey-patching](#monkey-patching)
* [Narrative](#narrative)
* [Guide](#guide)
    * [Prerequisites](#prerequisites)
    * [Step 1 (measure total execution time)](#step-1-measure-total-execution-time)
    * [Step 2 (measure each encrypt function execution time)](#step-2-measure-each-encrypt-function-execution-time)
    * [Step 3 (implement memoization)](#step-3-implement-memoization)
    * [Step 4 (optional, use memoization function from standard library)](#step-4-optional-use-memoization-function-from-standard-library)
* [Additional materials](#additional-materials)

## Theory

### Decorators overview

Decorators allow you to dynamically alter the functionality of a function, method, or class without permanently modifying the source code of the function being decorated.

Commonly used examples include:
* logging and timing functions
* enforcing AAA (Authentication, Authorization and Accounting)
* rate-limiting
* caching

In basic terms, a decorator is a function that takes a function as input and returns another function.
It is possible due to fact that decorators are first-class objects in Python. This means that functions can be assigned to variables and passed to functions as arguments.

### Decorators in practice
Generic decorator, you can start with during task implementation looks like:
```python
def foo_decarator(func):
    """ define here any variables you need to preserve between wrapper invocations """
    def wrapper(*args, **kwargs):
        """ put here code you need to run prior wrapped function call """
        result = func(*args, **kwargs)
        """ put here code you need to run after wrapped function call """
        return result
    return wrapper
```
`foo_decarator()` executes once (when we decorate function), `wrapper()` executes each time the decorated function runs.

`@` is just a syntactic sugar, you can wrap you functions directly when you need it:
```python
@foo_decorator
def func1():
    return "Hello world!"

def func2():
    return "Hello world!"
func2 = foo_decorator(func2)

>>> func1()
"Hello world!"
>>> func2()
"Hello world!"
````

### Monkey-patching

Monkey-patching allows you to extend or change functionality of third-party functions, methods or classes at runtime without changing third-party source code.

Commonly used examples include:
* extend or change functionality of standard or third-party libraries at runtime
* during testing mock behaviour of some libraries or classes
* quick fixes to code when you have no time (or intention) to do it properly

```python
import math

def circumference(r):
    return 2*math.pi*r

print(circumference(3)) # 18.84955592153876
math.pi = 4
print(circumference(3)) # 24
```

```python
class API():
  def add(self, a, b):
    raise Exception("Connection timed out")

def mock_api_add(self, a, b):
  return a+b

print(API().add(2, 2)) # raises exception
API.add = mock_api_add
print(API().add(2, 2)) # 4
```

## Narrative

You work with hardware security module (HSM) located overseas for words encryption. After several tests you understand that:
* encryption speed is insufficient due to:
    * network delay (you access device located on the other side of the globe over the Internet)
    * device encryption speed
* during each session (script run) you work with limited repeatable amount of words to encrypt.

You need to:
* prove the root cause of encryption speed insufficiency by measuring and printing encryption function execution time
* implement effective caching mechanism to reuse already encrypted words

with **minimum changes** to [HSM module](hsm.py) and [client script](hsm.py). You can put as much code as you want to [utility module](utils.py).

This directory contains files you should use during task implementation:
* [HSM module](hsm.py) - Python library which implements native Python interface to HSM device
* [Client script](client.py) - testing CLI script
* [Utility module](utils.py) - Python library with user-defined code.

## Guide

### Prerequisites

* create new virtual environment
* add `cryptography` module to requirements and install it

### Step 1 (measure total execution time)

Measure total script execution time:

```shell script
$ time python3 client.py
'apple' encrypted is 'gAAAAABfTAHvUmbgNQwogE5A4D8x2WVasi8fhdKNbCR6qpQP_tGHA7FmTSWydQbFs8yqWjDSlyVD6rf9AV6FdnJxIimqfe_i3A=='

'apple' encrypted is 'gAAAAABfTAHxR7npVE40faq4P4c4OMoFIgaCGQqp8QhrMBdKkG6pfk_A6q-L7Yr7xR3Lw0YWg-6EBwZKzRwbh77LwnEgPsi_5Q=='

'pear' encrypted is 'gAAAAABfTAHz6_TvbTh_v9-QwWQ6wDCau6Xcse45DMwHhNeG-7X3bPpa8yqG46UXEv0rta_T7HdY8bGzXnulIyE-dXbk7r5qXA=='

'banana' encrypted is 'gAAAAABfTAH0f_mk53Uur5ENfS31_Er1-Caao8ZBbIZwy7-ET__M0IcGIoc4YlIwI009bZ-rz21Ofhac9i_2oJViKRXy49SAtQ=='

'apple' encrypted is 'gAAAAABfTAH1ZqPYahc9viOsouw5IzZ0w-nAxfbqKsgdCmo0TSig5HgTrTcijyLYO2-gafYgOWUHlEz80iHUDG01_AK2cBzItw=='

'banana' encrypted is 'gAAAAABfTAH2Dqw_WfhynJ07g9BFb2c_AagqkZ8CFQ5NIBAGzZhCvBTOOIATDitx7hlhsxo8w-CsxrrtndVHDa4gT-mUJzel8g=='

'apple' encrypted is 'gAAAAABfTAH3s2QSYrrBw4KEwSmMj2b1xGFy4eMQDhTwHgMngD18XLM6AsXXVONbJT7oAt7IOktMEgsHU9pNHe6U80Gfj72HOA=='

'banana' encrypted is 'gAAAAABfTAH59MpR0ZIfbPLPU_0n93hNIhlHuODiun9gDW8QT21cEbXIIz6-LGk3Rtd2CgQEHS5bSzCs74bNiKFA-Sctp5utEg=='

'orange' encrypted is 'gAAAAABfTAH6QQegNIZWM-2BpJcOJOZcSYChvKe4OHGzIQCgeSPtVHuYvYilyvy4cJZGFG1ozxhF7QFKy3CMebp4ruY-CBwURQ=='

'orange' encrypted is 'gAAAAABfTAH8WxjK2L-MWbGxNAyrMQudQJnhhG6u-59AQEWeLKQ3rwbCU-RAqDO7iXV4ZjoDNxY7esOLkfhFmd283druEEt2aQ=='

'pear' encrypted is 'gAAAAABfTAH9P66HC1gtO3U8OnLjN3Adzu-WbpGjLtvhvTukTCLiVFsqKtcQLC1GXoFScAbNMBlpo6UIjhrOAZlC1VlofynGAA=='

'orange' encrypted is 'gAAAAABfTAH-_zYg_MkRH5fwjOARGaGHiP2Qj5W_0f8WaPhDDz53KpoVZkpVYwkhl9ROt_0BJ5IwJpr1knOP0NYaSsfTxO6maw=='

'orange' encrypted is 'gAAAAABfTAIA7xb89B34kxHqFz5XhbUVBXOMa7BTJJEbLBglyIBeZ9DlptV2v-2q31uzu6FIiaLNsAkUL3882vmuMSfvHrvUiA=='

python3 client.py  0,12s user 0,03s system 0% cpu 19,289 total
```

It took ~20 seconds to encrypt all the values.

### Step 2 (measure each encrypt function execution time)

1. In [utility module](utils.py) implement decorator to measure arbitrary function execution time
2. In [client script](client.py) monkey patch HSM.encrypt() method with implemented decorator
3. Measure each encrypt function execution time:

```shell script
$ time python3 client.py
=== time_it ===> 'encrypt(pear)' duration '1.88'
'pear' encrypted is 'gAAAAABfTAHDJP4KoyDwCqxUUktQp9zSpZx56YYGsO2kzvbqi8r5wwzes_YkpfgGhhRgqG-bPjrzQPlkT2FLismyVNytX17O_w=='

=== time_it ===> 'encrypt(orange)' duration '1.95'
'orange' encrypted is 'gAAAAABfTAHFCaJSMpJbmDTxQWlWl8-y6XWychgftCnJ9TGkfoW4J0HO86An9ulV1FpItj4ngcNEr60kqTYnpgtTTR--eEoV_w=='

=== time_it ===> 'encrypt(apple)' duration '1.88'
'apple' encrypted is 'gAAAAABfTAHGLmuDBilRzuWKf_0OKLCpEIqk1WT1kBhVIn9O1s-QrX6zoBpS--UblaSh-k_hjW68QpCTSRI8uTD0VZvGecxr2g=='

=== time_it ===> 'encrypt(apple)' duration '1.00'
'apple' encrypted is 'gAAAAABfTAHHBM_LdZyjimQxkH6RJJf9qx3HxGHQWSGC7x670p8YXnSw7TwzqI3P13Fmiry72l0c_rBZRJBNnyUbnE94vwC0zQ=='

=== time_it ===> 'encrypt(orange)' duration '1.73'
'orange' encrypted is 'gAAAAABfTAHJHUVYmSWTprIBk2GYaJ6GAg_bKDfEdP6T5Ig6WebjhlKOVw071Pj7--OVvlVx1OweHQshs22NxVUpesbhoaoMYg=='

=== time_it ===> 'encrypt(apple)' duration '1.50'
'apple' encrypted is 'gAAAAABfTAHL-iijUqcOtYx4cl1WmGc6NECp3dPZ21T17N0QBXyASYBJBto4hE5y9J_x3RcLjpJlWo_ONNav01ZzeE6ToXi0PA=='

=== time_it ===> 'encrypt(banana)' duration '1.64'
'banana' encrypted is 'gAAAAABfTAHMlCCOsMSsO9D253q4ST9u1Hrd6Ys-i60l_mUFaIE3GW6fuXf6L8ZW-FF1ISPmvY4O8G_0PhKP4P3gaN-ZL1ZzzA=='

=== time_it ===> 'encrypt(banana)' duration '1.12'
'banana' encrypted is 'gAAAAABfTAHNe9zB_VVAyNX40e0npCB4oWDRLA78ZKzb5wAIfUBO4_sqRxXF-Oweio0b3AKhDu524sPKNdAO7BnvBEsxPy6SHQ=='

=== time_it ===> 'encrypt(banana)' duration '1.95'
'banana' encrypted is 'gAAAAABfTAHPGZ4QGFYRhZFs7_Q8P6YB6gwjECBmdxzbAzlCoSOhPLbMqSlrni1BVQ06OxeFaGp0NVFzRz1EuUo1Sb5Sx4FvrA=='

=== time_it ===> 'encrypt(pear)' duration '1.66'
'pear' encrypted is 'gAAAAABfTAHRLMWyb0bhtsJFKahtdOHz-fWnp4fxaRQpNq4OtKSLMrBvGUHUBNaWkbldUomMCZg7ONqGsx_UghWp6-MimSh7GQ=='

python3 client.py  0,12s user 0,03s system 0% cpu 16,478 total
``` 

It takes from 1 to 2 seconds to encrypt single value.

### Step 3 (implement memoization)

1. In [utility module](utils.py) implement decorator to cache function output based on input arguments
2. In [HSM module](hsm.py) decorate HSM.encrypt() method with implemented decorator
3. Measure each encrypt function and total script execution time:

```shell script
=== cache_it ===> calculating new value of 'encrypt(HSM, banana)'
=== time_it ===> 'wrapper(banana)' duration '1.16'
'banana' encrypted is 'gAAAAABfTAFxA9Yivi0SJLgq1xNOjgRNJL1INvR8XXLv02768uJ3sbQWm4nYJRU1nO8O725P941ZFIxy5BK8UmO0TH_1M1QTEg=='

=== cache_it ===> calculating new value of 'encrypt(HSM, apple)'
=== time_it ===> 'wrapper(apple)' duration '1.66'
'apple' encrypted is 'gAAAAABfTAFy93CCFEndXgPh-ZITW_4-uwqyyj-yibcVNVSLnkd7WOp2YcYSh21zX5W-fjNvvh4_5w63GiDyLGmLybwK2T0NUw=='

=== cache_it ===> using already calculated value of 'encrypt(HSM, banana)'
=== time_it ===> 'wrapper(banana)' duration '0.00'
'banana' encrypted is 'gAAAAABfTAFxA9Yivi0SJLgq1xNOjgRNJL1INvR8XXLv02768uJ3sbQWm4nYJRU1nO8O725P941ZFIxy5BK8UmO0TH_1M1QTEg=='

=== cache_it ===> calculating new value of 'encrypt(HSM, orange)'
=== time_it ===> 'wrapper(orange)' duration '1.07'
'orange' encrypted is 'gAAAAABfTAFzi9Vlh7CKhr4fPRvP8ry4Zh4OXwI_yVF6R0jqHb4hWsQ5jMvtYkT2hK0n0iJ2eEwHnqQ0Wa00JIIG2jH9hNSsUQ=='

=== cache_it ===> calculating new value of 'encrypt(HSM, pear)'
=== time_it ===> 'wrapper(pear)' duration '1.26'
'pear' encrypted is 'gAAAAABfTAF11BG0euFyPSwa9LHs0ufDlLozlENq1Mg5Oys3AXnhrHPNrWuT5HW1kGVWEtRpfUngjCpECcI3DZmiSBuCp9m2-Q=='

=== cache_it ===> using already calculated value of 'encrypt(HSM, apple)'
=== time_it ===> 'wrapper(apple)' duration '0.00'
'apple' encrypted is 'gAAAAABfTAFy93CCFEndXgPh-ZITW_4-uwqyyj-yibcVNVSLnkd7WOp2YcYSh21zX5W-fjNvvh4_5w63GiDyLGmLybwK2T0NUw=='

=== cache_it ===> using already calculated value of 'encrypt(HSM, pear)'
=== time_it ===> 'wrapper(pear)' duration '0.00'
'pear' encrypted is 'gAAAAABfTAF11BG0euFyPSwa9LHs0ufDlLozlENq1Mg5Oys3AXnhrHPNrWuT5HW1kGVWEtRpfUngjCpECcI3DZmiSBuCp9m2-Q=='

=== cache_it ===> using already calculated value of 'encrypt(HSM, orange)'
=== time_it ===> 'wrapper(orange)' duration '0.00'
'orange' encrypted is 'gAAAAABfTAFzi9Vlh7CKhr4fPRvP8ry4Zh4OXwI_yVF6R0jqHb4hWsQ5jMvtYkT2hK0n0iJ2eEwHnqQ0Wa00JIIG2jH9hNSsUQ=='

=== cache_it ===> using already calculated value of 'encrypt(HSM, apple)'
=== time_it ===> 'wrapper(apple)' duration '0.00'
'apple' encrypted is 'gAAAAABfTAFy93CCFEndXgPh-ZITW_4-uwqyyj-yibcVNVSLnkd7WOp2YcYSh21zX5W-fjNvvh4_5w63GiDyLGmLybwK2T0NUw=='

=== cache_it ===> using already calculated value of 'encrypt(HSM, pear)'
=== time_it ===> 'wrapper(pear)' duration '0.00'
'pear' encrypted is 'gAAAAABfTAF11BG0euFyPSwa9LHs0ufDlLozlENq1Mg5Oys3AXnhrHPNrWuT5HW1kGVWEtRpfUngjCpECcI3DZmiSBuCp9m2-Q=='

=== cache_it ===> using already calculated value of 'encrypt(HSM, banana)'
=== time_it ===> 'wrapper(banana)' duration '0.00'
'banana' encrypted is 'gAAAAABfTAFxA9Yivi0SJLgq1xNOjgRNJL1INvR8XXLv02768uJ3sbQWm4nYJRU1nO8O725P941ZFIxy5BK8UmO0TH_1M1QTEg=='

=== cache_it ===> using already calculated value of 'encrypt(HSM, apple)'
=== time_it ===> 'wrapper(apple)' duration '0.00'
'apple' encrypted is 'gAAAAABfTAFy93CCFEndXgPh-ZITW_4-uwqyyj-yibcVNVSLnkd7WOp2YcYSh21zX5W-fjNvvh4_5w63GiDyLGmLybwK2T0NUw=='

python3 client.py  0,11s user 0,02s system 2% cpu 5,279 total
```

* only first invocation of encryption function with some defined text takes time, all consecutive invocations are almost instant
* total execution time decreased from ~20 to ~5 seconds.

### Step 4 (optional, use memoization function from standard library)

Replace self-written caching decorator with [functools.lru_cache()](https://docs.python.org/3/library/functools.html#functools.lru_cache) from standard library.

What are the benefits of using `functools.lru_cache()` over self-written caching decorator?

## Additional materials

* [Practical decorators](https://www.youtube.com/watch?v=MjHpMCIvwsY)
