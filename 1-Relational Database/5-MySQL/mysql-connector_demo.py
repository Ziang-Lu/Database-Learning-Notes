#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple usage demo of mysql-connector library (driver).

Before running this script, first create a MySQL database called "test":
> mysql -u root -p
> create database test
"""

__author__ = 'Ziang Lu'

import argparse
from typing import List

import mysql.connector as sql

DB_NAME = 'test'


def init_db(user: str, pwd: str) -> None:
    """
    Initialize a DB by inserting rows into it.
    :param user: str
    :param pwd: str
    :return: None
    """
    conn = sql.connect(user=user, password=pwd, database=DB_NAME)

    # Get the cursor
    with conn.cursor() as cursor:
        # Remove any existing DB
        cursor.execute('''
        drop table if exists %s
        ''', (DB_NAME,))  # # Provide arguments to SQL query

        # Whenever we make changes to a DB, these changes will go into a
        # "transaction", and it will take effect only when we call conn.commit()
        # method.
        conn.commit()
        # If we close a connection or the code crashes without committing the
        # changes, the changes will be rolled back.

        cursor.execute('''
        create table scores (
            id int not null auto_increment,
            name varchar(20) not null,
            score int,
            primary key(id)
        )
        ''')
        # Note that specifying a primary key in MySQL is like above

        cursor.execute('''
        insert into scores (name, score)
        values
            ('Adam', 95),
            ('Bart', 62),
            ('Lisa', 78)
        ''')
        print('Finished DB initialization...')
        print(f'Number of inserted rows: {cursor.rowcount}')

        conn.commit()

    # Always remember to close the connection
    conn.close()


def get_score_within(user: str, pwd: str, low: int, high: int) -> List[str]:
    """
    Gets students whose score is within the given range, ordered by the score in
    ascending order.
    :param user: str
    :param pwd: str
    :param low: lower bound
    :param high: upper bound
    :return: list[str]
    """
    print(f'List students whose score is within {low} and {high}, ordered by '
          f'the score in ascending order:')
    conn = sql.connect(user=user, password=pwd, database=DB_NAME)

    # Get the cursor
    with conn.cursor() as cursor:
        cursor.execute('''
        select name
        from scores
        where score between %s and %s
        order by score
        ''', (low, high))  # Provide arguments to SQL query
        # Note that the placeholder used in MySQL is "%s"
        results = cursor.fetchall()
        desired_results = list(map(lambda x: x[0], results))

    # Always to remember to close the connection
    conn.close()

    return desired_results


def main():
    parser = argparse.ArgumentParser(
        description='MySQL simple demo using mysql-connector'
    )

    parser.add_argument('-u', '--user', help='User to login')
    parser.add_argument('-p', '--password',
                        help='Password for the user to login')

    args = parser.parse_args()

    user = args.user
    pwd = args.password

    init_db(user, pwd)
    print(get_score_within(user, pwd, low=60, high=80))


if __name__ == '__main__':
    main()

# Output:
# Finished DB initialization...
# Number of inserted rows: 3
# List students whose score is within 60 and 80, ordered by the score in ascending order:
# ['Bart', 'Lisa']
