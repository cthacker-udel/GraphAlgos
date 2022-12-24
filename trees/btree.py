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
        self.parent: Optional[TreeNode] = None

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
        """
        Adds a child to the current TreeNode

        :param value: The value we are adding
        :return: The modified TreeNode
        """
        for each_key_pointer in self.key_pointers:
            if each_key_pointer.value_in_range(value):
                added_node = TreeNode(value)
                added_node.parent = self
                each_key_pointer.children.append(added_node)
                break
        return self

    def get_children(self) -> Optional[List[TreeNode]]:
        """
        Fetches all the children from the node

        :return: The list of all children the node has
        """
        children = []
        for each_key_pointer in self.key_pointers:
            children_keys: Optional[List[TreeNode]] = each_key_pointer.children
            if children_keys is not None:
                for each_key in children_keys:
                    children.extend(each_key.keys)
        return children

    def reorder_children(self, new_key_pointers: List[RangePointer]) -> TreeNode:
        """
        Re-orders the children of the node according to the revised range pointers

        :param new_key_pointers: The list of new range pointers we will apply after gathering all the children from
        the current node
        :return: The modified TreeNode
        """
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

    def reorder_children_no_new(self) -> TreeNode:
        """
                Re-orders the children of the node according to its internal key_pointers

                :return: The modified TreeNode
                """
        children = []
        for each_key_pointer in self.key_pointers:
            children_keys: Optional[List[TreeNode]] = each_key_pointer.children
            if children_keys is not None:
                for each_key in children_keys:
                    children.extend(each_key.keys)
            each_key_pointer.children = []
        # compiled a list of all children
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
        """
        Initializes a B-Tree with an empty root node
        """
        self.root: Optional[TreeNode] = None

    def find_node(self, value: int) -> TreeNode | None:
        """
        Finds a node within the B-Tree

        :param value: The value we are searching for
        :return: The modified B-Tree
        """
        curr_node = self.root
        while curr_node is not None:
            for each_range_pointer in curr_node.key_pointers:
                if each_range_pointer.value_in_range(value):
                    for each_child in each_range_pointer.children:
                        if value in each_child.keys:
                            curr_node = each_child
                            return curr_node
        return curr_node

    def delete(self, value: int) -> BTree:
        found_node = self.find_node(value)
        # take that node, if the value is the only key within the node, then re-populate the parent with the
        # children of this node, else, just remove the key, and recalibrate the children
        if len(found_node.keys) > 1:
            # more than one key
            del found_node.keys[found_node.keys.index(value)]
            found_node.reorder_children_no_new()
        elif len(found_node.keys) == 0:
            # the only key within the node
            found_node_children = found_node.get_children()
            found_node_parent = found_node.parent
            for each_key_pointer in found_node_parent.key_pointers:
                for each_child in each_key_pointer.children:
                    if each_child == found_node:
                        each_child = None
                        for each_sub_child in found_node_children:
                            for each_child_key in each_sub_child.keys:
                                found_node_parent.add_child(each_child_key)
                        return self
        return self




if __name__ == '__main__':
    tree = BTree()
    tree.root = TreeNode(7)
    tree.root.add_child(1)
    tree.root.add_child(2)
    tree.root.add_child(9)
    tree.root.add_key(16)
    print("Done!")
