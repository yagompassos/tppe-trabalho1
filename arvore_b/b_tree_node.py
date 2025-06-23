from __future__ import annotations
from typing import List


class BTreeNode:
    def __init__(self, t: int, leaf: bool):
        self.t = t
        self.leaf = leaf
        self.keys: List[int] = []
        self.children: List[BTreeNode] = []

    def __str__(self):
        return str(self.keys)

    def find_key(self, k):
        i = 0
        while i < len(self.keys) and self.keys[i] < k:
            i += 1
        return i

    def traverse(self):
        result = []
        for i in range(len(self.keys)):
            if not self.leaf:
                result += self.children[i].traverse()
            result.append(self.keys[i])
        if not self.leaf:
            result += self.children[len(self.keys)].traverse()
        return result

    def search(self, k):
        i = self.find_key(k)
        if i < len(self.keys) and self.keys[i] == k:
            return self
        if self.leaf:
            return None
        return self.children[i].search(k)

    def insert_non_full(self, k):
        i = len(self.keys) - 1
        if self.leaf:
            self.keys.append(0)
            while i >= 0 and k < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = k
        else:
            while i >= 0 and k < self.keys[i]:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 2 * self.t - 1:
                self.split_child(i, self.children[i])
                if k > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(k)

    def split_child(self, i, y):
        z = BTreeNode(y.t, y.leaf)
        z.keys = y.keys[self.t :]
        if not y.leaf:
            z.children = y.children[self.t :]

        mid_key = y.keys[self.t - 1]
        y.keys = y.keys[: self.t - 1]
        y.children = y.children[: self.t] if not y.leaf else y.children

        self.children.insert(i + 1, z)
        self.keys.insert(i, mid_key)

    def remove(self, k):
        idx = self.find_key(k)

        if idx < len(self.keys) and self.keys[idx] == k:
            if self.leaf:
                self.keys.pop(idx)
            else:
                self.remove_from_internal_node(idx)
        else:
            if self.leaf:
                return  # key not found
            flag = idx == len(self.keys)
            if len(self.children[idx].keys) < self.t:
                self.fill(idx)
            if flag and idx > len(self.keys):
                self.children[idx - 1].remove(k)
            else:
                self.children[idx].remove(k)

    def remove_from_internal_node(self, idx):
        k = self.keys[idx]
        if len(self.children[idx].keys) >= self.t:
            pred = self.get_predecessor(idx)
            self.keys[idx] = pred
            self.children[idx].remove(pred)
        elif len(self.children[idx + 1].keys) >= self.t:
            succ = self.get_successor(idx)
            self.keys[idx] = succ
            self.children[idx + 1].remove(succ)
        else:
            self.merge(idx)
            self.children[idx].remove(k)

    def get_predecessor(self, idx):
        cur = self.children[idx]
        while not cur.leaf:
            cur = cur.children[-1]
        return cur.keys[-1]

    def get_successor(self, idx):
        cur = self.children[idx + 1]
        while not cur.leaf:
            cur = cur.children[0]
        return cur.keys[0]

    def fill(self, idx):
        if idx != 0 and len(self.children[idx - 1].keys) >= self.t:
            self.borrow_from_prev(idx)
        elif idx != len(self.keys) and len(self.children[idx + 1].keys) >= self.t:
            self.borrow_from_next(idx)
        else:
            if idx != len(self.keys):
                self.merge(idx)
            else:
                self.merge(idx - 1)

    def borrow_from_prev(self, idx):
        child = self.children[idx]
        sibling = self.children[idx - 1]
        child.keys.insert(0, self.keys[idx - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        self.keys[idx - 1] = sibling.keys.pop()

    def borrow_from_next(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]
        child.keys.append(self.keys[idx])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        self.keys[idx] = sibling.keys.pop(0)

    def merge(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]
        child.keys.append(self.keys[idx])
        child.keys += sibling.keys
        if not child.leaf:
            child.children += sibling.children
        self.keys.pop(idx)
        self.children.pop(idx + 1)

    def print_tree(self, prefix="", is_left=None):
        label = ""
        if is_left is True:
            label = "Esq "
        elif is_left is False:
            label = "Dir "
        print(f"{prefix}{label}{self.keys}")
        if self.children:
            for i, child in enumerate(self.children):
                if i == 0:
                    child_label = True
                elif i == len(self.children) - 1:
                    child_label = False
                else:
                    child_label = None  # Meio
                connector = "├── " if i < len(self.children) - 1 else "└── "
                child.print_tree(prefix + connector, child_label)