#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple usage demo of psycopg2 library (driver).

Before running this script, first create a MySQL database called "test":
> createdb test
"""

__author__ = 'Ziang Lu'

from typing import List, Tuple

import psycopg2

DB_NAME = 'test'


def init_db() -> None:
    """
    Initialize a DB by inserting rows into it.
    :return: None
    """
    with psycopg2.connect(dbname=DB_NAME) as conn:
        # Get the cursor
        with conn.cursor() as cursor:
            cursor.execute('''
            create table students (
                id serial primary key,
                name varchar(20) not null,
                email varchar(100) not null,
                is_del boolean default false
            );
            ''')
            # Note that specifying autoincrement in PostgreSQL is like above, by
            # by using "serial" data type
            cursor.execute('''
            insert into students (name, email)
            values
                ('Adam', 'adam@gmail.com'),
                ('Bart', 'bart@gmail.com'),
                ('Lisa', 'lisa@gmail.com')
            ''')
            # Whenever we make changes to a DB, these changes will go into a
            # "transaction", and it will take effect only when we call
            # conn.commit()
            # method.
            conn.commit()
            # If we close a connection or the code crashes without committing
            # the changes, the changes will be rolled back.

            cursor.execute('''
            create table courses (
                id char(5) primary key,
                name varchar(30) not null,
                is_del boolean default false
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
                is_del boolean default false,
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


def get_score_within(low: int, high: int) -> List[Tuple[str]]:
    """
    Gets students and courses where score is within the given range, ordered by
    the score in ascending order.
    :param low: lower bound
    :param high: upper bound
    :return: list[tuple(str)]
    """
    print(f'List students and courses where score is within {low} and {high}, '
          f'ordered by the score in ascending order:')
    with psycopg2.connect(dbname=DB_NAME) as conn:
        # Get the cursor
        with conn.cursor() as cursor:
            cursor.execute('''
            select students.name, courses.name
            from scores
            join students on scores.student_id = students.id
            join courses on scores.course_id = courses.id
            where scores.score between %s and %s
            order by scores.score
            ''', (low, high))
            # Note that PostgreSQL uses %s placeholder
            results = cursor.fetchall()
    return results


def main():
    # init_db()
    print(get_score_within(low=60, high=80))


if __name__ == '__main__':
    main()

# Output:
# Finished DB initialization
# List students and courses where score is within 60 and 80, ordered by the score in ascending order:
# [('Lisa', 'Intro to Computer Science'), ('Bart', 'Intro to Computer Science')]
