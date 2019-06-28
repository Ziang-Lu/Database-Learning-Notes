#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Weighted random selection using "zrangebyscore" operation of Sorted Set.

Before running this script, first make sure Redis server is up and running.
"""

__author__ = 'Ziang Lu'

import random
from typing import List, Tuple

import redis


def weighted_random_selection(elems: List[Tuple[str, float]]) -> None:
    """
    Weighted random selection, from the given elements (value-weight pair).
    :param elems: list[tuple]
    :return: None
    """
    r = redis.Redis()
    print(r.ping())

    # Data insertion
    total_score = sum(map(lambda x: x[1], elems))
    acc_score = 0.0
    data_mapping = {}
    for val, score in elems:
        acc_score += score
        data_mapping[val] = acc_score / total_score
    # [0.16, 0.5, 1.0]
    # [ A,    B,   C]
    r.zadd('elements', mapping=data_mapping)
    # The weighted random selection is transformed to:
    # Random selection from
    # [0, 0.16] -> A
    # [0.16, 0.5] -> B
    # [0.5, 1) -> C

    # Weighted random selection
    rand_score = random.random()
    random_selected = r.zrangebyscore('elements', min=rand_score, max='inf')
    print(random_selected)


def main():
    weighted_random_selection([('A', 1.0), ('B', 2.0), ('C', 3.0)])


if __name__ == '__main__':
    main()
