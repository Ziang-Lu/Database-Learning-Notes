#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Ziang Lu'

from bisect import bisect_left
from typing import List, Optional


class Entry:
    """
    Entry class.
    This is the class used in each node.
    """
    __slots__ = ['_key']

    def __init__(self, key: int):
        """
        Constructor with parameter.
        :param key: int
        """
        self._key = key

    @property
    def key(self) -> int:
        """
        Accessor of key.
        :return: int
        """
        return self._key


class Node:
    """
    Node class.
    Essentially, this can be seen as a block on disk, on which the database
    table is stored.
    """
    __slots__ = ['_ORDER', '_entries', '_size', '_children']

    def __init__(self, order: int, from_entries: List[Entry],
                 from_children: list):
        """
        Constructor with parameter.
        :param order: int
        :param from_entries: list[Entry]
        :param from_children: list[Node]
        """
        self._ORDER = order
        # Index entries
        self._entries = [None] * order  # Extend 1 position for temporary overflow
        size = len(from_entries)
        self._size = size
        self._entries[:size] = from_entries
        # Children
        self._children = [None] * (order + 1)  # Extend 1 position for temporary overflow
        self._children[:len(from_children)] = from_children

    def entries(self) -> List[Optional[Entry]]:
        """
        Return the entries of this node.
        :return: list[Entry]
        """
        return self._entries

    def get_entry(self, pos: int) -> Optional[Entry]:
        """
        Returns the entry at the given position.
        :param pos: int
        :return: Entry
        """
        if pos < 0 or pos >= self._size:
            raise IndexError('Invalid entry position')
        return self._entries[pos]

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
            map(lambda index_entry: index_entry.key, self._entries), key,
            lo=0, hi=self._size
        )

    def insert_entry(self, pos: int, entry: Entry, left_child,
                     right_child) -> None:
        """
        Inserts the given key-record mapping into this node, at the given
        position, with the given left and right children.
        :param pos: int
        :param entry: Entry
        :param left_child: Node
        :param right_child: Node
        :return: None
        """
        # Handle keys
        self._entries[pos + 1:self._size + 1] = self._entries[pos:self._size]
        self._entries[pos] = entry
        # Handle the children
        self._children[pos + 2:self._size + 2] =\
            self._children[pos + 1:self._size + 1]
        self._children[pos] = left_child
        self._children[pos + 1] = right_child


class IndexEntry(Entry):
    """
    IndexEntry class.
    This is the class used in the nodes that actually have table record
    addresses.
    """
    __slots__ = ['_record_address']

    def __init__(self, key: int, record_address: Optional[str]):
        """
        Constructor with parameter.
        :param key: int
        :param record_address: str or None
        """
        super().__init__(key)
        self._record_address = record_address

    @property
    def record_address(self) -> Optional[str]:
        """
        Accessor of record_address.
        :return: str or None
        """
        return self._record_address


class BPlusTreeLeaf(Node):
    """
    B+ tree leaf class.
    In B+ trees, these leaf nodes actually have table record addresses.
    """
    __slots__ = ['next']

    def __init__(self, order: int, from_index_entries: List[IndexEntry],
                 next_leaf):
        """
        Constructor with parameter.
        :param order: int
        :param from_index_entries: list[IndexEntry]
        :param next_leaf: BPlusTreeLeaf
        """
        super().__init__(
            order, from_entries=from_index_entries, from_children=[]
        )
        self.next = next_leaf
