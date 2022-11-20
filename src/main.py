import logging
from time import sleep
from mpi4py import MPI
import sys
from itertools import islice

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.size


def check_args():
    if len(sys.argv) != 2:
        abort_all_processes(
            "Usage:  mpiexec -n num_processes python3 main.py <input_file>"
        )


def abort_all_processes(error_message: str) -> None:
    print(f"Rank {rank}: {error_message}")
    sys.stdout.flush()
    comm.Abort()


# print(f'{rank=}, {comm.size=}')


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
        string = f'\n{rank=}\n' + f"{self.n=}\n" + "\n".join(
            [f"{i}: {' '.join([str(x) for x in self.graph[i]])}" for i in self.graph]
        )
        return string


def main():
    logging.basicConfig(level=logging.DEBUG)
    check_args()
    graph = Graph(sys.argv[1])
    logging.debug(graph)


if __name__ == "__main__":
    main()
