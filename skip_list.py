# explanations for member functions are provided in requirements.py
# each file that uses a skip list should import it from this file.

from typing import TypeVar
import random
from zip_tree import ZipTree

KeyType = TypeVar("KeyType")
ValType = TypeVar("ValType")


class Node:
    def __init__(self, key: KeyType, val: ValType, level: int):
        self.key = key
        self.val = val
        self.forward = [None] * (level + 1)

    def __repr__(self):
        return f"Node({self.key}, {self.val}, {len(self.forward) - 1})"


class SkipList:
    def __init__(self):
        self.max_level = 20
        self.header = Node(None, None, self.max_level)
        self.level = 0  # the current referencing level
        self.n = 0

    def __len__(self) -> int:
        return self.n

    def get_random_level(self, key: KeyType) -> int:
        # Do not change this function. Use this function to determine what level each key should be at. Assume levels start at 0 (i.e. the bottom-most list is at level 0)
        # e.g. for some key x, if get_random_level(x) = 5, then x should be in the lists on levels 0, 1, 2, 3, 4 and 5 in the skip list.
        random.seed(str(key))
        level = 0
        while random.random() < 0.5 and level < 20:
            level += 1
        return level

    def insert(self, key: KeyType, val: ValType, level: int = -1):
        current, path = self._search(key)
        if current and current.key == key:
            current.val = val
        else:
            if level == -1:
                level = self.get_random_level(key)
            if level > self.level:
                for i in range(self.level + 1, level + 1):
                    path[i] = self.header
                self.level = level
            node = Node(key, val, level)
            for i in range(level + 1):
                node.forward[i] = path[i].forward[i]
                path[i].forward[i] = node
            self.n += 1

    def remove(self, key: KeyType):
        current, path = self._search(key)
        if current is not None and current.key == key:
            ret = current
            for i in range(self.level + 1):
                if path[i].forward[i] != current:
                    break
                path[i].forward[i] = current.forward[i]
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1
            self.n -= 1
            return ret

    def find(self, key: KeyType) -> ValType:
        current, _ = self._search(key)
        return current.val if current and current.key == key else None

    def _search(self, key):
        path = [None] * (self.max_level + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            path[i] = current
        current = current.forward[0]
        return current, path

    def get_list_size_at_level(self, level: int):
        if level > self.level:
            return 0
        count = 0
        node = self.header.forward[level]
        while node is not None:
            count += 1
            node = node.forward[level]
        return count

    def from_zip_tree(self, zip_tree: ZipTree) -> None:
        def inorder(node, level):
            if node:
                inorder(node.left, level + 1)
                self.insert(node.key, node.val, node.rank)
                inorder(node.right, level + 1)

        inorder(zip_tree.root, 0)


# feel free to define new classes/methods in addition to the above
# fill in the definitions of each required member function (above),
# and any additional member functions you define
