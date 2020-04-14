#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A very simple B+ tree implementation.
"""

__author__ = 'Ziang Lu'

from typing import List, Optional

from btree_base import BTreeBase
from common_constructs import IndexEntry, Node


class BPlusTree(BTreeBase):

    def __init__(self, order: int):
        """
        Constructor with parameter.
        :param order: int
        """
        super().__init__(order)

    def _search_helper(self, curr: Node, key: int) -> Optional[str]:
        pos = curr.find_insert_pos(key)
        if curr.is_leaf():  # Leaf
            if pos < curr.size() and key == curr.get_index_entry(pos).key:  # Found it
                return curr.get_index_entry(pos).record_address
            else:
                return None
        # Non-leaf
        # Go to the appropriate child
        return self._search_helper(curr.get_child(pos), key)

    def _percolate_up(self, curr: Node, path: List[Node],
                      past_insert_positions: List[int]) -> None:
        # curr is overflowed
        # -> Percolate a copy of the middle key of curr
        mid = curr.size() // 2
        mid_key = curr.get_index_entry(mid).key
        up_dummy_entry = IndexEntry(mid_key, record_address=None)
        left_child = Node(
            self._ORDER,
            from_index_entries=curr.index_entries()[:mid + 1],
            from_children=curr.children()[:mid + 2]
        )
        right_child = Node(
            self._ORDER,
            from_index_entries=curr.index_entries()[mid + 1:],
            from_children=curr.children()[mid + 2:]
        )

        if curr is self._root:
            self._root = Node(
                self._ORDER,
                from_index_entries=[up_dummy_entry],
                from_children=[left_child, right_child]
            )
            return

        # Insert into this parent node first, and if the parent node is
        # overflowed, keep percolating up
        parent = path.pop()
        past_insert_pos = past_insert_positions.pop()
        parent.insert_entry(
            past_insert_pos,
            up_dummy_entry,
            left_child=left_child,
            right_child=right_child
        )
        if parent.is_overflowed():
            self._percolate_up(parent, path, past_insert_positions)