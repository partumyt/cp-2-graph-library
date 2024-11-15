class Graph:
    """
    A class to represent an undirected graph.

    Provides methods to manipulate the graph, including adding/removing nodes and edges, and checking edge existence.
    """

    def __init__(self):
        """
        Initializes an empty graph.
        """
        self.adjacency_list = {}

    @staticmethod
    def from_file(filename: str) -> 'Graph':
        """
        Reads a graph from a file and creates a Graph instance.

        :param filename: Path to the file containing graph edges in "node1,node2" format.
        :return: An instance of Graph with edges from the file.
        """
        graph = Graph()
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                node1, node2 = map(int, line.strip().split(","))
                graph.add_edge((node1, node2))
        return graph

    def to_edge_list(self) -> list[tuple[int, int]]:
        """
        Converts the graph to a list of edges.

        :return: A list of edges as tuples.
        """
        edges = []
        for node, neighbors in self.adjacency_list.items():
            for neighbor in neighbors:
                if (neighbor, node) not in edges:
                    edges.append((node, neighbor))
        return edges

    def add_edge(self, edge: tuple[int, int]) -> None:
        """
        Adds an edge to the graph.

        :param edge: A tuple representing the edge to add.
        """
        node1, node2 = edge
        self.adjacency_list.setdefault(node1, []).append(node2)
        self.adjacency_list.setdefault(node2, []).append(node1)

    def remove_edge(self, edge: tuple[int, int]) -> None:
        """
        Removes an edge from the graph.

        :param edge: A tuple representing the edge to remove.
        """
        node1, node2 = edge
        self.adjacency_list.get(node1, []).remove(node2) if node2 in self.adjacency_list.get(node1, []) else None
        self.adjacency_list.get(node2, []).remove(node1) if node1 in self.adjacency_list.get(node2, []) else None

    def add_node(self, node: int) -> None:
        """
        Adds a node to the graph.

        :param node: The node to add.
        """
        self.adjacency_list.setdefault(node, [])

    def remove_node(self, node: int) -> None:
        """
        Removes a node and all its incident edges from the graph.

        :param node: The node to remove.
        """
        if node in self.adjacency_list:
            del self.adjacency_list[node]
            for neighbors in self.adjacency_list.values():
                if node in neighbors:
                    neighbors.remove(node)

    def has_edge(self, edge: tuple[int, int]) -> bool:
        """
        Checks if an edge exists in the graph.

        :param edge: A tuple representing the edge to check.
        :return: True if the edge exists, False otherwise.
        """
        node1, node2 = edge
        return node2 in self.adjacency_list.get(node1, []) or node1 in self.adjacency_list.get(node2, [])

    def to_dict(self) -> dict[int, list[int]]:
        """
        Returns the graph as a dictionary of adjacency lists.

        :return: The adjacency list representation of the graph.
        """
        return {node: sorted(neighbors) for node, neighbors in self.adjacency_list.items()}

    def clear(self) -> dict():
        """
        Returns empty dict.

        :return: clear dict
        """
        return dict()
