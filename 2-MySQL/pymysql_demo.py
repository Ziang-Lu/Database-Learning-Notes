#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple usage demo of mysql-connector library (driver).

Before running this script, first make sure MySQL server is up and running, and
create a MySQL database called "test":
> mysql -u root -p
(inside interactive shell) > create database test;
"""

import argparse
from typing import List, Tuple

import pymysql
from pymysql.cursors import DictCursor

DB_NAME = 'test'


def init_db(user: str, pwd: str) -> None:
    """
    Initialize a DB by inserting rows into it.
    :param user: str
    :param pwd: str
    :return: None
    """
    conn = pymysql.connect(user=user, password=pwd, database=DB_NAME)

    # Get the cursor
    with conn.cursor() as cursor:
        cursor.execute('''
        create table students (
            id integer primary key auto_increment,
            name varchar(20) not null,
            email varchar(100) not null,
            is_del boolean default false
        );
        ''')
        # Note that specifying autoincrement in MySQL is like above
        cursor.execute('''
        insert into students (name, email)
        values
            ('Adam', 'adam@gmail.com'),
            ('Bart', 'bart@gmail.com'),
            ('Lisa', 'lisa@gmail.com')
        ''')
        # Whenever we make changes to a DB, these changes will go into a
        # "transaction", and it will take effect only when we call conn.commit()
        # method.
        conn.commit()
        # If we close a connection or the code crashes without committing the
        # changes, the changes will be rolled back.

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

    # Always remember to close the connection
    conn.close()


def get_score_within(user: str, pwd: str, low: int,
                     high: int) -> List[Tuple[str]]:
    """
    Gets students and courses where score is within the given range, ordered by
    the score in ascending order.
    :param user: str
    :param pwd: str
    :param low: lower bound
    :param high: upper bound
    :return: list[tuple(str)]
    """
    print(f'List students and courses where score is within {low} and {high}, '
          f'ordered by the score in ascending order:')
    conn = pymysql.connect(
        user=user, password=pwd, database=DB_NAME, cursorclass=DictCursor
    )

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
        # Note that MySQL uses %s placeholder
        results = cursor.fetchall()

    # Always to remember to close the connection
    conn.close()

    return results


def main():
    parser = argparse.ArgumentParser(
        description='MySQL simple demo using mysql-connector'
    )

    parser.add_argument('-u', '--user', help='User to login', default='root')
    parser.add_argument(
        '-p', '--password', help='Password for the user to login',
        default='password'
    )

    args = parser.parse_args()

    user = args.user
    pwd = args.password

    init_db(user, pwd)
    print(get_score_within(user, pwd, low=60, high=80))


if __name__ == '__main__':
    main()

# Output:
# Finished DB initialization...
# List students and courses where score is within 60 and 80, ordered by the score in ascending order:
# [{'name': 'Lisa', 'courses.name': 'Intro to Computer Science'}, {'name': 'Bart', 'courses.name': 'Intro to Computer Science'}]
