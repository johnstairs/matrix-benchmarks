# Matrix benchmarks


## Summary

| System                            | Backend  | Matmul (8192²) | Inverse (8192²) | SVD (4096²) | Cholesky (8192²) | Eigen (2048²) |
|-----------------------------------|----------|----------------|-----------------|-------------|------------------|---------------|
| Macbook Air M2 (8 cores ARM)      | OpenBLAS | 5.14s          | 8.77s           | 20.95s      | 1.90s            | 5.75s         |
| DGX Spark (20 cores ARM)          | OpenBLAS | 2.78s          | **4.30s**       | **8.03s**   | **1.49s**        | **1.92s**     |
| Azure NC24ads A100 (24 cores AMD) | MKL      | **1.55s**      | 4.65s           | 10.05s      | 2.49s            | 5.16s         |
| Azure NC24ads A100 (24 cores AMD) | OpenBLAS | 1.62s          | 8.00s           | 17.89s      | 5.91s            | 4.37s         |
| Azure F16s_v2 (16 cores Intel)    | MKL      | 2.11s          | 4.45s           | 11.89s      | 1.50s            | 3.67s         |
| Azure F16s_v2 (16 cores Intel)    | OpenBLAS | 2.49s          | 5.98s           | 16.29s      | 2.63s            | 5.12s         |

*Times in seconds (lower is better). Best results in **bold**.*

---

## Detailed Results

### Macbook Air M2 (8 cores - ARM)

```
Multiplied two 8192x8192 matrices in 5.14 s.
Inverted a 8192x8192 matrix in 8.77 s.
SVD of a 4096x4096 matrix in 20.95 s.
Cholesky decomposition of a 8192x8192 matrix in 1.90 s.
Eigendecomposition of a 2048x2048 matrix in 5.75 s.
```

### DGX Spark (20 cores - ARM) 

```
Multiplied two 8192x8192 matrices in 2.78 s.
Inverted a 8192x8192 matrix in 4.30 s.
SVD of a 4096x4096 matrix in 8.03 s.
Cholesky decomposition of a 8192x8192 matrix in 1.49 s.
Eigendecomposition of a 2048x2048 matrix in 1.92 s.
```

### Azure Standard_NC24ads_A100_v4 (24 cores - AMD EPYC 7V13)

### MKL:
```
Multiplied two 8192x8192 matrices in 1.55 s.
Inverted a 8192x8192 matrix in 4.65 s.
SVD of a 4096x4096 matrix in 10.05 s.
Cholesky decomposition of a 8192x8192 matrix in 2.49 s.
Eigendecomposition of a 2048x2048 matrix in 5.16 s.
```

### OpenBLAS:
```
Multiplied two 8192x8192 matrices in 1.62 s.
Inverted a 8192x8192 matrix in 8.00 s.
SVD of a 4096x4096 matrix in 17.89 s.
Cholesky decomposition of a 8192x8192 matrix in 5.91 s.
Eigendecomposition of a 2048x2048 matrix in 4.37 s.
```

### Azure Standard_F16s_v2 (16 cores - Intel Xeon Platinum 8272CL)

### MKL:

```
Multiplied two 8192x8192 matrices in 2.11 s.
Inverted a 8192x8192 matrix in 4.45 s.
SVD of a 4096x4096 matrix in 11.89 s.
Cholesky decomposition of a 8192x8192 matrix in 1.50 s.
Eigendecomposition of a 2048x2048 matrix in 3.67 s.
```

### OpenBLAS:

```
Multiplied two 8192x8192 matrices in 2.49 s.
Inverted a 8192x8192 matrix in 5.98 s.
SVD of a 4096x4096 matrix in 16.29 s.
Cholesky decomposition of a 8192x8192 matrix in 2.63 s.
Eigendecomposition of a 2048x2048 matrix in 5.12 s.
```

## Running the bechmarks

``` bash 
pixi run -e openblas bench

# or 

pixi run -e mkl bench
```