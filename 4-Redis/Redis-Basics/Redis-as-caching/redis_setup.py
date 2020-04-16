#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Redis setup module.
"""

import pymysql
import redis


def redis_setup(mysql_user: str, mysql_pwd: str) -> None:
    """
    Redis setup.
    :param mysql_user: str
    :param mysql_pwd: str
    :return: None
    """
    conn = pymysql.connect(user=mysql_user, password=mysql_pwd, database='test')

    with conn.cursor() as cursor:
        cursor.execute('''
        select *
        from product
        ''')
        products = cursor.fetchall()

        r = redis.Redis()
        print(r.ping())

        # Start a command queue (Similar to a transaction, but allow partial
        # success, and cannot rollback)
        queue = r.pipeline()
        for product in products:
            key = f'PRODUCT:{product[0]}'
            queue.hmset(key, mapping={
                'name': product[1],
                'description': product[2],
                'price': product[3]
            })
        # Execute the command queue
        queue.execute()

        product_prices = {
            f'PRODUCT:{product[0]}': product[3] for product in products
        }
        r.zadd('product_price', mapping=product_prices)

    conn.close()
