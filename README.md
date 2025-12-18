# Matrix benchmarks

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