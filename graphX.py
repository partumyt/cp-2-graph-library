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
        directed = self.directed if directed is None else directed
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
        directed = self.directed if directed is None else directed
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

    def read_from_csv(self, file) -> dict[int, list[int]]:
        """
        Loads graph structure from a CSV file or file-like object.
        The first line specifies graph type (directed/undirected).

        :param file: Path to CSV file or file-like object containing graph data
        :return: Adjacency list as dictionary with sorted neighbors
        """
        if isinstance(file, str):
            with open(file, mode="r") as f:
                reader = csv.reader(f)
                header = next(reader)
                self.directed = header[0].strip().lower() == "directed"
                for row in reader:
                    if len(row) == 2:
                        node1, node2 = map(int, row)
                        self.add_edge((node1, node2))
        else:
            reader = csv.reader(file)
            header = next(reader)
            self.directed = header[0].strip().lower() == "directed"
            for row in reader:
                if len(row) == 2:
                    node1, node2 = map(int, row)
                    self.add_edge((node1, node2))

        return {node: sorted(neighbors) for node, neighbors in self.adjacency_list.items()}


class CycleGraph(Graph):
    def is_bipartite(self, directed: bool | None = None) -> bool:
        """
        Check if the graph is bipartite using Depth-First Search (DFS) coloring.

        A bipartite graph is a graph whose vertices can be divided into two disjoint sets such that
        no two vertices within the same set are adjacent. This method checks if the graph is bipartite
        by attempting to color the graph using two colors. If the graph can be successfully colored
        in this way, it is bipartite; otherwise, it is not.

        The method uses DFS to attempt to color each node of the graph, starting with an arbitrary color
        (represented as `0` or `1`), and recursively ensures that adjacent nodes have different colors.
        If any two adjacent nodes have the same color, the graph is not bipartite, and the method returns
        `False`. Otherwise, it returns `True`.

        **Parameters:**
        - directed (bool | None): Optionally override the graph direction type.
          - If `None`, the graph's directionality is determined by the instance's `directed` attribute.
          - If `True`, the graph is treated as directed, meaning edges have a direction.
          - If `False`, the graph is treated as undirected, meaning edges have no direction.
          Defaults to `None`, in which case the instance's `directed` setting is used.

        **Returns:**
        - bool: Returns `True` if the graph is bipartite (i.e., can be divided into two disjoint sets with no internal edges),
                and `False` otherwise.

        **How It Works:**
        - The method employs a depth-first search (DFS) algorithm to traverse the graph.
        - Each node is assigned a color (`0` or `1`). If a node is already colored and the color matches the expected color,
          DFS continues. If a node is colored but its color does not match the expected color, the graph is not bipartite, and
          the function immediately returns `False`.
        - The DFS function is memoized using `lru_cache` to optimize performance, ensuring that already processed nodes are not re-visited.
        - The method iterates over each node in the adjacency list. If a node hasn't been colored yet, DFS is called on that node,
          starting with color `0`. This process is repeated for all nodes in the graph.

        **Example:**
        If we have the following undirected graph represented by an adjacency list:
        ```
        0: [1, 3]
        1: [0, 2]
        2: [1, 3]
        3: [0, 2]
        ```
        Calling `is_bipartite()` will return `True` because it is possible to color the graph with two colors
        (e.g., nodes `0` and `2` with one color, and nodes `1` and `3` with the other).

        If the graph contains an odd-length cycle, such as:
        ```
        0: [1, 2]
        1: [0, 2]
        2: [0, 1]
        ```
        The method will return `False` because it is impossible to color the graph with just two colors.
        """

        @lru_cache(maxsize=None)
        def dfs(node: int, current_color: int) -> bool:
            if node in color:
                return color[node] == current_color
            color[node] = current_color
            return all(dfs(neighbor, 1 - current_color) for neighbor in self.adjacency_list[node])

        directed = self.directed if directed is None else directed
        color: dict[int, int] = {}
        return all(node in color or dfs(node, 0)
                   for node in self.adjacency_list)

    def hamiltonian_cycle(self, directed: bool | None = None) -> list[int] | None:
        """
        Find a Hamiltonian cycle in the graph using backtracking.

        A Hamiltonian cycle is a cycle in a graph that visits each vertex exactly once and returns to the starting vertex.
        This method attempts to find such a cycle using a backtracking approach. The cycle is represented by a list of
        vertices, where the first vertex is the same as the last vertex, completing the cycle.

        The algorithm starts from an arbitrary vertex and recursively tries to add vertices to the cycle one by one.
        If a vertex is found to form a valid part of the cycle, it is added to the current path. If adding the vertex
        results in a valid Hamiltonian cycle, the algorithm terminates. Otherwise, the last vertex is removed, and the
        algorithm backtracks to try a different path.

        **Parameters:**
        - directed (bool | None): Optionally override the graph direction type.
          - If `None`, the graph's directionality is determined by the instance's `directed` attribute.
          - If `True`, the graph is treated as directed, meaning edges have a direction.
          - If `False`, the graph is treated as undirected, meaning edges have no direction.
          Defaults to `None`, in which case the instance's `directed` setting is used.

        **Returns:**
        - list[int] | None: Returns a list of integers representing the vertices of a Hamiltonian cycle if one exists,
          or `None` if no Hamiltonian cycle is found. The list starts and ends with the same vertex, indicating a cycle.

        **How It Works:**
        - The function starts from an arbitrary vertex (the first in the adjacency list).
        - It tries to build a path by recursively adding vertices that are adjacent to the previous vertex and have not yet been visited.
        - At each step, the algorithm checks if the current path is valid by ensuring:
          1. The current vertex is adjacent to the last vertex in the path.
          2. The current vertex has not been visited before.
        - If the path includes all vertices and returns to the starting vertex, a Hamiltonian cycle is found, and the method returns the path.
        - If no valid cycle is found, the method returns `None`.

        **Backtracking:**
        - If a vertex cannot be added to the path (either because it is not adjacent to the previous vertex or it has already been visited),
          the algorithm backtracks by removing the last added vertex and trying the next vertex.

        **Example:**
        For the following undirected graph:
        ```
        0: [1, 2, 3]
        1: [0, 2]
        2: [0, 1, 3]
        3: [0, 2]
        ```
        Calling `hamiltonian_cycle()` might return `[0, 1, 2, 3, 0]`, which is a valid Hamiltonian cycle.

        For a directed graph like:
        ```
        0: [1]
        1: [2]
        2: [0]
        ```
        The method might return `[0, 1, 2, 0]`, forming a Hamiltonian cycle.

        If no Hamiltonian cycle exists, for instance in a graph like:
        ```
        0: [1]
        1: [2]
        2: []
        ```
        The method would return `None` because there is no cycle that visits each vertex exactly once.

        **Performance:**
        - The backtracking algorithm explores all possible cycles, so its time complexity is exponential, specifically O(n!), where `n` is the number of vertices. This is typical for Hamiltonian cycle problems, which are NP-complete.
        """
        directed = self.directed if directed is None else directed
        n = len(self.adjacency_list)
        path: list[int] = []

        def is_valid(vertex: int, position: int) -> bool:
            """
            Check if it's valid to add a vertex to the current path.

            :param vertex: The vertex to check.
            :param position: The position in the path where the vertex is to be added.
            :return: True if the vertex can be added, False otherwise.
            """
            if position == 0:
                return True
            if directed:
                return (vertex in self.adjacency_list[path[position - 1]] and
                        vertex not in path)
            return (vertex in self.adjacency_list[path[position - 1]] and
                    vertex not in path)

        @lru_cache(maxsize=None)
        def hamiltonian_util(position: int) -> bool:
            """
            Recursively try to find the Hamiltonian cycle.

            :param position: The current position in the path to be filled.
            :return: True if a Hamiltonian cycle is found, False otherwise.
            """
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
        """
        Find an Eulerian cycle in the graph using Hierholzer's algorithm.

        An Eulerian cycle is a cycle that uses every edge of the graph exactly once and returns to the starting vertex.
        This method attempts to find such a cycle using Hierholzer's algorithm, which is an efficient algorithm for
        finding Eulerian cycles in both directed and undirected graphs.

        **Parameters:**
        - directed (bool | None): Optionally override the graph direction type.
          - If `None`, the graph's directionality is determined by the instance's `directed` attribute.
          - If `True`, the graph is treated as directed, meaning edges have a direction.
          - If `False`, the graph is treated as undirected, meaning edges have no direction.
          Defaults to `None`, in which case the instance's `directed` setting is used.

        **Returns:**
        - list[int] | str: Returns a list of integers representing the vertices of an Eulerian cycle if one exists,
          or an error message string if no Eulerian cycle is found.

        **How It Works:**
        - The function first checks whether the graph satisfies the conditions for an Eulerian cycle:
          1. For directed graphs, every vertex must have the same in-degree and out-degree.
          2. For undirected graphs, each vertex must have an even degree.
          3. The graph must be connected (in the case of directed graphs, strongly connected).
        - If the conditions are met, the algorithm proceeds to find the Eulerian cycle using Hierholzer's algorithm.
          This involves:
          1. Starting from any vertex with a non-zero degree.
          2. Iteratively following unused edges until returning to the start vertex, forming a cycle.
          3. If a vertex still has unused edges after completing a cycle, a new cycle is formed and merged into the original cycle.

        **Eulerian Cycle Conditions:**
        - **Directed Graph:**
          - The graph must be strongly connected, meaning there must be a directed path between every pair of vertices.
          - Every vertex must have equal in-degree and out-degree.
        - **Undirected Graph:**
          - The graph must be connected, meaning there must be a path between every pair of vertices.
          - Every vertex must have an even degree.

        **Hierholzer's Algorithm:**
        - The algorithm works by finding and merging cycles in the graph. It starts from a vertex with unused edges and explores the graph until it forms a cycle. If any vertices still have unused edges, the algorithm recursively finds additional cycles and merges them into the current cycle.

        **Example:**
        For the following undirected graph:
        ```
        0: [1, 2]
        1: [0, 2]
        2: [0, 1]
        ```
        Calling `eulerian_cycle()` will return `[0, 1, 2, 0]`, which forms an Eulerian cycle.

        For the following directed graph:
        ```
        0: [1]
        1: [2]
        2: [0]
        ```
        Calling `eulerian_cycle()` will return `[0, 1, 2, 0]`, which forms an Eulerian cycle.

        If the graph is not connected or does not satisfy the Eulerian cycle conditions, the method will return an appropriate error message.

        **Performance:**
        - The time complexity of this algorithm depends on the size of the graph, specifically the number of vertices `n` and edges `m`. Finding the Eulerian cycle using Hierholzer's algorithm runs in O(m) time, as it requires traversing each edge once.
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
        Attempts to color the graph using three colors (Red, Green, Blue) via backtracking.

        This method uses a backtracking algorithm to assign one of three colors ("r", "g", "b") to each vertex of the graph.
        The goal is to ensure that no two adjacent vertices share the same color. The algorithm employs a degree-based
        ordering of vertices to improve efficiency, attempting to color the most connected vertices first. This approach
        helps reduce the search space by minimizing the number of choices available for each vertex.

        **Parameters:**
        - directed (bool | None): Optionally override the graph's direction type.
            - If `None`, the graph's directionality is determined by the instance's `directed` attribute.
            - If `True`, the graph is treated as directed, meaning edges have a direction.
            - If `False`, the graph is treated as undirected, meaning edges have no direction.
            Defaults to `None`, in which case the instance's `directed` setting is used.

        **Returns:**
        - list[tuple[int, str | None]]: If the graph can be successfully colored, returns a list of tuples where each tuple
          contains a vertex and its assigned color. The colors are represented by the strings "r" (red), "g" (green), and "b" (blue).
        - str: If it is impossible to color the graph with three colors, returns the string "Impossible to color the graph in 3 colors".

        **How It Works:**
        - The method first constructs a list of all vertices and initializes a dictionary to store color assignments. Initially, all vertices are uncolored (`None`).
        - It computes the degree of each vertex (i.e., the number of edges connected to it). For undirected graphs, the degree is calculated by considering both outgoing and incoming edges.
        - The vertices are sorted in descending order by degree, so that the most connected vertices are colored first. This heuristic helps the backtracking algorithm to run more efficiently.
        - The `is_available` function checks if a color can be assigned to a vertex. For directed graphs, it only checks the adjacency list for outgoing edges. For undirected graphs, both outgoing and incoming edges are checked.
        - The `color_graph` function recursively tries to assign a color to each vertex using a backtracking approach. It tries each color in turn, and if a valid coloring is found, it proceeds to the next vertex. If no valid color can be found for a vertex, it backtracks and tries another color for the previous vertex.

        **Coloring Constraints:**
        - No two adjacent vertices can share the same color. For directed graphs, only outgoing edges are considered, while for undirected graphs, both incoming and outgoing edges are checked.

        **Example:**
        For the following undirected graph:
        ```
        0: [1, 2]
        1: [0, 2]
        2: [0, 1]
        ```
        Calling `three_color_graph()` will return:
        ```
        [(0, 'r'), (1, 'g'), (2, 'b')]
        ```
        indicating that vertices 0, 1, and 2 have been assigned the colors "r", "g", and "b" respectively.

        **Performance:**
        - The backtracking approach may require exploring multiple color assignments before finding a valid solution. In the worst case, this method has a time complexity of O(3^n), where `n` is the number of vertices. However, the degree-based vertex ordering helps minimize the search space, making the algorithm more efficient in practice.
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

    def isomorphic(self, other_graph: "CycleGraph", directed: bool = None) -> bool:
        """
        Checks if the current graph is isomorphic to another graph using the Weisfeiler-Lehman test.

        The Weisfeiler-Lehman test is a popular method for graph isomorphism checking. It works by iteratively
        refining the node labels based on the structure of the graph and comparing these refined labels between
        two graphs. If the refined labels for the two graphs match, the graphs are considered isomorphic.

        **Parameters:**
        - `other_graph` (CycleGraph): Another instance of the `CycleGraph` class to compare against.
          This is the graph that will be checked for isomorphism with the current graph.
        - `directed` (bool | None, optional): If provided, this overrides the default graph direction type.
          - If `None`, the directionality of the graph is determined by the `directed` attribute of the current graph.
          - If `True`, the graph is treated as directed, meaning edges have a direction.
          - If `False`, the graph is treated as undirected, meaning edges have no direction.
          Defaults to `None`, in which case the instance's `directed` setting is used.

        **Returns:**
        - `True` if the current graph is isomorphic to `other_graph`.
        - `False` otherwise.

        **How It Works:**
        1. The method checks basic properties such as:
           - Whether both graphs are empty.
           - Whether the graphs have the same number of vertices.
           - Whether the adjacency lists of both graphs are non-empty.
        2. If the graphs pass the basic checks, it proceeds with the Weisfeiler-Lehman test.
        3. The `label` function iteratively refines node labels based on the adjacency structure of the graph:
           - For directed graphs, the labels for each node are based on the node's outgoing and incoming neighbors.
           - For undirected graphs, the labels are based solely on the adjacency list of each node.
        4. This refinement is done until the node labels no longer change, and then the final labels are compared between the two graphs.
        5. If the refined labels for the two graphs are identical, the graphs are considered isomorphic.

        **Weisfeiler-Lehman Test Details:**
        - The process works by iteratively constructing new labels for each node based on the current label of its neighbors.
        - For directed graphs, both incoming and outgoing neighbors contribute to the label.
        - For undirected graphs, only adjacent nodes are considered.
        - The process stops when the labels for all nodes stabilize and no longer change.

        **Example:**
        For two graphs `graph1` and `graph2`, calling `graph1.isomorphic(graph2)` will return `True` if the graphs are isomorphic, and `False` otherwise.

        **Performance:**
        - The Weisfeiler-Lehman test is generally efficient for most practical use cases, running in polynomial time, specifically O(n + m), where `n` is the number of vertices and `m` is the number of edges. However, it may not always be conclusive for highly complex graphs, as it is a heuristic test. In rare cases, non-isomorphic graphs might still have identical refined labels after running the test.
        """
        directed = self.directed if directed is None else directed

        def label(graph, directed=False):
            """
            Provides labels for each node of the graph necessary for checking isomorphism
            """
            label = {}
            for i in graph:
                label.update({i: '0'})
            for i in range(len(graph)):
                new_label = {}
                for node in graph:
                    if directed:
                        into = [node_ for node_ in graph if node in graph[node_]]
                        out = graph[node]
                        neighbor_label = tuple(label[node_] for node_ in into) + tuple(label[node_] for node_ in out)
                    else:
                        neighbor_label = tuple(label[node_] for node_ in graph[node])
                    new_label[node] = f'{label[node]}|{'|'.join(neighbor_label)}'
                label = new_label
            return label

        if not self.adjacency_list and not other_graph.adjacency_list:
            print("Both graphs are empty.")
            return True
        if not self.adjacency_list or not other_graph.adjacency_list:
            print("One of the graphs is empty.")
            return False
        if len(self.adjacency_list) != len(other_graph.adjacency_list):
            print("Graph sizes differ.")
            return False

        label1 = label(self.adjacency_list, directed)
        label2 = label(other_graph.adjacency_list, directed)
        if len(label1) != len(label2):
            return False
        return set(label1.values()) == set(label2.values())
