#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple demo to use Redis between the application layer and the actual DB (here,
MySQL) as a cache.

Before running this script, first make sure:
1. MySQL server is up and running, and create a MySQL database called "test":
   > mysql -u root -p
   (inside interactive shell) > create database test;
2. Redis server is up and running.
"""

import argparse

import redis

from mysql_setup import mysql_setup
from redis_setup import redis_setup


def query_products_between(min_price: int, max_price: int) -> None:
    """
    Simple query to get all the products with price between the given range.
    Rather than directly querying from the actual database (MySQL), query from
    cache (Redis).
    :return: None
    """
    r = redis.Redis()
    print(f'Query connected to Redis (cache)? {r.ping()}')

    print(r.zrangebyscore(
        'product_price', min=min_price, max=max_price, withscores=True
    ))


if __name__ == '__main__':
    # MySQL setup
    parser = argparse.ArgumentParser(description='MySQL setup')
    parser.add_argument('-u', '--user', help='User to login', default='root')
    parser.add_argument(
        '-p', '--password',
        help='Password for the user to login',
        default='password'
    )

    args = parser.parse_args()
    user = args.user
    pwd = args.password

    mysql_setup(user, pwd)

    # Redis setup
    redis_setup(mysql_user=user, mysql_pwd=pwd)

    # Do a simply query
    query_products_between(min_price=200, max_price=500)
