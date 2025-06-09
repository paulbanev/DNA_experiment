#analysis
import numpy as np

def computations(NN, A, MD, eVperhbar, t, L, h):
    # For checking eigenvalues only:
    idio = np.linalg.eigvals(A)
    # We sort them to be in accordace toprevious matlab results. just a formalisation
    idx = idio.argsort()
    idio_sorted = idio[idx]

    
    # Compute right eigenvectors (V) and eigenvalues (D)
    D_vals, V = np.linalg.eig(A)

    #normalize the eigenvectors before sorting. matlab does it automatically with eig(A)
    V = V / np.linalg.norm(V, axis=0, keepdims=True)

    idx = D_vals.argsort()
    D = np.diag(D_vals[idx])
    V = V[:, idx]

    print("\nEigenvector matrix V (columns are eigenvectors):")
    np.set_printoptions(precision=4, suppress=True)  # Optional: for readability
    print(V)

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

            # start of Density of States (DOS) calculation
    DOSFLAG = 'T'
    if DOSFLAG == 'T':

        thesi = np.zeros(NN)

        if idio[0] < 0:
            thesi[0] = 1.01 * idio[0]
            thesi[-1] = 0.99 * idio[MD-1]
            step = (thesi[-1] - thesi[0]) / (NN - 1)
        elif idio[0] > 0:
            thesi[0] = 0.99 * idio[0]
            thesi[-1] = 1.01 * idio[MD-1]
            step = (thesi[-1] - thesi[0]) / (NN - 1)

        for j in range(NN):
            thesi[j] = thesi[0] + j * step

        count = np.zeros(NN-1)

        for i in range(MD):
            for j in range(NN-1):
                if (idio[i] > thesi[j]) and (idio[i] <= thesi[j+1]):
                    count[j] += 1

        count = count / (MD * step)

        mesithesi = np.zeros(NN-1)
        if np.min(idio) > 0:
            for j in range(NN-1):
                mesithesi[j] = -(thesi[j+1] + thesi[j]) / 2
        elif np.min(idio) < 0:
            for j in range(NN-1):
                mesithesi[j] = (thesi[j+1] + thesi[j]) / 2

    # Compute square norms and sums
    xsquare = np.abs(x)**2
    summ = np.sum(xsquare, axis=0)

    maxxsquare = np.max(xsquare, axis=1)
    meanxsquares = np.mean(xsquare, axis=1)
    
    
    meanprob = np.zeros(MD, dtype=np.float64)

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
    pr = 1.0 / (B * np.sum(np.abs(V) ** 4, axis=0))

    # Compute difference from mean probabilities
    proboftminusmeanprob = xsquare - meanprob[:, np.newaxis]
    index = np.zeros(MD, dtype=int)
    
    # Initialize these as complex to avoid casting warnings
    R = np.zeros(MD, dtype=np.float64)
    tmean = np.zeros(MD, dtype=np.float64)

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

    meantransferrate = np.zeros(MD, dtype=np.float64)
    nonzero_mask = tmean != 0
    meantransferrate[nonzero_mask] = meanprob[nonzero_mask] / tmean[nonzero_mask]

    print("Mean transfer rate per site:\n", meantransferrate)


    #DIPOLE MOMENT CALCULATIONS
    a0 = 0.52917721067  # Bohr radius in Å
    factor_x = 3.4 / a0
    factor_y = 10 / a0

    if (MD // 3) % 2 == 0:
        xcenter = (MD // 3) // 2 + 0.5
    else:
        xcenter = (MD // 3) // 2 + 1
    ycenter = 2

    dmx = np.zeros_like(t)
    dmy = np.zeros_like(t)

    for beta in range(1, MD + 1):
        sigma = beta % 3 or 3
        nu = 1 + (beta - sigma) // 3
        idx = beta - 1

        dmx += (nu - xcenter) * factor_x * xsquare[idx, :]
        dmy += (sigma - ycenter) * factor_y * xsquare[idx, :]
    #dipole momens calculated

      #let's calculate the dipole moment fast fourier transform--dmFFT
    L = len(t)
    dmFs = (L - 1) / t[-1]  # Sampling frequency (inverse of dt)
    dmNFFT = 2 ** int(np.ceil(np.log2(L)))  # Next power of 2 from L

    dmYY1 = np.fft.fft(dmx, dmNFFT) / L  # FFT of the dipole moment x-component
    dmf1 = dmFs / 2 * np.linspace(0, 1, dmNFFT // 2 + 1)  # Frequency vector

   
    dmYY2 = np.fft.fft(dmy, dmNFFT) / L  # FFT of the dipole moment y-component
    dmf2 = dmFs / 2 * np.linspace(0, 1, dmNFFT // 2 + 1)  # Frequency vector

    
    num_pairs = MD * (MD - 1) // 2
    freqs = np.zeros(num_pairs)
    FC = np.zeros((MD, num_pairs), dtype=complex)
    
    # Step 1: Build frequency array and FC matrix
    l = 0
    for i in range(MD):
        for j in range(i + 1, MD):
            freqs[l] = (D[j, j] - D[i, i]) / h
            FC[:, l] = c[i] * V[:, i] * c[j] * V[:, j]
            l += 1

    # Step 2: Round to eliminate degeneracy issues (to ~1e-12 precision)
    rounded_freqs = np.round(freqs * 1e12) / 1e12
    uniquefreqs, unique_indices = np.unique(rounded_freqs, return_index=True)
    rest_indices = np.setdiff1d(np.arange(len(freqs)), unique_indices)

    # Step 3: Aggregate degenerate frequency amplitudes
    for i in unique_indices:
        for j in rest_indices:
            if np.isclose(rounded_freqs[i], rounded_freqs[j]):
                FC[:, i] += FC[:, j]

    # Step 4: Extract unique FCs and convert frequency units to THz
    unique_FC = FC[:, unique_indices]
    uniquefreqs *= 1000  # to THz
    FCamp = 2 * np.abs(unique_FC)

    # Step 5: Total Weighted Mean Frequency
    FCamp[:, 0] = 0  # Clear DC component
    WMF = np.zeros(MD)
    TWMF = 0.0
    for i in range(MD):
        if np.sum(FCamp[i, :]) != 0:
            WMF[i] = np.sum(uniquefreqs * FCamp[i, :]) / np.sum(FCamp[i, :])
        TWMF += WMF[i] * meanprob[i]
    TWMF_per_MD = TWMF / MD

   
    

    return {
        'idiotimes': idio_sorted,
        'pithanotites': meanprob.real,
        'pinakas': A,
        'mesox': meanxsquares,
        'participation ratio': pr,
        'mean transfer rate': meantransferrate.real,
        'eigenvector matrix': V,
        'x axis dipole moment': dmx,
        'y axis dipole moment': dmy,
        'total weighted mean frequency': TWMF,
        'count': count,
        'mesi thesi': mesithesi   
    }

