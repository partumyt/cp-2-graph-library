"""
Library to work with graphs

Created by team #2
"""

import csv

class Graph:
    """
    A class representing a graph, supporting both directed and undirected graphs.
    Provides functionalities such as adding/removing nodes and edges, detecting Hamiltonian/Eulerian cycles,
    checking bipartiteness, converting the adjacency list to a dictionary, and coloring the graph using 3 colors.

    Attributes:
        adjacency_list (dict[int, set[int]]): The adjacency list representation of the graph using sets.
        directed (bool): Indicates if the graph is directed or undirected.
    """
    def __init__(self, directed: bool = False):
        """
        Initialize a new graph.

        :param directed: Whether the graph is directed. Defaults to False (undirected).
        """
        self.adjacency_list: dict[int, set[int]] = {}
        self.directed = directed

    def add_edge(self, edge: tuple[int, int]) -> None:
        """
        Add an edge between two nodes. Ensures no duplicate edges are added.

        :param edge: A tuple representing the edge (node1, node2).
        """
        node1, node2 = edge
        self.adjacency_list.setdefault(node1, set()).add(node2)
        if not self.directed:
            self.adjacency_list.setdefault(node2, set()).add(node1)

    def remove_edge(self, edge: tuple[int, int]) -> None:
        """
        Remove an edge between two nodes.

        :param edge: A tuple representing the edge (node1, node2).
        """
        node1, node2 = edge
        self.adjacency_list.get(node1, set()).discard(node2)
        if not self.directed:
            self.adjacency_list.get(node2, set()).discard(node1)

    def add_node(self, node: int) -> None:
        """
        Add a new node to the graph.

        :param node: The node to be added.
        """
        self.adjacency_list.setdefault(node, set())

    def remove_node(self, node: int) -> None:
        """
        Remove a node and all its associated edges from the graph.

        :param node: The node to be removed.
        """
        if node in self.adjacency_list:
            for neighbor in list(self.adjacency_list[node]):
                self.adjacency_list[neighbor].discard(node)
            del self.adjacency_list[node]

    def read_from_csv(self, file_path: str) -> dict[int, list[int]]:
        """
        Read a graph from a CSV file. The first line specifies whether the graph is directed or undirected.
        Subsequent lines represent edges as pairs of nodes.

        :param file_path: The path to the CSV file.
        :return: The adjacency list of the graph as a dictionary with sorted sets as values.
        """
        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            header = next(reader)
            self.directed = header[0].strip().lower() == "directed"
            for row in reader:
                if len(row) == 2:
                    node1, node2 = map(int, row)
                    self.add_edge((node1, node2))
        sorted_adjacency_list = {node: sorted(neighbors) for node, neighbors in self.adjacency_list.items()}
        return sorted_adjacency_list

    def is_bipartite(self) -> bool:
        """
        Check if the graph is bipartite.

        :return: True if the graph is bipartite, False otherwise.
        """
        color: dict[int, int] = {}

        def dfs(node: int, current_color: int) -> bool:
            if node in color:
                return color[node] == current_color
            color[node] = current_color
            neighbors = self.adjacency_list[node]
            if self.directed:
                # Include incoming edges for directed graphs
                neighbors.update(v for v in self.adjacency_list if node in self.adjacency_list[v])
            return all(dfs(neighbor, 1 - current_color) for neighbor in neighbors)

        return all(dfs(node, 0) for node in self.adjacency_list if node not in color)

    def hamiltonian_cycle(self) -> list[int] | None:
        """
        Find a Hamiltonian cycle in the graph, if it exists.

        :return: A list of nodes representing the Hamiltonian cycle, or None if no cycle exists.
        """
        n = len(self.adjacency_list)
        path: list[int] = []

        def is_valid(vertex: int, position: int) -> bool:
            if vertex not in self.adjacency_list[path[position - 1]]:
                return False
            if vertex in path:
                return False
            return True

        def hamiltonian_util(position: int) -> bool:
            if position == n:
                return path[0] in self.adjacency_list[path[-1]]
            for vertex in self.adjacency_list.keys():
                if is_valid(vertex, position):
                    path.append(vertex)
                    if hamiltonian_util(position + 1):
                        return True
                    path.pop()
            return False

        start_vertex = next(iter(self.adjacency_list))
        path.append(start_vertex)
        if hamiltonian_util(1):
            return path
        return None

    def eulerian_cycle(self) -> list[int] | str:
        """
        Find an Eulerian cycle in the graph, if it exists.

        :return: A list of nodes representing the Eulerian cycle, or a message if no cycle exists.
        """
        def find_cycle(start: int) -> list[int]:
            stack = [start]
            cycle = []
            local_graph = {node: neighbors.copy() for node, neighbors in self.adjacency_list.items()}
            while stack:
                u = stack[-1]
                if local_graph[u]:
                    v = local_graph[u].pop()
                    if not self.directed:
                        local_graph[v].remove(u)
                    stack.append(v)
                else:
                    cycle.append(stack.pop())
            return cycle[::-1]

        if self.directed:
            for node in self.adjacency_list:
                out_degree = len(self.adjacency_list[node])
                in_degree = sum(1 for neighbors in self.adjacency_list.values() if node in neighbors)
                if out_degree != in_degree:
                    return "The directed graph does not have an Eulerian cycle"
        else:
            if any(len(neighbors) % 2 != 0 for neighbors in self.adjacency_list.values()):
                return "The undirected graph does not have an Eulerian cycle"

        cycle = find_cycle(next(iter(self.adjacency_list)))
        if any(local_graph for local_graph in self.adjacency_list.values()):
            return "The graph does not have an Eulerian cycle"
        return cycle

    def to_dict(self) -> dict[int, list[int]]:
        """
        Get the graph's adjacency list as a dictionary with sorted neighbors.

        :return: A dictionary representation of the graph's adjacency list.
        """
        return {node: sorted(neighbors) for node, neighbors in self.adjacency_list.items()}

    def display(self) -> None:
        """
        Print the adjacency list in a readable format.
        """
        print("Adjacency List:")
        for node, neighbors in self.to_dict().items():
            print(f"{node}: {neighbors}")

    def label(self) -> dict[int, str]:
        """
        Provides labels for each node of the graph necessary for checking isomorphism.

        :return: A dictionary with nodes as keys and labels as values.
        """
        label = {node: '0' for node in self.adjacency_list}
        for _ in range(len(self.adjacency_list)):
            new_label = {}
            for node in self.adjacency_list:
                if self.directed:
                    into = [n for n in self.adjacency_list if node in self.adjacency_list[n]]
                    out = self.adjacency_list[node]
                    neighbor_label = tuple(label[n] for n in into) + tuple(label[n] for n in out)
                else:
                    neighbor_label = tuple(label[n] for n in self.adjacency_list[node])
                new_label[node] = f'{label[node]}|{"|".join(neighbor_label)}'
            label = new_label
        return label

    def isomorphic(self, other: 'Graph') -> bool:
        """
        Check if two graphs are isomorphic.

        :param other: The other graph to compare against.
        :return: True if the graphs are isomorphic, False otherwise.
        """
        if len(self.adjacency_list) != len(other.adjacency_list):
            return False
        return set(self.label().values()) == set(other.label().values())

    def three_color_graph(self) -> list[tuple[int, str | None]] | str:
        vertices = list(self.adjacency_list.keys())
        colors = {v: None for v in vertices}
        available_colors = ["r", "g", "b"]
        degrees = {v: len(neighbors) for v, neighbors in self.adjacency_list.items()}
        degree_order = sorted(vertices, key=lambda v: degrees[v], reverse=True)

        if self.color_graph(colors, 0, available_colors, degree_order):
            if all(colors[vertex] is not None for vertex in vertices):
                return [(vertex, colors[vertex]) for vertex in vertices]
        return "Impossible to color the graph in 3 colors"

    def color_graph(self, colors: dict[int, str | None], vertex_index: int, available_colors: list[str],
                    degree_order: list[int]) -> bool:
        if vertex_index == len(degree_order):
            return True

        current_vertex = degree_order[vertex_index]
        for color in available_colors:
            if self.is_available(current_vertex, color, colors):
                colors[current_vertex] = color
                if self.color_graph(colors, vertex_index + 1, available_colors, degree_order):
                    return True
                colors[current_vertex] = None
        return False

    def is_available(self, vertex: int, color: str, colors: dict[int, str]) -> bool:
        return all(colors[neighbor] != color for neighbor in self.adjacency_list[vertex])
