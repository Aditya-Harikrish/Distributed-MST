from utils import *


class Graph:
    def __init__(self, filepath):
        try:
            with open(filepath, "r") as f:
                self.n = int(f.readline())
                self.start_node = rank * int(self.n / size)
                self.num_nodes = (
                    int(self.n / size) if rank < size - 1 else self.n - self.start_node
                )
                self.graph = {
                    i: set()
                    for i in range(self.start_node, self.start_node + self.num_nodes)
                }
                for i, line in enumerate(
                    islice(
                        f,
                        self.start_node,
                        (rank + 1) * int(self.n / size) if rank != size - 1 else None,
                    )
                ):
                    j = i + self.start_node
                    if j not in self.graph:
                        abort_all_processes(f"Error: {j} not in {self.graph}")
                    self.graph[j].update(map(int, line.split()))

        except FileNotFoundError:
            abort_all_processes(f"File {filepath} not found")

        except Exception as e:
            abort_all_processes(f"Error: {e}")

    def __str__(self) -> str:
        string = (
            f"\n{rank=}\n"
            + f"{self.n=}\n"
            + "\n".join(
                [
                    f"{i}: {' '.join([str(x) for x in self.graph[i]])}"
                    for i in self.graph
                ]
            )
        )
        return string
