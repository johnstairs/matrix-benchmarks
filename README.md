# Matrix benchmarks


### Macbook Air M2 (8 cores)

```
Dotted two 8192x8192 matrices in 5.17 s.
Dotted two vectors of length 4194304 in 0.99 ms.
SVD of a 4096x2048 matrix in 4.78 s.
Cholesky decomposition of a 8192x8192 matrix in 1.90 s.
Eigendecomposition of a 2048x2048 matrix in 5.58 s.
```

### DGX Spark (ARM 20 cores) 

```
Dotted two 8192x8192 matrices in 2.78 s.
Dotted two vectors of length 4194304 in 0.38 ms.
SVD of a 4096x2048 matrix in 1.69 s.
Cholesky decomposition of a 8192x8192 matrix in 1.47 s.
Eigendecomposition of a 2048x2048 matrix in 1.83 s.
```

### Azure Standard_NC24ads_A100_v4 (24 cores)

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