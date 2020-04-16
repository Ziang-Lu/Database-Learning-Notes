#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple demo of Redis Publisher-Subscriber mechanism.
"""

__author__ = 'Ziang Lu'

import time

import redis

IGNORE_SUBSCRIBE_MESSAGE = False


def pub_sub_demo() -> None:
    """
    Simple demo of Redis Pub/Sub mechanism.
    :return: None
    """
    r1 = redis.Redis()
    print(r1.ping())

    # Create a PubSub instance for client-1
    p1 = r1.pubsub(ignore_subscribe_messages=IGNORE_SUBSCRIBE_MESSAGE)
    # Subscribe to "news" channel
    p1.subscribe('news')

    # To avoid commands executing at the same time and ensure the commands
    # order, let the program sleep 2 seconds.
    time.sleep(2)

    r2 = redis.Redis()
    print(r2.ping())

    # Create a PubSub instance for client-2
    p2 = r2.pubsub(ignore_subscribe_messages=IGNORE_SUBSCRIBE_MESSAGE)
    # Register a callback function for messages received from "news" channel
    p2.subscribe(**{'news': _message_handler})
    # => Once a message is received from "news" channel, that message is sent to
    #    the registered callback function.

    time.sleep(2)

    r3 = redis.Redis()
    print(r3.ping())

    # Publish some message to "news" channel
    r3.publish('news', "It's a good day!")

    time.sleep(2)

    print('here')

    print(p1.get_message())
    # {'type': 'message', 'pattern': None, 'channel': b'news', 'data': b"It's a good day!"}
    print(p2.get_message())
    # MESSAGE HANDLER: "It's a good day!"


def _message_handler(msg: dict) -> None:
    """
    Dummy message callback function.
    :param msg: dict
    :return: None
    """
    print(f"MESSAGE HANDLER: {msg['data']}")


if __name__ == '__main__':
    pub_sub_demo()
