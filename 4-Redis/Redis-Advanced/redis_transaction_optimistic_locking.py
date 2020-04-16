#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple demo of Redis queued commands ("transaction") and optimistic locking
mechanism.

For detailed explanation:
https://github.com/andymccurdy/redis-py#pipelines
"""

__author__ = 'Ziang Lu'

import redis


def ticket_booking_with_optimistic_locking() -> None:
    """
    Ticket-booking with optimistic locking mechanism.
    :return: None
    """
    r1 = redis.Redis()
    print(r1.ping())

    r1.set('ziang', 500)
    r1.set('tickets', 1)

    # "ziang" wants to book the only remaining ticket.

    # Start a command queue (With a "watch", this becomes a true transaction.)
    queue = r1.pipeline()
    # Watch the key "tickets"
    # => If during the further "execute()", any watched key has been changed by
    #    some other Redis client, then the entire transaction is discarded.
    queue.watch('tickets')
    queue.multi()
    queue.decrby('ziang', 100)
    queue.decr('tickets')

    # Another Redis client booked the only remaining ticket.
    r2 = redis.Redis()
    print(r2.ping())
    r2.decr('tickets')
    print(r2.get('tickets'))
    # Afterwards,
    # 'ziang' -> 500
    # 'tickets' -> 0 (booked)

    try:
        # Execute the command queue
        queue.execute()
    except Exception as ex:
        print(f'{type(ex).__name__}: {ex}')
    # WatchError: Watched variable changed.

    print(r1.mget('ziang', 'tickets'))
    # Afterwards,
    # 'ziang' -> 500 (transaction discarded)
    # 'tickets' -> 0


if __name__ == '__main__':
    ticket_booking_with_optimistic_locking()
