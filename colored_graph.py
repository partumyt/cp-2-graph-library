def is_available(vertex, color, graph, colors, directed=False):
    """
    Check if a color can be assigned to the vertex without conflicts.

    :param vertex: The current vertex to color.
    :param color: The color to assign.
    :param graph: The adjacency list of the graph.
    :param colors: The dictionary of assigned colors.
    :param directed: Flag indicating if the graph is directed.
    :return: True if the color can be assigned, False otherwise.
    """
    if directed:
        return all(colors[neighbor] != color for neighbor in graph[vertex]) and \
               all(colors[neighbor] != color for neighbor in graph if vertex in graph[neighbor])
    else:
        return all(colors[neighbor] != color for neighbor in graph[vertex])

def color_graph(graph, colors, vertex_index, available_colors, degree_order, directed=False):
    """
    Recursively try to color the graph using backtracking.

    :param graph: The adjacency list of the graph.
    :param colors: The dictionary of assigned colors.
    :param vertex_index: The current index of the vertex to color.
    :param available_colors: The list of available colors.
    :param degree_order: The list of vertices sorted by degree.
    :param directed: Flag indicating if the graph is directed.
    :return: True if the graph can be colored, False otherwise.
    """
    if vertex_index == len(degree_order):
        return True

    current_vertex = degree_order[vertex_index]
    for color in available_colors:
        if is_available(current_vertex, color, graph, colors, directed):
            colors[current_vertex] = color
            if color_graph(graph, colors, vertex_index + 1, available_colors, degree_order, directed):
                return True
            colors[current_vertex] = None
    return False

def three_color_graph(graph: dict, directed=False) -> list[tuple]:
    """
    Attempt to color the graph using 3 colors.

    :param graph: The adjacency list of the graph.
    :param directed: Flag indicating if the graph is directed.
    :return: A list of tuples representing vertex-color pairs if the graph can be colored, otherwise a message.
    """
    vertices = list(graph.keys())
    colors = {v: None for v in vertices}
    available_colors = ["r", "g", "b"]
    degrees = {v: len(neighbors) for v, neighbors in graph.items()}
    degree_order = sorted(vertices, key=lambda v: degrees[v], reverse=True)

    return [(vertex, colors[vertex]) for vertex in vertices] \
        if color_graph(graph, colors, 0, available_colors, degree_order, directed) \
        else "Impossible to color the graph in 3 colors"
