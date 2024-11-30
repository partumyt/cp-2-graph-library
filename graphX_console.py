import argparse
from graphX import Graph, CycleGraph
import sys


def print_graph(graph):
    """Displays the adjacency list of the graph."""
    print("Adjacency List:")
    for node, neighbors in graph.to_dict().items():
        print(f"{node}: {', '.join(map(str, neighbors))}")


def load_graph(graph, file_path):
    """Loads a graph from a CSV file."""
    try:
        with open(file_path, 'r') as file:
            graph.read_from_csv(file)
        print("Graph loaded successfully!")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Console-based Graph Operations")
    parser.add_argument("--directed", action="store_true", help="Set the graph to directed mode.")

    # Operations
    subparsers = parser.add_subparsers(dest="command", help="Graph operations")

    # Add node
    parser_add_node = subparsers.add_parser("add-node", help="Add a node to the graph")
    parser_add_node.add_argument("node", type=int, help="Node to add")

    # Remove node
    parser_remove_node = subparsers.add_parser("remove-node", help="Remove a node from the graph")
    parser_remove_node.add_argument("node", type=int, help="Node to remove")

    # Add edge
    parser_add_edge = subparsers.add_parser("add-edge", help="Add an edge to the graph")
    parser_add_edge.add_argument("node1", type=int, help="Start node of the edge")
    parser_add_edge.add_argument("node2", type=int, help="End node of the edge")

    # Remove edge
    parser_remove_edge = subparsers.add_parser("remove-edge", help="Remove an edge from the graph")
    parser_remove_edge.add_argument("node1", type=int, help="Start node of the edge")
    parser_remove_edge.add_argument("node2", type=int, help="End node of the edge")

    # Load graph
    parser_load = subparsers.add_parser("load", help="Load a graph from a CSV file")
    parser_load.add_argument("file", type=str, help="Path to the CSV file")

    # Display graph
    subparsers.add_parser("display", help="Display the adjacency list of the graph")

    # Check bipartite
    subparsers.add_parser("check-bipartite", help="Check if the graph is bipartite")

    # Hamiltonian cycle
    subparsers.add_parser("hamiltonian", help="Find a Hamiltonian cycle")

    # Eulerian cycle
    subparsers.add_parser("eulerian", help="Find an Eulerian cycle")

    # Three-color graph
    subparsers.add_parser("three-color", help="Attempt to three-color the graph")

    # Parse arguments
    args = parser.parse_args()

    # Initialize graph
    graph = CycleGraph(directed=args.directed)

    # Command handlers
    if args.command == "add-node":
        graph.add_node(args.node)
        print(f"Node {args.node} added.")
    elif args.command == "remove-node":
        graph.remove_node(args.node)
        print(f"Node {args.node} removed.")
    elif args.command == "add-edge":
        graph.add_edge((args.node1, args.node2))
        print(f"Edge ({args.node1}, {args.node2}) added.")
    elif args.command == "remove-edge":
        graph.remove_edge((args.node1, args.node2))
        print(f"Edge ({args.node1}, {args.node2}) removed.")
    elif args.command == "load":
        load_graph(graph, args.file)
    elif args.command == "display":
        print_graph(graph)
    elif args.command == "check-bipartite":
        print("Bipartite!" if graph.is_bipartite() else "Not Bipartite.")
    elif args.command == "hamiltonian":
        cycle = graph.hamiltonian_cycle()
        print(f"Hamiltonian Cycle: {cycle}" if cycle else "No Hamiltonian Cycle found.")
    elif args.command == "eulerian":
        cycle = graph.eulerian_cycle()
        print(f"Eulerian Cycle: {cycle}" if isinstance(cycle, list) else cycle)
    elif args.command == "three-color":
        result = graph.three_color_graph()
        if isinstance(result, str):
            print(result)
        else:
            print("Three-coloring result:")
            for node, color in result:
                print(f"Node {node}: {color}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
