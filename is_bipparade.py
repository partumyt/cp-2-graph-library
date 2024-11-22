def is_dicotyledonous(graph: dict) -> bool:
    """
    Перевіряє критерій дводольності графа.
    Починаємо з будь-якої вершини, фарбуємо її кольором 0.
    Її сусідів фарбуємо кольором 1, сусідів сусідів — знову 0, і так далі.
    Якщо на якомусь кроці знайдемо вершину, яка вже пофарбована, 
    але має такий самий колір, як її сусід, граф не є дводольним.
    
    Функція підтримує як орієнтовані, так і неорієнтовані графи.
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
    """
    color = {}  # словник для зберігання кольору вершини (ключ - вершина, значення - колір 0 або 1)

    def check_if_dye(start):
        """
        Ця функція перевіряє чи можна забарвити компонент графа, 
        що містить початкову вершину, згідно з принципом дводольності.
        """
        queue = [start]  # додаємо початкову вершину в чергу
        color[start] = 0  # розфарбовуємо початкову вершину в 0 колір
        while queue:
            node = queue.pop(0)  # витягуємо вершину з черги
            for neighbor in graph[node]:
                # Для неорієнтованих графів додаємо зворотні ребра
                if isinstance(graph[neighbor], list):  # перевірка на неорієнтовані графи
                    for reverse_neighbor in graph[neighbor]:
                        if reverse_neighbor not in graph[node]:
                            graph[node].append(reverse_neighbor)
                
                if neighbor not in color:  # якщо сусід ще не пофарбований
                    color[neighbor] = 1 - color[node]  # фарбуємо в протилежний колір
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:  # якщо сусід має такий самий колір
                    return False  # граф не дводольний
        return True

    for node in graph:  # перевіряємо всі компоненти графа
        if node not in color:
            if not check_if_dye(node):
                return False

    return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()
