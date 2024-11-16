import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from io import StringIO


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

    def from_file(self, file: StringIO) -> None:
        """
        Reads a graph from a file and creates a Graph instance.

        :param file: A file-like object containing graph edges in "node1,node2" format.
        """
        for line in file:
            node1, node2 = map(int, line.strip().split(","))
            self.add_edge((node1, node2))

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

    def clear(self) -> dict:
        """
        Clears the graph's adjacency list.

        :return: An empty dictionary.
        """
        return {}


def draw_graph(G, ax):
    """
    Draws the graph on the provided axes (ax) object.

    :param G: The graph object containing nodes and edges.
    :param ax: The axes on which to draw the graph.
    """
    if len(G.adjacency_list) == 0:  # Check if the graph is empty
        st.warning("Graph is empty!")
        return

    # Convert the adjacency list into a NetworkX graph
    nx_graph = nx.Graph(G.adjacency_list)

    ax.clear()  # Clear the previous drawing (important to reuse the same axes)

    # Draw the graph with updated data
    pos = nx.spring_layout(nx_graph)  # Layout for positioning the nodes
    nx.draw(nx_graph, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold",
            edge_color="gray", ax=ax)
    ax.set_title("Graph Visualization")
    st.pyplot(fig=ax.figure)  # Update the existing figure without creating a new one


def main():
    st.title("Graph Visualization and Interaction")

    # Create a graph instance
    G = Graph()

    # Matplotlib figure and axis for updating graph visualization
    fig, ax = plt.subplots(figsize=(8, 6))

    # File Upload for Graph Data
    uploaded_file = st.file_uploader("Upload a Graph File (CSV format with node1,node2 per line)", type=["csv"])

    if uploaded_file is not None:
        # Read the file content and update the graph
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        G.from_file(stringio)
        st.success("Graph loaded from file!")
        draw_graph(G, ax)  # Automatically visualize after file upload

    # Dropdown for graph operations
    option = st.selectbox("Choose an operation",
                          ("Add Node", "Remove Node", "Add Edge", "Remove Edge", "Visualize Graph"))

    # Add Node
    if option == "Add Node":
        node = st.number_input("Enter Node", min_value=1, step=1)
        if st.button("Add Node"):
            G.add_node(node)
            st.success(f"Node {node} added.")
            draw_graph(G, ax)  # Re-render graph after adding a node

    # Remove Node
    elif option == "Remove Node":
        node = st.number_input("Enter Node to Remove", min_value=1, step=1)
        if st.button("Remove Node"):
            G.remove_node(node)
            st.success(f"Node {node} removed.")
            draw_graph(G, ax)  # Re-render graph after removing a node

    # Add Edge
    elif option == "Add Edge":
        node1 = st.number_input("Enter First Node", min_value=1, step=1)
        node2 = st.number_input("Enter Second Node", min_value=1, step=1)
        if st.button("Add Edge"):
            G.add_edge((node1, node2))
            st.success(f"Edge ({node1}, {node2}) added.")
            draw_graph(G, ax)  # Re-render graph after adding an edge

    # Remove Edge
    elif option == "Remove Edge":
        node1 = st.number_input("Enter First Node", min_value=1, step=1)
        node2 = st.number_input("Enter Second Node", min_value=1, step=1)
        if st.button("Remove Edge"):
            G.remove_edge((node1, node2))
            st.success(f"Edge ({node1}, {node2}) removed.")
            draw_graph(G, ax)  # Re-render graph after removing an edge

    # Visualize Graph
    elif option == "Visualize Graph":
        draw_graph(G, ax)


if __name__ == "__main__":
    main()
