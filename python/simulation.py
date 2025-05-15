import numpy as np
from Bio.Seq import Seq
import matplotlib.pyplot as plt
import random

# Determine the matrix to be diagonalized
N = int(input('Number of base-pairs: '))
print('Matrix dimensions =')
MD = 3 * N  # matrix dimension
print(MD)

# HOMO or LUMO?
HL = int(input('HOMO (1) or LUMO (2) calculations: '))
symmetry = int(input('symmetry (1) or asymmetry (2)'))
if HL == 1:
    print('HOMO calculations')
    ES = 9.0
    tS = 0.02
    if symmetry == 1:
        tSp = tS
    else: tSp = 0.16
    EGkC = 8.0
    EAkT = 8.3
    tAA = 0.02
    tTT = tAA
    tAT = -0.035
    tAG = 0.03
    tCT = tAG
    tAC = -0.01
    tGT = tAC
    tTA = -0.05
    tTG = 0.01
    tCA = tTG
    tGA = 0.11
    tTC = tGA
    tGG = 0.1
    tCC = tGG
    tGC = -0.01
    tCG = 0.05

elif HL == 2:
    print('LUMO calculations')
    ES = 0.0
    tS = 0.0
    EGkC = -4.5
    EAkT = -4.9
    tAA = -0.029
    tTT = tAA
    tAT = 0.0005
    tAG = 0.003
    tCT = tAG
    tAC = 0.032
    tGT = tAC
    tTA = 0.002
    tTG = 0.017
    tCA = tTG
    tGA = -0.001
    tTC = tGA
    tGG = 0.020
    tCC = tGG
    tGC = -0.010
    tCG = -0.008

# Constants
h = 4.135667517  # eV·fs (Planck's constant)
hbar = h / (2 * np.pi)  # reduced Planck's constant (eV·fs)
eVperhbar = (2 * np.pi) / h  # 1/fs
bps = 0.34  # base pair spacing in nm

# Initialize the matrix

# Ask user to input DNA sequence as a string
# dna_input = input("Enter the DNA sequence (e.g., ATGC...): ").upper()
# dna_seq = Seq(dna_input)

# print("Your DNA sequence is saved as a Biopython Seq object:")

# print(dna_seq)

# def disordermover(matrixes):
#    if DISORDER==10:
#        while DISORDER>0:
#            matrixes(DISORDER)
#            computations(A)
#            plots()
#            print('2ANTOOOOON')
#            DISORDER-=1
#    else:
#        matrixes()
#        computations()
#        plots()
#    return{results,plots}

# for now it only calculates GGGG...G

DISORDER = int(input('what kind of disorder would you like, 0 for nothing, 1 for EG, 2 for ES, 3 for ES+EG, 4 for ES+ES, 5 for All energies, 6 for tG, 7 for ts, 8 for ts and tg, 9 for ALL, 10 for everything: '))


