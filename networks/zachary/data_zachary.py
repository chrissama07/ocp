import numpy as np
import pathes

A = np.loadtxt(pathes.zachary_data)

Cn = np.loadtxt(pathes.zachary_cost)

gamma = np.loadtxt(pathes.zachary_curingrate)

Rou = np.loadtxt(pathes.zachary_rou)

with open(pathes.zachary_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])