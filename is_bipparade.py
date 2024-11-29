def is_dicotyledonous(graph: dict, directed=False) -> bool:
    """
    Checks the bipartiteness criterion of a graph.
    We start with any vertex, color it with color 0.
    We color its neighbors with color 1, neighbors of neighbors — again 0, and so on.
    If at some step we find a vertex that is already colored,
    but has the same color as its neighbor, the graph is not bipartite.

    The function supports both directed and undirected graphs.
    
    :param graph (dict): Graph represented as an adjacency list.
    :param directed (bool): Whether to consider the graph as directed.

    Returns:
    - bool: True if the graph is bipartite, False otherwise.
    >>> is_dicotyledonous({
    ...     1: [2, 3],
    ...     2: [1, 4],
    ...     3: [1, 4],
    ...     4: [2, 3]})
    True
    >>> is_dicotyledonous({
    ...     1: [2, 3],
    ...     2: [1, 3],
    ...     3: [1, 2]})
    False
    >>> is_dicotyledonous({
    ...     1: [2],
    ...     2: [1],
    ...     3: [4],
    ...     4: [3]})
    True
    >>> is_dicotyledonous({
    ...     1: [2],
    ...     2: [3],
    ...     3: [1]})
    False
    >>> is_dicotyledonous({
    ...     1: [2],
    ...     2: [3],
    ...     3: []}, directed=True)
    True
    >>> is_dicotyledonous({
    ...     1: [2],
    ...     2: [1]}, directed=True)
    True
    """
    color = {}  # dictionary for storing vertex color (key is vertex, value is color 0 or 1)

    def check_if_dye(start):
        """
        This function checks whether a graph component can be colored, 
        containing the initial vertex, according to the bipartite principle.
        """
        queue = [start]  # add the initial vertex to the queue
        color[start] = 0  # color the initial vertex in 0 color
        while queue:
            node = queue.pop(0)  # remove the vertex from the queue
            for neighbor in graph[node]:
                if neighbor not in color:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False
                if directed and color[neighbor] != 1 - color[node]:
                    return False
        return True

    for node in graph:  # check all graph components
        if node not in color:
            if not check_if_dye(node):
                return False

    return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()