def matrixes(DISORDER):
    A = np.zeros((MD, MD))

    for k1 in range(MD):
        for k2 in range(k1, MD):
            if k1 == k2:
                if k1 % 3 == 0:
                    if DISORDER in [2, 3, 4, 5, 9]:
                        ESpeiragmeno = ES * (1 - 0.05 * random.random() + 0.025)
                        A[k1, k2] = ESpeiragmeno
                    else:  # handles DISORDER == 0 or 1
                        ESpeiragmeno = ES
                        A[k1, k2] = ESpeiragmeno
                elif k1 % 3 == 1:
                    if DISORDER in[1, 3, 5, 9]:
                        EGkCPeiragmeno = EGkC * (1 - 0.05 * random.random() + 0.025)
                        A[k1, k2] = EGkCPeiragmeno
                    else:
                        EGkCPeiragmeno = EGkC
                        A[k1, k2] = EGkCPeiragmeno
                elif k1 % 3 == 2:
                    if DISORDER in [2, 3, 4, 5, 9]:
                        ESpeiragmeno = ES * (1 - 0.05 * random.random() + 0.025)
                        A[k1, k2] = ESpeiragmeno
                    else:  # handles DISORDER == 0 or 1
                        ESpeiragmeno = ES
                        A[k1, k2] = ESpeiragmeno
            elif k1 % 3 == 1 and k2 % 3 == 1 and abs(k1 - k2) == 3:
                if DISORDER in[6, 8, 9]:
                        tGGPeiragmeno = tGG * (1 - 0.5 * random.random() + 0.25)
                        A[k1, k2] = tGGPeiragmeno
                else:
                        tGGPeiragmeno = tGG
                        A[k1, k2] = tGGPeiragmeno
            elif k1 % 3 == 0 and k2 % 3 == 1 and abs(k1 - k2) == 1:
                if DISORDER in[7, 8, 9]:
                    tSPeiragmeno = tS * (1 - 0.5 * random.random() + 0.25)
                    A[k1, k2] = tSPeiragmeno
                else:
                    tSPeiragmeno = tS
                    A[k1, k2] = tSPeiragmeno
            elif k1 % 3 == 1 and k2 % 3 == 0 and abs(k1 - k2) == 1:
                if DISORDER in[7, 8, 9]:
                    tSPeiragmeno = tS * (1 - 0.5 * random.random() + 0.25)
                    A[k1, k2] = tSPeiragmeno
                else:
                    tSPeiragmeno = tS
                    A[k1, k2] = tSPeiragmeno
            elif k1 % 3 == 2 and k2 % 3 == 1 and abs(k1 - k2) == 1:
                if DISORDER in[7, 8, 9]:
                    tSpPeiragmeno = tSp * (1 - 0.5 * random.random() + 0.25)
                    A[k1, k2] = tSpPeiragmeno
                else:
                    tSpPeiragmeno = tSp
                    A[k1, k2] = tSpPeiragmeno
            elif k1 % 3 == 1 and k2 % 3 == 2 and abs(k1 - k2) == 1:
                if DISORDER in[7, 8, 9]:
                    tSpPeiragmeno = tSp * (1 - 0.5 * random.random() + 0.25)
                    A[k1, k2] = tSpPeiragmeno
                else:
                    tSpPeiragmeno = tSp
                    A[k1, k2] = tSpPeiragmeno
            else:
                A[k1, k2] = 0.0
    for k1 in range(MD):
        for k2 in range(k1):
            A[k1, k2] = A[k2, k1]
    return A


A = matrixes(DISORDER)

# print(A)

# For checking eigenvalues only:
idio = np.linalg.eigvals(A)
# print(idio)

# Time vector setup
L = 64 * 16385  # or L = 100
t = np.linspace(0, 100000, L)  # time in femtoseconds


