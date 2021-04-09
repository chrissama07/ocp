import numpy as np
import random
import re

beta_min = 0.5
beta_max = 0.8

with open(r'networks/emailNet/source/Email-EuAll.txt') as f:
    lines = f.readlines()

lines.pop(0)
lines.pop(0)
properties = lines.pop(0)
lines.pop(0)

node_number = int(re.findall("\d+", properties)[0])  # number of nodes
edge_number = int(re.findall("\d+", properties)[1])

# sparse adjacency matrix of network
lines = np.array(lines)
edges = np.empty([edge_number, 3])

i = 0
for line in lines:
    numbers = [int(i) for i in line.split()]
    for j in range(3):
        if j < 2:
            edges[i][j] = numbers[j]
        else:
            edges[i][j] = random.uniform(beta_min, beta_max)
    i += 1

Cn = np.array([random.randint(10, 20) for _ in range(node_number)])  # the cost of vaccine
gamma = np.array([random.uniform(0.6, 0.7) for _ in range(node_number)])  # curing rate

# save edges data
np.savetxt("networks/emailNet/emailNet.data.txt", edges)

np.savetxt("networks/emailNet/emailNet.curingrate.txt", gamma)

np.savetxt("networks/emailNet/emailNet.cost.txt", Cn)

with open("networks/emailNet/emailNet.parameter.txt", "w") as f:
    text = f.write(str(node_number) + "\n" + str(edge_number))
f.close()
