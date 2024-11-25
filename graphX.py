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
        self.default_directed = directed

    def add_edge(self, edge: tuple[int, int], directed: bool = None) -> dict[int, list[int]]:
        """
        Add an edge between two nodes. Ensures no duplicate edges are added.

        :param edge: A tuple representing the edge (node1, node2).
        :param directed: Whether the graph is directed or undirected.
        :return: The updated adjacency list as a dictionary with sorted neighbors.
        """
        directed = self.default_directed if directed is None else directed
        node1, node2 = edge
        self.adjacency_list.setdefault(node1, set()).add(node2)
        if not directed:
            self.adjacency_list.setdefault(node2, set()).add(node1)
        return self.to_dict()

    def remove_edge(self, edge: tuple[int, int], directed: bool = None) -> dict[int, list[int]]:
        """
        Remove an edge between two nodes.

        :param edge: A tuple representing the edge (node1, node2).
        :param directed: Whether the graph is directed or undirected.
        :return: The updated adjacency list as a dictionary with sorted neighbors.
        """
        directed = self.default_directed if directed is None else directed
        node1, node2 = edge
        if node1 in self.adjacency_list:
            self.adjacency_list[node1].discard(node2)
        if not directed and node2 in self.adjacency_list:
            self.adjacency_list[node2].discard(node1)
        return self.to_dict()

    def add_node(self, node: int) -> dict[int, list[int]]:
        """
        Add a new node to the graph.

        :param node: The node to be added.
        :return: The updated adjacency list as a dictionary with sorted neighbors.
        """
        self.adjacency_list.setdefault(node, set())
        return self.to_dict()

    def remove_node(self, node: int) -> dict[int, list[int]]:
        """
        Remove a node and all its associated edges from the graph.

        :param node: The node to be removed.
        :return: The updated adjacency list as a dictionary with sorted neighbors.
        """
        if node in self.adjacency_list:
            for neighbor in list(self.adjacency_list[node]):
                self.adjacency_list[neighbor].discard(node)
            del self.adjacency_list[node]
        return self.to_dict()

    def to_dict(self) -> dict[int, list[int]]:
        """
        Get the graph's adjacency list as a dictionary with sorted neighbors.

        :return: A dictionary representation of the graph's adjacency list.
        """
        return {node: sorted(neighbors) for node, neighbors in self.adjacency_list.items()}

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

    def is_bipartite(self, directed: bool = None) -> bool:
        """
        Check if the graph is bipartite.

        :param directed: Whether the graph is directed or undirected.
        :return: True if the graph is bipartite, False otherwise.
        """
        directed = self.default_directed if directed is None else directed
        color: dict[int, int] = {}

        def dfs(node: int, current_color: int) -> bool:
            if node in color:
                return color[node] == current_color
            color[node] = current_color
            neighbors = self.adjacency_list[node]

            for neighbor in neighbors:
                if not dfs(neighbor, 1 - current_color):
                    return False

            return True
        for node in self.adjacency_list:
            if node not in color:
                if not dfs(node, 0):
                    return False
        return True

    def hamiltonian_cycle(self, directed: bool = None) -> list[int] | None:
        """
        Find a Hamiltonian cycle in the graph, if it exists.

        :param directed: Whether the graph is directed or undirected.
        :return: A list of nodes representing the Hamiltonian cycle, or None if no cycle exists.
        """
        directed = self.default_directed if directed is None else directed
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

    def eulerian_cycle(self, directed: bool = None) -> list[int] | str:
        """
        Find the Eulerian cycle for the graph (directed or undirected).

        :param directed: Whether the graph is directed or undirected.
        :return: A list of vertices in the Eulerian cycle, or a message if no cycle exists.
        """
        directed = self.default_directed if directed is None else directed

        def has_even_degrees() -> bool:
            """Check if all vertices in an undirected graph have even degrees."""
            return all(len(neighbors) % 2 == 0 for neighbors in self.adjacency_list.values())

        def has_equal_in_out_degrees() -> bool:
            """Check if all vertices in a directed graph have equal in-degree and out-degree."""
            in_degrees = {node: 0 for node in self.adjacency_list}
            for node, neighbors in self.adjacency_list.items():
                for neighbor in neighbors:
                    in_degrees[neighbor] += 1
            return all(len(self.adjacency_list[node]) == in_degrees[node] for node in self.adjacency_list)

        def is_connected(for_directed: bool) -> bool:
            """
            Check if the graph is connected.

            For directed graphs, checks strong connectivity (using forward and reverse DFS).
            For undirected graphs, checks simple connectivity (using single DFS).
            """
            visited = set()

            def dfs(node: int, reverse: bool = False):
                if node not in visited:
                    visited.add(node)
                    neighbors = (
                        [n for n in self.adjacency_list if node in self.adjacency_list[n]]
                        if reverse and for_directed else
                        self.adjacency_list[node]
                    )
                    for neighbor in neighbors:
                        dfs(neighbor, reverse=reverse)
            start_node = next(iter(self.adjacency_list))
            dfs(start_node, reverse=False)
            if len(visited) != len(self.adjacency_list):
                return False
            if for_directed:
                visited.clear()
                dfs(start_node, reverse=True)
                if len(visited) != len(self.adjacency_list):
                    return False

            return True

        def find_cycle(start: int, local_graph: dict[int, list[int]]) -> list[int]:
            """
            Find an Eulerian cycle using Hierholzer's algorithm.
            """
            stack = [start]
            cycle = []
            while stack:
                u = stack[-1]
                if local_graph[u]:
                    v = local_graph[u].pop()
                    if not directed:
                        local_graph[v].remove(u)
                    stack.append(v)
                else:
                    cycle.append(stack.pop())
            return cycle[::-1]

        if directed:
            if not has_equal_in_out_degrees():
                return "The directed graph does not have an Eulerian cycle"
            if not is_connected(for_directed=True):
                return "The directed graph is not strongly connected"
        else:
            if not has_even_degrees():
                return "The undirected graph does not have an Eulerian cycle"
            if not is_connected(for_directed=False):
                return "The undirected graph is not connected"

        local_graph = {node: list(neighbors) for node, neighbors in self.adjacency_list.items()}
        start_node = next(iter(local_graph))
        cycle = find_cycle(start_node, local_graph)
        if any(local_graph[node] for node in local_graph):
            return "The graph does not have an Eulerian cycle"

        return cycle

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
