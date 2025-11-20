"""Quantum Transport Analysis and Computations

This module performs the core quantum mechanical calculations for DNA transport
simulations. It solves the time-dependent Schrödinger equation for charge transport
and computes various transport metrics.

Key Computations:
    - Eigenvalue/eigenvector decomposition of Hamiltonian
    - Time evolution of quantum states
    - Participation ratio (delocalization measure)
    - Transfer rates and mean probabilities
    - Density of States (DOS)
    - Dipole moments and frequency analysis
    - Weighted mean frequencies

The module implements tight-binding quantum mechanics with coherent transport
(no dissipation or decoherence).
"""

import numpy as np

def computations(NN, A, MD, eVperhbar, t, L, h, dos_flag=True,
                 analytical_flag=True, fft_flag=True, 
                 dipole_fft_flag=True, fourier_flag=True):
    """Perform all quantum transport computations for the DNA system.
    
    This function is the computational heart of the simulation. It:
    1. Solves the Hamiltonian to get energy levels and eigenstates
    2. Propagates the initial state in time quantum mechanically
    3. Computes observables (probabilities, transfer rates, etc.)
    4. Analyzes the density of states (if enabled)
    5. Calculates dipole moments and frequency spectrum
    
    Args:
        NN (int): Number of bins for Density of States histogram
        A (ndarray): Hamiltonian matrix (MD × MD) representing the quantum system.
                     Diagonal: onsite energies, Off-diagonal: hopping integrals
        MD (int): Matrix dimension = number of sites in the system
                  (e.g., for FISHBONE: MD = 3 × number_of_base_pairs)
        eVperhbar (float): Conversion factor 2π/h in fs⁻¹, converts energy to
                          frequency for time evolution
        t (ndarray): Time array for quantum evolution (in femtoseconds)
                     Typically ~1 million time points from 0 to 100,000 fs
        L (int): Length of time array (number of time points)
        h (float): Planck constant in eV·fs (4.135667517)
        dos_flag (bool): Enable DOS calculation (default: True)
        analytical_flag (bool): Enable analytical calculations (default: True)
        fft_flag (bool): Enable FFT analysis (default: True)
        dipole_fft_flag (bool): Enable dipole FFT analysis (default: True)
        fourier_flag (bool): Enable Fourier analysis (default: True)
    
    Returns:
        dict: Dictionary containing all computed metrics:
            'idiotimes' (ndarray): Sorted eigenvalues (energy levels) in eV
            'pithanotites' (ndarray): Time-averaged probability at each site
            'pinakas' (ndarray): Copy of input Hamiltonian matrix A
            'mesox' (ndarray): Mean of squared wavefunction |ψ(t)|² over time
            'participation ratio' (ndarray): Delocalization measure for each eigenstate
                PR ≈ 1: localized, PR ≈ N: delocalized
            'mean transfer rate' (ndarray): Transfer rate to each site (prob/time)
            'eigenvector matrix' (ndarray): Matrix V where columns are eigenvectors
            'x axis dipole moment' (ndarray): Dipole moment along sequence vs time
            'y axis dipole moment' (ndarray): Dipole moment across strands vs time
            'total weighted mean frequency' (float): Overall characteristic frequency
            'weighted mean frequency' (ndarray): Frequency per site in THz
            'PWMF' (ndarray): Probability-weighted mean frequency per site
            'mesi thesi' (ndarray): Energy bin centers for DOS
            'count' (ndarray): Normalized DOS (states per eV)
    
    Physics:
        The time evolution follows: |ψ(t)⟩ = Σₖ cₖ |vₖ⟩ exp(-iλₖt)
        where |vₖ⟩ are eigenvectors, λₖ = -i(2π/h)Eₖ, and cₖ are coefficients
        determined by initial condition |ψ(0)⟩ = |site 1⟩ (first base pair)
    
    Notes:
        - Handles both degenerate and non-degenerate eigenvalue cases
        - Performs degeneracy detection with threshold 10⁻¹²
        - Uses multiple methods to verify numerical stability
        - FFT analysis extracts characteristic oscillation frequencies
    """
    # ===== Stage 1: Solve Hamiltonian for Energy Levels =====
    # Calculate eigenvalues only (for reference)
    idio = np.linalg.eigvals(A)
    # Sort eigenvalues to ensure consistent ordering with previous MATLAB results
    idx = idio.argsort()
    idio_sorted = idio[idx]

    # ===== Stage 2: Full Eigenvalue/Eigenvector Decomposition =====
    # Compute both eigenvalues (D_vals) and right eigenvectors (V)
    # V[:,k] is the kth eigenvector corresponding to eigenvalue D_vals[k]
    D_vals, V = np.linalg.eig(A)

    # Normalize eigenvectors (MATLAB does this automatically)
    # Each column of V is normalized to unit length: ||V[:,k]|| = 1
    V = V / np.linalg.norm(V, axis=0, keepdims=True)

    # Sort eigenvectors and eigenvalues by increasing energy
    idx = D_vals.argsort()
    D = np.diag(D_vals[idx])  # Diagonal matrix of sorted eigenvalues
    V = V[:, idx]  # Sorted eigenvector matrix

    print("\nEigenvector matrix V (columns are eigenvectors):")
    np.set_printoptions(precision=4, suppress=True)  # Readable output
    print(V)

    # ===== Stage 3: Left Eigenvectors (for non-Hermitian case) =====
    # Compute left eigenvectors from transpose: eigenvectors of A^T
    # For Hermitian matrices, left = conjugate of right
    D_trans_vals, W = np.linalg.eig(A.T)
    W = W[:, idx]  # Sort to match V
    W = np.conj(W)  # Conjugate for consistency with A^† (Hermitian adjoint)

    # ===== Stage 4: Degeneracy Detection =====
    # Detect degenerate energy levels (identical eigenvalues within tolerance)
    # Degeneracy threshold: |E_i - E_j| < 10^-12 eV

    degenerate = np.zeros(MD, dtype=int)  # Flag array for degenerate states
    DegeneracyFLAG = 'F'  # Global degeneracy flag (F=false, T=true)

    # Check all pairs of eigenvalues for degeneracy
    for k in range(MD):
        for j in range(k + 1, MD):
            if np.abs(idio_sorted[k] - idio_sorted[j]) <= 1.0e-12:
                DegeneracyFLAG = 'T'
                print(f"Degeneracy detected between indices k={k}, j={j}")
                degenerate[k] = 1
                degenerate[j] = 1

    print("DegeneracyFLAG =", DegeneracyFLAG)

    # ===== Stage 5: Time Evolution Parameters =====
    # Check if Hamiltonian is Hermitian (A = A†)
    # For real symmetric matrices: A = A^T
    if np.allclose(A.conj().T, A):
        # Compute time evolution frequencies: λ_k = -i*(2π/h)*E_k
        # These appear in exp(λ_k*t) = exp(-i*ω_k*t) where ω_k = (2π/h)*E_k
        lambda_vals = np.zeros(MD, dtype=complex)
        for k in range(MD):
            lambda_vals[k] = -1j * eVperhbar * D[k, k]  # Complex frequency
        print("lambda:", lambda_vals)

        # Check if system is purely real (all λ are imaginary)
        if np.allclose(lambda_vals.real, np.zeros(MD)):
            print("Sum of periodic functions.")
        else:
            print("The sum of periodic functions is NOT generally a periodic function.")

    # ===== Stage 6: Initial Conditions =====
    # Set initial state: charge placed at first base pair (site index 1)
    # |ψ(0)⟩ = |1⟩ in site basis
    print("\nDetermine Initial Conditions")
    x0 = np.zeros(MD)
    x0[1] = 1  # Initial state at first base pair (FISHBONE: this is the base site)

    # ===== Stage 7: Expansion Coefficients =====
    # Find coefficients c such that |ψ(0)⟩ = Σ_k c_k |v_k⟩
    # Solution: c = V^-1 · x0
    # Use three methods to verify numerical stability:
    # Method 1: Linear solver (most stable)
    ca = np.linalg.solve(V, x0)
    # Method 2: Least squares (handles rank-deficient matrices)
    cb = np.linalg.lstsq(V, x0, rcond=None)[0]
    # Method 3: Direct inversion (least stable, but reference)
    cc = np.dot(np.linalg.inv(V), x0)

    # Compare results and choose most reliable
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
        c = cb  # Default to least squares
        print("3 different results for c")

    # ===== Stage 8: Linear Independence Check =====
    # Verify eigenvectors are linearly independent
    # If V is invertible, then V*M = 0 implies M = 0
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

    if np.allclose(M, Z):  # M should be zero vector if linearly independent
        print("OK linearly independent")

    # ===== Stage 9: Time Evolution of Quantum State =====
    # Propagate initial state in time: |ψ(t)⟩ = Σ_k c_k |v_k⟩ exp(λ_k*t)
    # x[i,t] = ψ_i(t) is the amplitude at site i at time t
    
    # OPTIMIZED: Vectorized computation (10-100x faster than loop)
    # Instead of: x += c[k] * np.outer(V[:, k], np.exp(lambda_vals[k] * t)) for each k
    # We compute all k simultaneously using broadcasting and matrix multiplication
    
    # Step 1: Compute time evolution factors for all eigenstates at once
    # Shape: (MD, L) where each row k is exp(λ_k * t) evaluated at all time points
    exp_terms = np.exp(np.outer(lambda_vals, t))  # (MD, L) matrix
    
    # Step 2: Weight by coefficients and combine with eigenvectors in one operation
    # V @ (c[:, np.newaxis] * exp_terms) performs:
    #   - c[:, np.newaxis] * exp_terms broadcasts c to (MD, L)
    #   - V @ (...) does matrix-vector product for each time point
    # Result: x[i, t_j] = Σ_k c_k * V[i, k] * exp(λ_k * t_j)
    x = V @ (c[:, np.newaxis] * exp_terms)  # (MD, MD) @ (MD, L) = (MD, L)

    # ===== Stage 10: Density of States (DOS) Calculation =====
    # DOS shows the distribution of energy levels
    # User can disable this via --disable-dos flag to save computation time
    if dos_flag:

        # ===== OPTIMIZED DOS Calculation using NumPy =====
        # Use NumPy's built-in histogram for 100-1000x speedup over nested loops
        
        # Determine energy range for bins
        e_min = idio_sorted[0]
        e_max = idio_sorted[-1]
        
        # Extend range by 1% to ensure all eigenvalues are captured
        if e_min < 0:
            e_min = 1.01 * e_min  # Extend downward for negative
            e_max = 0.99 * e_max if e_max < 0 else 1.01 * e_max
        elif e_min > 0:
            e_min = 0.99 * e_min  # Shrink upward for positive
            e_max = 1.01 * e_max
        else:  # e_min == 0
            e_min = 1.01 * e_min if e_min < 0 else 0.99 * e_min
            e_max = 1.01 * e_max
        
        # Use NumPy's histogram - much faster than nested loops!
        # histogram returns (counts, bin_edges) where bin_edges has length NN
        count_raw, bin_edges = np.histogram(idio_sorted, bins=NN, range=(e_min, e_max))
        
        # Normalize DOS: divide by (total states × bin width) to get states per eV
        bin_width = (e_max - e_min) / NN
        count = count_raw / (MD * bin_width)
        
        # Calculate bin centers (midpoints) - vectorized!
        mesithesi = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Handle legacy sign convention for positive eigenvalues
        if np.min(idio_sorted) > 0:
            mesithesi = -mesithesi  # Negate (legacy code compatibility)

        # Print diagnostic information
        print(f"DOS arrays: mesithesi size = {mesithesi.shape}, count size = {count.shape}")
        print(f"Energy range: {e_min:.6f} to {e_max:.6f} eV")
        print(f"Eigenvalue range: {idio_sorted[0]:.6f} to {idio_sorted[-1]:.6f} eV")

    else:
        # DOS disabled - create empty arrays to maintain consistent return structure
        mesithesi = np.zeros(NN-1)
        count = np.zeros(NN-1)

        
    # Compute square norms and sums
    xsquare = np.abs(x)**2
    summ = np.sum(xsquare, axis=0)

    maxxsquare = np.max(xsquare, axis=1)
    meanxsquares = np.mean(xsquare, axis=1)
    
    # ===== Analytical Calculations (controlled by --disable-analytical flag) =====
    if analytical_flag:
        # Calculate mean probabilities
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
        proboftminusmeanprob = xsquare - meanprob[:, np.newaxis]  # P(i,t) - ⟨P(i)⟩
        index = np.zeros(MD, dtype=int)  # Index of arrival time
        
        # Initialize arrays for transfer rate computation
        R = np.zeros(MD, dtype=np.float64)  # Interpolation ratio
        tmean = np.zeros(MD, dtype=np.float64)  # Mean arrival time

        # ===== Find arrival time for each site =====
        # Arrival time = first time when P(i,t) crosses ⟨P(i)⟩ from below

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
    else:
        # Analytical calculations disabled - create empty arrays
        meanprob = np.zeros(MD, dtype=np.float64)
        pr = np.zeros(MD)
        meantransferrate = np.zeros(MD, dtype=np.float64)



    # ===== Stage 15: Dipole Moment Calculations (controlled by --disable-dipole-fft flag) =====
    if dipole_fft_flag:
        # Compute electric dipole moment: d = Σᵢ rᵢ × P(i,t)
        # where rᵢ is position of site i and P(i,t) is probability
        
        # Physical constants for unit conversion
        a0 = 0.52917721067  # Bohr radius in Angstroms
        factor_x = 3.4 / a0  # Convert x-direction (base stacking, 3.4 Å) to Bohr radii
        factor_y = 10 / a0   # Convert y-direction (cross-strand, 10 Å) to Bohr radii

        # ===== Determine center of mass (origin for dipole) =====
        # For FISHBONE: base pairs numbered 1, 2, ..., N
        if (MD // 3) % 2 == 0:  # Even number of base pairs
            xcenter = (MD // 3) // 2 + 0.5  # Center between middle two bases
        else:  # Odd number of base pairs
            xcenter = (MD // 3) // 2 + 1  # Middle base
        ycenter = 2  # Center strand (assuming 3 sites: 0, 1, 2 per base pair)

        # Initialize dipole moment arrays
        dmx = np.zeros_like(t)  # x-component (along sequence)
        dmy = np.zeros_like(t)  # y-component (across strands)

        # ===== Compute dipole moments from probability distribution =====
        # Loop over all sites in FISHBONE model

        for beta in range(1, MD + 1):  # Sites numbered 1 to MD (1-indexed)
            sigma = beta % 3 or 3  # Strand index: 1, 2, or 3
            nu = 1 + (beta - sigma) // 3  # Base pair index: 1, 2, ..., N
            idx = beta - 1  # Convert to 0-indexed for Python arrays

            # Accumulate weighted probability for x and y dipole components
            dmx += (nu - xcenter) * factor_x * xsquare[idx, :]  # x: along sequence
            dmy += (sigma - ycenter) * factor_y * xsquare[idx, :]  # y: across strands
        
        # Dipole moments computed (in units of Bohr radii)

        # ===== Stage 16: FFT Analysis of Dipole Moments =====
        # Analyze frequency content of dipole oscillations
        # FFT reveals characteristic oscillation frequencies of charge
        
        L_fft = len(t)  # Number of time points
        dmFs = (L_fft - 1) / t[-1]  # Sampling frequency in fs^-1
        dmNFFT = 2 ** int(np.ceil(np.log2(L_fft)))  # Next power of 2 (for efficient FFT)

        # FFT of x-component dipole moment
        dmYY1 = np.fft.fft(dmx, dmNFFT) / L_fft  # Normalize by L
        dmf1 = dmFs / 2 * np.linspace(0, 1, dmNFFT // 2 + 1)  # Frequency vector (0 to Nyquist)


        # FFT of y-component dipole moment
        dmYY2 = np.fft.fft(dmy, dmNFFT) / L_fft
        dmf2 = dmFs / 2 * np.linspace(0, 1, dmNFFT // 2 + 1)
    else:
        # Dipole moment calculations disabled - create empty arrays
        dmx = np.zeros_like(t)
        dmy = np.zeros_like(t)
    
    # ===== Stage 17: Transition Frequencies and Franck-Condon Factors =====
    # Compute frequencies from energy differences: f_ij = (E_j - E_i) / h
    # Franck-Condon factors: FC_ij = c_i * V_i * c_j * V_j
    # ===== Build frequency and Franck-Condon arrays =====
    num_pairs = MD * (MD - 1) // 2  # Number of unique state pairs
    freqs = np.zeros(num_pairs)  # Transition frequencies
    FC = np.zeros((MD, num_pairs), dtype=complex)  # Franck-Condon factors
    
    # Step 1: Build frequency array and FC matrix
    # Loop over all pairs of states (i, j) with i < j
    l = 0  # Pair index
    for i in range(MD):
        for j in range(i + 1, MD):
            # Transition frequency between states i and j
            freqs[l] = (D[j, j] - D[i, i]) / h  # Convert energy difference to frequency
            # Franck-Condon amplitude (transition probability amplitude)
            FC[:, l] = c[i] * V[:, i] * c[j] * V[:, j]
            l += 1

    # Step 2: Handle degeneracy by rounding frequencies
    # Round to eliminate degeneracy issues (to ~10^-12 precision)
    rounded_freqs = np.round(freqs * 1e12) / 1e12
    uniquefreqs, unique_indices = np.unique(rounded_freqs, return_index=True)
    rest_indices = np.setdiff1d(np.arange(len(freqs)), unique_indices)

    # Step 3: Aggregate degenerate frequency amplitudes
    # If multiple transitions have same frequency, sum their FC factors
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
    PWMF=np.zeros(V.shape[1])
    TWMF = 0.0
    for i in range(MD):
        if np.sum(FCamp[i, :]) != 0:
            WMF[i] = np.sum(uniquefreqs * FCamp[i, :]) / np.sum(FCamp[i, :])
        PWMF[i]= WMF[i]*meanprob[i]
        TWMF += PWMF[i]
        
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
        'weighted mean frequency': WMF,
        'PWMF': PWMF,
        'mesi thesi': mesithesi,
        'count': count   
    }

