"""
Conditions for the existence of an Eulerian cycle:
    1. The graph must be connected.
    2. Every vertex must have an even degree.
"""
from typing import Dict, List, Union

def find_eulerian_cycle(graph: Dict[int, List[int]]) -> Union[List[int], str]:
    """
    Finds an Eulerian cycle in the graph or returns a message if it doesn't exist.

    :param: A dictionary where the key is a vertex, 
                  and the value is a list of adjacent vertices (undirected graph).
    :return: A list of vertices in the order of the Eulerian cycle, 
             or a message indicating its absence.

    Example usage:
    >>> graph1 = {1: [2, 3], 2: [1, 3], 3: [1, 2]}
    >>> find_eulerian_cycle(graph1)
    [1, 2, 3, 1]

    >>> graph2 = {1: [2], 2: [1, 3], 3: [2]}
    >>> find_eulerian_cycle(graph2)
    'Eulerian cycle is not possible: not all vertices have an even degree.'

    >>> graph3 = {1: [2, 3, 4], 2: [1, 3], 3: [1, 2, 4], 4: [1, 3]}
    >>> find_eulerian_cycle(graph3)
    'Eulerian cycle is not possible: not all vertices have an even degree.'

    >>> graph4 = {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]}
    >>> find_eulerian_cycle(graph4)
    [1, 2, 3, 4, 1]
    """
    # filter out vertices with no edges
    filtered_graph = {v: neighbors for v, neighbors in graph.items() if neighbors}

    # check if all vertices with edges have an even degree
    for vertex, neighbors in filtered_graph.items():
        if len(neighbors) % 2 != 0:
            return "Eulerian cycle is not possible: not all vertices have an even degree."

    # check if the graph is connected
    def is_connected(graph: Dict[int, List[int]]) -> bool:
        """
        >>> graph1 = {1: [2], 2: [1, 3], 3: [2]}  # connected graph
        >>> is_connected(graph1)
        True

        >>> graph2 = {1: [2], 2: [1], 3: []}  # disconnected graph (vertex 3 isolated)
        >>> is_connected(graph2)
        False

        >>> graph3 = {}  # empty graph
        >>> is_connected(graph3)
        True

        >>> graph4 = {1: []}  # graph with a single vertex and no edges
        >>> is_connected(graph4)
        True
        """
        visited = set()

        def dfs(v):
            visited.add(v)
            for neighbor in graph[v]:
                if neighbor not in visited:
                    dfs(neighbor)

        # start DFS from any vertex in the filtered graph
        start = next(iter(graph))
        dfs(start)

        return len(visited) == len(graph)

    if not is_connected(filtered_graph):
        return "Eulerian cycle is not possible: the graph is not connected."

    # recursive function to find the Eulerian cycle
    def dfs_cycle(v: int) -> None:
        """
        >>> filtered_graph = {1: [2], 2: [1, 3], 3: [2, 1]}
        >>> cycle = []
        >>> start_vertex = 1
        >>> dfs_cycle(start_vertex)
        >>> cycle
        [1, 2, 3, 1]

        >>> filtered_graph = {1: [2], 2: [1], 3: []}
        >>> cycle = []
        >>> start_vertex = 1
        >>> dfs_cycle(start_vertex)
        >>> cycle
        [1, 2, 1]
        """
        while filtered_graph[v]:
            u = filtered_graph[v].pop()
            filtered_graph[u].remove(v)
            dfs_cycle(u)
        cycle.append(v)

    # create a copy of the graph for traversal
    cycle: List[int] = []
    start_vertex = next(iter(filtered_graph))  # start from any vertex with edges
    dfs_cycle(start_vertex)

    return cycle

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
