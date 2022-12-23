from __future__ import annotations
from typing import List, Optional


class RangePointer:
    """
    Represents a pointer within the key ranges
    """

    def __init__(self):
        """
        Initializes a RangePointer, which contains a less_than field, a greater_than field, and an array of all the
        children present.
        """
        self.less_than: Optional[int] = None
        self.greater_than: Optional[int] = None
        self.children: Optional[List[TreeNode]] = []

    def set_range(self, **kwargs) -> RangePointer:
        self.less_than = kwargs["lt"] if 'lt' in kwargs else None
        self.greater_than = kwargs["gt"] if 'gt' in kwargs else None
        return self

    def value_in_range(self, value: int) -> bool:
        if self.less_than and self.greater_than:
            return value < self.less_than and value > self.greater_than
        elif self.less_than:
            return value < self.less_than
        else:
            return value > self.greater_than


class TreeNode:
    """
    Represents a node in the B-Tree
    """

    def __init__(self, initial_key: int):
        """
        Initializes a B-Tree Node, setting its key array to contain one of the initial keys

        :param initial_key: The initial key to create the node with
        """
        self.keys: List[int] = [initial_key]
        self.key_pointers: List[RangePointer] = [
            RangePointer().set_range(lt=initial_key), RangePointer().set_range(gt=initial_key)
        ]
        self.threshold = .70

    def set_threshold(self: TreeNode, threshold: float) -> TreeNode:
        """
        Sets the threshold of the TreeNode

        :param threshold: The new threshold of the node, if the node is x% amount full, then the node is split to
        keep some semblance of self-balancing tree
        :return: The updated TreeNode
        """
        self.threshold = threshold
        return self

    def add_key(self, new_key: int) -> TreeNode:
        """
        Adds a key to the internal node's `key` array, which partitions its children into subtrees dependent on
        its keys.

        :param new_key: The key we are appending to the current node
        :return: The edited B-Tree node
        """
        if new_key not in self.keys:
            self.keys.append(new_key)
            self.keys.sort()
            # generate range pointers
            new_range_pointers = []
            for ind, each_key in enumerate(self.keys):
                if ind == 0:
                    new_range_pointers.append(RangePointer().set_range(lt=each_key))
                elif ind == len(self.keys) - 1:
                    new_range_pointers.append(RangePointer().set_range(lt=each_key, gt=self.keys[ind - 1]))
                    new_range_pointers.append(RangePointer().set_range(gt=each_key))
                else:
                    new_range_pointers.append(RangePointer().set_range(lt=each_key, gt=self.keys[ind - 1]))
            self.reorder_children(new_range_pointers)
        return self

    def add_child(self, value: int) -> TreeNode:
        for each_key_pointer in self.key_pointers:
            if each_key_pointer.value_in_range(value):
                each_key_pointer.children.append(TreeNode(value))
                break
        return self

    def reorder_children(self, new_key_pointers: List[RangePointer]) -> TreeNode:
        children = []
        for each_key_pointer in self.key_pointers:
            children_keys: Optional[List[TreeNode]] = each_key_pointer.children
            if children_keys is not None:
                for each_key in children_keys:
                    children.extend(each_key.keys)
            each_key_pointer.children = []
        # compiled a list of all children
        self.key_pointers = new_key_pointers
        for each_child in children:
            for each_key_pointer in self.key_pointers:
                if each_key_pointer.value_in_range(each_child):
                    each_key_pointer.children.append(each_child)
                    break
        return self


class BTree:
    """
    Represents a B-Tree data structure
    """

    def __init__(self):
        self.root: Optional[TreeNode] = None


if __name__ == '__main__':
    tree = BTree()
    tree.root = TreeNode(7)
    tree.root.add_child(1)
    tree.root.add_child(2)
    tree.root.add_child(9)
    tree.root.add_key(16)
    print("Done!")
