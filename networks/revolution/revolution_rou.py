import random
import pathes
import numpy as np

rou_min = 0.2
rou_max = 0.7

with open(pathes.revolution_parameter) as f:
    lines = f.readlines()

node_number = int(lines[0])

Rou = np.array([random.uniform(rou_min, rou_max) for _ in range(node_number)])

np.savetxt(pathes.revolution_rou, Rou)

