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
    st.title("Graph Visualization and Operations")

    # Initialize the graph and visualizer
    if 'graph' not in st.session_state:
        st.session_state.graph = None
    if 'visualizer' not in st.session_state:
        st.session_state.visualizer = GraphVisualizer()
    if 'plot_placeholder' not in st.session_state:
        st.session_state.plot_placeholder = st.empty()

    visualizer = st.session_state.visualizer
    plot_placeholder = st.session_state.plot_placeholder

    def refresh_graph(layout="spring"):
        """Refreshes the graph visualization."""
        if st.session_state.graph is not None:
            visualizer.draw_graph(st.session_state.graph, plot_placeholder, layout)

    # Initial Choice: Upload or Create
    if st.session_state.graph is None:
        st.header("Choose an Action")
        choice = st.radio("Select how to start:", ["Upload Graph from File", "Create New Graph"])

        if choice == "Upload Graph from File":
            uploaded_file = st.file_uploader("Upload Graph (CSV)", type=["csv"])
            if uploaded_file is not None:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                graph = CycleGraph()
                graph.read_from_csv(stringio)
                st.session_state.graph = graph
                st.success("Graph loaded successfully!")
        elif choice == "Create New Graph":
            is_directed = st.radio("Is the graph directed?", ["Yes", "No"]) == "Yes"
            if st.button("Create Graph"):
                st.session_state.graph = CycleGraph(directed=is_directed)
                st.success("Graph created successfully!")

    if st.session_state.graph is not None:
        G = st.session_state.graph

        # Sidebar for Layout
        st.sidebar.header("Graph Layout")
        layout = st.sidebar.radio("Select Layout", ["spring", "circular", "shell"])

        # Graph Operations
        st.sidebar.header("Graph Operations")

        # Add Node
        with st.sidebar:
            add_node_id = st.number_input("Node ID to Add", min_value=0, step=1, key="add_node_id")
            if st.button("Add Node"):
                G.add_node(add_node_id)
                st.success(f"Node {add_node_id} added.")
                refresh_graph(layout)

        # Remove Node
        with st.sidebar:
            remove_node_id = st.number_input("Node ID to Remove", min_value=0, step=1, key="remove_node_id")
            if st.button("Remove Node"):
                G.remove_node(remove_node_id)
                st.success(f"Node {remove_node_id} removed.")
                refresh_graph(layout)

        # Add Edge
        with st.sidebar:
            edge_start = st.number_input("Start Node for Edge", min_value=0, step=1, key="edge_start")
            edge_end = st.number_input("End Node for Edge", min_value=0, step=1, key="edge_end")
            if st.button("Add Edge"):
                G.add_edge((edge_start, edge_end))
                st.success(f"Edge ({edge_start}, {edge_end}) added.")
                refresh_graph(layout)

        # Remove Edge
        with st.sidebar:
            remove_edge_start = st.number_input("Start Node to Remove Edge", min_value=0, step=1, key="remove_edge_start")
            remove_edge_end = st.number_input("End Node to Remove Edge", min_value=0, step=1, key="remove_edge_end")
            if st.button("Remove Edge"):
                G.remove_edge((remove_edge_start, remove_edge_end))
                st.success(f"Edge ({remove_edge_start}, {remove_edge_end}) removed.")
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

        # Isomorphic Check
        st.sidebar.subheader("Isomorphic Check")
        uploaded_iso_file = st.sidebar.file_uploader("Upload Graph for Isomorphism Check (CSV)", type=["csv"])
        if uploaded_iso_file:
            stringio_iso = StringIO(uploaded_iso_file.getvalue().decode("utf-8"))
            other_graph = CycleGraph()
            other_graph.read_from_csv(stringio_iso)
            if st.sidebar.button("Check Isomorphism"):
                result = G.isomorphic(other_graph)
                st.sidebar.success("Graphs have same canonical form, but there is a slight chance they aren't isomorphic!" \
                    if result else "Graphs are NOT Isomorphic.")

        # Reset Colors Button
        st.sidebar.header("Reset Operations")
        if st.sidebar.button("Reset Node Colors"):
            visualizer.reset_colors()
            refresh_graph(layout)

        if st.sidebar.button("Reset Edge Color to Black"):
            visualizer.reset_edge_color()
            refresh_graph(layout)

        # Draw Graph
        refresh_graph(layout)


if __name__ == "__main__":
    main()
