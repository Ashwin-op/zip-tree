# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file.

from random import random
from typing import TypeVar

KeyType = TypeVar("KeyType")
ValType = TypeVar("ValType")


class Node:
    def __init__(self, key: KeyType, val: ValType, rank: int, left=None, right=None):
        self.key = key
        self.val = val
        self.rank = rank
        self.left = left
        self.right = right

    def __str__(self):
        return f"Node({self.key}, {self.val}, {self.rank})"


class ZipTree:
    def __init__(self):
        self.root = None
        self.size = 0

    @staticmethod
    def get_random_rank() -> int:
        # https://stats.stackexchange.com/a/487939
        rank = 0
        while True:
            if random() < 0.5:
                return rank
            rank += 1

    # Method for inserting new node with key
    # i)  Find node to be replaced by new node depending on key and sampled rank
    # ii) Unzipping of subtree
    def insert(self, key: KeyType, val: ValType, rank: int = -1):
        self.size += 1

        new_node = Node(key, val, rank if rank != -1 else self.get_random_rank())

        # current: for storing the node to be replaced
        # previous: for storing the parent of current
        current = self.root
        previous = None

        # find node to be replaced
        while current is not None and (
            new_node.rank < current.rank
            or (new_node.rank == current.rank and new_node.key > current.key)
        ):
            previous = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        # insert new node
        if current == self.root:
            self.root = new_node
        elif new_node.key < previous.key:
            previous.left = new_node
        else:
            previous.right = new_node

        # preserving replaced node
        if current is None:
            return
        if new_node.key < current.key:
            new_node.right = current
        else:
            new_node.left = current
        previous = new_node

        # Unzip
        # current: moves along search path, stops temporarily when element changes relation (smaller or greater) to inserted key
        # previous: last element with different relation to inserted element than "current"
        # temp: starts at inserted element, changes to "previous" whenever "previous" changes; place for "current" to be inserted when it stops moving
        temp = None
        while current is not None:
            temp = previous

            if current.key < new_node.key:
                while current is not None and current.key < new_node.key:
                    previous = current
                    current = current.right
            else:
                while current is not None and current.key > new_node.key:
                    previous = current
                    current = current.left

            if temp.key > new_node.key or (
                temp == new_node and previous.key > new_node.key
            ):
                temp.left = current
            else:
                temp.right = current

    # Method for deletion of certain key
    # i)   Find key in tree
    # ii)  Replace node with a child, depending on rank
    # iii) Zipping of subtrees of deleted node
    def remove(self, key: KeyType):
        self.size -= 1

        # current: at first node to be deleted; then replacing node
        # previous: parent of "current"
        # left: left child of "current", first part for zipping
        # right: right child of "current", second part for zipping
        current = self.root
        previous = None
        left = None
        right = None

        # find key
        while key != current.key:
            previous = current
            if key < current.key:
                current = current.left
            else:
                current = current.right

        left = current.left
        right = current.right

        # 0 or 1 child: child becomes replacing node
        if left is None:
            current = right
        elif right is None:
            current = left
        # 2 children: child with higher rank (or lower key in case of a tie) becomes replacing node
        elif left.rank >= right.rank:
            current = left
        else:
            current = right

        # replace node
        if self.root.key == key:
            self.root = current
        elif key < previous.key:
            previous.left = current
        else:
            previous.right = current

        # Zip
        # previous: builds zipped path depending on rank of the elements
        while left is not None and right is not None:
            if left.rank >= right.rank:
                while left is not None and left.rank >= right.rank:
                    previous = left
                    left = left.right
                previous.right = right
            else:
                while right is not None and left.rank < right.rank:
                    previous = right
                    right = right.left
                previous.left = left

    def find(self, key: KeyType) -> ValType:
        current = self.root
        while key != current.key:
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return current.val

    def get_size(self) -> int:
        return self.size

    def get_height(self) -> int:
        def height(node):
            if node is None:
                return 0
            return 1 + max(height(node.left), height(node.right))

        return height(self.root) - 1

    def get_depth(self, key: KeyType):
        current = self.root
        depth = 0
        while key != current.key:
            if key < current.key:
                current = current.left
            else:
                current = current.right
            depth += 1
        return depth


# feel free to define new classes/methods in addition to the above
# fill in the definitions of each required member function (above),
# and any additional member functions you define
