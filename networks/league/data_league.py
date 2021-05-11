import numpy as np
import pathes

A = np.loadtxt(pathes.league_data)

Cn = np.loadtxt(pathes.league_cost)

gamma = np.loadtxt(pathes.league_curingrate)

with open(pathes.league_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])