#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Ziang Lu'

from bisect import bisect_left
from typing import List, Optional


class IndexEntry:
    __slots__ = ['_key', '_record_address']

    def __init__(self, key: int, record_address: Optional[str]):
        """
        Constructor with parameter.
        :param key: int
        :param record_address: str or None
        """
        self._key = key
        self._record_address = record_address

    @property
    def key(self) -> int:
        """
        Accessor of key.
        :return:
        """
        return self._key

    @property
    def record_address(self) -> Optional[str]:
        """
        Accessor of record_address.
        :return: str or None
        """
        return self._record_address


class Node:
    __slots__ = ['_ORDER', '_index_entries', '_size', '_children']

    def __init__(self, order: int, from_index_entries: List[IndexEntry],
                 from_children: list):
        """
        Constructor with parameter.
        :param order: int
        :param from_index_entries: list[IndexEntry]
        :param from_children: list[Node]
        """
        self._ORDER = order
        # Index entries
        self._index_entries = [None] * order  # Extend 1 position for temporary overflow
        size = len(from_index_entries)
        self._size = size
        self._index_entries[:size] = from_index_entries
        # Children
        self._children = [None] * (order + 1)  # Extend 1 position for temporary overflow
        self._children[:len(from_children)] = from_children

    def index_entries(self) -> List[Optional[IndexEntry]]:
        """
        Return the index entries of this node.
        :return: list[IndexEntry]
        """
        return self._index_entries

    def get_index_entry(self, pos: int) -> Optional[IndexEntry]:
        """
        Returns the index entry at the given position.
        :param pos: int
        :return: IndexEntry
        """
        if pos < 0 or pos >= self._size:
            raise IndexError('Invalid index entry position')
        return self._index_entries[pos]

    def children(self) -> list:
        """
        Returns the children of this node.
        :return:
        """
        return self._children

    def get_child(self, pos: int):
        """
        Returns the child at the given position.
        :param pos: int
        :return: Node
        """
        if pos < 0 or pos > self._size:
            raise IndexError('Invalid child position')
        return self._children[pos]

    def size(self) -> int:
        """
        Accessor of size.
        :return: int
        """
        return self._size

    def capacity(self) -> int:
        """
        Returns the maximum capacity of this node, which is 1 less than the
        order.
        :return: int
        """
        return self._ORDER - 1

    def is_leaf(self) -> bool:
        """
        Returns whether this node is a leaf.
        :return: bool
        """
        return self._children[0] is None

    def is_overflowed(self) -> bool:
        """
        Returns whether this node is overflowed.
        :return: bool
        """
        return self._size > self.capacity()

    def find_insert_pos(self, key: int) -> int:
        """
        Finds the insert position for the given key, using binary search.
        :param key: int
        :return: int
        """
        return bisect_left(
            map(lambda index_entry: index_entry.key, self._index_entries), key,
            lo=0, hi=self._size
        )

    def insert_entry(self, pos: int, index_entry: IndexEntry, left_child,
                     right_child) -> None:
        """
        Inserts the given key-record mapping into this node, at the given
        position, with the given left and right children.
        :param pos: int
        :param index_entry: IndexEntry
        :param left_child: Node
        :param right_child: Node
        :return: None
        """
        # Handle keys
        self._index_entries[pos + 1:self._size + 1] =\
            self._index_entries[pos:self._size]
        self._index_entries[pos] = index_entry
        # Handle the children
        self._children[pos + 2:self._size + 2] =\
            self._children[pos + 1:self._size + 1]
        self._children[pos] = left_child
        self._children[pos + 1] = right_child
