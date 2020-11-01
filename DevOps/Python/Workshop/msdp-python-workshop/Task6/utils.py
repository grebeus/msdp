import logging
import random
import time


from functools import reduce


def params_to_str(*args, **kwargs):
    args_str = [str(a) for a in args]
    kwargs_str = [f"{k}={v}" for k, v in kwargs.items()]
    params = ", ".join(args_str + kwargs_str)
    return params


"""
Step 2.1. Write decorator to measure function execution time:
    * use `time.perf_counter()` as monothonic time source
"""
### Block implemented by student
### Block implemented by student


"""
Step 3.1. Write decorator to cache function output based on input arguments:
    * use dictionary as a cache data type
    * use positional arguments as a cache keys, ignore keyword arguments
"""
### Block implemented by student
### Block implemented by student


def tokens():
    result = reduce(
                list.__add__,
                [
                    [fruit]*random.randint(2,4)
                        for fruit in ['orange', 'apple', 'pear', 'banana']
                ]
    )
    random.shuffle(result)
    return result