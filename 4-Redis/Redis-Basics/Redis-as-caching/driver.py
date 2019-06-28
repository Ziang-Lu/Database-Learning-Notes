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


def simply_query() -> None:
    """
    Simple query.
    :return: None
    """
    r = redis.Redis()
    print(r.ping())

    # Get all the products with price between [200, 500]
    print(r.zrangebyscore('product_price', min=200, max=500, withscores=True))


def main():
    # MySQL setup
    parser = argparse.ArgumentParser(description='MySQL setup')
    parser.add_argument('-u', '--user', help='User to login', default='root')
    parser.add_argument(
        '-p', '--password', help='Password for the user to login',
        default='password'
    )

    args = parser.parse_args()
    user = args.user
    pwd = args.password

    mysql_setup(user, pwd)

    # Redis setup
    redis_setup()

    # Do a simply query
    simply_query()


if __name__ == '__main__':
    main()
