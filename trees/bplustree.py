from __future__ import annotations
from enum import Enum
from typing import Optional, List, Set
from collections import OrderedDict


class RangePointer:
    """
    Represents a range pointer within the B+ tree data structure
    """

    def __init__(self):
        """
        Initializes a RangePointer instance
        """
        self.ge: Optional[int] = None  # Whether the range has the greater than or equal to applied
        self.lt: Optional[int] = None  # Whether the range has the less than applied
        self.child: Optional[TreeNode] = None  # The child the RangePointer points to
        self.parent: Optional[TreeNode] = None  # The parent of the RangePointer
        self.ends: bool = False  # Whether the range pointer is on the ends of the node (far left or far right)
        # in the tree

    def set_range(self, **kwargs) -> RangePointer:
        """
        Sets the range of the RangePointer

        :param kwargs: Takes a variable number of keyword arguments
        :return: The modified instance
        """
        if 'ge' in kwargs:
            self.ge = kwargs['ge']
        if 'lt' in kwargs:
            self.lt = kwargs['lt']
        if 'ends' in kwargs:
            self.ends = kwargs['ends']
        return self

    def in_range(self, value: int) -> bool:
        """
        Determines whether the value supplied to it is within range of this RangePointer's lt and ge attributes

        :param value: The value we are determining if it is in range
        :return: Whether the value is in range
        """
        if self.ge is None and self.lt is None:
            return False
        elif self.ge is not None and self.lt is not None:
            return value >= self.ge and value < self.lt
        elif self.ge is not None and self.lt is None:
            return value >= self.ge
        elif self.ge is None and self.lt is not None:
            return value < self.lt
        return False

    def set_parent(self, parent: TreeNode) -> RangePointer:
        """
        Sets the value of the internal `parent` field of the BPlusTree node

        :param parent: The value we are setting the `parent` field to
        :return: The modified instance
        """
        self.parent = parent
        return self


class TreeNode:
    """
    Represents a node within the B+ tree data structure
    """

    def __init__(self):
        """
        Initializes a node within the B+ Tree data structure
        """
        self.keys: Optional[List[int]] = []  # The keys within the node
        self.range_pointers: Optional[List[RangePointer]] = None  # The range pointers within the node
        self.level: int = 1
        self.parent: Optional[TreeNode] = None
        self.right_link: Optional[TreeNode] = None  # Property of B+ tree, a horizontal link to its subsequent node

    def generate_range_pointers(self) -> List[RangePointer]:
        """
        Generates the range pointers from a given node's keys

        :return: The new list of RangePointers
        """
        range_pointers = []
        for ind, element in enumerate(self.keys):
            if ind == 0:
                if len(self.keys) == 1:
                    range_pointers.append(RangePointer().set_range(lt=element, ends=True).set_parent(self))
                    range_pointers.append(RangePointer().set_range(ge=element, ends=True).set_parent(self))
                else:
                    range_pointers.append(RangePointer().set_range(lt=element, ends=True).set_parent(self))
            else:
                range_pointers.append(RangePointer().set_range(ge=self.keys[ind - 1], lt=element).set_parent(self))
                range_pointers.append(RangePointer()
                                      .set_range(ge=element, ends=ind == len(self.keys) - 1)
                                      .set_parent(self))
        return range_pointers

    def modify_range_pointers(self) -> TreeNode:
        """
        Modifies the existing range pointers, when adding a key most likely

        :return: The modified TreeNode instance
        """
        modified_range_pointers = self.generate_range_pointers()
        # parse through each range_pointers children, grabbing their max from their keys, and comparing it to the
        # new and existing range pointer, if we find any matching keys, potential for splitting?
        if self.range_pointers is None:
            self.range_pointers = modified_range_pointers
            return self

        key_map: dict[int, TreeNode] = {}  # The maximum key mapped to the RangePointer's child
        for each_range_pointer in self.range_pointers:  # Populating the dictionaries of both key_map and level_map
            range_pointer_child = each_range_pointer.child
            if range_pointer_child is not None:
                max_child_keys = max(range_pointer_child.keys)
                key_map[max_child_keys] = range_pointer_child

        self.range_pointers = modified_range_pointers  # Set the new range pointers to be the original modified range
        # pointers after we have collected all the children from our current position in the subtree

        for each_max_key in key_map.keys():  # Assigning new children to the range pointers
            for each_range_pointer in self.range_pointers:
                if each_range_pointer.in_range(each_max_key):
                    each_range_pointer.child = key_map[each_max_key]
                    break
        return self

    def add_key(self, value: int):
        """
        Adds a key to the node itself

        :param value: The key to add
        :return: The modified node instance
        """
        self.keys.append(value)
        self.modify_range_pointers()
        return self

    def add_child(self, node: TreeNode) -> TreeNode:
        """
        Adds child to one of the TreeNode's range pointers

        :param node: The node to add
        :return: The modified TreeNode instance
        """
        max_key = max(node.keys)
        for each_range_pointer in self.range_pointers:
            if each_range_pointer.in_range(max_key) and each_range_pointer.child is None:
                each_range_pointer.child = node
                break
        return self


