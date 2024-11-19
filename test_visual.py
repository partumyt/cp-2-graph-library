import time
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from io import StringIO


class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def from_file(self, file: StringIO) -> None:
        for line in file:
            node1, node2 = map(int, line.strip().split(","))
            self.add_edge((node1, node2))

    def to_edge_list(self) -> list[tuple[int, int]]:
        edges = []
        for node, neighbors in self.adjacency_list.items():
            for neighbor in neighbors:
                if (neighbor, node) not in edges:
                    edges.append((node, neighbor))
        return edges

    def add_edge(self, edge: tuple[int, int]) -> None:
        node1, node2 = edge
        self.adjacency_list.setdefault(node1, []).append(node2)
        self.adjacency_list.setdefault(node2, []).append(node1)

    def remove_edge(self, edge: tuple[int, int]) -> None:
        node1, node2 = edge
        self.adjacency_list.get(node1, []).remove(node2) if node2 in self.adjacency_list.get(node1, []) else None
        self.adjacency_list.get(node2, []).remove(node1) if node1 in self.adjacency_list.get(node2, []) else None

    def add_node(self, node: int) -> None:
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def remove_node(self, node: int) -> None:
        """
        Removes a node and all its incident edges from the graph.
        """
        if node in self.adjacency_list:
            # Remove this node from all its neighbors' adjacency lists
            for neighbor in self.adjacency_list[node]:
                if neighbor in self.adjacency_list:
                    self.adjacency_list[neighbor].remove(node)

            # Delete the node's adjacency list
            del self.adjacency_list[node]

    def clear(self) -> None:
        self.adjacency_list.clear()

    def to_dict(self) -> dict[int, list[int]]:
        return {node: sorted(neighbors) for node, neighbors in self.adjacency_list.items()}


class GraphVisualizer:
    def __init__(self):
        self.colors = {}

    def draw_graph(self, G: Graph, plot_placeholder):
        """
        Draws the graph and ensures updates occur in the same placeholder.
        """
        if len(G.adjacency_list) == 0:
            plot_placeholder.warning("Graph is empty!")
            return

        nx_graph = nx.Graph(G.adjacency_list)
        pos = nx.spring_layout(nx_graph)
        node_colors = [self.colors.get(node, 'skyblue') for node in nx_graph.nodes()]

        fig, ax = plt.subplots(figsize=(16, 12))
        nx.draw(nx_graph, pos, with_labels=True, node_size=400, node_color=node_colors, font_size=10, font_weight="bold",
                edge_color="gray", ax=ax)
        ax.set_title("Graph Visualization")

        # Update the placeholder
        plot_placeholder.pyplot(fig)

    def reset_colors(self):
        """Reset all node colors to the default."""
        self.colors.clear()

    def update_node_color(self, colors: dict[int, str]):
        self.colors = colors


def three_color_graph(graph: dict) -> dict[int, str] | str:
    def is_available(vertex, color, graph, colors):
        return all(colors[neighbor] != color for neighbor in graph[vertex])

    def color_graph(colors, vertex, available_colors, degree_order):
        if vertex == len(degree_order):
            return True
        current_vertex = degree_order[vertex]
        for color in available_colors:
            if is_available(current_vertex, color, graph, colors):
                colors[current_vertex] = color
                if color_graph(colors, vertex + 1, available_colors, degree_order):
                    return True
                colors[current_vertex] = None
        return False

    vertices = list(graph.keys())
    colors = {v: None for v in vertices}
    available_colors = ["r", "g", "b"]
    degree_order = sorted(vertices, key=lambda v: len(graph[v]), reverse=True)

    if color_graph(colors, 0, available_colors, degree_order):
        return colors
    return "Impossible to color the graph in 3 colors."


def main():
    st.title("Graph Visualization and Interaction")

    # Initialize graph and visualizer in session state
    if 'graph' not in st.session_state:
        st.session_state.graph = Graph()

    if 'visualizer' not in st.session_state:
        st.session_state.visualizer = GraphVisualizer()

    # Placeholder for the graph plot
    if 'plot_placeholder' not in st.session_state:
        st.session_state.plot_placeholder = st.empty()

    G = st.session_state.graph
    visualizer = st.session_state.visualizer
    plot_placeholder = st.session_state.plot_placeholder

    def refresh_graph():
        """Helper to redraw the graph using the single placeholder."""
        visualizer.draw_graph(G, plot_placeholder)

    # File upload handling
    uploaded_file = st.file_uploader("Upload a Graph File (CSV format with node1,node2 per line)", type=["csv"])

    if uploaded_file is not None:
        # Load graph from file and update the session state
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        G.from_file(stringio)
        st.success("Graph loaded from file!")
        visualizer.reset_colors()  # Reset colors to default
        refresh_graph()  # Refresh visualization

    # Clear graph button
    if st.button("Clear Graph"):
        G.clear()
        visualizer.reset_colors()
        st.success("Graph cleared.")
        refresh_graph()

    # Dropdown for graph operations
    option = st.selectbox("Choose an operation", ("Add Node", "Remove Node", "Add Edge", "Remove Edge", "Color Graph"))

    if option == "Add Node":
        node = st.number_input("Enter Node", min_value=1, step=1)
        if st.button("Add Node"):
            G.add_node(node)
            visualizer.reset_colors()  # Reset colors to default
            refresh_graph()  # Update visualization

    elif option == "Remove Node":
        node = st.number_input("Enter Node to Remove", min_value=1, step=1)
        if st.button("Remove Node"):
            G.remove_node(node)
            visualizer.reset_colors()  # Reset colors to default
            refresh_graph()  # Update visualization

    elif option == "Add Edge":
        node1 = st.number_input("Enter First Node", min_value=1, step=1)
        node2 = st.number_input("Enter Second Node", min_value=1, step=1)
        if st.button("Add Edge"):
            G.add_edge((node1, node2))
            visualizer.reset_colors()  # Reset colors to default
            refresh_graph()  # Update visualization

    elif option == "Remove Edge":
        node1 = st.number_input("Enter First Node", min_value=1, step=1)
        node2 = st.number_input("Enter Second Node", min_value=1, step=1)
        if st.button("Remove Edge"):
            G.remove_edge((node1, node2))
            visualizer.reset_colors()  # Reset colors to default
            refresh_graph()  # Update visualization

    elif option == "Color Graph":
        result = three_color_graph(G.to_dict())
        if isinstance(result, dict):
            visualizer.update_node_color({node: color for node, color in result.items()})
            refresh_graph()  # Update visualization
        else:
            st.error(result)


if __name__ == "__main__":
    main()
