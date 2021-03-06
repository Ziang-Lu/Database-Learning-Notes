#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple usage demo of pymongo library (driver).

Before running this script, first make sure MongoDB server is up and running.
"""

__author__ = 'Ziang Lu'

from datetime import datetime

from pymongo import (
    ASCENDING, DESCENDING, InsertOne, MongoClient, TEXT, UpdateOne
)


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
        'title': 'First Post',
        'content': 'What to write...',
        'tags': ['diary', 'python'],
        'date': datetime.now()
    }
    inserted_id = posts.insert_one(first_post).inserted_id
    print(f'Just inserted: {inserted_id}')
    inserted_ids = posts.insert_many([
        {
            'author': 'Mike',
            'title': 'Second Post',
            'tags': ['diary'],
            'date': datetime.now()
        },
        {
            'author': 'Ziang',
            'title': 'Third Post',
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
            {'author': 'Ziang'},
            projection={'_id': False, 'tags': False, 'date': False}
    ):
        print(post)

    print("Same result sorted by 'title':")
    for post in posts.find(
            {'author': 'Ziang'},
            projection={'_id': False, 'tags': False, 'date': False},
    ).sort('title', ASCENDING):
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
        {'author': 'Ziang'}, update={'$set': {'rank': 1}}
    )
    print(f'Number of updated documents: {update_result.modified_count}')

    ####################

    # We can also do bulk write as follows:
    requests = [
        InsertOne({'x': 1}),
        UpdateOne({'author': 'Ziang'}, update={'$set': {'rank': 1}})
    ]
    write_result = posts.bulk_write(requests)
    print(f'Number of inserted documents: {write_result.inserted_count}')
    print(f'Number of updated documents: {write_result.modified_count}')


def test_index() -> None:
    """
    Tests index-related stuff.
    :return: None
    """
    cli = MongoClient()
    db = cli.test
    posts = db.posts

    # Single-Field Index
    posts.create_index([('title', ASCENDING)], unique=True)  # "title" must be unique
    # Compound Index
    posts.create_index([('title', ASCENDING), ('date', DESCENDING)])
    # Text Index
    posts.create_index([('title', TEXT)])

    print(list(posts.index_information()))

    # Check index
    posts.insert_one({
        'author': 'Ziang',
        'title': 'Fourth Post'
    })  # This is fine.

    posts.insert_one({
        'author': 'Ziang',
        'title': 'Fourth Post'
    })  # DuplicateKeyError


if __name__ == '__main__':
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
    # {'author': 'Ziang', 'title': 'First Post', 'content': 'What to write...'}
    # {'author': 'Ziang', 'title': 'Third Post'}
    # Same result sorted by 'title':
    # {'author': 'Ziang', 'title': 'First Post', 'content': 'What to write...'}
    # {'author': 'Ziang', 'title': 'Third Post'}

    update_db()

    # Output:
    # Number of updated documents: 2
    #
    # Number of inserted documents: 1
    # Number of updated documents: 0

    test_index()

    # Output:
    # ['_id_', 'title_1']
