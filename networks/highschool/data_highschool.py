import numpy as np
import pathes

A = np.loadtxt(pathes.highschool_data)

Cn = np.loadtxt(pathes.highschool_cost)

gamma = np.loadtxt(pathes.highschool_curingrate)

Rou = np.loadtxt(pathes.highschool_rou)

with open(pathes.highschool_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])