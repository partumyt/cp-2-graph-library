"""Weisfeiler Leman graph isomorphism test"""
from graphX import CycleGraph


def label(graph, directed = False):
    """
    Provides labels for each node of the graph necessary for checking isomorphism
    """
    label = {}
    for i in graph:
        label.update({i : '0'})
    for i in range(len(graph)):
        new_label = {}
        for node in graph:
            if directed:
                into = [node_ for node_ in graph if node in graph[node_]]
                out = graph[node]
                neighbor_label = tuple(label[node_] for node_ in into) + tuple(label[node_] for node_ in out)
            else:
                neighbor_label = tuple(label[node_] for node_ in graph[node])
            new_label[node] = f'{label[node]}|{'|'.join(neighbor_label)}'
        label = new_label
    return label


def isomorphic(graph1, graph2, directed = False):
    """
    >>> g1 = {1: [1, 2], 2: [2, 1, 3], 3: [2]}
    >>> g2 = {2: [2, 1, 3], 3: [2], 1: [1, 2]}
    >>> isomorphic(g1, g2)
    True
    >>> g1 = {0: {1, 2, 4}, 1: {0, 2}, 2: {0, 1, 3}, 3: {2, 4}, 4: {0, 3}}
    >>> g2 = {0: {1, 2, 4}, 1: {0, 3}, 2: {0, 3}, 3: {1, 2, 4}, 4: {0, 3}}
    >>> isomorphic(g1, g2)
    False
    >>> g1 = {0: {1, 2, 4}, 1: {0, 2}, 2: {0, 1, 3}, 3: {2, 4}, 4: {0, 3}}
    >>> g2 = {0: {3, 4}, 1: {2, 3, 4}, 2: {1, 3}, 3: {0, 1, 2}, 4: {0, 1}}
    >>> isomorphic(g1, g2)
    True
    >>> g1 = {0: {1, 2}, 1: {0, 3}, 2: {0, 3}, 3: {1, 2}}
    >>> g2 = {'a': {'b', 'c'}, 'b': {'a', 'd'}, 'c': {'a', 'd'}, 'd': {'b', 'c'}}
    >>> isomorphic(g1, g2)
    True
    >>> g1 = {0: [1], 1: [2], 2: [0]}
    >>> g2 = {0: [1, 2], 1: [], 2: []}
    >>> isomorphic(g1, g2)
    False
    >>> g1 = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    >>> g2 = {0: [1, 2], 1: [2], 2: [1]}
    >>> isomorphic(g1, g2)
    False
    >>> g1 = {0: [1], 1: [2], 2: [0]}
    >>> g2 = {'A': ['B'], 'B': ['C'], 'C': ['A']}
    >>> isomorphic(g1, g2, directed = True)
    True
    """
    label1 = label(graph1, directed)
    label2 = label(graph2, directed)
    if len(label1) != len(label2):
        return False
    return set(label1.values()) == set(label2.values())

if __name__ == '__main__':
    import doctest
    print(doctest.testmod(verbose = False))
