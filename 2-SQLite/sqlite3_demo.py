#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple usage demo of sqlite3 library (driver).
"""

__author__ = 'Ziang Lu'

import argparse
import os
import sqlite3
from typing import List, Tuple


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
        create table students (
            id integer primary key autoincrement,
            name varchar(20) not null,
            email varchar(100) not null,
            is_del integer default 0
        );
        ''')
        # Note that specifying autoincrement in SQLite is like above
        cursor.execute('''
        insert into students (name, email)
        values
            ('Adam', 'adam@gmail.com'),
            ('Bart', 'bart@gmail.com'),
            ('Lisa', 'lisa@gmail.com')
        ''')
        # Whenever we make changes to a DB, these changes will go into a
        # "transaction", and it will take effect only when we call
        # conn.commit() method.
        conn.commit()
        # If we close a connection or the code crashes without committing
        # the changes, the changes will be rolled back.

        cursor.execute('''
        create table courses (
            id char(5) primary key,
            name varchar(30) not null
            is_del integer default 0
        );
        ''')
        cursor.execute('''
        insert into courses
        values
            ('CS101', 'Intro to Computer Science'),
            ('CS105', 'Data Structures')
        ''')
        conn.commit()

        cursor.execute('''
        create table scores (
            student_id integer references students(id),
            course_id char(5) references courses(id),
            score integer,
            is_del integer default 0,
            primary key(student_id, course_id)
        );
        ''')
        cursor.execute('''
        insert into scores
        values
            (1, 'CS101', 55),
            (2, 'CS101', 80),
            (3, 'CS101', 70),
            (1, 'CS105', null),
            (2, 'CS105', 95),
            (3, 'CS105', 90)
        ''')
        conn.commit()

        print('Finished DB initialization...')

        # Always remember to close the cursor
        cursor.close()


def get_score_within(db_filename: str, low: int, high: int) -> List[Tuple[str]]:
    """
    Gets students and courses where score is within the given range, ordered by
    the score in ascending order.
    :param db_filename: str
    :param low: lower bound
    :param high: upper bound
    :return: list[tuple(str)]
    """
    print(f'List students and courses where score is within {low} and {high}, '
          f'ordered by the score in ascending order:')
    with sqlite3.connect(db_filename) as conn:
        # Get the cursor
        cursor = conn.cursor()

        cursor.execute('''
        select students.name, courses.name
        from scores
        join students on scores.student_id = students.id
        join courses on scores.course_id = courses.id
        where scores.score between ? and ?
        order by scores.score
        ''', (low, high))
        # Note that SQLite uses ? placeholder
        results = cursor.fetchall()

        # Always remember to close the cursor
        cursor.close()

    return results


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
# List students and courses where score is within 60 and 80, ordered by the score in ascending order:
# [('Lisa', 'Intro to Computer Science'), ('Bart', 'Intro to Computer Science')]
