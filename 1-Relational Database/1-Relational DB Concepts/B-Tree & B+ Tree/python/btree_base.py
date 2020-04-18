#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Ziang Lu'

from abc import ABC, abstractmethod
from typing import Any, List, Optional

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

    def search(self, key: Any) -> Optional[str]:
        """
        Searches for the given key in this B-tree, and returns the associated
        record address if found.
        :param key: Any
        :return: str or None
        """
        if not self._root:
            return None
        return self._search_helper(self._root, key)

    @abstractmethod
    def _search_helper(self, curr: Node, key: Any) -> Optional[str]:
        """
        Private helper method to search for the given key in the given subtree
        recursively.
        :param curr: Node
        :param key: Any
        :return: str or None
        """
        pass

    def insert(self, key: Any, record_address: str) -> None:
        """
        Inserts the given key-record mapping to the B-tree.
        :param key: Any
        :param record_address: str
        :return: None
        """
        if not self._root:
            self._root = Node(
                self._ORDER,
                from_entries=[IndexEntry(key, record_address)],
                from_children=[]
            )
            return
        self._insert_helper(self._root, key, record_address, [], [])

    @abstractmethod
    def _insert_helper(
                self,
                curr: Node,
                key: Any,
                record_address: str,
                path: List[Node],
                past_insert_positions: List[int]
            ) -> None:
        """
        Private helper method to insert the given key-record mapping to the
        given subtree recursively.
        :param curr: Node
        :param key: Any
        :param record_address: str
        :param path: list[Node]
        :param past_insert_positions: list[int]
        :return: None
        """
        pos = curr.find_insert_pos(key)
        if key == curr.get_entry(pos).key:  # Found it
            # No duplicate key allowed to be inserted
            return
        if curr.is_leaf():  # Leaf
            # Insert into the leaf node first, and if the leaf node itself is
            # overflowed, percolate up
            curr.insert_entry(
                pos,
                IndexEntry(key, record_address),
                left_child=None,
                right_child=None
            )
            if curr.is_overflowed():
                self._percolate_up(curr, path, past_insert_positions)
            return
        # Non-leaf
        # Go to the appropriate child
        path.append(curr)
        past_insert_positions.append(pos)
        self._insert_helper(
            curr.get_child(pos),
            key,
            record_address,
            path,
            past_insert_positions
        )

    def _percolate_up(self, curr: Node, path: List[Node],
                      past_insert_positions: List[int]) -> None:
        """
        Private helper method to percolate up.
        :param curr: Node
        :param path: list[Node]
        :param past_insert_positions: list[int]
        :return: None
        """
        # curr is overflowed
        # -> Percolate up the middle index entry of curr
        mid = curr.size() // 2
        mid_entry = curr.get_entry(mid)
        left_child = Node(
            self._ORDER,
            from_entries=curr.entries()[:mid],
            from_children=curr.children()[:mid + 1]
        )
        right_child = Node(
            self._ORDER,
            from_entries=curr.entries()[mid + 1:],
            from_children=curr.children()[mid + 1:]
        )

        if curr is self._root:
            self._root = Node(
                self._ORDER,
                from_entries=[mid_entry],
                from_children=[left_child, right_child]
            )
            return

        # Insert into this parent node first, and if the parent node is
        # overflowed, keep percolating up
        parent = path.pop()
        parent_insert_pos = past_insert_positions.pop()
        parent.insert_entry(
            parent_insert_pos,
            mid_entry,
            left_child=left_child,
            right_child=right_child
        )
        if parent.is_overflowed():
            self._percolate_up(parent, path, past_insert_positions)
            BTreeBase._percolate_up(self, parent, path, past_insert_positions)
