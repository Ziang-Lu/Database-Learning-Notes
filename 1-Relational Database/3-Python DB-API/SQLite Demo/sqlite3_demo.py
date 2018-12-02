#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple usage demo of sqlite3 library (driver).
"""

__author__ = 'Ziang Lu'

import os
import sqlite3
from typing import List

DB_NAME = 'sample.db'


def init_db() -> None:
    """
    Creates a DB and insert rows into it.
    :return: None
    """
    # Remove any existing DB
    full_path = os.path.join(os.path.dirname(__file__), DB_NAME)
    if os.path.isfile(full_path):
        os.remove(full_path)

    # Establish a connection to the DB
    with sqlite3.connect(DB_NAME) as conn:
        # If the DB doesn't exist, it will be created.

        # Get the cursor
        cursor = conn.cursor()

        # Create a 'user' table
        cursor.execute('''
        create table scores (
            id varchar(20) primary key,
            name varchar(20),
            score int
        )
        ''')  # TODO: figure out 'primary key'?
        # Insert 3 rows to 'user' table
        cursor.execute('''
        insert into scores values
            ('A-001', 'Adam', 95),
            ('A-002', 'Bart', 62),
            ('A-003', 'Lisa', 78)
        ''')
        print('Finished DB initialization...')
        print(f'Number of inserted rows: {cursor.rowcount}')
        # TODO: figure out cursor.rowcount only reflects the affected rows

        # Always remember to close the cursor
        cursor.close()

        # Whenever we make changes to a DB, these changes will go into a
        # "trasaction", and it will take effect only when we call conn.commit()
        # method.
        conn.commit()
        # If we close a connection or the code crashes without commiting the
        # changes, the changes will be rolled back.


def get_score_within(low: int, high: int) -> List[str]:
    """
    Gets students whose score is within the given range, ordered by the score in
    ascending order.
    :param low: lower bound
    :param high: upper bound
    :return: list[str]
    """
    print(f'List students whose score is within {low} and {high}, ordered by '
          f'the score in ascending order:')
    with sqlite3.connect(DB_NAME) as conn:
        # Get the cursor
        cursor = conn.cursor()

        # Execute the query
        cursor.execute('''
        select name
        from scores
        where score between ? and ?
        order by score
        ''', (low, high))  # Provide arguments to SQL query
        # Fetch all the results
        results = cursor.fetchall()
        desired_results = list(map(lambda x: x[0], results))

        # Always remember to close the cursor
        cursor.close()

        return desired_results


def main():
    init_db()
    print(get_score_within(low=60, high=80))


if __name__ == '__main__':
    main()

# Output:
# Finished DB initialization...
# Number of inserted rows: 3
# List students whose score is within 60 and 80, ordered by the score in ascending order:
# ['Bart', 'Lisa']
