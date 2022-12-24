from __future__ import annotations
from enum import Enum
from typing import Optional, List


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
        elif self.ge is not None and self.lt is None:
            return value >= self.ge
        elif self.ge is None and self.lt is not None:
            return value < self.lt
        return False


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
                    range_pointers.append(RangePointer().set_range(lt=element, ends=True))
                    range_pointers.append(RangePointer().set_range(ge=element, ends=True))
                else:
                    range_pointers.append(RangePointer().set_range(lt=element, ends=True))
            elif ind == len(self.keys) - 1:
                range_pointers.append(RangePointer().set_range(ge=element, ends=True))
            else:
                range_pointers.append(RangePointer().set_range(ge=self.keys[ind - 1], lt=element))
        return range_pointers

    def modify_range_pointers(self) -> TreeNode:
        """
        Modifies the existing range pointers, when adding a key most likely

        :return: The modified TreeNode instance
        """
        modified_range_pointers = self.generate_range_pointers()
        # parse through each range_pointers children, grabbing their max from their keys, and comparing it to the
        # new and existing range pointer, if we find any matching keys, potential for splitting?
        key_map: dict[int, TreeNode] = {}  # The maximum key mapped to the RangePointer's child
        level_map: dict[int, List[TreeNode]] = {}
        for each_range_pointer in self.range_pointers:  # Populating the dictionaries of both key_map and level_map
            range_pointer_child = each_range_pointer.child
            max_child_keys = max(range_pointer_child.keys)
            key_map[max_child_keys] = range_pointer_child
            if range_pointer_child.level in level_map:
                level_map[range_pointer_child.level].append(range_pointer_child)
            else:
                level_map[range_pointer_child.level] = [range_pointer_child]

        self.range_pointers = modified_range_pointers  # Set the new range pointers to be the original modified range
        # pointers after we have collected all the children from our current position in the subtree

        for each_max_key in key_map.keys():  # Assigning new children to the range pointers
            for each_range_pointer in self.range_pointers:
                if each_range_pointer.in_range(each_max_key):
                    each_range_pointer.child = key_map[each_max_key]
                    break

        for element in level_map.keys():  # Assigning right links
            list_level_nodes = level_map[element]
            for ind, each_node in enumerate(list_level_nodes):
                if ind == len(list_level_nodes) - 1:
                    break
                else:
                    each_node.right_link = list_level_nodes[ind + 1]

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

    def insert_key(self, value: int, level: int) -> BPlusTree:
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
                        if each_range_pointer.child.level == level and each_range_pointer.in_range(value):
                            each_range_pointer.child.add_key(value)
                            inserted = True
                            break
                        elif each_range_pointer.in_range(value) and each_range_pointer.child is not None:
                            curr_node = each_range_pointer.child
                            break
                        elif each_range_pointer.in_range(value) and each_range_pointer.child is None:
                            each_range_pointer.child = TreeNode().add_key(value)
                            inserted = True
                            break


