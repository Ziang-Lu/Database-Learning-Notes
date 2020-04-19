#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Distributed locking mechanism.
Instead, this time we use context manager, such that the distributed lock
becomes more usable and portable.
"""

import time
from contextlib import contextmanager

import redis
from redlock import MultipleRedlockException, Redlock

LOCK_KEY = 'lock'
BUSINESS_RUNTIME = 30  # in seconds


def set_up() -> None:
    """
    Stock setup.
    :return: None
    """
    r = redis.Redis()

    r.set('stock', 10)


@contextmanager
def naive_distributed_lock(wait_interval: int, business_runtime: int):
    """
    Naive distributed locking implementation.
    :param wait_interval: int
    :param business_runtime: int
    :return:
    """
    r = redis.Redis()

    client_id = r.client_id()
    result = r.setnx(LOCK_KEY, client_id)
    while not result:
        time.sleep(wait_interval)
        result = r.setnx(LOCK_KEY, client_id)

    r.expire(LOCK_KEY, business_runtime)

    try:
        yield r  # Business codes
    finally:
        lock_val = r.get(LOCK_KEY)
        if lock_val != client_id:
            raise Exception('Business codes timed out.')
        r.delete(LOCK_KEY)


def lightning_order(waiting_interval: int, business_runtime) -> None:
    """
    Lightning order.
    :param waiting_interval: int
    :param business_runtime: int
    :return: None
    """
    # with naive_distributed_lock(waiting_interval, business_runtime=30) as r:
    #     remaining = int(r.get('stock'))
    #     if remaining > 0:
    #         r.set('stock', str(remaining - 1))
    #         print(f'Deducted stock, {remaining - 1} remaining')
    #     else:
    #         print('Failed to deduct stock')

    with redlock(business_runtime) as r:
        remaining = int(r.get('stock'))
        if remaining > 0:
            r.set('stock', str(remaining - 1))
            print(f'Deducted stock, {remaining - 1} remaining')
        else:
            print('Failed to deduct stock')


@contextmanager
def redlock(business_runtime: int):
    """
    Distributed lock with Redlock algorithm.
    :param business_runtime: int
    :return:
    """
    r = redis.Redis()

    dlm = Redlock([{
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }, ])  # Stands for "distributed lock manager"

    lock = None
    try:
        # Try to acquire the lock
        lock = dlm.lock(LOCK_KEY, business_runtime)
        yield r  # Business codes
    except MultipleRedlockException as e:
        print(e)
    finally:
        # Release the lock
        dlm.unlock(lock)
