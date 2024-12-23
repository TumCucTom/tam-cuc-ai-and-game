import re
from collections import defaultdict
import pyperclip

# Read input from file
input_file = "../data/23.txt"
with open(input_file, "r") as file:
    connections = file.read().strip().split("\n")

# Build adjacency list
adj_list = defaultdict(set)
for connection in connections:
    a, b = connection.split("-")
    adj_list[a].add(b)
    adj_list[b].add(a)

# Bron-Kerbosch algorithm to find the largest clique
def bron_kerbosch(r, p, x, adj_list):
    if not p and not x:
        yield r
    while p:
        v = p.pop()
        yield from bron_kerbosch(r.union({v}), p.intersection(adj_list[v]), x.intersection(adj_list[v]), adj_list)
        x.add(v)

# Find the largest clique
all_nodes = set(adj_list.keys())
largest_clique = max(bron_kerbosch(set(), all_nodes, set(), adj_list), key=len)
password = ",".join(sorted(largest_clique))

# Output the result
print(password)

# Copy the result to clipboard
pyperclip.copy(password)
