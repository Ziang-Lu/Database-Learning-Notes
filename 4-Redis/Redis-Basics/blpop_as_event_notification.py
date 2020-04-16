#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Scenario:
Using blocking list operations, it's possible to mount different blocking
primitives.
For instance, for some application you may need to block waiting for elements
into a Redis Set, so that as far as a new element is added to the set, it is
possible to retrieve it without resorting to polling.
=> This would require a blocking version of "spop", which is not available.

However, we can use a helper indicator List and its "blpop" operation as event
notification.

Before running this script, first make sure Redis server is up and running.
"""

__author__ = 'Ziang Lu'

import time
from multiprocessing import Process

import redis


def set_element_processing(set_key: str, indicator_list: str) -> None:
    """
    Process function to process set elements, using a helper indicator List and
    its "blpop" operation as event notification.
    :param set_key: str
    :param indicator_list: str
    :return: None
    """
    r = redis.Redis()
    print(r.ping())

    while True:
        r.blpop(indicator_list)
        while r.scard(set_key) > 0:
            elem = r.spop(set_key)
            print(f'Processing {elem}...')


def add_set_elements(set_key: str, indicator_list: str) -> None:
    """
    Process function to add elements to set.
    :param set_key: str
    :param indicator_list: str
    :return: None
    """
    r = redis.Redis()
    print(r.ping())

    # Start a transaction
    queue = r.pipeline()
    queue.sadd(set_key, 'Judy')
    queue.sadd(set_key, 'Vance')
    queue.sadd(set_key, 'Jessie')
    queue.lpush(indicator_list, 'Notification')
    # Commit the transaction
    queue.execute()


if __name__ == '__main__':
    set_key = 'students'
    indicator_list = 'indicator'
    p1 = Process(
        target=set_element_processing, args=(set_key, indicator_list)
    )
    p1.start()
    time.sleep(3)

    for _ in range(3):
        p = Process(
            target=add_set_elements, args=(set_key, indicator_list)
        )
        p.start()
        time.sleep(3)

    # Manually kill the processing process
    p1.terminate()

# Output:
# True
# True
# Processing b'Jessie'...
# Processing b'Judy'...
# Processing b'Vance'...
# True
# Processing b'Judy'...
# Processing b'Jessie'...
# Processing b'Vance'...
# True
# Processing b'Vance'...
# Processing b'Judy'...
# Processing b'Jessie'...
