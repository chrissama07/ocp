from scipy import sparse
import random
import numpy as np

beta_min = 0.5
beta_max = 0.8

with open(r'networks/iceland/source/out.iceland') as f:
    lines = f.readlines()

# parameters
lines.pop(0)
node_number = 76
edge_number = len(lines)

lines = np.array(lines)
edges = np.empty([edge_number, 3])

# get three tuples of adjacency matrix

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
np.savetxt("networks/iceland/iceland.data.txt", edges)

np.savetxt("networks/iceland/iceland.curingrate.txt", gamma)

np.savetxt("networks/iceland/iceland.cost.txt", Cn)

with open("networks/iceland/iceland.parameter.txt", "w") as f:
    text = f.write(str(node_number) + "\n" + str(edge_number))
f.close()

# sp_a = sparse.lil_matrix((node_number, node_number))
#
# for line in lines:
#     numbers = [int(i) for i in line.split()]
#     sp_a[numbers[0], numbers[1]] = random.uniform(beta_min, beta_max)
#
# sp_a = sp_a.tocsr()

