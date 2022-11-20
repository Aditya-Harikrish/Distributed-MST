"""
Usage: python GenerateInput.py file_path.mtx
Output goes to: file_path.in

Converts matrix market files to directed graphs of the following format:

1. The first line has N, the number of vertices.
2. Each of the following N lines have the vertices that are connected to that vertex. If there are none, the line is empty.

In other words:

N
vertices that vertex 1 has outgoing edges towards
vertices that vertex 2 has outgoing edges towards
...
vertices that vertex N has outgoing edges towards

"""

import os
import sys
from typing import List


def GetFilePath() -> str:
    if len(sys.argv) != 2:
        sys.exit(f"Usage: python GenerateInput.py file_path.mtx")
    elif not sys.argv[1].endswith(".mtx"):
        sys.exit(f"The input file must end in .mtx")
    return sys.argv[1]


# Loads the input file into an adjacency list
def SetGraph(inputFilePath: str) -> List[set]:
    firstLine: bool = True
    try:
        with open(inputFilePath, "r") as f:
            print(f"Reading {inputFilePath}")
            for line in f:
                if line[0] == "%" or line.isspace() or line in [None, ""]:
                    continue
                line = line.split()
                if firstLine:
                    nrows, ncols, nnz = int(line[0]), int(line[1]), float(line[2])
                    firstLine = False
                    graph = [set() for j in range(nrows)]
                else:
                    i, j = int(line[0]), int(line[1])
                    graph[i - 1].add(j - 1)
    except FileNotFoundError:
        sys.exit(f"File {inputFilePath} not found")

    return graph


# Writes to file_path.in
def WriteOutput(inputFilePath: str, graph: List[str]):
    inputFilePath = os.path.abspath(inputFilePath)
    outputFilePath = inputFilePath[: len(inputFilePath) - 3] + "in"
    print(f"Writing to {outputFilePath}")
    with open(outputFilePath, "w") as f:
        print(len(graph), file=f)
        for i, node in enumerate(graph):
            print(*node, sep=" ", end="\n", file=f)
    print("Done")


def main() -> None:
    inputFilePath = GetFilePath()
    graph = SetGraph(inputFilePath)
    WriteOutput(inputFilePath, graph)


if __name__ == "__main__":
    main()
