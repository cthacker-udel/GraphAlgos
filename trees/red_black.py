from __future__ import annotations

from enum import Enum

"""
Enum for the colors, makes it easier to represent
"""


class color(Enum):
    black = 0
    red = 1


"""
The node class, represents a red-black tree node
"""


class Node:
    """
    The initializer, constructs the node class

    :param: self - The node instance
    :param: value - The value to assign to the  node
    """

    def __init__(self, value: int | None = None):
        if value is None:  # if the value is nothing, we are constructing an empty node, NIL, which is colored black
            self.color = color.black
        else:  # if the value is passed, we are making a new node, so set it to red by default
            self.color: color = color.red
        self.right: Node = None  # starts out as None because no children assigned yet
        self.left: Node = None  # starts out as None because no children assigned yet
        self.parent: Node | None = None  # starts out as None because no parent assigned yet
        self.value: int = value if value is not None else 0  # is 0 if the value is not given, else is the value
        self.black_height = 1  # starts out as 1, is not assigned yet
        self.height = 0

    """
    Sets the color of the node
    
    :param: self - The node instance
    :param: color - The new color
    :return: The node instance with the color changed
    """

    def set_color(self, color: color) -> Node:
        self.color = color
        return self

    """
    Sets the right child of the node
    
    :param: self - The node instance
    :param: node - The  new node to assign to the right child of the node
    :return: The node instance with the modified right child
    """

    def set_right(self, node: Node) -> Node:
        self.right = node
        return self

    """
    Sets the left child of the node

    :param: self - The node instance
    :param: node - The  new node to assign to the left child of the node
    :return: The node instance with the modified left child
    """

    def set_left(self, node: Node) -> Node:
        self.left = node
        return self

    """
    Sets the parent of the node

    :param: self - The node instance
    :param: node - The  new node to assign to the parent of the node
    :return: The node instance with the modified parent
    """

    def set_parent(self, node: Node) -> Node:
        self.parent = node
        return self

    """
    Sets the value of the node

    :param: self - The node instance
    :param: node - The  new node to assign to the value of the node
    :return: The node instance with the modified value
    """

    def set_value(self, value: int) -> Node:
        self.value = value
        return self

    """
    Prints the node with it's value, and color
    
    :param: self - The node instance
    """

    def print_node(self) -> None:
        print('Value: {} | Color: {} | Black Height {}'.format(self.value,
                                                               'black' if self.color == color.black else 'red',
                                                               self.black_height))


