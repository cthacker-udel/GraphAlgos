from __future__ import annotations

from queue import Queue
from typing import List, Set
from enum import Enum


class NodeLabel(Enum):
    NOT_DISCOVERED = 0
    DISCOVERED = 1
    FULLY_DISCOVERED = 2


class DFSOrder(Enum):
    PREORDER = 0
    POSTORDER = 1
    REVERSE_PREORDER = 2
    REVERSE_POSTORDER = 3


class Stack:  # FILO data structure
    def __init__(self, *values):
        self.internal_array = [] + values if values else []

    def push(self, value) -> Stack:
        self.internal_array.insert(0, value)
        return self

    def pop(self) -> Node:
        return self.internal_array.pop()

    def empty(self) -> bool:
        return len(self.internal_array) == 0


class Edge:
    def __init__(self, node: Node, distance: int):
        self.node = node
        self.distance = distance


class Node:
    def __init__(self, value: int = 0):
        self.left: Node | None = None
        self.right: Node | None = None
        self.value: Node | None = value
        self.parent: Node | None = None
        self.height: int = 1
        self.connections: List[Node] = []
        self.edges: List[Edge] = []
        self.label: NodeLabel = NodeLabel.NOT_DISCOVERED
        self.distance = 0
        self.letter_label = ''

    def set_parent(self, node: Node) -> Node:
        self.parent = node
        return self

    def set_value(self, value: int) -> Node:
        self.value = value
        return self

    def set_left(self, node: Node) -> Node:
        self.left = node
        return self

    def set_right(self, node: Node) -> Node:
        self.right = node
        return self

    def set_height(self, height: int) -> Node:
        self.height = height
        return self

    def connect(self, node: Node) -> Node:
        self.connections.append(node)
        return self

    def add_edge(self, node: Node, distance: int) -> Node:
        self.edges.append(Edge(node, distance))
        node.edges.append(Edge(self, distance))
        return self

    def set_label(self, label: NodeLabel) -> Node:
        self.label = label
        return self

    def set_distance(self, distance: int) -> Node:
        self.distance = distance
        return self

    def print_node(self) -> None:
        print('Value {} | Distance {} | Label {}'.format(self.value, self.distance, self.letter_label))

    def set_letter_label(self, label: str) -> Node:
        self.letter_label = label
        return self


