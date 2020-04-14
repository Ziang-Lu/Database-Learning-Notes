#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Ziang Lu'

from abc import ABC, abstractmethod
from typing import List, Optional

from common_constructs import IndexEntry, Node


class BTreeBase(ABC):
    __slots__ = ['_ORDER', '_root']

    def __init__(self, order: int):
        """
        Constructor with parameter.
        :param order: int
        """
        self._ORDER = order
        self._root = None

    def search(self, key: int) -> Optional[str]:
        """
        Searches for the given key in this B-tree, and returns the associated
        record address if found.
        :param key: int
        :return: str or None
        """
        if not self._root:
            return None
        return self._search_helper(self._root, key)

    @abstractmethod
    def _search_helper(self, curr: Node, key: int) -> Optional[str]:
        pass

    def insert(self, key: int, record_address: str) -> None:
        """
        Inserts the given key-record mapping to the B-tree.
        :param key: int
        :param record_address: str
        :return: None
        """
        index_entry = IndexEntry(key, record_address)
        if not self._root:
            self._root = Node(
                self._ORDER, from_index_entries=[index_entry], from_children=[]
            )
            return
        self._insert_helper(self._root, index_entry, [], [])

    def _insert_helper(
                self,
                curr: Node,
                key: int,
                record_address: str,
                path: List[Node],
                past_insert_positions: List[int]
            ) -> None:
        """
        Private helper method to insert the given key-record mapping to the
        given subtree recursively.
        :param curr: Node
        :param key: int
        :param record_address: str
        :param path: list[Node]
        :param past_insert_positions: list[int]
        :return: None
        """
        pos = curr.find_insert_pos(key)
        if key == curr.get_index_entry(pos).key:  # Found it
            # No duplicate key allowed
            return
        index_entry = IndexEntry(key, record_address)
        if curr.is_leaf():  # Leaf
            # Insert into the leaf node first, and if the leaf node itself is
            # overflowed, percolate up
            curr.insert_entry(
                pos, index_entry, left_child=None, right_child=None
            )
            if curr.is_overflowed():
                self._percolate_up(curr, path, past_insert_positions)
            return
        # Non-leaf
        # Go to the appropriate child
        path.append(curr)
        past_insert_positions.append(pos)
        self._insert_helper(
            curr.get_child(pos), key, record_address, path, past_insert_positions
        )

    @abstractmethod
    def _percolate_up(self, curr: Node, path: List[Node],
                      past_insert_positions: List[int]) -> None:
        """
        Private helper method to percolate up.
        :param curr: Node
        :param path: list[Node]
        :param past_insert_positions: list[int]
        :return: None
        """
        pass
