#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple usage of redis library (driver).

Before running this script, first make sure Redis server is up and running.
"""

__author__ = 'Ziang Lu'

import redis


# Connect to Redis DB-2
r = redis.Redis(db=2)
# r provides a Python interface to all Redis commands.
print(r.ping())  # This method is used to test if the connection is still alive

print(f"Set Record: {r.set('key', 'foo', nx=True)}")
print(f"Get Record: {r.get('key')}")

# Output:
# Redis<ConnectionPool<Connection<host=localhost,port=6379,db=2>>>
# Set Record: True
# Get Record: b'foo'
