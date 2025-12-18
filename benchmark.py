from webbrowser import get
import platform
from time import time
import numpy as np


# Seed numpy for reproducibility.
np.random.seed(666)

size = 8192
A, B = np.random.random((size, size)), np.random.random((size, size))
C, D = np.random.random((size * 512,)), np.random.random((size * 512,))
E = np.random.random((int(size / 2), int(size / 4)))
F = np.random.random((int(size), int(size)))
F = np.dot(F, F.T)
G = np.random.random((int(size / 4), int(size / 4)))

# Matrix multiplication
N = 5
t = time()
for i in range(N):
    np.dot(A, B)
delta = time() - t
print(f'Dotted two {A.shape[0]}x{A.shape[1]} matrices in {delta / N:0.2f} s.')
del A, B

# Vector multiplication
N = 5000
t = time()
for i in range(N):
    np.dot(C, D)
delta = time() - t
print(f'Dotted two vectors of length {C.shape[0]} in {1e3 * delta / N:0.2f} ms.')
del C, D

# Singular Value Decomposition (SVD)
N = 3
t = time()
for i in range(N):
    np.linalg.svd(E, full_matrices = False)
delta = time() - t
print(f"SVD of a {E.shape[0]}x{E.shape[1]} matrix in {delta / N:0.2f} s.")
del E

# Cholesky Decomposition
N = 3
t = time()
for i in range(N):
    np.linalg.cholesky(F)
delta = time() - t
print(f"Cholesky decomposition of a {F.shape[0]}x{F.shape[1]} matrix in {delta / N:0.2f} s.")

# Eigendecomposition
t = time()
for i in range(N):
    np.linalg.eig(G)
delta = time() - t
print(f"Eigendecomposition of a {G.shape[0]}x{G.shape[1]} matrix in {delta / N:0.2f} s.")