"""
An algorithm to find a Hamiltonian cycle if it exists.
"""
def hamiltonian_cycle(graph: dict) -> list | None:
    """
    Finds a Hamiltonian cycle in a graph if it exists.
    :param graph: A dictionary where keys are vertices and values are lists of neighbors.
    :return: A list representing the Hamiltonian cycle, or None if no cycle exists.
    >>> graph1 = {
    ...     0: [1, 2, 3],
    ...     1: [0, 2, 4],
    ...     2: [0, 1, 3],
    ...     3: [0, 2, 4],
    ...     4: [1, 3]
    ... }
    >>> hamiltonian_cycle(graph1)
    [0, 1, 4, 3, 2]
    """
    n = len(graph)
    path = []

    def is_valid(vertex: int, position: int) -> bool:
        """
        Checks if we can add a vertex to the path.
        :param vertex: The vertex to check.
        :param position: The current position in the path.
        :return: True if the vertex can be added, False in other way.
        """
        if vertex not in graph[path[position - 1]]:
            return False
        if vertex in path:
            return False
        return True

    def hamiltonian_util(position: int) -> bool:
        """
        Tries to find a Hamiltonian cycle using recursion and backtracking.
        :param position: The current position in the path.
        :return: True if a Hamiltonian cycle is found, False otherwise.
        """
        if position == n:
            return path[0] in graph[path[-1]]
        for vertex in graph.keys():
            if is_valid(vertex, position):
                path.append(vertex)
                if hamiltonian_util(position + 1):
                    return True
                path.pop()
        return False
    start_vertex = next(iter(graph))
    path.append(start_vertex)
    if hamiltonian_util(1):
        return path
    return None
    
