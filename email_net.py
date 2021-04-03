from scipy import sparse
import random
from scipy.linalg import eig, eigh
from scipy.sparse.linalg import eigs, eigsh
import re

beta_min = 0.5
beta_max = 0.8

with open(r'Email-EuAll.txt') as f:
    lines = f.readlines()

lines.pop(0)
lines.pop(0)
properties = lines.pop(0)
lines.pop(0)

node_number = int(re.findall("\d+", properties)[0])  # number of nodes

# sparse adjacency matrix of network
sp_a = sparse.lil_matrix((node_number, node_number))

# initialize adjacency matrix of network (add beta)
for line in lines:
    numbers = [int(i) for i in line.split()]
    sp_a[numbers[0], numbers[1]] = random.uniform(beta_min, beta_max)

sp_a = sp_a.tocsr()


# get max eigenvalues of adjacency matrix
# evals_large, evecs_large = eigsh(sp_a, 1, which='LM')
