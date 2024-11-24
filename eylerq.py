"""
Conditions for the existence of an Eulerian cycle:
    1. The graph must be connected.
    2. Every vertex must have an even degree.
"""
def find_eulerian_cycle_general(graph: Dict[int, List[int]]) -> Union[List[int]:
    """
    Finding the Euler cycle for a nonhomogeneous graph.

    :param graph: dictionary of adjacency lists.
    :return: a list of vertices in the order of the Euler cycle or a message about its absence.

    >>> general_graph = {
    ...     0: [1, 2],
    ...     1: [0, 2],
    ...     2: [0, 1]
    ... }
    >>> print(find_eulerian_cycle_general(general_graph))
    [0, 2, 1, 0]
    """
    def find_cycle(start, local_graph):
        stack = [start]
        cycle = []
        while stack:
            u = stack[-1]
            if local_graph[u]:
                v = local_graph[u].pop()
                local_graph[v].remove(u)
                stack.append(v)
            else:
                cycle.append(stack.pop())
        return cycle[::-1]

    if any(len(neighbors) % 2 != 0 for neighbors in graph.values()):
        return "The graph does not have an Euler cycle"

    local_graph = {node: neighbors[:] for node, neighbors in graph.items()}

    start_node = next(iter(local_graph))
    cycle = find_cycle(start_node, local_graph)

    if any(neighbors for neighbors in local_graph.values()):
        return "The graph does not have an Euler cycle"

    return cycle


def find_eulerian_cycle_uniform(graph: Dict[int, List[int]]) -> Union[List[int]:
    """
    Finding the Euler cycle for a homogeneous graph.

    :param graph: dictionary of adjacency lists.
    :return: a list of vertices in the order of the Euler cycle or a message about its absence.
    
    >>> uniform_graph = {
    ...     0: [1, 2, 3, 1],
    ...     1: [0, 2, 3, 0],
    ...     2: [0, 1, 3, 3],
    ...     3: [0, 1, 2, 2]
    ... }
    >>> print(find_eulerian_cycle_uniform(uniform_graph))
    [0, 1, 0, 3, 2, 3, 1, 2, 0]
    """
    def find_cycle(start, local_graph):
        stack = [start]
        cycle = []
        while stack:
            u = stack[-1]
            if local_graph[u]:
                v = local_graph[u].pop()
                local_graph[v].remove(u)
                stack.append(v)
            else:
                cycle.append(stack.pop())
        return cycle[::-1]

    # Check if all degrees are even
    if any(len(neighbors) % 2 != 0 for neighbors in graph.values()):
        return "The graph does not have an Euler cycle"

    # Check if the graph is connected
    visited = set()

    def dfs(node):
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                dfs(neighbor)

    start_node = next(iter(graph))
    dfs(start_node)

    if len(visited) != len(graph):
        return "The graph is not connected"

    # Create a local copy of the graph
    local_graph = {node: neighbors[:] for node, neighbors in graph.items()}

    # Find Eulerian cycle
    cycle = find_cycle(start_node, local_graph)

    # Ensure no edges are left
    if any(neighbors for neighbors in local_graph.values()):
        return "The graph does not have an Euler cycle"

    return cycle


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
