def add_edge(graph, edge):
    if edge[0] in graph.keys():
        if edge[1] not in graph[edge[0]]:
            graph[edge[0]].append(edge[1])
    else:
        graph.update({edge[0] : [edge[1]]})
    if edge[1] in graph.keys():
        if edge[0] not in graph[edge[1]]:
            graph[edge[1]].append(edge[0])
    else:
        graph.update({edge[1] : [edge[0]]})
    return graph

def list_to_dict(graph1:list[tuple[int, int]]) -> dict[int, list[int]]:
    '''
    Converts graph from list to dict
    '''
    result = {}
    for edge in graph1:
        result = add_edge(result, tuple(edge))
    for val in result.values():
        val.sort()
    result = dict(sorted(result.items()))
    return result


def labels(graph1, directed = False):
    graph = list_to_dict(graph1)
    labels = {}
    for i in graph:
        labels.update({i : '0'})
    for i in range(len(graph)):
        new_labels = {}
        for node in graph:
            if directed:
                into = [node_ for node_ in graph if node in graph[node_]]
                out = graph[node]
                neighbor_labels = tuple(labels[node_] for node_ in into) + tuple(labels[node_] for node_ in out)
            else:
                neighbor_labels = tuple(labels[node_] for node_ in graph[node])
            new_labels[node] = f'{labels[node]}|{'|'.join(neighbor_labels)}'
        labels = new_labels
    return labels


def isomorphic(graph1, graph2, directed = False):
    '''
    # >>> g1 = [(0,1), (0,2), (0,4), (1, 0), (1, 2), (2,0), (2,1), (2,3), (3, 2), (3, 4), (4, 0), (4, 3)]
    # >>> g2 = [(0,1), (0,2), (0,4), (1, 0), (1, 3), (2, 0), (2, 3), (3, 1), (3, 2), (3, 4), (4, 0), (4, 3)]
    #         >>> # Undirected graphs
    #     >>> graph1 = [(1, 2), (2, 3), (3, 1)]
    #     >>> graph2 = [(3, 2), (2, 1), (1, 3)]
    #     >>> isomorphic(graph1, graph2)
    #     True
        
    #     >>> graph1 = [(1, 2), (2, 3), (3, 1)]
    #     >>> graph2 = [(3, 2), (2, 4), (4, 3)]
    #     >>> isomorphic(graph1, graph2)
    #     True
        
    #     >>> # Directed graphs
    #     >>> graph1 = [(1, 2), (2, 3), (3, 1)]
    #     >>> graph2 = [(3, 1), (1, 2), (2, 3)]
    #     >>> isomorphic(graph1, graph2, directed=True)
    #     True
        
    #     >>> graph1 = [(1, 2), (2, 3), (3, 1)]
    #     >>> graph2 = [(2, 1), (3, 2), (1, 3)]
    #     >>> isomorphic(graph1, graph2, directed=True)
    #     True
        
    #     >>> # Non-isomorphic graphs with different numbers of edges
    #     >>> graph1 = [(1, 2), (2, 3)]
    #     >>> graph2 = [(1, 2), (2, 3), (3, 4)]
    #     >>> isomorphic(graph1, graph2)
    #     False
    #     >>> g3 = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
    #     >>> g4 = [('x', 'y'), ('x', 'z'), ('y', 'x'), ('y', 'z'), ('z', 'x'), ('z', 'y')]
    #     >>> isomorphic(g3, g4)
    #     True
        >>> graph_0002 = {1: [1, 2], 2: [2, 1, 3], 3: [2]}
        >>> graph_0003 = {2: [2, 1, 3], 3: [2], 1: [1, 2]}
        >>> g2 = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 2)]
        >>> g1 = [(2, 1), (2, 2), (2, 3), (3, 2), (1 ,1), (1, 2)]
        >>> isomorphic(g1, g2)

    '''
    labels1 = labels(graph1, directed)
    labels2 = labels(graph2, directed)
    if len(labels1) != len(labels2):
        return False


    # for _, label1 in labels1.items():
    #     for key2, label2 in labels2.items():
    #         if label1 == label2 and key2 not in used_labels2:
    #             used_labels2.add(key2)
    #             break
    #     else:
    #         return False
        
    # return True
    a = list(labels1.values())
    b = list(labels2.values())
    for i in a:
        if i in b:
            a.remove(i)
            b.remove(i)
        else:
            return False
    return True







g5_00 = {0: {1, 2, 4}, 1: {0, 2}, 2: {0, 1, 3}, 3: {2, 4}, 4: {0, 3}}
g5_02 = {0: {1, 2, 4}, 1: {0, 3}, 2: {0, 3}, 3: {1, 2, 4}, 4: {0, 3}}
g1 = [(0,1), (0,2), (0,4), (1, 0), (1, 2), (2,0), (2,1), (2,3), (3, 2), (3, 4), (4, 0), (4, 3)]
g2 = [(0,1), (0,2), (0,4), (1, 0), (1, 3), (2, 0), (2, 3), (3, 1), (3, 2), (3, 4), (4, 0), (4, 3)]

if __name__ == '__main__':
    import doctest
    print(doctest.testmod(verbose = False))
    print(isomorphic(g1, g2))