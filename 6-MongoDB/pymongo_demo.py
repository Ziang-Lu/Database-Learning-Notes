#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple usage demo of pymongo library (driver).

Before running this script, first make sure MongoDB server is up and running.
"""

__author__ = 'Ziang Lu'

from datetime import datetime

from pymongo import ASCENDING, MongoClient


def init_db() -> None:
    """
    Initialize a DB by inserting documents.
    :return: None
    """
    # Connect to MongoDB server
    cli = MongoClient()
    print(cli)
    # Select "test" database; create "test" database if it doesn't exist
    db = cli.test
    print(db)
    # Select "posts" collection; create "posts" collection if it doesn't exist
    posts = db.posts
    print(posts)

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
    print(f'Existing collections: {db.list_collection_names()}')


def query_db() -> None:
    """
    Queries "test" DB.
    :return: None
    """
    cli = MongoClient()
    db = cli.test
    posts = db.posts

    print(f"Documents with author 'Ziang': "
          f"{posts.count_documents({'author': 'Ziang'})}")
    for post in posts.find(
            filter={'author': 'Ziang'},
            projection={'_id': False, 'tags': False, 'date': False}
    ):
        print(post)

    print("Same result sorted by 'title':")
    for post in posts.find(
            filter={'author': 'Ziang'},
            projection={'_id': False, 'tags': False, 'date': False},
    ).sort('title', direction=ASCENDING):
        print(post)


def update_db() -> None:
    """
    Updates the DB by updating the documents.
    :return: None
    """
    cli = MongoClient()
    db = cli.test
    posts = db.posts

    update_result = posts.update_many(
        filter={'author': 'Ziang'}, update={'$set': {'rank': 1}}
    )
    print(f'Number of updated documents: {update_result.modified_count}')


def test_index() -> None:
    """
    Tests index-related stuff.
    :return: None
    """
    cli = MongoClient()
    db = cli.test
    posts = db.posts

    # Create index
    posts.create_index([('title', ASCENDING)], unique=True)
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
    init_db()

    # Output:
    # MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True)
    # Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'test')
    # Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'test'), 'posts')
    # Just inserted: ObjectId(5c341c987cb9471ee3934d71)
    # Just inserted: [ObjectId('5c341c997cb9471ee3934d72'), ObjectId('5c341c997cb9471ee3934d73')]
    # Finished DB initialization
    # Existing collections: ['posts']

    query_db()

    # Output:
    # Documents with author 'Ziang': 2
    # {'author': 'Ziang', 'title': 'First Blog', 'content': 'What to write...'}
    # {'author': 'Ziang', 'title': 'Third Blog'}
    # Same result sorted by 'title':
    # {'author': 'Ziang', 'title': 'First Blog', 'content': 'What to write...'}
    # {'author': 'Ziang', 'title': 'Third Blog'}

    update_db()

    # Output:
    # Number of updated documents: 2

    test_index()

    # Output:
    # ['_id_', 'title_1']


if __name__ == '__main__':
    main()
