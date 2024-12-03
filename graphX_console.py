import argparse
import json
from graphX import CycleGraph

STATE_FILE = "graph_state.json"  # File to persist graph state


def save_graph_state(graph: CycleGraph) -> None:
    """Save the current graph state to a JSON file."""
    with open(STATE_FILE, "w") as file:
        json.dump({"directed": graph.directed, "adjacency_list": graph.to_dict()}, file)


def load_graph_state() -> CycleGraph:
    """Load the graph state from a JSON file."""
    try:
        with open(STATE_FILE, "r") as file:
            data = json.load(file)
            graph = CycleGraph(directed=data["directed"])
            for node, neighbors in data["adjacency_list"].items():
                for neighbor in neighbors:
                    graph.add_edge((int(node), neighbor))
            return graph
    except FileNotFoundError:
        return CycleGraph()
    except Exception as e:
        print(f"Error loading graph state: {e}")
        return CycleGraph()


def display_graph(graph: CycleGraph) -> None:
    """Display the adjacency list of the graph."""
    print("Adjacency List:")
    for node, neighbors in graph.to_dict().items():
        print(f"{node}: {', '.join(map(str, neighbors))}")


def create_graph() -> CycleGraph:
    """Interactively create a new graph."""
    directed = input("Is the graph directed? (yes/no): ").strip().lower() == "yes"
    graph = CycleGraph(directed=directed)

    print("Graph creation: Add nodes and edges.")
    while True:
        action = input("Choose an action - (1) Add node, (2) Add edge, (3) Display graph, (4) Finish: ").strip()
        if action == "1":
            try:
                node = int(input("Enter node ID: ").strip())
                graph.add_node(node)
                print(f"Node {node} added.")
            except ValueError:
                print("Invalid input. Please enter a valid node ID.")
        elif action == "2":
            try:
                node1 = int(input("Enter first node ID: ").strip())
                node2 = int(input("Enter second node ID: ").strip())
                graph.add_edge((node1, node2))
                print(f"Edge ({node1}, {node2}) added.")
            except ValueError:
                print("Invalid input. Please enter valid node IDs.")
        elif action == "3":
            display_graph(graph)
        elif action == "4":
            print("Graph creation finished.")
            break
        else:
            print("Invalid option. Please choose again.")
    return graph


def handle_command(graph: CycleGraph, command: list[str]) -> CycleGraph:
    """Process a single command and return the updated graph."""
    subcommand = command[0]
    try:
        if subcommand == "create":
            graph = create_graph()
            print("Graph created successfully!")
        elif subcommand == "load":
            file_path = command[1]
            with open(file_path, "r") as file:
                graph.read_from_csv(file)
            print("Graph loaded successfully!")
        elif subcommand == "add-node":
            node = int(command[1])
            graph.add_node(node)
            print(f"Node {node} added.")
        elif subcommand == "remove-node":
            node = int(command[1])
            graph.remove_node(node)
            print(f"Node {node} removed.")
        elif subcommand == "add-edge":
            node1, node2 = int(command[1]), int(command[2])
            graph.add_edge((node1, node2))
            print(f"Edge ({node1}, {node2}) added.")
        elif subcommand == "remove-edge":
            node1, node2 = int(command[1]), int(command[2])
            graph.remove_edge((node1, node2))
            print(f"Edge ({node1}, {node2}) removed.")
        elif subcommand == "three-color":
            result = graph.three_color_graph()
            if isinstance(result, str):
                print(result)
            else:
                print("Three-coloring result:")
                for node, color in result:
                    print(f"Node {node}: {color}")
        elif subcommand == "display":
            display_graph(graph)
        elif subcommand == "check-bipartite":
            result = graph.is_bipartite()
            print("Bipartite!" if result else "Not Bipartite.")
        elif subcommand == "hamiltonian":
            cycle = graph.hamiltonian_cycle()
            print(f"Hamiltonian Cycle: {cycle}" if cycle else "No Hamiltonian Cycle found.")
        elif subcommand == "eulerian":
            cycle = graph.eulerian_cycle()
            print(f"Eulerian Cycle: {cycle}" if isinstance(cycle, list) else cycle)
        elif subcommand == "isomorphic":
            file_path = command[1]
            other_graph = CycleGraph()
            with open(file_path, "r") as file:
                other_graph.read_from_csv(file)
            result = graph.isomorphic(other_graph)
            print("Graphs have same canonical form, but there is a slight chance they aren't isomorphic!" \
                if result else "Graphs are NOT Isomorphic.")
        else:
            print(f"Command '{subcommand}' not recognized.")
    except IndexError:
        print(f"Invalid arguments for command '{subcommand}'. Use --help for details.")
    except Exception as e:
        print(f"Error executing command '{subcommand}': {e}")

    save_graph_state(graph)
    return graph


def main() -> None:
    parser = argparse.ArgumentParser(description="Console-based Graph Operations")
    parser.add_argument("commands", nargs="+", help="Commands and arguments to execute sequentially.")
    args = parser.parse_args()

    # Load existing graph state or start fresh
    graph = load_graph_state()

    # Parse commands with arguments
    commands = args.commands
    grouped_commands = []
    current_command = []

    for token in commands:
        if token in {"create", "load", "add-node", "remove-node", "add-edge", "remove-edge", "three-color",
                     "display", "check-bipartite", "hamiltonian", "eulerian", "isomorphic"}:
            if current_command:
                grouped_commands.append(current_command)
            current_command = [token]
        else:
            current_command.append(token)

    if current_command:
        grouped_commands.append(current_command)

    # Process each grouped command
    for command in grouped_commands:
        graph = handle_command(graph, command)


if __name__ == "__main__":
    main()
