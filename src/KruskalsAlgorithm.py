import sys
from utils import check_args
from graph import dsu
import os
import time


def main() -> None:
    assert len(sys.argv) == 2, (
        "Usage: python3" + os.path.basename(__file__) + "<path_to_input_file>"
    )
    start_time = time.time()
    file_path = os.path.abspath(sys.argv[1])
    with open(file_path, "r") as f:
        n = int(f.readline())
        edges: list[tuple[int, int, float]] = []
        for i, line in enumerate(f):
            neighbours_and_weights = line.split()
            for j, x in enumerate(neighbours_and_weights):
                x = x.split(",")
                edges.append((i, int(x[0]), float(x[1])))

        edges.sort(key=lambda x: x[2])
        d = dsu(n)
        mst: list[tuple[int, int, float]] = []
        total_cost: float = 0

        for i, edge in enumerate(edges):
            x = d.find_set(edge[0])
            y = d.find_set(edge[1])
            if x != y:
                mst.append(edge)
                d.union_sets(x, y)
                total_cost += edge[2]
            if len(mst) == n - 1:
                break

        if len(mst) != n - 1:
            print(f"MST not found")
            return
        execution_time = time.time() - start_time
        print(f"Time taken = {execution_time} seconds")
        print(f"Total cost = {total_cost}")
        # print(f"mst = {mst}")
        print(f"MST Found")


if __name__ == "__main__":
    main()