class BPlusTree:
    """
    Represents an instance of the BPlus tree data structure
    """

    def __init__(self):
        """
        Initializes a B+ tree data structure
        """
        self.root: Optional[TreeNode] = None  # The root node of the tree
        self.level_nodes: Optional[List[TreeNode]] = None  # A list of the nodes within a level, to make for optimal
        # chaining

    def gather_nodes_of_level(self, level: int, curr_node: Optional[TreeNode] = None) -> Optional[List[TreeNode]]:
        """
        Sets the right links of all nodes with the specified level

        :return: The modified tree instance
        """
        if curr_node is not None and curr_node.level > level:
            return None
        if curr_node is None:
            curr_node = self.root
        accumulated_nodes = OrderedDict()
        for each_range_pointer in curr_node.range_pointers:
            if each_range_pointer.parent.level < level:
                if each_range_pointer.child is not None:
                    gathered_nodes = self.gather_nodes_of_level(level, each_range_pointer.child)
                    for each_node in gathered_nodes:
                        accumulated_nodes[each_node] = None
            elif each_range_pointer.parent.level == level:
                accumulated_nodes[each_range_pointer.parent] = None
        return list(accumulated_nodes.keys())

    def set_right_links(self, level: int) -> BPlusTree:
        """
        Sets the right links of all the nodes at a specific level

        :param level: The level to construct the right links on
        :return: The modified Tree instance
        """
        all_nodes_on_level = self.gather_nodes_of_level(level)
        print("nodes on level = ", all_nodes_on_level)
        for ind, element in enumerate(all_nodes_on_level):
            if ind == len(all_nodes_on_level) - 1:
                break
            else:
                all_nodes_on_level[ind].right_link = all_nodes_on_level[ind + 1]
        return self

    def insert_node(self, value: int, level: int = 1) -> BPlusTree:
        """
        Inserts a key within the BPlus tree

        :param value: The value we are inserting
        :param level: The level we want to insert the node at
        :return: The tree itself
        """
        if self.root is None:
            self.root = TreeNode().add_key(value)
        else:
            if level == 1:
                self.root.add_key(value)
            else:
                curr_node: Optional[TreeNode] = self.root
                inserted: bool = False
                while curr_node is not None and not inserted:
                    for each_range_pointer in curr_node.range_pointers:
                        if each_range_pointer.child is not None and each_range_pointer.child.level == level and each_range_pointer.in_range(
                                value):
                            each_range_pointer.child.add_key(value)
                            inserted = True
                            break
                        elif each_range_pointer.in_range(value) and each_range_pointer.child is not None:
                            curr_node = each_range_pointer.child
                            inserted = False
                            break
                        elif each_range_pointer.in_range(value) and each_range_pointer.child is None:
                            inserted_node = TreeNode().add_key(value)
                            inserted_node.level = each_range_pointer.parent.level + 1
                            each_range_pointer.child = inserted_node
                            inserted = True
                            break
                        else:
                            inserted = True
        self.set_right_links(level)
        return self


if __name__ == '__main__':
    tree = BPlusTree()
    tree.insert_node(3)
    tree.insert_node(5)
    tree.insert_node(1, 2)
    tree.insert_node(2, 2)
    tree.insert_node(3, 2)
    tree.insert_node(4, 2)
    tree.insert_node(5, 2)
    tree.insert_node(6, 2)
    tree.insert_node(7, 2)
    print('Done!')