class Tree:
    """
    Instantiates the tree

    :param: self - The instance of the tree
    :return: None
    """

    def __init__(self):
        self.root: Node | None = None

    """
    Sets the root variable of the Tree instance
    :param: self - The Tree instance
    :param: root - The new node to override the root
    :return: The  tree instance modified
    """

    def set_root(self: Tree, root: Node) -> Tree:
        self.root = root.set_color(color.black)
        return self

    """
    Recolors the entire tree, recursively calling the grandparent if uncle of node is red
    
    :param: self - The  tree instance
    :return: The tree instance modified
    """

    def recolor(self: Tree, curr_node: Node) -> Tree:
        if curr_node is None:
            return self
        elif curr_node == self.root:
            curr_node.color = color.black
            return self
        else:
            if curr_node.parent.parent is not None and curr_node.parent == curr_node.parent.parent.right:  # parent is right child of grandparent
                if curr_node.parent.parent.left is not None and curr_node.parent.parent.left.color == color.red:
                    curr_node.parent.parent.left.color = color.black
                    curr_node.parent.color = color.black
                    curr_node.parent.parent.color = color.red
                    self.recolor(curr_node.parent.parent)
                elif curr_node == curr_node.parent.right:
                    self.right_right_rotation(curr_node)
                elif curr_node == curr_node.parent.left:
                    self.right_left_rotation(curr_node)
            elif curr_node.parent.parent is not None and curr_node.parent == curr_node.parent.parent.left:  # parent is left child of grandparent
                if curr_node.parent.parent is not None and curr_node.parent.parent.right.color == color.red:
                    curr_node.parent.parent.right.color = color.black
                    curr_node.parent.color = color.black
                    curr_node.parent.parent.color = color.red
                    self.recolor(curr_node.parent.parent)
                elif curr_node == curr_node.parent.left:  # node is left child of parent
                    self.left_left_rotation(curr_node)
                elif curr_node == curr_node.parent.right:
                    self.left_right_rotation(curr_node)
        return self

    """
    Executes a left-left rotation on the current node, see more here: https://www.geeksforgeeks.org/insertion-in-red-black-tree/ (I know, geeksforgeeks)
    
    :param: self - The tree instance
    :param: node - The current node we are recursively iterating on
    :return: boolean if the operation was successful, aka it reached the end, just there to return something really, could do a try-catch, but if the operation fails, the tree is broken!
    """

    def left_left_rotation(self, node: Node) -> bool:
        grandparent = node.parent.parent
        parent = node.parent
        grandparent.left = parent.right
        parent.right = grandparent
        parent.parent = grandparent.parent
        if grandparent.parent is not None:
            if grandparent.parent.right == grandparent:
                grandparent.parent.right = parent
            else:
                grandparent.parent.left = parent
        if grandparent == self.root:
            self.set_root(parent)
        grandparent.parent = parent
        return True

    """
    Executes a left-right rotation on the tree, read more here: https://www.geeksforgeeks.org/insertion-in-red-black-tree/
    
    :param: self - The tree instance itself
    :param: node - The current node we are recursively iterated on
    :return: A boolean if the rotation was succesful
    """

    def left_right_rotation(self, node: Node) -> bool:
        grandparent = node.parent.parent
        parent = node.parent
        parent.right = node.left
        node.parent = grandparent
        grandparent.left = node
        parent.parent = node
        if self.root == parent:
            self.set_root(node)
        node.left = parent
        self.left_left_rotation(node)
        return True

    """
    Executes a right-right rotation on the tree, read more here: https://www.geeksforgeeks.org/insertion-in-red-black-tree/
    
    :param: self - The tree instance
    :param: node - The current node we are recursively iterated on
    :return: Boolean indicating if the operation was successful
    """

    def right_right_rotation(self, node: Node) -> bool:
        grandparent = node.parent.parent
        parent = node.parent
        grandparent.right = parent.left
        parent.left = grandparent
        parent.parent = grandparent.parent
        if grandparent.parent is not None:
            if grandparent.parent.right == grandparent:
                grandparent.parent.right = parent
            else:
                grandparent.parent.left = parent
        if grandparent == self.root:
            self.set_root(parent)
        grandparent.parent = parent
        grandparent_color = grandparent.color
        parent_color = parent.color
        grandparent.color, parent.color = parent_color, grandparent_color
        return True

    """
    Executes a right-left rotation on the tree, read more here: https://www.geeksforgeeks.org/insertion-in-red-black-tree/
    
    :param: self - The tree instance
    :param: node - The current node we are recursively iterated on
    :return: Boolean indicating if the operation was a success
    """

    def right_left_rotation(self, node: Node) -> bool:
        grandparent = node.parent.parent
        parent = node.parent

        parent.left = node.right
        node.right = parent
        parent.parent = node
        if self.root == parent:
            self.set_root(node)
        node.parent = grandparent
        grandparent.right = node
        self.right_right_rotation(node)
        return True

    """
    Helper function to take in an variable amount of integers, and insert them into the tree one-by-one
    
    :param: self - The tree instance
    :param: *args - The variable arguments, allows the callee to call this function with as many comma separated integers as they please, as long as it doesn't break anything!
    """

    def insert_many(self, *args) -> Tree:
        for each_number in args:
            self.insert(each_number)
        return self

    """
    Inserts a node into the Tree instance
    
    :param: self - The Tree instance
    :param: nodeInstance - The instance of the node being inserted
    :return: The Red-Black tree instance
    """

    def insert(self: Tree, node_instance: Node | int) -> Tree:
        node: Node | None | int = None
        if type(node_instance) is int:
            node = Node(node_instance)
        if self.root is None:
            self.root = node.set_color(color.black)
            return self
        else:
            curr_node: Node | None = self.root
            while curr_node is not None:
                if curr_node.value > node.value:
                    if curr_node.left is not None:
                        curr_node = curr_node.left
                    else:
                        curr_node.left = node
                        node.parent = curr_node
                        if node.parent.color == color.red:
                            self.recolor(node)
                        return self
                elif curr_node.value < node.value:
                    if curr_node.right is not None:
                        curr_node = curr_node.right
                    else:
                        curr_node.right = node
                        node.parent = curr_node
                        if node.parent.color == color.red:
                            self.recolor(node)
                        return self
            return self

    """
    Prints the tree in-order
    
    :param: self - The Tree instance
    :param: node - The node instance, used for recursion but instantiated to None to not be required on initial call 
    :return: None
    """

    def print_tree_inorder(self, node: Node | None | int = -1) -> None:
        if node == -1:
            node = self.root
        if node is None:
            return
        else:
            self.print_tree_inorder(node.left)
            node.print_node()
            self.print_tree_inorder(node.right)
            return

    """
    Prints the tree in post-order
    
    :param: self - The tree instance
    :param: node - The recursive parameter
    :return: None
    """

    def print_tree_postorder(self, node: Node | None | int = -1) -> None:
        if node == -1:
            node = self.root
        if node is None:
            return
        else:
            self.print_tree_postorder(node.left)
            self.print_tree_postorder(node.right)
            node.print_node()

    """
    Prints the tree in pre-order
    
    :param: self - The tree instance
    :param: node - The recursive parameter
    :return: None
    """

    def print_tree_preorder(self, node: Node | None | int = -1) -> None:
        if node == -1:
            node = self.root
        if node is None:
            return
        else:
            node.print_node()
            self.print_tree_preorder(node.left)
            self.print_tree_preorder(node.right)
            return

    def percolate_height(self, node: Node | None) -> None:
        while node is not None:
            node.height = max(node.left.height if node.left is not None else 0,
                              node.right.height if node.right is not None else 0) + 1
            node = node.parent

    def recompute_black_height(self, curr_node: Node | None | int = -1) -> int | Tree:
        if curr_node == -1:
            curr_node = self.root
        if curr_node is None:
            return 1
        else:
            computed_right = self.recompute_black_height(curr_node.right)
            computed_left = self.recompute_black_height(curr_node.left)
            curr_node.black_height = max(computed_left, computed_right) + (1 if curr_node.color == color.black else 0)
            return curr_node.black_height



if __name__ == '__main__':
    tree: Tree = Tree()
    tree.insert_many(7, 3, 18, 22, 12, 15, 30, 2, 35, 40).recompute_black_height()
    tree.print_tree_postorder()
