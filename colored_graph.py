def is_available(vertex, color, graph, colors):
    """
    Check if a color can be assigned to the vertex without conflicts.
    """
    return all(colors[neighbor] != color for neighbor in graph[vertex])


def color_graph(graph, colors, vertex, available_colors, degree_order):
    """
    Recursively try to color the graph using backtracking.
    """
    if vertex == len(graph):
        return True
    current_vertex = degree_order[vertex]
    for color in available_colors:
        if is_available(current_vertex, color, graph, colors):
            colors[current_vertex] = color
            if color_graph(graph, colors, vertex + 1, available_colors, degree_order):
                return True
            colors[current_vertex] = None
    return False


def three_color_graph(graph: dict) -> list[tuple]:
    """
    Attempt to color the graph using 3 colors.
    """
    # Ensure that the graph vertices are sorted correctly
    vertices = list(graph.keys())
    num_vertices = len(vertices)
    colors = {v: None for v in vertices}  # Use a dictionary to store colors by vertex label
    available_colors = ["r", "g", "b"]

    # Sort vertices by degree (highest degree first)
    degrees = {v: len(neighbors) for v, neighbors in graph.items()}
    degree_order = sorted(vertices, key=lambda v: degrees[v], reverse=True)

    # Try coloring the graph
    if color_graph(graph, colors, 0, available_colors, degree_order):
        return [(vertex, colors[vertex]) for vertex in vertices]
    else:
        return "Impossible to color the graph in 3 colors"


# Example graph
g = {
    1: [2, 3, 5],
    2: [1, 4, 6],
    3: [1, 7, 8],
    4: [2, 9, 10],
    5: [1, 11, 12],
    6: [2, 13, 14],
    7: [3, 15, 16],
    8: [3, 17, 18],
    9: [4, 19, 20],
    10: [4, 21, 22],
    11: [5, 23, 24],
    12: [5, 25, 26],
    13: [6, 27, 28],
    14: [6, 29, 30],
    15: [7, 1, 9],
    16: [7, 2, 10],
    17: [8, 3, 11],
    18: [8, 4, 12],
    19: [9, 5, 13],
    20: [9, 6, 14],
    21: [10, 7, 15],
    22: [10, 8, 16],
    23: [11, 9, 17],
    24: [11, 10, 18],
    25: [12, 11, 19],
    26: [12, 12, 20],
    27: [13, 17, 23],
    28: [13, 18, 24],
    29: [14, 19, 25],
    30: [14, 20, 26]
}



print(three_color_graph(g))
