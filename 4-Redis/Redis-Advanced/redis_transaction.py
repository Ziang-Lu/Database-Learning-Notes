#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple demo of Redis queued commands ("transaction").

For detailed explanation:
https://github.com/andymccurdy/redis-py#pipelines
"""

__author__ = 'Ziang Lu'

import redis


def redis_transaction() -> None:
    """
    Simulates a money transfer in a transaction.
    :return: None
    """
    r = redis.Redis()
    print(r.ping())

    r.set('ziang', 500)
    r.set('mama', 300)

    queue = r.pipeline()
    queue.decrby('ziang', 100)
    queue.incrby('mama', 100)
    try:
        queue.execute()
    except Exception as ex:
        print(f'{type(ex).__name__}: {ex}')

    print(r.mget('ziang', 'mama'))
    # Afterwards,
    # 'ziang' -> 400
    # 'mama' -> 400


def redis_transaction_error() -> None:
    """
    Simulates a money transfer in a transaction, but with an invalid command in
    the transaction.
    :return: None
    """
    r = redis.Redis()
    print(r.ping())

    queue = r.pipeline()
    queue.incrby('ziang', 100)
    queue.sadd('ziang', 'rocks')  # This is correct syntax, but invalid command that doesn't work.
    # Redis cannot detect these kinds of errors, and will queue that command.
    try:
        queue.execute()
    except Exception as ex:
        print(f'{type(ex).__name__}: {ex}')
    # ResponseError: Command # 2 (SADD ziang rocks) of pipeline caused error: WRONGTYPE Operation against a key holding the wrong kind of value

    print(r.get('ziang'))
    # Afterwards,
    # 'ziang' -> 500 (successfully incremented)


if __name__ == '__main__':
    redis_transaction()
    redis_transaction_error()
