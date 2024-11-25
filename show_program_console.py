import graphX as gX
import time as t


def main():
    directed = input("Is this graph directed? (yes/no): ").strip().lower() == "yes"
    graph = gX.Graph(directed=directed)

    while True:
        print("\nChoose action:")
        print("""
        1 - Add node
        2 - Delete node
        3 - Add edge
        4 - Delete edge
        5 - Load from CSV
        6 - Hamiltonian cycle
        7 - Eulerian cycle
        8 - Is bipartite
        9 - Is isomorphic
        10 - Color graph in 3 colors
        11 - Display adjacency list
        0 - Exit
        """)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            try:
                node = int(input("Enter node to add: "))
                graph.add_node(node)
                print(f"Node {node} added.")
            except ValueError:
                print("Invalid input. Node must be an integer.")

        elif choice == "2":
            try:
                node = int(input("Enter node to delete: "))
                graph.remove_node(node)
                print(f"Node {node} deleted.")
            except ValueError:
                print("Invalid input. Node must be an integer.")

        elif choice == "3":
            try:
                node1 = int(input("Enter the first node of the edge: "))
                node2 = int(input("Enter the second node of the edge: "))
                graph.add_edge((node1, node2))
                print(f"Edge ({node1}, {node2}) added.")
            except ValueError:
                print("Invalid input. Nodes must be integers.")

        elif choice == "4":
            try:
                node1 = int(input("Enter the first node of the edge to delete: "))
                node2 = int(input("Enter the second node of the edge to delete: "))
                graph.remove_edge((node1, node2))
                print(f"Edge ({node1}, {node2}) deleted.")
            except ValueError:
                print("Invalid input. Nodes must be integers.")

        elif choice == "5":
            file_path = input("Enter the CSV file path: ").strip()
            try:
                adjacency_list = graph.read_from_csv(file_path)
                print(f"Graph loaded from {file_path}.")
                t.sleep(1)
                print("Adjacency List:")
                for node, neighbors in adjacency_list.items():
                    print(f"{node}: {neighbors}")
            except FileNotFoundError:
                print("File not found. Please check the file path.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == "6":
            result = graph.hamiltonian_cycle()
            if result:
                print("Hamiltonian Cycle:", result)
            else:
                print("No Hamiltonian Cycle exists.")

        elif choice == "7":
            result = graph.eulerian_cycle()
            if isinstance(result, str):
                print(result)
            else:
                print("Eulerian Cycle:", result)

        elif choice == "8":
            if graph.is_bipartite():
                print("The graph is bipartite.")
            else:
                print("The graph is not bipartite.")

        elif choice == "9":
            file_path = input("Enter the CSV file path of the second graph: ").strip()
            try:
                second_graph = gX.Graph(directed=graph.directed)
                second_graph.read_from_csv(file_path)
                if graph.isomorphic(second_graph):
                    print("The graphs are isomorphic.")
                else:
                    print("The graphs are not isomorphic.")
            except FileNotFoundError:
                print("File not found. Please check the file path.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == "10":
            result = graph.three_color_graph()
            if isinstance(result, str):
                print(result)
            else:
                print("3-Coloring of the graph:")
                for node, color in result:
                    print(f"Node {node}: {color}")

        elif choice == "11":
            graph.display()

        elif choice == "0":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")
        t.sleep(2)


if __name__ == "__main__":
    main()
