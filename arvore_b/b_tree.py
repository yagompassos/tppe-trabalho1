from __future__ import annotations
from typing import List, Optional
from icontract import require, ensure, invariant
from b_tree_node import BTreeNode


@invariant(
    lambda self: all(
        len(c.keys) >= self.t - 1 or c is self.root for c in self._get_all_nodes()
    )
)
@invariant(
    lambda self: all(len(c.keys) <= 2 * self.t - 1 for c in self._get_all_nodes())
)
@invariant(lambda self: self._leaves_on_same_level())
@invariant(
    lambda self: all(self._is_sorted(node.keys) for node in self._get_all_nodes())
)
class BTree:
    def __init__(self, t: int):
        self.t = t
        self.root: Optional[BTreeNode] = None

    def _get_all_nodes(self):
        def traverse(node):
            if node is None:
                return []
            result = [node]
            for c in node.children:
                result += traverse(c)
            return result

        return traverse(self.root)

    def _leaves_on_same_level(self):
        levels = []

        def traverse(node, depth):
            if node is None:
                return
            if node.leaf:
                levels.append(depth)
            for c in node.children:
                traverse(c, depth + 1)

        traverse(self.root, 0)
        return len(set(levels)) <= 1

    def _is_sorted(self, lst: List[int]) -> bool:
        return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))

    @require(lambda self, k: self.search(k) is None)
    @ensure(lambda self, k: self.search(k) is not None)
    @ensure(
        lambda self: all(
            (
                (1 <= len(node.keys) <= 2 * self.t - 1)
                if node == self.root
                else (self.t - 1 <= len(node.keys) <= 2 * self.t - 1)
            )
            for node in self._get_all_nodes()
        )
    )
    @ensure(
        lambda self: all(
            (
                (2 <= len(node.children) <= 2 * self.t)
                if node == self.root
                else (self.t <= len(node.children) <= 2 * self.t)
            )
            for node in self._get_all_nodes()
            if not node.leaf
        )
    )
    def insert(self, k: int):
        if self.root is None:
            self.root = BTreeNode(self.t, True)
            self.root.keys.append(k)
        else:
            if len(self.root.keys) == 2 * self.t - 1:
                s = BTreeNode(self.t, False)
                s.children.append(self.root)
                s.split_child(0, self.root)
                i = 0
                if s.keys[0] < k:
                    i += 1
                s.children[i].insert_non_full(k)
                self.root = s
            else:
                self.root.insert_non_full(k)

    def search(self, k: int):
        return self.root.search(k) if self.root else None

    @require(lambda self, k: self.search(k) is not None)
    @ensure(lambda self, k: self.search(k) is None)
    @ensure(
        lambda self: all(
            (
                (1 <= len(node.keys) <= 2 * self.t - 1)
                if node == self.root
                else (self.t - 1 <= len(node.keys) <= 2 * self.t - 1)
            )
            for node in self._get_all_nodes()
        )
    )
    @ensure(
        lambda self: all(
            (
                (2 <= len(node.children) <= 2 * self.t)
                if node == self.root
                else (self.t <= len(node.children) <= 2 * self.t)
            )
            for node in self._get_all_nodes()
            if not node.leaf
        )
    )
    def remove(self, k: int):
        if not self.root:
            return
        self.root.remove(k)
        if len(self.root.keys) == 0:
            if self.root.leaf:
                self.root = None
            else:
                self.root = self.root.children[0]

    @ensure(lambda self, result: True)
    def traverse(self):
        return self.root.traverse() if self.root else []
