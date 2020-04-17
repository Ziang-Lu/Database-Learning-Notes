#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A very simple B-tree implementation.
"""

__author__ = 'Ziang Lu'

from typing import Optional

from btree_base import BTreeBase
from common_constructs import Node


class BTree(BTreeBase):
    __slots__ = []

    def __init__(self, order: int):
        """
        Constructor with parameter.
        :param order: int
        """
        super().__init__(order)

    def _search_helper(self, curr: Node, key: int) -> Optional[str]:
        pos = curr.find_insert_pos(key)
        if pos < curr.size() and key == curr.get_entry(pos).key:  # Found it
            return curr.get_entry(pos).record_address
        if curr.is_leaf():  # Not found
            return None
        # Non-leaf
        # Go to the appropriate child
        return self._search_helper(curr.get_child(pos), key)
