from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from enum import Enum


class Color(Enum):
    """
    The color of the tree node
    """
    RED = 0
    BLACK = 1


class TreeNode:
    """
    Node representation
    """

    def __init__(self, value: int):
        """
        The initialization of the AATree node

        :param value: The value we are assigning the tree node
        """
        self.value: int = value
        self.color: Color = Color.RED
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None
        self.parent: Optional[TreeNode] = None
        self.level: int = 0

    def has_one_child(self) -> bool:
        """
        Returns whether the node has one child

        :return: Whether the node has one child
        """
        return (self.left is not None and self.right is None) or (self.right is not None and self.left is None)

    def has_two_children(self) -> bool:
        """
        Returns whether the node has two children

        :return: Whether the node has two children
        """
        return self.left is not None and self.right is not None


class AATree:
    """
    AA (Arne Anderson) Tree representation
    """

    def __init__(self, root: Optional[TreeNode] = None):
        """
        The initialization of the AATree

        :param root: The root we are assigning to the tree
        """
        if root is not None:
            root.color = Color.BLACK
            self.root = root
        else:
            self.root = None

    def split(self, insertion_node: TreeNode, p: TreeNode) -> AATree:
        """
        Split operation when a double horizontal link is detected

        :param insertion_node: The node we are inserting
        :param p: The parent node in the operation
        :return: The modified Tree
        """

        x = p.parent
        b = p.left

        p.left = x

        if x is not None:
            if x.parent is not None:
                if x.parent.left == x:
                    x.parent.left = p
                    self.skew(p, x.parent)  # need to skew because now we have a left red child
                else:
                    x.parent.right = p
                    if x.parent.color == Color.RED:
                        #  double right links
                        self.split(p, x.parent)
                p.parent = x.parent
            x.parent = p
            x.right = b

        if b is not None:
            b.parent = x

        insertion_node.color = Color.BLACK
        p.right = insertion_node
        insertion_node.parent = p

        if self.root == x:
            p.color = Color.BLACK
            self.root = p
        p.level += 1

        #  now we need to skew because we have a black right child, which is disallowed

    def skew(self, left_node: TreeNode, parent_node: TreeNode) -> AATree:
        """
        Split operation when a left horizontal link is detected

        :param left_node: The node we are inserting
        :param parent_node: The parent node in the operation
        :return: The modified Tree
        """
        l_node_right = left_node.right

        if parent_node.parent is not None and parent_node.parent.left == parent_node:
            parent_node.parent.left = left_node
        elif parent_node.parent is not None:
            parent_node.parent.right = left_node

        left_node.right = parent_node
        parent_node.left = l_node_right
        parent_node.color = Color.RED
        left_node.color = Color.BLACK
        parent_node.parent = left_node
        if parent_node.left is not None:
            parent_node.left.parent = parent_node
        if parent_node == self.root:
            self.root = left_node

    def insert(self, node: TreeNode) -> AATree:
        """
        Inserts a node into the AATree

        :param node: The node we are inserting
        :return: The modified Tree
        """
        # Find place in traditional binary tree fashion
        curr_node: Optional[TreeNode] = self.root
        curr_node_parent: Optional[TreeNode] = None
        while curr_node is not None:
            curr_node_parent = curr_node
            if curr_node.value > node.value:
                curr_node = curr_node.left
            elif curr_node.value < node.value:
                curr_node = curr_node.right
        # found parent, if the node we are inserting is going to the right of the node, then create a horizontal link,
        # and the level of the node is the same level as the parent
        if curr_node_parent.value < node.value:  # inserting node to the right
            # The node we are placing is moving to the right
            curr_node_parent.right = node
            node.level = curr_node_parent.level
            if curr_node_parent.color == Color.RED:
                #  double horizontal, split
                self.split(node, curr_node_parent)
            else:
                node.parent = curr_node_parent
        else:  # inserting node to the left
            node.level = curr_node_parent.level - 1
            self.skew(node, curr_node_parent)
        return self

    def insert_many(self, *args):
        for each_argument in args:
            node = TreeNode(each_argument)
            self.insert(node)

    def delete(self, value: int) -> bool:
        """
        Deletes a node from the tree, given a value to find the node associated with it

        :param value: The value to find, traditional way we insert a node, however, we go until we find the node that matches the value
        :return: Whether the deletion was successful or not
        """

        found_node: Optional[TreeNode] = None
        temporary_root: Optional[TreeNode] = self.root

        while temporary_root is not None:
            if temporary_root.value > value:
                # move to the left
                temporary_root = temporary_root.left
            elif temporary_root.value < value:
                # move to the right
                temporary_root = temporary_root.right
            else:
                # is equal, we found our node
                found_node = temporary_root
                break
        if found_node is None:
            return False

        # found node, keep continuing
        if found_node.color == Color.RED and found_node.left is None:
            # is red and is a leaf
            found_node.parent.right = None
            found_node.parent = None
        elif found_node.color == Color.BLACK and found_node.has_one_child():
            # is a black node and has one child
            if found_node.right is not None:
                found_node.value = found_node.right.value
                found_node.right = None
        elif found_node.color == Color.BLACK and found_node.has_two_children():
            # find minimum of right subtree for successor
            inorder_successor = found_node.right
            while inorder_successor.left is not None:
                inorder_successor = inorder_successor.left
            # found successor
            if inorder_successor.color == Color.RED:
                found_node.value = inorder_successor.value
                found_node.level = inorder_successor.level
            elif inorder_successor.color == Color.BLACK and inorder_successor.right is not None:
                found_node.value = inorder_successor.right.value
                found_node.level = inorder_successor.right.level
                inorder_successor.right = None
            else:
                found_node.value = inorder_successor.value
                found_node.level = inorder_successor.level
            if inorder_successor is not None and inorder_successor.parent is not None:
                if inorder_successor.parent.right == inorder_successor:
                    inorder_successor.parent.right = None
                else:
                    inorder_successor.parent.left = None
            if found_node.right == inorder_successor:
                found_node.right = None
                if found_node.left is not None and found_node.left.level == found_node.level:
                    self.skew(found_node.left, found_node)
            else:
                found_node.left = None
        return True


if __name__ == '__main__':
    tree = AATree()
    root = TreeNode(10)
    root.color = Color.BLACK
    tree.root = root
    tree.insert(TreeNode(5))
    tree.insert(TreeNode(12))
    tree.insert(TreeNode(25))
    tree.insert(TreeNode(26))
    tree.insert(TreeNode(30))
    tree.insert(TreeNode(31))
    tree.delete(30)
