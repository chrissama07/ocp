from scipy import sparse
import random
from scipy.linalg import eig, eigh
from scipy.sparse.linalg import eigs, eigsh
import ocpde

with open(r'Email-EuAll.txt') as f:
    lines = f.readlines()

lines.pop(0)
lines.pop(0)
properties = lines.pop(0)
lines.pop(0)

sp_a = sparse.lil_matrix((265214,265214))


for line in lines:
    numbers = [int(i) for i in line.split()]
    sp_a[numbers[0],numbers[1]] = random.random()

sp_a = sp_a.tocsr()

evals_large, evecs_large = eigsh(sp_a, 1, which='LM')