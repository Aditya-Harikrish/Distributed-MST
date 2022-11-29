import utils as u
from utils import abort_all_processes
from itertools import islice
import sys
import logging


class dsu:
    def __init__(self, n) -> None:
        self.parent = [i for i in range(n)]
        self.rank = [i for i in range(n)]

    def find_set(self, v: int) -> int:
        if v == self.parent[v]:
            return v
        self.parent[v] = self.find_set(self.parent[v])
        return self.parent[v]

    def union_sets(self, a: int, b: int) -> None:
        a = self.find_set(a)
        b = self.find_set(b)
        if a != b:
            if self.rank[a] < self.rank[b]:
                a, b = b, a
            self.parent[b] = a
            if self.rank[a] == self.rank[b]:
                self.rank[a] += 1

    def allsame(self) -> bool:
        parents = set()
        for p in self.parent:
            parents.add(self.find_set(p))
            # if len(parents) > 1:
            #     return False
        # print(len(parents))
        # logging.debug(parents)
        # logging.debug(len(parents))
        if len(parents) > 1:
            return False
        return True


class Graph:
    # class Fragment:
    #     def __init__(self, root: int) -> None:
    #         self.root = root
    #         self.members = set([root])
    #         self.edges =

    class VertexProperties:
        def __init__(self, fragment_ID: int) -> None:
            self.fragment_ID = fragment_ID
            self.neighbours: set[
                tuple[int, float]
            ] = set()  # set of tuples (vertex, weight)
            self.moe: int = -1  # minimum outgoing edge
            self.moe_weight = None

    def __init__(self, filepath) -> None:
        """ 
        Loads that part of the graph the corresponds to the rank from the input file into an adjacency list.
        """
        try:
            with open(filepath, "r") as f:
                self.n = int(f.readline())
                self.dsu = dsu(self.n)
                self.update_size()
                # self.start_node = u.rank * int(self.n / u.size)
                # self.num_nodes = (
                #     int(self.n / u.size)
                #     if u.rank < u.size - 1
                #     else self.n - self.start_node
                # )
                self.start_node = u.rank * int((self.n + u.size - 1) / u.size)
                self.num_nodes = min(
                    int((self.n + u.size - 1) / u.size), self.n - self.start_node
                )
                self.graph = {
                    i: self.VertexProperties(i)
                    for i in range(self.start_node, self.start_node + self.num_nodes)
                }
                # Iterate over the lines in the file belonging to the rank
                for i, line in enumerate(
                    islice(
                        f,
                        self.start_node,
                        self.start_node+self.num_nodes
                        if u.rank != u.size - 1
                        else None,
                    )
                ):
                    j = i + self.start_node
                    if j not in self.graph:
                        abort_all_processes(f"Error: {j} not in {self.graph}")
                    neighbours_and_weights = line.split()
                    for i, x in enumerate(neighbours_and_weights):
                        x = x.split(",")
                        neighbours_and_weights[i] = (int(x[0]), float(x[1]))
                    self.graph.get(j).neighbours.update(neighbours_and_weights)

        except FileNotFoundError:
            abort_all_processes(f"File {filepath} not found")

        except Exception as e:
            abort_all_processes(f"Error: {e}")

    # def init_fragments(self) -> None:
    #     self.fragments = {
    #         i: self.Fragment(i)
    #         for i in range(self.start_node, self.start_node + self.num_nodes)
    #     }

    def process_of_vertex(self, v: int) -> int:
        return int(v / int((self.n + u.size - 1) / u.size))

    def belongs_to_this_process(self, vertex: int) -> bool:
        return self.start_node <= vertex < self.start_node + self.num_nodes

    def belong_to_same_fragment(self, u: int, v: int) -> bool:
        if self.dsu.find_set(u) == self.dsu.find_set(v):
            return True
        return False

    def update_size(self):
        """ 
        Handles the unlikely case where the number of processes is greater than or equal to the number of vertices in the graph. Call it paranoia.
        """
        # global u.size, u.rank
        if u.rank >= self.n:
            sys.exit(0)
        if self.n < u.size:
            u.size = self.n

    def __str__(self) -> str:
        string = f"\n{u.rank=}\n" f"n = {self.n}\n" + "\n".join(
            [
                f"{i}: "
                # f"fragment {self.graph.get(i).fragment_ID} | "
                f"moe: {self.graph.get(i).moe} | "
                f"{' '.join([str(x) for x in self.graph.get(i).neighbours])}"
                for i in self.graph
            ]
        )
        return string
