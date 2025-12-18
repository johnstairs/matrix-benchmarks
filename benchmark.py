from webbrowser import get
import platform
from time import time
import numpy as np


def get_blas_info():
    """Detect and display the BLAS backend being used by NumPy."""
    print("=" * 60)
    print("NumPy BLAS Configuration")
    print("=" * 60)
    
    # Trigger numpy to load BLAS libraries
    _ = np.dot(np.random.random((10, 10)), np.random.random((10, 10)))
    
    # Check loaded shared libraries for BLAS indicators
    try:
        import re
        
        # Read /proc/self/maps to see loaded libraries
        with open('/proc/self/maps', 'r') as f:
            maps = f.read()
        
        blas_libs = set()
        # Look for specific BLAS library patterns
        patterns = [
            (r'/[^\s]*libmkl[^\s]*\.so[^\s]*', 'MKL'),
            (r'/[^\s]*libopenblas[^\s]*\.so[^\s]*', 'OpenBLAS'),
            (r'/[^\s]*libblis[^\s]*\.so[^\s]*', 'BLIS'),
            (r'/[^\s]*libatlas[^\s]*\.so[^\s]*', 'ATLAS'),
        ]
        
        detected_backend = None
        for pattern, name in patterns:
            matches = re.findall(pattern, maps)
            if matches:
                detected_backend = name
                for lib in set(matches):
                    blas_libs.add(lib)
        
        if detected_backend:
            print(f"BLAS Backend: {detected_backend}")
            print("Loaded BLAS libraries:")
            for lib in sorted(blas_libs):
                print(f"  - {lib}")
        else:
            print("BLAS Backend: Unknown (possibly netlib or system default)")
    except Exception as e:
        print(f"Could not inspect loaded libraries: {e}")
    
    print("=" * 60)
    print()


get_blas_info()

# Seed numpy for reproducibility.
np.random.seed(666)

size = 8192
A, B = np.random.random((size, size)), np.random.random((size, size))
E = np.random.random((int(size / 2), int(size / 2)))
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

# Matrix inversion
N = 5
t = time()
for i in range(N):
    np.linalg.inv(A)
delta = time() - t
print(f'Inverted a {A.shape[0]}x{A.shape[1]} matrix in {delta / N:0.2f} s.')

# Singular Value Decomposition (SVD)
N = 3
t = time()
for i in range(N):
    np.linalg.svd(E, full_matrices = False)
delta = time() - t
print(f"SVD of a {E.shape[0]}x{E.shape[1]} matrix in {delta / N:0.2f} s.")

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