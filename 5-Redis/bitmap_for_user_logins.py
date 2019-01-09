#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Instructions:
Combining "setbit" and "getbit", we can use a string as an O(1) random-access
array.
Using strings (together as a bitmap) to keep track of user logins and find
active users

We can keep track of user logins per day using a string:
Assume there are 5,000,000 users, we can have a string of length 5,000,000 bits (= 625,000 bytes =610.35 KB) to represent the user logins per day:

"00000100011110000101......001010"  # 5,000,000 in total (for 01/08/2019)

(-> Active user: 7 consecutive logins in the last week)
To find the active users, we just need to stack the 7 strings of last week
together:

"00000100011110000101......001010"  # 5,000,000 in total (for 01/02/2019)
...
"00100100011010010101......001010"  # 5,000,000 in total (for 01/07/2019)
"00010100011101000101......100010"  # 5,000,000 in total (for 01/08/2019)

Then, we can do an "AND" operation on the 7 strings:

> bitop AND result mon tue wed thu fri sat sun

In result, a "1" represents that user has 7 consecutive logins in the last week,
which means that he/she is an active user.

However, this approach can only record the logins for distinct users, but not
person-time (人次).


Before running this script, first make sure Redis server is up and running.
"""

__author__ = 'Ziang Lu'

import random
from typing import List

import redis

N_LOGIN_PER_DAY_MAX = 200000
N_LOGIN_PER_DAY_MIN = 100000
N_USER = 5000000
SELECTED_DB = 2


def new_day(day: str) -> None:
    """
    Initializes a bitmap for the given day.
    :param day: str
    :return: None
    """
    # Connect to the selected Redis DB
    r = redis.Redis(db=SELECTED_DB)
    # r provies a Python interface to all Redis commands
    print(r.ping())  # This method is used to test if the connection is still alive

    # Create a long-enough bitmap for the given day, where each offset (bit)
    # represents a user
    r.setbit(day, N_USER, 0)


def simulate_one_day(day: str) -> None:
    """
    Simulates user logins for the given day.
    :param day: str
    :return: None
    """
    r = redis.Redis(db=SELECTED_DB)
    print(r.ping())

    for _ in range(random.randint(N_LOGIN_PER_DAY_MIN, N_LOGIN_PER_DAY_MAX)):
        r.setbit(day, random.randint(0, N_USER), 1)
    print(f'Number of set bits: {r.bitcount(day, start=0, end=-1)}')


def find_active_users(days: List[str]) -> None:
    """
    Finds the number of active users.
    :param days: list[str]
    :return: None
    """
    r = redis.Redis(db=SELECTED_DB)
    print(r.ping())

    r.bitop('AND', 'result', *days)
    print(f"Number of active users: {r.bitcount('result', start=0, end=-1)}")


def main():
    days = ['mon', 'tue', 'wed']
    for day in days:
        new_day(day)
        simulate_one_day(day)
    find_active_users(days)


if __name__ == '__main__':
    main()
