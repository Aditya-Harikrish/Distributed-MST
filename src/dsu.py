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
