"""Benchmark script for NumPy linear algebra operations."""

import ctypes
import re
import sys
from time import time

import numpy as np
from threadpoolctl import threadpool_info

# Configuration
MATRIX_SIZE = 8192
RANDOM_SEED = 666

# (regex, backend label) tuples. First match wins per kind.
BLAS_PATTERNS = [
    (re.compile(r"libmkl_rt|libmkl_core", re.I), "MKL"),
    (re.compile(r"libopenblas", re.I), "OpenBLAS"),
    (re.compile(r"libblis", re.I), "BLIS"),
    (re.compile(r"Accelerate\.framework.*libBLAS|libvecLib", re.I), "Apple Accelerate"),
    (re.compile(r"libatlas", re.I), "ATLAS"),
]

LAPACK_PATTERNS = [
    (re.compile(r"libmkl_rt|libmkl_core", re.I), "MKL"),
    (re.compile(r"libopenblas", re.I), "OpenBLAS"),
    (re.compile(r"liblapack-netlib|libreflapack|liblapack\.", re.I), "Netlib (reference)"),
    (re.compile(r"Accelerate\.framework.*libLAPACK|libvecLibFort", re.I), "Apple Accelerate"),
]


def benchmark(func, iterations):
    """Run a function multiple times and return the average execution time."""
    start = time()
    for _ in range(iterations):
        func()
    return (time() - start) / iterations


def _loaded_libraries():
    """Return a list of paths of currently loaded shared libraries."""
    if sys.platform == "darwin":
        libc = ctypes.CDLL(None)
        libc._dyld_image_count.restype = ctypes.c_uint32
        libc._dyld_get_image_name.restype = ctypes.c_char_p
        libc._dyld_get_image_name.argtypes = [ctypes.c_uint32]
        return [
            libc._dyld_get_image_name(i).decode()
            for i in range(libc._dyld_image_count())
        ]
    if sys.platform.startswith("linux"):
        try:
            with open("/proc/self/maps") as f:
                paths = set()
                for line in f:
                    parts = line.rsplit(maxsplit=1)
                    if len(parts) == 2 and parts[1].startswith("/"):
                        paths.add(parts[1].rstrip())
                return sorted(paths)
        except OSError:
            return []
    return []


def _match(patterns, libs):
    """Return (label, library_path) for the first matching pattern, or (None, None)."""
    for pattern, label in patterns:
        for lib in libs:
            if pattern.search(lib):
                return label, lib
    return None, None


def get_blas_info():
    """Detect and display the BLAS/LAPACK backends being used by NumPy."""
    print("=" * 60)
    print("NumPy BLAS Configuration")
    print("=" * 60)

    # Trigger numpy to load BLAS/LAPACK libraries.
    a = np.random.random((10, 10))
    np.dot(a, a)
    np.linalg.svd(a)

    libs = _loaded_libraries()
    blas_name, blas_path = _match(BLAS_PATTERNS, libs)
    lapack_name, lapack_path = _match(LAPACK_PATTERNS, libs)

    # threadpoolctl gives us the active thread count when it can introspect the lib.
    pools_by_lib = {p.get("filepath"): p for p in threadpool_info()}

    for kind, name, path in (
        ("BLAS  ", blas_name, blas_path),
        ("LAPACK", lapack_name, lapack_path),
    ):
        if name:
            pool = pools_by_lib.get(path, {})
            extras = []
            version = pool.get("version")
            if version:
                extras.append(f"version {version}")
            threads = pool.get("num_threads")
            if threads is not None:
                extras.append(f"{threads} threads")
            suffix = f" ({', '.join(extras)})" if extras else ""
            print(f"{kind} Backend: {name}{suffix}")
            print(f"  library: {path}")
        else:
            print(f"{kind} Backend: Unknown")

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