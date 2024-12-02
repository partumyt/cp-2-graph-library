import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from io import StringIO
from graphX import Graph, CycleGraph


class GraphVisualizer:
    def __init__(self):
        self.colors = {}
        self.default_edge_color = "black"  # Default edge color

    def draw_graph(self, G: Graph, plot_placeholder, layout="spring"):
        """Draws the graph using matplotlib and networkx."""
        if len(G.adjacency_list) == 0:
            plot_placeholder.warning("Graph is empty!")
            return

        # Convert to networkx graph
        nx_graph = nx.Graph(G.adjacency_list)

        # Choose layout
        if layout == "spring":
            pos = nx.spring_layout(nx_graph, seed=42, k=0.3)
        elif layout == "circular":
            pos = nx.circular_layout(nx_graph)
        elif layout == "shell":
            pos = nx.shell_layout(nx_graph)
        else:
            pos = nx.spring_layout(nx_graph)

        # Assign colors
        node_colors = [self.colors.get(node, 'skyblue') for node in nx_graph.nodes()]
        edge_colors = [self.default_edge_color] * len(nx_graph.edges())

        # Plot graph
        fig, ax = plt.subplots(figsize=(14, 10))
        nx.draw(nx_graph, pos,
                with_labels=True,
                node_size=800,
                node_color=node_colors,
                edge_color=edge_colors,
                font_size=10,
                font_weight="bold",
                width=2,
                ax=ax)

        ax.set_title("Graph Visualization", fontsize=16)
        plot_placeholder.pyplot(fig)

    def reset_colors(self):
        """Resets node colors to default."""
        self.colors.clear()

    def reset_edge_color(self):
        """Resets edge colors to default."""
        self.default_edge_color = "black"

    def update_node_color(self, colors: dict[int, str]):
        """Updates node colors."""
        self.colors = colors

    def update_edge_color(self, color: str):
        """Updates edge color to a uniform color."""
        self.default_edge_color = color


def main():
    st.title("Enhanced Graph Visualization")

    # Initialize the graph and visualizer
    if 'graph' not in st.session_state:
        st.session_state.graph = CycleGraph()
    if 'visualizer' not in st.session_state:
        st.session_state.visualizer = GraphVisualizer()
    if 'plot_placeholder' not in st.session_state:
        st.session_state.plot_placeholder = st.empty()

    G = st.session_state.graph
    visualizer = st.session_state.visualizer
    plot_placeholder = st.session_state.plot_placeholder

    def refresh_graph(layout="spring"):
        """Refreshes the graph visualization."""
        visualizer.draw_graph(G, plot_placeholder, layout)

    # Layout selection
    st.sidebar.header("Graph Layout")
    layout = st.sidebar.radio("Select Layout", ["spring", "circular", "shell"])

    # File upload handling
    uploaded_file = st.file_uploader("Upload Graph (CSV)", type=["csv"])
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        G.read_from_csv(stringio)
        st.success("Graph loaded!")
        visualizer.reset_colors()
        refresh_graph(layout)

    # Graph Operations
    st.sidebar.header("Operations")
    with st.sidebar:
        if st.button("Add Node"):
            node = st.number_input("Node ID", min_value=0, step=1, key="add_node")
            G.add_node(node)
            refresh_graph(layout)

        if st.button("Remove Node"):
            node = st.number_input("Node ID", min_value=0, step=1, key="remove_node")
            G.remove_node(node)
            refresh_graph(layout)

        if st.button("Add Edge"):
            node1 = st.number_input("Start Node", min_value=0, step=1, key="add_edge_node1")
            node2 = st.number_input("End Node", min_value=0, step=1, key="add_edge_node2")
            G.add_edge((node1, node2))
            refresh_graph(layout)

        if st.button("Remove Edge"):
            node1 = st.number_input("Start Node", min_value=0, step=1, key="remove_edge_node1")
            node2 = st.number_input("End Node", min_value=0, step=1, key="remove_edge_node2")
            G.remove_edge((node1, node2))
            refresh_graph(layout)

    # Advanced Operations
    st.sidebar.header("Advanced Operations")
    if st.sidebar.button("Check Bipartite"):
        result = G.is_bipartite()
        st.sidebar.success("Bipartite!" if result else "Not Bipartite.")

    if st.sidebar.button("Hamiltonian Cycle"):
        result = G.hamiltonian_cycle()
        st.sidebar.success(f"Hamiltonian Cycle: {result}" if result else "No Hamiltonian Cycle.")

    if st.sidebar.button("Eulerian Cycle"):
        result = G.eulerian_cycle()
        st.sidebar.success(f"Eulerian Cycle: {result}" if isinstance(result, list) else result)

    if st.sidebar.button("Three-Color Graph"):
        result = G.three_color_graph()
        if isinstance(result, str):
            st.sidebar.error(result)
        else:
            colors = {node: color for node, color in result}
            visualizer.update_node_color(colors)
            refresh_graph(layout)

    # Isomorphic check
    st.sidebar.subheader("Isomorphic Check")
    uploaded_iso_file = st.sidebar.file_uploader("Upload Graph for Isomorphism Check (CSV)", type=["csv"])
    if uploaded_iso_file:
        stringio_iso = StringIO(uploaded_iso_file.getvalue().decode("utf-8"))
        other_graph = CycleGraph()
        other_graph.read_from_csv(stringio_iso)
        if st.sidebar.button("Check Isomorphism"):
            result = G.isomorphic(other_graph)
            st.sidebar.success("Graphs have same canonical form, but there is a slight chance they aren't isomorphic!" if result else "Graphs are NOT Isomorphic.")

    # Reset Colors Button
    st.sidebar.header("Reset Operations")
    if st.sidebar.button("Reset Node Colors"):
        visualizer.reset_colors()
        refresh_graph(layout)

    if st.sidebar.button("Reset Edge Color to Black"):
        visualizer.reset_edge_color()
        refresh_graph(layout)

    # Draw graph
    refresh_graph(layout)


if __name__ == "__main__":
    main()
