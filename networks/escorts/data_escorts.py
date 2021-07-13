import numpy as np
import pathes

A = np.loadtxt(pathes.escorts_data)

Cn = np.loadtxt(pathes.escorts_cost)

gamma = np.loadtxt(pathes.escorts_curingrate)

with open(pathes.escorts_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])