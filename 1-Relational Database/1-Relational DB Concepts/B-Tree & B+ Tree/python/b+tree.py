#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A very simple B+ tree implementation.
"""

__author__ = 'Ziang Lu'

from typing import List, Optional, Tuple

from btree_base import BTreeBase
from common_constructs import BPlusTreeLeaf, Entry, Node


class BPlusTree(BTreeBase):
    __slots__ = []

    def __init__(self, order: int):
        """
        Constructor with parameter.
        :param order: int
        """
        super().__init__(order)

    def _search_helper(self, curr: Node, key: int) -> Optional[str]:
        leaf, pos = self._locate_leaf_and_pos(curr, key)
        if pos < leaf.size() and key == leaf.get_entry(pos).key:  # Found it
            return leaf.get_entry(pos).record_address
        else:  # Not found
            return None

    def _locate_leaf_and_pos(self, curr: Node,
                             key: int) -> Tuple[BPlusTreeLeaf, int]:
        """
        Helper method to locate the given key in the given subtree recursively.
        :param curr: Node
        :param key: int
        :return: BPlusTreeLeaf, int
        """
        pos = curr.find_insert_pos(key)
        if curr.is_leaf():  # Leaf
            return curr, pos
        # Non-leaf
        # Go to the appropriate child
        return self._locate_leaf_and_pos(curr.get_child(pos), key)

    def range_search(self, from_key: int, to_key: int) -> List[str]:
        """
        Searches for the given range of keys in this B+ tree, and returns the
        associated record addresses if found.
        :param from_key: int
        :param to_key: int:
        :return: list[str]
        """
        if from_key > to_key:
            raise ValueError('from_key must be <= to_key')

        if not self._root:
            return []

        # 1. Find the from_key
        from_leaf, from_pos = self._locate_leaf_and_pos(self._root, from_key)
        # 2. Use the fact that all the leaves are connected, simply do a linear
        #    scan along the leaves (and thus the keys), find all the keys within
        #    the given range
        leaf_ptr, pos_ptr = from_leaf, from_pos
        result = []
        while leaf_ptr:
            if pos_ptr < leaf_ptr.size():
                entry = leaf_ptr.get_entry(pos_ptr)
                if entry.key > to_key:
                    break
                result.append(entry.record_address)
                pos_ptr += 1
            else:
                leaf_ptr = leaf_ptr.next
                pos_ptr = 0
        return result

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
