import numpy as np
import pathes

A = np.loadtxt(pathes.jazz_data)

Cn = np.loadtxt(pathes.jazz_cost)

gamma = np.loadtxt(pathes.jazz_curingrate)

Rou = np.loadtxt(pathes.jazz_rou)

with open(pathes.jazz_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])