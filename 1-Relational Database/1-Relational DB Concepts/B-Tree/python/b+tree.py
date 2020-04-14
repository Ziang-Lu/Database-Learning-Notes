#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A very simple B+ tree implementation.
"""

__author__ = 'Ziang Lu'

from typing import List, Optional

from btree_base import BTreeBase
from common_constructs import BPlusTreeLeaf, Entry, Node


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
            if pos < curr.size() and key == curr.get_entry(pos).key:  # Found it
                return curr.get_entry(pos).record_address
            else:  # Not found
                return None
        # Non-leaf
        # Go to the appropriate child
        return self._search_helper(curr.get_child(pos), key)

    def _percolate_up(self, curr: Node, path: List[Node],
                      past_insert_positions: List[int]) -> None:
        leaf = curr
        # leaf is overflowed
        # -> Percolate up a copy of the middle key of leaf
        mid = leaf.size() // 2
        mid_key = leaf.get_entry(mid).key
        right_child = BPlusTreeLeaf(
            self._ORDER,
            from_index_entries=leaf.entries()[mid:],
            next_leaf=None
        )
        left_child = BPlusTreeLeaf(
            self._ORDER,
            from_index_entries=leaf.entries()[:mid],
            next_leaf=right_child
        )  # Connect left_child and right_child

        if leaf is self._root:
            self._root = Node(
                self._ORDER,
                from_entries=[Entry(mid_key)],
                from_children=[left_child, right_child]
            )
            return

        # Insert into this parent node first, and if the parent node is
        # overflowed, keep percolating up
        parent = path.pop()
        past_insert_pos = past_insert_positions.pop()
        parent.insert_entry(
            past_insert_pos,
            Entry(mid_key),
            left_child=left_child,
            right_child=right_child
        )
        prev_leaf = parent.get_child(past_insert_pos - 1) if past_insert_pos > 0 else None
        next_leaf = parent.get_child(past_insert_pos + 1) if past_insert_pos < parent.size() else None
        if prev_leaf:
            prev_leaf.next = left_child
        right_child.next = next_leaf
        if parent.is_overflowed():
            super()._percolate_up(parent, path, past_insert_positions)
