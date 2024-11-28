"""
Team 2 library.

All rights reserved.
"""

import csv


class Graph:
    """
    A class to represent a graph structure and perform structural operations.

    Attributes:
        adjacency_list (dict[int, set[int]]): The adjacency list of the graph, where keys are node IDs
            and values are sets of neighboring node IDs.
        directed (bool): Whether the graph is directed. Defaults to False.
    """

    def __init__(self, directed=False):
        """
        Initialize a new graph.

        :param directed: Whether the graph is directed. Defaults to False.
        :type directed: bool
        """
        self.adjacency_list = {}  # dict[int, set[int]]
        self.directed = directed

    def add_edge(self, node1, node2):
        """
        Add an edge between two nodes.

        :param node1: The first node.
        :type node1: int
        :param node2: The second node.
        :type node2: int
        """
        self.adjacency_list.setdefault(node1, set()).add(node2)
        if not self.directed:
            self.adjacency_list.setdefault(node2, set()).add(node1)

    def remove_edge(self, node1, node2):
        """
        Remove an edge between two nodes.

        :param node1: The first node.
        :type node1: int
        :param node2: The second node.
        :type node2: int
        """
        self.adjacency_list[node1].discard(node2)
        if not self.directed:
            self.adjacency_list[node2].discard(node1)

    def add_node(self, node):
        """
        Add a node to the graph.

        :param node: The node to add.
        :type node: int
        """
        self.adjacency_list.setdefault(node, set())

    def remove_node(self, node):
        """
        Remove a node and all its edges.

        :param node: The node to remove.
        :type node: int
        """
        if node in self.adjacency_list:
            for neighbor in list(self.adjacency_list[node]):
                self.adjacency_list[neighbor].discard(node)
            del self.adjacency_list[node]

    def to_dict(self):
        """
        Convert the adjacency list to a dictionary with sorted neighbors.

        :return: A dictionary representation of the graph.
        :rtype: dict[int, list[int]]
        """
        return {node: sorted(neighbors) for node, neighbors in self.adjacency_list.items()}

    def read_from_csv(self, file_path):
        """
        Load graph data from a CSV file.

        :param file_path: The path to the CSV file.
        :type file_path: str
        """
        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            self.directed = next(reader)[0].strip().lower() == "directed"
            for row in reader:
                if len(row) == 2:
                    node1, node2 = map(int, row)
                    self.add_edge(node1, node2)

    def display(self):
        """
        Print the adjacency list in a readable format.
        """
        print("Adjacency List:")
        for node, neighbors in self.to_dict().items():
            print(f"{node}: {neighbors}")


class GraphAlgorithms:
    """
    A class containing graph analysis methods.
    """

    @staticmethod
    def find_hamiltonian_cycle(graph):
        """
        Find a Hamiltonian cycle in the graph, if it exists.

        :param graph: The graph object to analyze.
        :type graph: Graph
        :return: A list of nodes representing the Hamiltonian cycle, or None if no cycle exists.
        :rtype: list[int] | None
        """
        n = len(graph.adjacency_list)
        path = []  # list[int]

        def is_valid(vertex, position):
            if vertex not in graph.adjacency_list[path[position - 1]]:
                return False
            if vertex in path:
                return False
            return True

        def hamiltonian_util(position):
            if position == n:
                return path[0] in graph.adjacency_list[path[-1]]
            for vertex in graph.adjacency_list:
                if is_valid(vertex, position):
                    path.append(vertex)
                    if hamiltonian_util(position + 1):
                        return True
                    path.pop()
            return False

        start_vertex = next(iter(graph.adjacency_list))
        path.append(start_vertex)
        if hamiltonian_util(1):
            return path
        return None

    @staticmethod
    def find_eulerian_cycle(graph):
        """
        Find an Eulerian cycle in the graph, if it exists.

        :param graph: The graph object to analyze.
        :type graph: Graph
        :return: A list of nodes representing the Eulerian cycle, or a string explaining why it does not exist.
        :rtype: list[int] | str
        """
        if graph.directed:
            return "Directed Eulerian cycle is not supported."

        if not GraphAlgorithms._has_even_degrees(graph) or not GraphAlgorithms._is_connected(graph):
            return "The graph does not have an Eulerian cycle."

        local_graph = {node: list(neighbors) for node, neighbors in graph.adjacency_list.items()}
        cycle = []  # list[int]
        stack = [next(iter(local_graph))]

        while stack:
            u = stack[-1]
            if local_graph[u]:
                v = local_graph[u].pop()
                local_graph[v].remove(u)
                stack.append(v)
            else:
                cycle.append(stack.pop())

        return cycle[::-1]

    @staticmethod
    def _has_even_degrees(graph):
        """
        Check if all vertices in the graph have even degrees.

        :param graph: The graph object to analyze.
        :type graph: Graph
        :return: True if all vertices have even degrees, False otherwise.
        :rtype: bool
        """
        return all(len(neighbors) % 2 == 0 for neighbors in graph.adjacency_list.values())

    @staticmethod
    def _is_connected(graph):
        """
        Check if the graph is connected.

        :param graph: The graph object to analyze.
        :type graph: Graph
        :return: True if the graph is connected, False otherwise.
        :rtype: bool
        """
        visited = set()
        GraphAlgorithms._dfs(graph, next(iter(graph.adjacency_list)), visited)
        return len(visited) == len(graph.adjacency_list)

    @staticmethod
    def _dfs(graph, node, visited):
        """
        Depth-first search helper for connectivity check.

        :param graph: The graph object to analyze.
        :type graph: Graph
        :param node: The starting node for DFS.
        :type node: int
        :param visited: A set of visited nodes.
        :type visited: set[int]
        """
        visited.add(node)
        for neighbor in graph.adjacency_list[node]:
            if neighbor not in visited:
                GraphAlgorithms._dfs(graph, neighbor, visited)

    @staticmethod
    def is_bipartite(graph):
        """
        Check if the graph is bipartite.

        :param graph: The graph object to analyze.
        :type graph: Graph
        :return: True if the graph is bipartite, False otherwise.
        :rtype: bool
        """
        color = {}  # dict[int, int]

        def dfs(node, current_color):
            if node in color:
                return color[node] == current_color
            color[node] = current_color
            return all(dfs(neighbor, 1 - current_color) for neighbor in graph.adjacency_list[node])

        for node in graph.adjacency_list:
            if node not in color and not dfs(node, 0):
                return False
        return True

    @staticmethod
    def three_color_graph(graph):
        """
        Attempt to color the graph using three colors.

        :param graph: The graph object to analyze.
        :type graph: Graph
        :return: A list of nodes and their colors, or a message if coloring is not possible.
        :rtype: list[tuple[int, str]] | str
        """
        vertices = list(graph.adjacency_list.keys())
        colors = {v: None for v in vertices}
        available_colors = ["r", "g", "b"]

        def _color_graph(vertex_index):
            if vertex_index == len(vertices):
                return True

            current_vertex = vertices[vertex_index]
            for color in available_colors:
                if all(colors[neighbor] != color for neighbor in graph.adjacency_list[current_vertex]):
                    colors[current_vertex] = color
                    if _color_graph(vertex_index + 1):
                        return True
                    colors[current_vertex] = None
            return False

        if _color_graph(0):
            return [(vertex, colors[vertex]) for vertex in vertices]
        return "Impossible to color the graph with three colors."
