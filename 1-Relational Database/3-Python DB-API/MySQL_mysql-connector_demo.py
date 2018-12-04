#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple usage demo of mysql-connector library (driver).
"""

__author__ = 'Ziang Lu'

from typing import List

import mysql.connector as sql

DB_NAME = 'test'


def init_db() -> None:
    # TODO: Remove any existing DB?

    # TODO: figure out the correct and succesful way of connecting to MySQL
    with sql.connect('DB_NAME') as conn:
        # TODO: figure out whether it will create the DB if not existing?

        # Get the cursor
        cursor = conn.cursor()

        # Create a "score" table
        cursor.execute('''
        create table scores (
            id varchar(20),
            name varchar(20),
            score int,
            primary key(id)
        )
        ''')
        # Note that specifying a primary key in MySQL is like above
        cursor.execute('''
        insert into scores values
            ('A-001', 'Adam', 95),
            ('A-002', 'Bart', 62),
            ('A-003', 'Lisa', 78)
        ''')
        print('Finished DB initialization...')
        print(f'Number of inserted rows: {cursor.rowcount}')

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
    with sql.connect(DB_NAME) as conn:
        # Get the cursor
        cursor = conn.cursor()

        cursor.execute('''
        select name
        from scores
        where score between %s and %s
        order by score
        ''', (low, high))  # Provide arguments to SQL query
        # Note that the placeholder used in MySQL is "%s"
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
