import csv
import random

# File name for the output
output_file = "guaranteed_3_colorable_graph.csv"

# Parameters
num_nodes = 1000
edges_per_group_pair = 300  # Edges between any two groups

def generate_3_colorable_graph(num_nodes, edges_per_group_pair):
    """Generate a guaranteed 3-colorable graph by enforcing strict partitioning."""
    edges = []
    group_size = num_nodes // 3

    # Divide nodes into three disjoint groups
    group_a = list(range(0, group_size))
    group_b = list(range(group_size, 2 * group_size))
    group_c = list(range(2 * group_size, num_nodes))

    # Add edges between Group A and Group B
    edges.extend(random.sample(
        [(u, v) for u in group_a for v in group_b],
        min(edges_per_group_pair, len(group_a) * len(group_b))
    ))

    # Add edges between Group B and Group C
    edges.extend(random.sample(
        [(u, v) for u in group_b for v in group_c],
        min(edges_per_group_pair, len(group_b) * len(group_c))
    ))

    # Add edges between Group C and Group A
    edges.extend(random.sample(
        [(u, v) for u in group_c for v in group_a],
        min(edges_per_group_pair, len(group_c) * len(group_a))
    ))

    return edges

# Generate the graph
edges = generate_3_colorable_graph(num_nodes, edges_per_group_pair)

# Write to CSV
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["indirected"])  # The graph is undirected
    for edge in edges:
        writer.writerow(edge)

print(f"3-colorable graph with {num_nodes} nodes saved to {output_file}.")
