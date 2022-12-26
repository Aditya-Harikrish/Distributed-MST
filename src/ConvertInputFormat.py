"""
Usage: python3 ConvertInputFormat.py file_path.mtx <indexing>
<indexing> can be 0 or 1 or any other natural number 

Output goes to: file_path.in

Converts matrix market files to directed graphs of the following format:

1. The first line has N, the number of vertices.
2. Each of the following N lines have the vertices that are connected to that vertex. If there are none, the line is empty.

In other words:

N
v11,w11 v12,w12 ...
v21,w21 v22,w22 ...
...
vN1,wN1 vN2,wN2 ...

where vij is the vertex that vertex i has an outgoing edge towards, and wij is the weight of that edge.
"""

import os
import sys
from typing import List, Tuple


indexing: int = 0


def get_path() -> str:
    if len(sys.argv) != 3:
        sys.exit(f"Usage: python GenerateInput.py file_path.mtx")
    elif not sys.argv[1].endswith(".mtx"):
        sys.exit(f"The input file must end in .mtx")
    global indexing
    indexing = int(sys.argv[2])
    return sys.argv[1]


# Loads the input file into an adjacency list
def set_graph(input_path: str) -> List[Tuple[int, int]]:
    firstLine: bool = True
    try:
        with open(input_path, "r") as f:
            print(f"Reading {input_path}")
            for line in f:
                if line[0] == "%" or line.isspace() or line in [None, ""]:
                    continue
                line = line.split()
                if firstLine:
                    nrows, ncols, nnz = int(line[0]), int(line[1]), float(line[2])
                    firstLine = False
                    graph = [set() for j in range(nrows)]
                else:
                    i, j, w = int(line[0]), int(line[1]), float(line[2])
                    graph[i - indexing].add((j - indexing, w))
                    graph[j - indexing].add((i - indexing, w))
    except FileNotFoundError:
        sys.exit(f"File {input_path} not found")

    return graph


# Writes to file_path.in
def write_output(input_path: str, graph: List[Tuple[int, int]]):
    input_path = os.path.abspath(input_path)
    output_path = input_path[: len(input_path) - 3] + "in"
    print(f"Writing to {output_path}")
    with open(output_path, "w") as f:
        print(len(graph), file=f)
        for i, node in enumerate(graph):
            print(" ".join([f"{j},{w}" for j, w in node]), file=f)

            # print(*node, sep=" ", end="\n", file=f)
            # print(file=f)
    print("Done")


def main() -> None:
    input_path = get_path()
    graph = set_graph(input_path)
    write_output(input_path, graph)


if __name__ == "__main__":
    main()
