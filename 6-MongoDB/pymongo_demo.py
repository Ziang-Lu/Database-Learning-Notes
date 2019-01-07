#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple usage demo of pymongo library (driver).

Before running this script, first make sure MongoDB server is up and running.
"""

__author__ = 'Ziang Lu'

from datetime import datetime

import pymongo


def init_db() -> None:
    """
    Initialize a DB by inserting documents.
    :return: None
    """
    # Connect to MongoDB server
    conn = pymongo.MongoClient()
    # Select "test" database; create "test" database if it doesn't exist
    test_db = conn.test
    # Select "posts" collection; create "posts" collection if it doesn't exist
    posts = test_db.posts

    # Insert documents
    first_post = {
        'author': 'Ziang',
        'title': 'First Blog',
        'content': 'What to write...',
        'tags': ['diary', 'python'],
        'date': datetime.now()
    }
    inserted_id = posts.insert_one(first_post).inserted_id
    print(f'Just inserted: {inserted_id}')
    inserted_ids = posts.insert_many([
        {
            'author': 'Mike',
            'title': 'Second Blog',
            'tags': ['diary'],
            'date': datetime.now()
        },
        {
            'author': 'Ziang',
            'title': 'Third Blog',
            'tags': ['diary'],
            'date': datetime.now()
        }
    ]).inserted_ids
    print(f'Just inserted: {inserted_ids}')

    print('Finished DB initialization')
    # Show all the collections in "test" database
    print(f'Existing collections: {test_db.list_collection_names()}')


def query_db() -> None:
    """
    Queries "test" DB.
    :return: None
    """
    conn = pymongo.MongoClient()
    test_db = conn.test
    posts = test_db.posts

    print(f"Documents with author 'Ziang': "
          f"{posts.count_documents({'author': 'Ziang'})}")
    for post in posts.find(
        {'author': 'Ziang'}, {'_id': False, 'tags': False, 'date': False}
    ):
        print(post)

    print()

    print("Same result sorted by 'title':")
    for post in posts.find(
        {'author': 'Ziang'}, {'_id': False, 'tags': False, 'date': False},
    ).sort('title'):
        print(post)


def test_index() -> None:
    """
    Tests index-related stuff.
    :return: None
    """
    conn = pymongo.MongoClient()
    test_db = conn.test
    posts = test_db.posts

    # Create index
    posts.create_index([('title', pymongo.ASCENDING)], unique=True)
    print(list(posts.index_information()))

    # Check index
    posts.insert_one({
        'author': 'Ziang',
        'title': 'Fourth Blog'
    })  # This is fine.

    posts.insert_one({
        'author': 'Ziang',
        'title': 'Fourth Blog'
    })  # DuplicateKeyError


def main():
    # init_db()
    # query_db()
    test_index()


if __name__ == '__main__':
    main()
