"""Benchmark script for NumPy linear algebra operations."""

import re
from time import time

import numpy as np

# Configuration
MATRIX_SIZE = 8192
RANDOM_SEED = 666

BLAS_PATTERNS = [
    (r"/[^\s]*libmkl[^\s]*\.so[^\s]*", "MKL"),
    (r"/[^\s]*libopenblas[^\s]*\.so[^\s]*", "OpenBLAS"),
    (r"/[^\s]*libblis[^\s]*\.so[^\s]*", "BLIS"),
    (r"/[^\s]*libatlas[^\s]*\.so[^\s]*", "ATLAS"),
]


def benchmark(func, iterations):
    """Run a function multiple times and return the average execution time."""
    start = time()
    for _ in range(iterations):
        func()
    return (time() - start) / iterations


def get_blas_info():
    """Detect and display the BLAS backend being used by NumPy."""
    print("=" * 60)
    print("NumPy BLAS Configuration")
    print("=" * 60)

    # Trigger numpy to load BLAS libraries
    np.dot(np.random.random((10, 10)), np.random.random((10, 10)))

    try:
        with open("/proc/self/maps") as f:
            maps = f.read()

        blas_libs = set()
        detected_backend = None

        for pattern, name in BLAS_PATTERNS:
            matches = re.findall(pattern, maps)
            if matches:
                detected_backend = name
                blas_libs.update(matches)

        if detected_backend:
            print(f"BLAS Backend: {detected_backend}")
            print("Loaded BLAS libraries:")
            for lib in sorted(blas_libs):
                print(f"  - {lib}")
        else:
            print("BLAS Backend: Unknown (possibly netlib or system default)")
    except OSError as e:
        print(f"Could not inspect loaded libraries: {e}")

    print("=" * 60)
    print()


def run_benchmarks():
    """Run all matrix operation benchmarks."""
    np.random.seed(RANDOM_SEED)

    # Create test matrices
    a = np.random.random((MATRIX_SIZE, MATRIX_SIZE))
    b = np.random.random((MATRIX_SIZE, MATRIX_SIZE))
    svd_matrix = np.random.random((MATRIX_SIZE // 2, MATRIX_SIZE // 2))
    cholesky_matrix = np.random.random((MATRIX_SIZE, MATRIX_SIZE))
    cholesky_matrix = np.dot(cholesky_matrix, cholesky_matrix.T)
    eig_matrix = np.random.random((MATRIX_SIZE // 4, MATRIX_SIZE // 4))

    # Matrix multiplication
    avg_time = benchmark(lambda: np.matmul(a, b), iterations=5)
    print(f"Multiplied two {a.shape[0]}x{a.shape[1]} matrices in {avg_time:.2f} s.")

    # Matrix inversion
    avg_time = benchmark(lambda: np.linalg.inv(a), iterations=5)
    print(f"Inverted a {a.shape[0]}x{a.shape[1]} matrix in {avg_time:.2f} s.")

    # Singular Value Decomposition (SVD)
    avg_time = benchmark(
        lambda: np.linalg.svd(svd_matrix, full_matrices=False), iterations=3
    )
    print(f"SVD of a {svd_matrix.shape[0]}x{svd_matrix.shape[1]} matrix in {avg_time:.2f} s.")

    # Cholesky Decomposition
    avg_time = benchmark(lambda: np.linalg.cholesky(cholesky_matrix), iterations=3)
    print(
        f"Cholesky decomposition of a {cholesky_matrix.shape[0]}x{cholesky_matrix.shape[1]} "
        f"matrix in {avg_time:.2f} s."
    )

    # Eigendecomposition
    avg_time = benchmark(lambda: np.linalg.eig(eig_matrix), iterations=3)
    print(
        f"Eigendecomposition of a {eig_matrix.shape[0]}x{eig_matrix.shape[1]} "
        f"matrix in {avg_time:.2f} s."
    )


def main():
    """Main entry point."""
    get_blas_info()
    run_benchmarks()


if __name__ == "__main__":
    main()