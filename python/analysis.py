#analysis
import numpy as np

def computations(A, MD, eVperhbar, t):
    # For checking eigenvalues only:
    idio = np.linalg.eigvals(A)
    
    # Compute right eigenvectors (V) and eigenvalues (D)
    D_vals, V = np.linalg.eig(A)
    idx = D_vals.argsort()
    D = np.diag(D_vals[idx])
    V = V[:, idx]

    # Compute left eigenvectors (W): eigenvectors of A transpose
    D_trans_vals, W = np.linalg.eig(A.T)
    W = W[:, idx]
    W = np.conj(W)  # Conjugate as MATLAB does with A.'

    degenerate = np.zeros(MD, dtype=int)
    DegeneracyFLAG = 'F'

    for k in range(MD):
        for j in range(k + 1, MD):
            if np.abs(idio[k] - idio[j]) <= 1.0e-12:
                DegeneracyFLAG = 'T'
                print(f"Degeneracy detected between indices k={k}, j={j}")
                degenerate[k] = 1
                degenerate[j] = 1

    print("DegeneracyFLAG =", DegeneracyFLAG)

    # Check if A is Hermitian (i.e., A == A†)
    if np.allclose(A.conj().T, A):
        lambda_vals = np.zeros(MD, dtype=complex)
        for k in range(MD):
            lambda_vals[k] = -1j * eVperhbar * D[k, k]  # Matrix A
        print("λ (lambda):", lambda_vals)

        if np.allclose(lambda_vals.real, np.zeros(MD)):
            print("Sum of periodic functions.")
        else:
            print("The sum of periodic functions is NOT generally a periodic function.")

    # Determine initial conditions
    # Meaning where the hole(HOMO) or electron (LUMO) is placed in the polymer
    print("\nDetermine Initial Conditions")
    x0 = np.zeros(MD)
    x0[1] = 1  # First base-pair

    # Find coefficients c using numerically stable solve
    ca = np.linalg.solve(V, x0)
    cb = np.linalg.lstsq(V, x0, rcond=None)[0]
    cc = np.dot(np.linalg.inv(V), x0)

    if np.allclose(ca, cb) and np.allclose(cb, cc):
        c = ca
        print("3 identical results for c")
    elif np.allclose(ca, cc):
        c = ca
        print("2 identical results for c")
    elif np.allclose(ca, cb):
        c = ca
        print("2 identical results for c")
    elif np.allclose(cb, cc):
        c = cb
        print("2 identical results for c")
    else:
        c = cb
        print("3 different results for c")

    # Check whether the eigenvectors are linearly independent
    print("Check whether the eigenvectors are linearly independent")
    Z = np.zeros(MD)

    Ma = np.linalg.solve(V, Z)
    Mb = np.linalg.lstsq(V, Z, rcond=None)[0]
    Mc = np.dot(np.linalg.inv(V), Z)

    if np.allclose(Ma, Mb) and np.allclose(Mb, Mc):
        M = Ma
        print("3 identical results for M")
    elif np.allclose(Ma, Mc):
        M = Ma
        print("2 identical results for M")
    elif np.allclose(Ma, Mb):
        M = Ma
        print("2 identical results for M")
    elif np.allclose(Mb, Mc):
        M = Mb
        print("2 identical results for M")
    else:
        M = Mb
        print("3 different results for M")

    if np.allclose(M, Z):  # Linearly independent
        print("OK linearly independent")

    # Time evolution of the state x(t)
    x = np.zeros((MD, len(t)), dtype=complex)
    for k in range(MD):
        x += c[k] * np.outer(V[:, k], np.exp(lambda_vals[k] * t))

    # Compute square norms and sums
    xsquare = x * np.conj(x)
    summ = np.sum(xsquare, axis=0)

    maxxsquare = np.max(xsquare, axis=1)
    meanxsquares = np.mean(xsquare, axis=1)
    
    # Initialize meanprob as complex to avoid warnings later
    meanprob = np.zeros(MD, dtype=complex)

    for k in range(MD):
        if DegeneracyFLAG == 'F':
            meanprob[k] = np.sum((c ** 2) * (V[k, :] ** 2))
        else:
            evol = np.sum(c[:, np.newaxis] * V[k, :, np.newaxis] * np.exp(np.outer(lambda_vals, t)), axis=0)
            meanprob[k] = np.mean(evol * np.conj(evol))

    suma = np.sum(meanxsquares)
    print(meanprob)

    # PARTICIPATION RATIO
    B = V.shape[0]  # number of sites
    pr = np.zeros(V.shape[1])
    for k in range(V.shape[1]):
        vec = V[:, k]
        pr[k] = 1.0 / (B * np.sum(np.abs(vec) ** 4))

    # Compute difference from mean probabilities
    proboftminusmeanprob = xsquare - meanprob[:, np.newaxis]
    index = np.zeros(MD, dtype=int)
    
    # Initialize these as complex to avoid casting warnings
    R = np.zeros(MD, dtype=complex)
    tmean = np.zeros(MD, dtype=complex)

    for j in range(MD):
        pos_indices = np.where(proboftminusmeanprob[j, :] >= 0)[0]
        if len(pos_indices) > 0:
            index_j = pos_indices[0]
            index[j] = index_j
        else:
            index[j] = 0

        if index[j] != 0:
            idx = index[j]
            numerator = xsquare[j, idx] - meanprob[j]
            denominator = meanprob[j] - xsquare[j, idx - 1]
            R[j] = numerator / denominator if denominator != 0 else 0
            tmean[j] = (t[idx] + R[j] * t[idx - 1]) / (R[j] + 1) if (R[j] + 1) != 0 else 0
        else:
            R[j] = 0
            tmean[j] = meanprob[j]  # physically irrelevant case

    meantransferrate = np.zeros(MD, dtype=complex)
    nonzero_mask = tmean != 0
    meantransferrate[nonzero_mask] = meanprob[nonzero_mask] / tmean[nonzero_mask]

    print("Mean transfer rate per site:\n", meantransferrate)

    return {
        'idiotimes': idio,
        'pithanotites': meanprob,
        'pinakas': A,
        'mesox': meanxsquares,
        'participation ratio': pr,
        'mean transfer rate': meantransferrate
    }
