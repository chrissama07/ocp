import numpy as np

A = np.loadtxt("networks/emailNet/emailNet.data.txt")

Cn = np.loadtxt("networks/emailNet/emailNet.cost.txt")

txt = "networks/emailNet/emailNet.curingrate.txt"
gamma = np.loadtxt(txt)

with open(r'networks/emailNet/emailNet.parameter.txt') as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])