#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple usage demo of sqlite3 library (driver).
"""

__author__ = 'Ziang Lu'

import argparse
import os
import sqlite3
from typing import List


def init_db(db_filename: str) -> None:
    """
    Creates a DB and insert rows into it.
    :param db_filename: str
    :return: None
    """
    # Remove any existing DB
    full_path = os.path.join(os.path.dirname(__file__), db_filename)
    if os.path.isfile(full_path):
        os.remove(full_path)

    with sqlite3.connect(db_filename) as conn:
        # If the DB doesn't exist, it will be created.

        # Get the cursor
        cursor = conn.cursor()

        cursor.execute('''
        create table scores (
            id int primary key,
            name varchar(20) not null,
            score int
        )
        ''')
        # Note that specifying a primary key in SQLite is like above
        cursor.execute('''
        insert into scores (name, score)
        values
            ('Adam', 95),
            ('Bart', 62),
            ('Lisa', 78)
        ''')
        print('Finished DB initialization...')
        print(f'Number of inserted rows: {cursor.rowcount}')

        # Whenever we make changes to a DB, these changes will go into a
        # "transaction", and it will take effect only when we call
        # conn.commit() method.
        conn.commit()
        # If we close a connection or the code crashes without committing
        # the changes, the changes will be rolled back.

        # Always remember to close the cursor
        cursor.close()


def get_score_within(db_filename: str, low: int, high: int) -> List[str]:
    """
    Gets students whose score is within the given range, ordered by the score in
    ascending order.
    :param db_filename: str
    :param low: lower bound
    :param high: upper bound
    :return: list[str]
    """
    print(f'List students whose score is within {low} and {high}, ordered by '
          f'the score in ascending order:')
    with sqlite3.connect(db_filename) as conn:
        # Get the cursor
        cursor = conn.cursor()

        cursor.execute('''
        select name
        from scores
        where score between ? and ?
        order by score
        ''', (low, high))  # Provide arguments to SQL query
        # Note that the placeholder used in SQLite is "?"
        results = cursor.fetchall()
        desired_results = list(map(lambda x: x[0], results))

        # Always remember to close the cursor
        cursor.close()

    return desired_results


def main():
    parser = argparse.ArgumentParser(
        description='SQLite simple demo using sqlite3'
    )

    parser.add_argument('--database', help='Name of the database to use',
                        default='test')

    args = parser.parse_args()

    db_name = args.database
    db_filename = db_name + '.db'

    init_db(db_filename)
    print(get_score_within(db_filename, low=60, high=80))


if __name__ == '__main__':
    main()

# Output:
# Finished DB initialization...
# Number of inserted rows: 3
# List students whose score is within 60 and 80, ordered by the score in ascending order:
# ['Bart', 'Lisa']
