"""Main file with all functions"""


def read_file(filename: str) -> dict:
    """

    :param filename:
    :return:
    """
    ...


def hamiltonian_cycle(graph: dict) -> list | None:
    """

    :param graph:
    :return:
    """
    ...


def eulerian_cycle(graph: dict) -> list | None:
    """

    :param graph:
    :return:
    """
    ...


def is_bipartite(graph: dict) -> bool:
    """

    :param graph:
    :return:
    """
    ...


def are_isomorphic(graph1: dict, graph2: dict) -> bool:
    """

    :param graph1:
    :param graph2:
    :return:
    """
    ...


def colour_graph(connected_graph: dict) -> dict:
    """

    :param connected_graph:
    :return:
    """
    ...


def write_to_file(grapth: dict) -> None:
    """

    :param grapth:
    :return:
    """
    ...


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
