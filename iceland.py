from scipy import sparse
import random

beta_min = 0.5
beta_max = 0.8

with open(r'out.iceland') as f:
    lines = f.readlines()

lines.pop(0)
node_number = 76

sp_a = sparse.lil_matrix((node_number, node_number))

for line in lines:
    numbers = [int(i) for i in line.split()]
    sp_a[numbers[0], numbers[1]] = random.uniform(beta_min, beta_max)

sp_a = sp_a.tocsr()