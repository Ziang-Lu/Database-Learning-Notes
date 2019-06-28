#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MySQL setup module.
"""

import argparse

import pymysql


def mysql_setup(user: str, pwd: str) -> None:
    """
    MySQL setup.
    :param user: str
    :param pwd: str
    :return: None
    """
    conn = pymysql.connect(user=user, password=pwd, database='test')

    with conn.cursor() as cursor:
        cursor.execute('''
        create table product (
            id integer primary key,
            name varchar(30) not null,
            description text,
            price integer not null
        );
        ''')
        conn.commit()

        cursor.execute('''
        insert into product (id, name, description, price)
        values
            (1000001, 'AAAA', 'Description of AAAA', 100),
            (1000002, 'BBBB', 'Description of BBBB', 200),
            (1000003, 'CCCC', 'Description of CCCC', 200),
            (1000100, 'XXYZ', 'Description of XXYZ', 500)
        ''')
        conn.commit()

    conn.close()
