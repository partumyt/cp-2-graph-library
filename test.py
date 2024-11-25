from graphX import Graph


def test_read_and_color_graph():
    csv_file_path = "graph.csv"
    graph = Graph(directed=False)
    graph.read_from_csv(csv_file_path)
    result = graph.three_color_graph()
    print("\nThree Color Graph Result:")
    if result != "Impossible to color the graph in 3 colors":
        for vertex, color in result:
            print(f"Vertex {vertex} is colored {color}")
    else:
        print(result)


test_read_and_color_graph()
