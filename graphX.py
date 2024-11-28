"""
Library to work with graphs

Created by team #2
All rights reserved.
"""

from functools import lru_cache
import csv


class Graph:
    def __init__(self, directed: bool = False) -> None:
        """
        Initializes a new graph instance.

        :param directed: Whether the graph is directed, defaults to False
        :return: None
        """
        self.adjacency_list: dict[int, set[int]] = {}
        self.directed = directed

    def add_edge(self, edge: tuple[int, int], directed: bool = None) -> dict[int, list[int]]:
        """
        Adds an edge between two nodes while preventing duplicate edges.

        :param edge: Tuple containing two nodes (node1, node2) to connect
        :param directed: Override default graph direction type
        :return: Updated adjacency list as dictionary with sorted neighbors
        """
        directed = self.default_directed if directed is None else directed
        node1, node2 = edge
        self.adjacency_list.setdefault(node1, set()).add(node2)
        if not directed:
            self.adjacency_list.setdefault(node2, set()).add(node1)
        return self.to_dict()

    def remove_edge(self, edge: tuple[int, int], directed: bool = None) -> dict[int, list[int]]:
        """
        Removes an existing edge between two nodes.

        :param edge: Tuple containing two nodes (node1, node2) to disconnect
        :param directed: Override default graph direction type
        :return: Updated adjacency list as dictionary with sorted neighbors
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
        Adds a new isolated node to the graph.

        :param node: Integer identifier for the new node
        :return: Updated adjacency list as dictionary with sorted neighbors
        """
        self.adjacency_list.setdefault(node, set())
        return self.to_dict()

    def remove_node(self, node: int) -> dict[int, list[int]]:
        """
        Removes a node and all its connected edges.

        :param node: Integer identifier of node to remove
        :return: Updated adjacency list as dictionary with sorted neighbors
        """
        if node in self.adjacency_list:
            for neighbor in list(self.adjacency_list[node]):
                self.adjacency_list[neighbor].discard(node)
            del self.adjacency_list[node]
        return self.to_dict()

    def to_dict(self) -> dict[int, list[int]]:
        """
        Converts internal adjacency list to dictionary format with sorted neighbors.

        :return: Dictionary representation of graph's adjacency list
        """
        return {node: sorted(neighbors) for node, neighbors in self.adjacency_list.items()}

    def read_from_csv(self, file_path: str) -> dict[int, list[int]]:
        """
        Loads graph structure from CSV file. First line specifies graph type (directed/undirected).

        :param file_path: Path to CSV file containing graph data
        :return: Adjacency list as dictionary with sorted neighbors
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


class CycleGraph(Graph):
    def is_bipartite(self, directed: bool | None = None) -> bool:
        """Check if graph is bipartite using DFS coloring.

        :param directed: Override graph direction type, defaults to None
        :return: True if graph is bipartite, False otherwise
        """
        @lru_cache(maxsize=None)
        def dfs(node: int, current_color: int) -> bool:
            if node in color:
                return color[node] == current_color
            color[node] = current_color
            return all(dfs(neighbor, 1 - current_color)
                      for neighbor in self.adjacency_list[node])

        directed = self.directed if directed is None else directed
        color: dict[int, int] = {}
        return all(node in color or dfs(node, 0)
                  for node in self.adjacency_list)

    def hamiltonian_cycle(self, directed: bool | None = None) -> list[int] | None:
        """Find Hamiltonian cycle using backtracking.

        :param directed: Override graph direction type, defaults to None
        :return: List of vertices forming Hamiltonian cycle if exists, None otherwise
        """
        directed = self.directed if directed is None else directed
        n = len(self.adjacency_list)
        path: list[int] = []

        def is_valid(vertex: int, position: int) -> bool:
            if position == 0:
                return True
            if directed:
                return (vertex in self.adjacency_list[path[position - 1]] and
                       vertex not in path)
            return (vertex in self.adjacency_list[path[position - 1]] and
                   vertex not in path)

        def hamiltonian_util(position: int) -> bool:
            if position == n:
                return (path[0] in self.adjacency_list[path[-1]] if directed
                       else path[0] in self.adjacency_list[path[-1]] and
                       path[-1] in self.adjacency_list[path[0]])

            for vertex in self.adjacency_list:
                if is_valid(vertex, position):
                    path.append(vertex)
                    if hamiltonian_util(position + 1):
                        return True
                    path.pop()
            return False

        start_vertex = next(iter(self.adjacency_list))
        path.append(start_vertex)
        return path if hamiltonian_util(1) else None

    def eulerian_cycle(self, directed: bool | None = None) -> list[int] | str:
        """Find Eulerian cycle using Hierholzer's algorithm.

        :param directed: Override graph direction type, defaults to None
        :return: List of vertices forming Eulerian cycle if exists, error message otherwise
        """
        directed = self.directed if directed is None else directed

        def is_connected() -> bool:
            visited: set[int] = set()

            def dfs(node: int, reverse: bool = False) -> None:
                if node not in visited:
                    visited.add(node)
                    neighbors = ([n for n in self.adjacency_list
                                if node in self.adjacency_list[n]]
                               if reverse and directed
                               else self.adjacency_list[node])
                    for neighbor in neighbors:
                        dfs(neighbor, reverse)

            start_node = next(iter(self.adjacency_list))
            dfs(start_node)
            if len(visited) != len(self.adjacency_list):
                return False
            if directed:
                visited.clear()
                dfs(start_node, True)
                return len(visited) == len(self.adjacency_list)
            return True

        local_graph = {node: list(neighbors)
                      for node, neighbors in self.adjacency_list.items()}

        if directed:
            in_degrees = {node: 0 for node in self.adjacency_list}
            for node, neighbors in self.adjacency_list.items():
                for neighbor in neighbors:
                    in_degrees[neighbor] += 1
            if not all(len(self.adjacency_list[node]) == in_degrees[node]
                      for node in self.adjacency_list):
                return "The directed graph has no Eulerian cycle"
            if not is_connected():
                return "The directed graph is not strongly connected"
        else:
            if not all(len(neighbors) % 2 == 0
                      for neighbors in self.adjacency_list.values()):
                return "The undirected graph has no Eulerian cycle"
            if not is_connected():
                return "The undirected graph is not connected"

        def find_cycle(start: int) -> list[int]:
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

        start_node = next(iter(local_graph))
        cycle = find_cycle(start_node)
        return "No Eulerian cycle exists" if any(local_graph[node]
                                               for node in local_graph) else cycle

    def three_color_graph(self, directed: bool | None = None) -> list[tuple[int, str | None]] | str:
        """
        Attempts to color graph using three colors via backtracking.

        :param directed: Override default graph direction type
        :return: List of (vertex, color) pairs if possible, error message if impossible
        Internal helper methods:
         - Uses degree-based vertex ordering for optimization
         - Colors: "r" (red), "g" (green), "b" (blue)
         - Validates color assignments against neighbors
        """
        directed = self.directed if directed is None else directed
        vertices = list(self.adjacency_list.keys())
        colors: dict[int, str | None] = {v: None for v in vertices}
        available_colors = ["r", "g", "b"]

        degrees = {v: (len(self.adjacency_list[v]) if directed else
                      len(self.adjacency_list[v]) +
                      sum(1 for u in self.adjacency_list if v in self.adjacency_list[u]))
                  for v in vertices}
        degree_order = sorted(vertices, key=lambda v: degrees[v], reverse=True)

        def is_available(vertex: int, color: str) -> bool:
            if directed:
                return all(colors.get(neighbor) != color
                         for neighbor in self.adjacency_list[vertex])
            return all(colors.get(neighbor) != color
                      for neighbor in self.adjacency_list[vertex]) and \
                   all(colors.get(u) != color
                       for u in self.adjacency_list if vertex in self.adjacency_list[u])

        @lru_cache(maxsize=None)
        def color_graph(vertex_index: int) -> bool:
            if vertex_index == len(degree_order):
                return True

            current_vertex = degree_order[vertex_index]
            for color in available_colors:
                if is_available(current_vertex, color):
                    colors[current_vertex] = color
                    if color_graph(vertex_index + 1):
                        return True
                    colors[current_vertex] = None
            return False

        return ([(vertex, colors[vertex]) for vertex in vertices]
                if color_graph(0) else
                "Impossible to color the graph in 3 colors")
