import os
import random

n = 4
# path = os.path.abspath(os.path.join('..', 'data', 'test.in'))
path = os.path.abspath("data/test1.in")
with open(path, "w+") as f:
    print(n, file=f)
    for i in range(n):
        for j in range(n):
            print(f"{j},{random.random() * 100} ", end="", file=f)
        print(file=f)
