#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Interface with DB module.
"""

from datetime import datetime
from typing import Iterator, Tuple

import bleach
import psycopg2


def init_db() -> None:
    """
    Initializes the DB by creating "posts" table.
    :return: None
    """
    with psycopg2.connect('dbname=forum') as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
            create table if not exists posts (
                id serial primary key,
                content text not null,
                time timestamp default now()
            )
            ''')
            conn.commit()


def get_posts() -> Iterator[Tuple[str, datetime]]:
    """
    Returns the posts (most recent first) from the DB.
    :return: iterable(tuple)
    """
    # return reversed(posts)

    with psycopg2.connect('dbname=forum') as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
            select content, time
            from posts
            order by time
            ''')
            results = cursor.fetchall()
    return reversed(results)


# Script attack:
# If we provide the following post:
#
# <script>
# setTimeout(function() {
#     var tt = document.getElementById('content');
#     tt.value = "<h2 style='color: #FF6699; font-family: Comic Sans MS'>Spam, spam, spam, spam,<br>Wonderful spam, glorious spam!</h2>";
#     tt.form.submit();
# }, 2500);
# </script>
#
# Then
# 1. The post will be successfully saved to DB.
# 2. The browser will get all the posts back from DB for display.
# 3. The browser will execute the above JavaScript code, which create a spam
#    post every 2.5 seconds.
#
# To protect our application from script attack, we use a library called
# "bleach" to sanitize the HTML code.


def add_post(content: str) -> None:
    """
    Adds a new post with the current timestamp to the DB.
    :param content: str
    :return: None
    """
    # posts.append((content, datetime.now()))

    with psycopg2.connect('dbname=forum') as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
            insert into posts (content)
            values (%s)
            ''', (bleach.clean(content),))  # Input sanitization
            conn.commit()
