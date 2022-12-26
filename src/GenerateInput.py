import os
import random

n = 1000
# path = os.path.abspath(os.path.join('..', 'data', 'test.in'))
path = os.path.abspath("data/test" + str(n) + ".in")
with open(path, "w+") as f:
    print(n, file=f)
    adj_matrix = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(i + 1):
            adj_matrix[i][j] = adj_matrix[j][i] = random.random() * 100
    for i in range(n):
        for j in range(n):
            print(f"{j},{adj_matrix[i][j]} ", file=f, end="")
        print(file=f)
