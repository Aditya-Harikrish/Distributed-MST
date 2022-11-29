import sys
import os


def main() -> None:
    assert len(sys.argv) == 2, (
        "Usage: python3" + os.path.basename(__file__) + "<path_to_input_file>"
    )
    file_path = os.path.abspath(sys.argv[1])
    with open(file_path, "r") as f:
        edges: list[tuple[int, int, float]] = []
        n = int(f.readline())
        for i, line in enumerate(f):
            neighbours_and_weights = line.split()
            for j, x in enumerate(neighbours_and_weights):
                x = x.split(",")
                edges.append((i, int(x[0]), float(x[1])))
        edges.sort(key=lambda x: x[2])
        visited: list[bool] = [False for i in range(n)]
        mst: list[tuple[int, int, float]] = []
        total_cost: float = 0
        for i, edge in enumerate(edges):
            if visited[edge[0]] and visited[edge[1]]:
                continue
            elif edge[0] == edge[1]:
                continue
            mst.append(edge)
            visited[edge[0]] = True
            visited[edge[1]] = True
            total_cost += edge[2]
            if len(mst) == n - 1:
                break

        print(f"{mst=}")
        print(f"{total_cost=}")


if __name__ == "__main__":
    main()
