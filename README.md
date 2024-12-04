Презентація: https://www.canva.com/design/DAGYKXzqW0M/gf0c08k9utf9XYcSERd3ug/edit?utm_content=DAGYKXzqW0M&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
Звіт: https://docs.google.com/document/d/1OkH4zIPGHtI83R3um3aL0CPHuaLvNpOyfInOJ0O1V8k/edit?usp=sharing
# GraphX Library

GraphX — це Python-бібліотека для роботи з графами, яка включає можливості обробки, аналізу, візуалізації та роботи з різними типами графів.

## Особливості

- **Маніпуляції з графами**: Додавання/видалення вузлів та ребер, читання графів із CSV.
- **Аналіз графів**: Перевірка біпартитності, пошук Гамільтонових і Ейлерових циклів.
- **Алгоритми кольорування**: Трьохколірне кольорування графів.
- **Перевірка ізоморфності**: Використання тесту Вайсфайлер-Лемана.
- **Візуалізація**: Інтерактивне відображення графів через Streamlit із використанням NetworkX.

## Встановлення

### Залежності
- Python 3.12
- Модулі: `argparse`, `json`, `networkx`, `matplotlib`, `streamlit`

### Інструкції
1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com/partumyt/cp-2-graph-library
   cd cp-2-graph-library
   ```
2. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```

## Використання

### 1. Консольний інтерфейс
Файл `graphX_console.py` дозволяє взаємодіяти з графами через командний рядок.

#### Основні команди
- `create`: Створення нового графа.
- `add-node <node_id>`: Додавання вузла.
- `remove-node <node_id>`: Видалення вузла.
- `add-edge <node1> <node2>`: Додавання ребра.
- `remove-edge <node1> <node2>`: Видалення ребра.
- `display`: Відображення списку суміжності.
- `three-color`: Трьохколірне кольорування.
- `check-bipartite`: Перевірка біпартитності графа.
- `hamiltonian`: Пошук Гамільтонового циклу.
- `eulerian`: Пошук Ейлерового циклу.
- `isomorphic <path_to_csv>`: Перевірка ізоморфності з іншим графом.

#### Приклад
```bash
python graphX_console.py create
python graphX_console.py add-node 1
python graphX_console.py add-edge 1 2
python graphX_console.py display
```

### 2. Візуалізація
Файл `graphX_visual.py` надає графічний інтерфейс через Streamlit.

#### Запуск
```bash
streamlit run graphX_visual.py
```

#### Можливості
- Створення графів.
- Завантаження графів із CSV.
- Інтерактивне додавання/видалення вузлів і ребер.
- Вибір макета (spring, circular, shell).
- Операції: перевірка біпартитності, кольорування, пошук циклів, перевірка ізоморфності.

### 3. Бібліотека
Файл `graphX.py` містить основні класи `Graph` та `CycleGraph`.

#### Основні методи
- `add_node(node)`: Додає вузол.
- `add_edge(edge)`: Додає ребро.
- `remove_node(node)`: Видаляє вузол.
- `remove_edge(edge)`: Видаляє ребро.
- `is_bipartite()`: Перевіряє, чи є граф біпартитним.
- `hamiltonian_cycle()`: Пошук Гамільтонового циклу.
- `eulerian_cycle()`: Пошук Ейлерового циклу.
- `three_color_graph()`: Трьохколірне кольорування.

#### Приклад
```python
from graphX import CycleGraph

graph = CycleGraph(directed=False)
graph.add_node(1)
graph.add_edge((1, 2))
print(graph.to_dict())  # {1: [2], 2: [1]}
```

[Посилання на звіт](https://github.com/partumyt/cp-2-graph-library/blob/main/zvit.pdf)

## Автори
Створено командою #2. Усі права захищені.

## Ліцензія
MIT License.
```

Цей `README.md` описує всі аспекти вашої бібліотеки, її компоненти та можливості. Ви можете доповнити або змінити його за необхідності.