class Graph:
    def __init__(self, root: Node | None = None):
        self.root = root
        self.vertices: List[Node] = []

    def insert_vertex(self, node: Node | None):
        self.vertices.append(node)

    def insert_vertexes(self, nodes: List[Node]):
        for each_node in nodes:
            self.vertices.append(each_node)

    """
        What breadth first search does, is it searches all levels of the tree one by one, exploring all possible paths up to that depth level, without going all
        the way down the tree, so therefore if there exists the answer on any level, without exhausting all complete paths top to bottom, it searches level
        by level.
        
        :param: self - The instance
        :param: root - The root node
        :param: node - The node instance
        :return: the target node we were looking for
    """

    def bfs(self, root: Node,
            node: Node):  # Time complexity is O(|V| + |E|), because every vertex and every edge can potentially be traveled in the algorithm
        node_queue = Queue()  # create a queue to house the nodes
        root.set_label(NodeLabel.DISCOVERED)  # set root as discovered
        node_queue.put(root)  # Place the root into the queue
        while not node_queue.empty():
            vertex: Node = node_queue.get()  # get the node off the top of the queue
            if vertex == node:  # checks if the node is the node that we are aiming for, the  target node
                return node
            else:  # if it is not the target node
                for each_edge_vertex in vertex.connections:  # go to each node adjacent to the node
                    if each_edge_vertex.label == NodeLabel.NOT_DISCOVERED:  # if the node is not discovered yet
                        each_edge_vertex.label = NodeLabel.DISCOVERED  # mark the node as discovered
                        each_edge_vertex.parent = vertex  # change the nodes parent to the vertex
                        node_queue.put(each_edge_vertex)  # places the node on the queue (FIFO)

    def dfs(self, root: Node, target: Node,
            order: DFSOrder = DFSOrder.PREORDER) -> Node:  # Time complexity O(|V| + |E|), because the worst case scenario we iterate over every vertex and every edge in the  algorithm
        node_stack = Stack()
        order = []
        root.set_label(NodeLabel.DISCOVERED)
        node_stack.push(root)
        while not node_stack.empty():
            vertex: Node = node_stack.pop()
            if order == DFSOrder.PREORDER:
                order.append(vertex.value)
            if vertex == Node:
                return Node
            else:
                for each_edge_vertex in vertex.connections:
                    if each_edge_vertex.label == NodeLabel.NOT_DISCOVERED:
                        each_edge_vertex.label = NodeLabel.DISCOVERED
                        each_edge_vertex.parent = vertex
                        node_stack.push(each_edge_vertex)

    def dijkstras(self, initialNode: Node, target: Node) -> List[Node]:
        unvisited_set: List[Node] = []
        for eachnode in self.vertices:
            unvisited_set.append(eachnode.set_label(NodeLabel.NOT_DISCOVERED).set_distance(0 if eachnode.value == initialNode.value else float('inf')))
        i = 0
        current_node: Node = unvisited_set[0]
        while i < len(unvisited_set) and current_node is not None:
            # iterate through all it's neighbors, comparing the distances
            i += 1
            min_dist = float('inf')
            min_node = None
            for eachedge in current_node.edges:
                if eachedge.node.label != NodeLabel.DISCOVERED:
                    eachedge.node.distance = min(eachedge.node.distance, current_node.distance + eachedge.distance)
            current_node.set_label(NodeLabel.DISCOVERED)
            for eachedge in current_node.edges:
                if eachedge.node.distance < min_dist and eachedge.node.label != NodeLabel.DISCOVERED:
                    min_dist = eachedge.node.distance
                    min_node = eachedge.node
            current_node = min_node
        print('done!')

    def prims(self, graph: Graph):
        if len(graph.vertices) == 0:
            print('Unable to calculate prim\'s with graph with 0 vertices')
            return None

        mst_set: Set[Node] = set()
        graph.vertices[0].set_distance(0)
        for each_node in graph.vertices[1:]:
            each_node.set_distance(float('inf'))
        while len(mst_set) < len(graph.vertices):
            for each_node in mst_set:
                if each_node not in mst_set:
                    #  iterate through all adjacent nodes
                    mst_set.add(each_node)
                    for each_edge in each_node.edges:
                        #  calculate edge weight
                        edge_weight = each_edge.distance
                        if edge_weight < each_edge.node.distance:
                            each_edge.node.distance = edge_weight




if __name__ == '__main__':
    # g = Node(1).set_letter_label('g')
    # r = Node(2).set_letter_label('r')
    # s = Node(3).set_letter_label('s')
    # d = Node(4).set_letter_label('d')
    # h = Node(5).set_letter_label('h')
    # p = Node(6).set_letter_label('p')
    # a = Node(7).set_letter_label('a')
    # g.add_edge(r, 1)
    # g.add_edge(a, 3)
    # a.add_edge(r, 1)
    # a.add_edge(p, 3)
    # a.add_edge(d, 9)
    # r.add_edge(d, 7)
    # r.add_edge(p, 5)
    # r.add_edge(s, 2)
    # d.add_edge(s, 12)
    # d.add_edge(h, 1)
    # d.add_edge(p, 2)
    # h.add_edge(p, 2)
    # h.add_edge(g, 10)
    # G = Graph()
    # G.insert_vertexes([g, r, s, d, h, p, a])
    # G.dijkstras(g, h)

    a = Node().set_label('a').set_distance(0)
    b = Node().set_label('b').set_distance(1)
    c = Node().set_label('c').set_distance(2)
    d = Node().set_label('d').set_distance(3)
    e = Node().set_label('e').set_distance(4)
    f = Node().set_label('f').set_distance(5)
    g = Node().set_label('g').set_distance(6)
    h = Node().set_label('h').set_distance(7)
    i = Node().set_label('i').set_distance(8)