def computations(A):

    # Compute right eigenvectors (V) and eigenvalues (D)
    D_vals, V = np.linalg.eig(A)

    idx = D_vals.argsort()
    D = np.diag(D_vals[idx])
    V = V[:, idx]

    # Compute left eigenvectors (W): eigenvectors of A transpose
    D_trans_vals, W = np.linalg.eig(A.T)
    W = W[:, idx]
    W = np.conj(W)  # Conjugate as MATLAB does with A.'

    # Compare right and left eigenvectors
    # DLR = V - W

    # Print results
    # print("Eigenvectors (Right):")
    # print(V)

    # print("\nEigenvectors (Left, conjugated):")
    # print(W)

    # print("\nEigenvalue matrix (diagonal):")
    # print(D)

    # print("\nDifference between right and left eigenvectors (V - W):")
    # print(DLR)

    #
    #
    # UP TO HERE, OK
    #
    #
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
    # Assume A, V, D, MD, L, and eVperhbar are already defined

    # Check if A is Hermitian (i.e., A == A†)
    if np.allclose(A.conj().T, A):
        # HMonly
        lambda_vals = np.zeros(MD, dtype=complex)
        for k in range(MD):
            lambda_vals[k] = -1j * eVperhbar * D[k, k]  # Matrix A
        print("λ (lambda):", lambda_vals)

        if np.allclose(lambda_vals.real, np.zeros(MD)):
            print("Sum of periodic functions.")

        print("The sum of periodic functions is NOT generally a periodic function.")

    # Determine initial conditions
    print("\nDetermine Initial Conditions")
    x0 = np.zeros(MD)
    x0[1] = 1  # x0(2) in MATLAB

    x0 = x0.T  # Optional, already 1D

    # Find coefficients c
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

    # Initialize x matrix
    x = np.zeros((MD, L))

    # Time evolution of the state x(t)
    x = np.zeros((MD, len(t)), dtype=complex)

    for k in range(MD):
        x += c[k] * np.outer(V[:, k], np.exp(lambda_vals[k] * t))

    # Compute square norms
    xsquare = x * np.conj(x)

    # Sum over all components at each time point
    summ = np.sum(xsquare, axis=0)

    # In case of failure of linear independence check
    # (already printed earlier): print('SOS linearly dependent')

    # In case matrix A was not Hermitian
    # (already printed earlier): print('A is not Hermitian')

    maxxsquare = np.zeros(MD)
    meanxsquares = np.zeros(MD)
    meanprob = np.zeros(MD)

    for k in range(MD):
        maxxsquare[k] = np.max(xsquare[k,:])
        meanxsquares[k] = np.mean(xsquare[k,:])

        if DegeneracyFLAG == 'F':
            # No energy degeneracy
            meanprob[k] = np.sum((c ** 2) * (V[k,:] ** 2))
        elif DegeneracyFLAG == 'T':
            # With energy degeneracy
            evol = np.sum(c[:, np.newaxis] * V[k,:, np.newaxis] * np.exp(np.outer(lambda_vals, t)), axis=0)
            meanprob[k] = np.mean(evol * np.conj(evol))

    suma = np.sum(meanxsquares)

    print(meanprob)

    # PARTICIPATION RATIO--it works
    B = V.shape[0]  # number of sites
    pr = np.zeros(V.shape[1])  # one PR per eigenvector

    for k in range(V.shape[1]):
        vec = V[:, k]
        pr[k] = 1.0 / (B * np.sum(np.abs(vec) ** 4))

    # Compute the difference from mean probabilities
    # proboftminusmeanprob = xsquare - meanprob[:, np.newaxis]  # broadcasting like MATLAB's bsxfun(@minus,...)
        proboftminusmeanprob = xsquare - meanprob[:, np.newaxis]
        index = np.zeros(MD, dtype=int)
        R = np.zeros(MD)
        tmean = np.zeros(MD)

        for j in range(MD):
            # Find the first index where the probability rises above the mean
            pos_indices = np.where(proboftminusmeanprob[j,:] >= 0)[0]
            if len(pos_indices) > 0:
                index_j = pos_indices[0]
                index[j] = index_j
            else:
                index[j] = 0  # fallback if no index found

            if index[j] != 0:  # if not the initially populated site
                idx = index[j]
                if idx > 0:  # make sure idx-1 is valid
                    numerator = xsquare[j, idx] - meanprob[j]
                    denominator = meanprob[j] - xsquare[j, idx - 1]
                    R[j] = numerator / denominator if denominator != 0 else 0
                    tmean[j] = (t[idx] + R[j] * t[idx - 1]) / (R[j] + 1) if R[j] + 1 != 0 else 0
                else:
                    R[j] = 0
                    tmean[j] = meanprob[j]  # physically irrelevant case
            else:
                R[j] = 0
                tmean[j] = meanprob[j]  # physically irrelevant case

        # Calculate mean transfer rate
        meantransferrate = np.zeros(MD)
        nonzero_mask = tmean != 0
        meantransferrate[nonzero_mask] = meanprob[nonzero_mask] / tmean[nonzero_mask]

        print("Mean transfer rate per site:\n", meantransferrate)

    return{
        'idiotimes': idio,
        'pithanotites': meanprob,
        'pinakas': A,
        'mesox': meanxsquares,
        'participation ratio':pr,
        'mean transfer rate':meantransferrate
        }


results = computations(A)
print('eeeelamoyelaaaaamoy')

print(results)


# def elgrande(DISORDER):
#     if DISORDER in [0,1,2,3,4,5]:
#         matrixes(DISORDER)

#     else:

#     eigenenergies=[]
#     Vmatrixes=[]
#     meanprobabilities=[]
#     meantransferrates=[]
#     participationratios=[]

#     return 0
