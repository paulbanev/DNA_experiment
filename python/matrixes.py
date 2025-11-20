"""Hamiltonian Matrix Construction

This module builds the tight-binding Hamiltonian matrix for DNA transport models.
It handles different model architectures (WIRE, FISHBONE, LADDER) and applies
disorder to onsite energies and hopping integrals based on the disorder model.

The matrix A represents the quantum mechanical Hamiltonian where:
    - Diagonal elements = onsite energies
    - Off-diagonal elements = hopping integrals (couplings)
"""


import numpy as np
import random
def matrixes(Ebp, tbb, disorder_params, sequence, model, mode, seed=None, symmetry='symmetric'):
    """Construct the Hamiltonian matrix for DNA transport model.
    
    Builds the tight-binding Hamiltonian matrix A based on the specified model
    architecture, with optional disorder applied to energies and hopping terms.
    
    Args:
        Ebp (list): Onsite energies (eV) for each base pair in sequence
        tbb (list): Hopping integrals (eV) between adjacent base pairs
        disorder_params (dict): Disorder strengths for various parameters:
            - 'eg_disorder': Base pair energy disorder (typically 0.05)
            - 'es_disorder': Sugar energy disorder (typically 0.05)
            - 'tg_disorder': Base-base hopping disorder (typically 0.5)
            - 'ts_disorder': Sugar-base hopping disorder (typically 0.5)
            - 'tsp_disorder': Asymmetric sugar-base disorder (typically 0.5)
        sequence (str): DNA sequence (used for length)
        model (str): Transport model - 'WIRE', 'FISHBONE', 'LADDER',
                    'EXTENDED_LADDER', or 'SPECIALE'
        mode (str): Electronic mode - 'HOMO' or 'LUMO'
        seed (int, optional): Random seed for disorder reproducibility
        symmetry (str): 'symmetric' (tSp=tS) or 'asymmetric' (tSp=0.16)
    
    Returns:
        tuple: (A, MD) where:
            - A (ndarray): Hamiltonian matrix (MD × MD)
            - MD (int): Matrix dimension (number of sites)
    
    Matrix Structure (FISHBONE model):
        Sites are indexed as: 3k (left sugar), 3k+1 (base), 3k+2 (right sugar)
        for k = 0, 1, ..., N-1 where N = number of base pairs
        
        Diagonal: Onsite energies
        Off-diagonal: Hopping integrals between nearest neighbors
    
    Raises:
        ValueError: If model is not recognized or mode is invalid
    
    Notes:
        - Matrix is symmetrized to ensure Hermiticity
        - Disorder is applied as multiplicative Gaussian noise: E_new = E * (1 + δ*N(0,1))
        - LADDER and SPECIALE models are not yet fully implemented
    """
    # ===== WIRE and FISHBONE Models (Implemented) =====
    if model in("FISHBONE", "WIRE"): 
        # Set random seed for reproducibility
        if seed is not None:
            random.seed(seed)
        
        length = len(sequence)
        MD = 3 * length  # 3 sites per base pair in FISHBONE
        A = np.zeros((MD, MD), dtype=np.float64)  # Initialize Hamiltonian matrix

        # ===== Model-specific parameters =====
        # HOMO or LUMO setup
        if mode == "HOMO":
            ES = 9.0  # Sugar onsite energy (eV)
            tS = 0.02 if model == "FISHBONE" else 0.0  # Sugar-base hopping (eV)
            if model =="FISHBONE":
                tSp = tS if symmetry == 'symmetric' else 0.16  # Opposite strand coupling
            else: 
                tSp=0.0
        elif mode == "LUMO":
            ES = 0.0  # LUMO has no sugar contribution
            tS = 0.0  # No sugar-base hopping in LUMO
            tSp = tS if symmetry == 'symmetric' else 0.0
        else:
            raise ValueError("Mode must be 'HOMO' or 'LUMO'")

        # ===== Populate Hamiltonian matrix with disorder =====
        # Matrix population
        # Indexing: Site i = 3k + σ where k = base pair index, σ ∈ {0,1,2}
        # σ=0: left sugar, σ=1: base pair, σ=2: right sugar 
        for k1 in range(MD):
            for k2 in range(k1, MD):  # Upper triangular only (will symmetrize later)
                # ===== Diagonal elements (onsite energies) =====
                if k1 == k2:
                    if k1 % 3 == 0 or k1 % 3 == 2:  # Sugar sites
                        A[k1, k2] = ES * (1 + disorder_params.get("es_disorder", 0) * random.gauss(0, 1))
                    elif k1 % 3 == 1:  # Base pair sites
                        A[k1, k2] = Ebp[k1//3] * (1 + disorder_params.get("eg_disorder", 0) * random.gauss(0, 1))
                
                # ===== Base-to-base hopping (along sequence) =====
                elif k1 % 3 == 1 and k2 % 3 == 1 and abs(k1 - k2) == 3:
                    # Hopping between adjacent bases (tbb with disorder)
                    if (k1 // 3) < len(tbb):
                        tbb_dis = tbb[k1 // 3] * (1 + disorder_params.get("tg_disorder", 0) * random.gauss(0, 1))
                    A[k1, k2] = tbb_dis
                
                # ===== Sugar-base couplings (nearest neighbor) =====
                elif abs(k1 - k2) == 1:
                    if {k1 % 3, k2 % 3} == {0, 1}:  # Left sugar to base
                        tS_dis = tS * (1 + disorder_params.get("ts_disorder", 0) * random.gauss(0, 1))
                        A[k1, k2] = tS_dis
                    elif {k1 % 3, k2 % 3} == {1, 2}:  # Base to right sugar
                        tSp_dis = tSp * (1 + disorder_params.get("tsp_disorder", 0) * random.gauss(0, 1))
                        A[k1, k2] = tSp_dis
                    else:
                        A[k1, k2] = 0.0
                else:
                    A[k1, k2] = 0.0  # All other elements are zero

        # ===== Symmetrize matrix to ensure Hermiticity =====
        # Copy upper triangle to lower triangle (A = A^T)
        for k1 in range(MD):
            for k2 in range(k1):
                A[k1, k2] = A[k2, k1]
    
    # ===== LADDER and EXTENDED_LADDER Models (Not Implemented) =====
    elif model in ("LADDER", "EXTENDED_LADDER"):
        # TODO: Implement LADDER model
        # - 2 sites per base pair (one per strand)
        # - Intrastrand hopping
        # - Interstrand (cross-base) hopping
        # - Optional: diagonal hopping for EXTENDED_LADDER
        vaggelis=5  # <-- Placeholder, delete this
        # Remember to nullify diagonal hopping in case of simple ladder!!!
    
    # ===== SPECIALE Model (Not Implemented) =====
    elif model == "SPECIALE":
        # TODO: Implement SPECIALE model
        # - Modified code for polymer discussed with Simse
        apapa=2  # <-- Placeholder, delete this
    
    else:
        raise ValueError(f"Invalid model: {model}. Choose from WIRE, FISHBONE, LADDER, EXTENDED_LADDER, SPECIALE")
    
    # Debug output (TODO: Remove in production)
    print("Hamiltonian matrix constructed successfully")
    print(A)
    return A, MD
