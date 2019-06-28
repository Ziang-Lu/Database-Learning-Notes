#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Redis setup module.
"""

import redis


def redis_setup() -> None:
    """
    Redis setup.
    :return: None
    """
    r = redis.Redis()
    print(r.ping())

    # Start a transaction
    queue = r.pipeline()
    queue.hmset('PRODUCT:1000001', mapping={
        'name': 'AAAA',
        'description': 'Description of AAAA',
        'price': 100
    })
    queue.hmset('PRODUCT:1000002', mapping={
        'name': 'BBBB',
        'description': 'Description of BBBB',
        'price': 200
    })
    queue.hmset('PRODUCT:1000003', mapping={
        'name': 'CCCC',
        'description': 'Description of CCCC',
        'price': 200
    })
    queue.hmset('PRODUCT:1000100', mapping={
        'name': 'XXYZ',
        'description': 'Description of XXYZ',
        'price': 500
    })
    queue.execute()

    r.zadd('product_price', mapping={
        'PRODUCT:1000001': 100,
        'PRODUCT:1000002': 200,
        'PRODUCT:1000003': 200,
        'PRODUCT:1000100': 500
    })
