# Physics and Mathematical Formulation

This document explains the quantum mechanical framework and physical models used in the DNA transport simulation.

## Table of Contents
1. [Tight-Binding Hamiltonian](#tight-binding-hamiltonian)
2. [Transport Models](#transport-models)
3. [Energy Parameters](#energy-parameters)
4. [Time Evolution](#time-evolution)
5. [Computed Metrics](#computed-metrics)
6. [Disorder Models](#disorder-models)

## Tight-Binding Hamiltonian

### Overview

The tight-binding model treats charge transport in DNA as a quantum mechanical problem where an electron (LUMO) or hole (HOMO) hops between discrete sites representing nucleotide bases.

### General Hamiltonian

The system is described by a Hamiltonian matrix **A**:

```
H = Σᵢ Eᵢ |i⟩⟨i| + Σᵢⱼ tᵢⱼ |i⟩⟨j|
```

Where:
- **Eᵢ** = onsite energy at site i (base pair or sugar)
- **tᵢⱼ** = hopping integral (coupling) between sites i and j
- **|i⟩** = quantum state localized at site i

### Matrix Structure

The Hamiltonian matrix **A** is:
- **Hermitian** (A = A†) for physical validity
- **Sparse** (only diagonal and nearest-neighbor terms)
- **Size:** Depends on model architecture

## Transport Models

### 1. WIRE Model

**Structure:** 1D chain of base pairs only

**Sites:** N sites (one per base pair)

**Matrix Size:** N × N

**Hamiltonian Elements:**
```
A[i,i] = Ebp[i]           (onsite energies)
A[i,i+1] = tbb[i]         (base-to-base hopping)
```

**Use Case:** Simplest model ignoring sugar backbones

### 2. FISHBONE Model (Implemented)

**Structure:** Double helix with sugar backbones

**Sites per base pair:** 3
- Site 0: Sugar on one strand (S)
- Site 1: Base pair (bp)
- Site 2: Sugar on complementary strand (S')

**Total Sites:** MD = 3N (for N base pairs)

**Matrix Size:** 3N × 3N

**Indexing Scheme:**
```
Site index = 3k + σ
where:
  k = base pair number (0 to N-1)
  σ = 0 (left sugar), 1 (base pair), 2 (right sugar)
```

**Hamiltonian Elements:**

*Diagonal (onsite energies):*
```
A[3k, 3k] = ES           (left sugar)
A[3k+1, 3k+1] = Ebp[k]  (base pair)
A[3k+2, 3k+2] = ES       (right sugar)
```

*Off-diagonal (hopping):*
```
A[3k, 3k+1] = tS         (sugar-to-base, left)
A[3k+1, 3k+2] = tSp      (base-to-sugar, right)
A[3k+1, 3k+4] = tbb[k]   (base-to-base along strand)
```

**Symmetry Parameter:**
- **Symmetric:** tSp = tS (symmetric coupling)
- **Asymmetric:** tSp = 0.16 (strand asymmetry)

**Physical Parameters (HOMO):**
- ES = 9.0 eV (sugar onsite energy)
- tS = 0.02 eV (sugar-base coupling)
- Ebp and tbb from sequence

**Physical Parameters (LUMO):**
- ES = 0.0 eV
- tS = 0.0 eV (no sugar coupling in LUMO)

### 3. LADDER Model (Not Yet Implemented)

**Structure:** Two parallel strands with base pairing

**Sites:** 2N (two sites per base pair level)

**Features:**
- Intrastrand hopping (along each strand)
- Interstrand hopping (across base pairs)
- Optional diagonal hopping

### 4. EXTENDED_LADDER Model (Not Yet Implemented)

**Structure:** LADDER with diagonal couplings

**Additional Terms:**
- Diagonal hopping between non-adjacent sites
- Long-range interactions

### 5. SPECIALE Model (Not Yet Implemented)

**Structure:** Custom polymer model for specialized research

## Energy Parameters

All values in electronvolts (eV).

### HOMO (Hole Transport)

**Onsite Energies (Base Pairs):**
| Base | Energy (eV) | Source |
|------|-------------|--------|
| A (Adenine) | 8.49 / 8.3* | MLS data |
| T (Thymine) | 8.49 / 8.3* | MLS data |
| G (Guanine) | 8.3 / 8.0* | MLS data |
| C (Cytosine) | 8.3 / 8.0* | MLS data |
| M (A-C mismatch) | 8.43 | Estimated |

*First value for FISHBONE/WIRE, second for LADDER models

**Hopping Integrals (5'→3' direction):**
| Pair | tbb (eV) | Notes |
|------|----------|-------|
| AA, TT | 0.038 / 0.02* | Purine-purine |
| AT | -0.005 / -0.035* | Anti-parallel |
| TA | -0.037 / -0.05* | Weak coupling |
| AG, CT | 0.037 / 0.03* | Mixed |
| GA, TC | 0.142 / 0.11* | Strong coupling |
| AC, TG | -0.016 / -0.01* | Weak |
| CA, GT | 0.028 / 0.01* | Moderate |
| GG, CC | 0.116 / 0.1* | Strong |
| GC | -0.01 | Weak |
| CG | 0.075 / 0.05* | Moderate |

*First value for FISHBONE/WIRE, second for LADDER

### LUMO (Electron Transport)

**Onsite Energies:**
| Base | Energy (eV) |
|------|-------------|
| A | -4.9 |
| T | -4.9 |
| G | 0.0 |
| C | -4.5 |

**Hopping Integrals:**
| Pair | tbb (eV) |
|------|----------|
| AA, TT | -0.029 |
| AT | 0.0005 |
| TA | 0.002 |
| AG, CT | 0.003 |
| GA, TC | -0.001 |
| AC, TG | 0.032 |
| CA, GT | 0.017 |
| GG, CC | 0.020 |
| GC | -0.010 |
| CG | -0.008 |

## Time Evolution

### Quantum Dynamics

The time-dependent state vector evolves as:

```
|ψ(t)⟩ = Σₖ cₖ |vₖ⟩ exp(-iλₖt)
```

Where:
- **|vₖ⟩** = kth eigenvector of H (eigenstate)
- **λₖ** = -i(2π/h)Eₖ (complex frequency)
- **Eₖ** = kth eigenvalue (energy)
- **cₖ** = expansion coefficient
- **h** = 4.135667517 eV·fs (Planck constant)

### Initial Condition

Charge placed at first base pair:
```
|ψ(0)⟩ = |site 1⟩
```

Expansion coefficients found from:
```
c = V⁻¹ · x₀
```
where V is the eigenvector matrix.

### Probability Density

Probability of finding charge at site i at time t:
```
P(i,t) = |⟨i|ψ(t)⟩|² = |Σₖ cₖ vₖᵢ exp(-iλₖt)|²
```

## Computed Metrics

### 1. Eigenvalue Spectrum

**Definition:** Energy levels Eₖ of the system

**Physical Meaning:** Allowed energies for charge states

**Computed:** `np.linalg.eigvals(A)`

**Output:** Sorted eigenvalues (idiotimes)

### 2. Participation Ratio (PR)

**Definition:**
```
PR[k] = 1 / (N · Σᵢ |vₖᵢ|⁴)
```

**Physical Meaning:**
- PR ≈ 1: State localized on one site
- PR ≈ N: State delocalized over all N sites

**Interpretation:** Measures quantum delocalization/localization

### 3. Mean Probability

**Definition:**
```
⟨P(i)⟩ = (1/T) ∫₀ᵀ |ψᵢ(t)|² dt
```

**Physical Meaning:** Time-averaged charge density at site i

**For non-degenerate states:**
```
⟨P(i)⟩ = Σₖ |cₖ|² |vₖᵢ|²
```

**Normalization:** Σᵢ⟨P(i)⟩ = 1

### 4. Transfer Rate

**Definition:**
```
Rate(i) = ⟨P(i)⟩ / t_arrival(i)
```

Where t_arrival is when P(i,t) first exceeds ⟨P(i)⟩.

**Physical Meaning:** How quickly charge reaches site i

**Units:** Probability per femtosecond

### 5. Density of States (DOS)

**Definition:** Number of states per energy interval

**Computation:**
1. Create energy bins: [E_min, E_max] divided into NN bins
2. Count eigenvalues in each bin
3. Normalize: DOS(E) = count / (total_states × bin_width)

**Physical Meaning:** Energy distribution of available states

### 6. Dipole Moment

**x-component (along sequence):**
```
dₓ(t) = (3.4 Å / a₀) · Σᵢ (νᵢ - νcenter) · P(i,t)
```
where νᵢ is the base pair index.

**y-component (across strands):**
```
dᵧ(t) = (10 Å / a₀) · Σᵢ (σᵢ - σcenter) · P(i,t)
```
where σᵢ is the strand index (0, 1, or 2 in FISHBONE).

**Units:** Bohr radii (a₀ = 0.52917721067 Å)

### 7. Weighted Mean Frequency (WMF)

**Definition:**
```
WMF[i] = Σⱼ (fⱼ · FCᵢⱼ) / Σⱼ FCᵢⱼ
```

Where:
- **fⱼ** = transition frequency between states
- **FCᵢⱼ** = Franck-Condon amplitude at site i for transition j

**Total WMF:**
```
TWMF = Σᵢ WMF[i] · ⟨P(i)⟩
```

**Physical Meaning:** Characteristic oscillation frequency weighted by probability

**Units:** THz (terahertz)

## Disorder Models

### Physical Motivation

Real DNA molecules have:
- Thermal fluctuations
- Structural variations
- Environmental effects
- Manufacturing defects (for synthetic sequences)

### Implementation

Disorder adds Gaussian noise to parameters:

```
E_disordered = E₀ · (1 + δ · N(0,1))
t_disordered = t₀ · (1 + δ · N(0,1))
```

Where:
- **E₀, t₀** = clean parameter values
- **δ** = disorder strength (percentile)
- **N(0,1)** = standard normal distribution

### Disorder Strengths

**Energy Parameters:**
- δ = 0.05 (5% fluctuation)
- Rationale: Onsite energies are relatively stable

**Hopping Integrals:**
- δ = 0.50 (50% fluctuation)
- Rationale: Hopping depends sensitively on distance and overlap

### Disorder Types

See README.md for the complete table of disorder types 0-10.

**Statistical Sampling:**
- Clean system (disorder = 0): 1 run
- Disordered system (disorder > 0): 10 runs with different seeds
- Results reported as mean ± standard error

## Physical Constants

| Constant | Symbol | Value | Units |
|----------|--------|-------|-------|
| Planck constant | h | 4.135667517 | eV·fs |
| Reduced Planck | ℏ | h/(2π) | eV·fs |
| Bohr radius | a₀ | 0.52917721067 | Å |
| Base stacking | d_stack | 3.4 | Å |
| Strand separation | d_strand | 10 | Å |

**Conversion:**
- eV per ℏ: 2π/h ≈ 1.519 fs⁻¹

## Time Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Time points | L = 64 × 16385 | ~1 million points |
| Time range | 0 to 100,000 fs | 100 picoseconds |
| Time step | Δt ≈ 0.096 fs | Ultra-fast resolution |

## Numerical Methods

### Eigenvalue Solver
- Method: `numpy.linalg.eig()`
- Computes both eigenvalues and eigenvectors
- Handles non-Hermitian matrices (for verification)

### Initial Coefficients
Three methods verified for consistency:
1. `np.linalg.solve(V, x₀)` - Linear solver
2. `np.linalg.lstsq(V, x₀)` - Least squares
3. `np.dot(np.linalg.inv(V), x₀)` - Direct inversion

### Degeneracy Handling
- Degeneracy threshold: |Eᵢ - Eⱼ| < 10⁻¹²
- Special treatment for time-averaged probabilities

### FFT Analysis
- Zero-padding to next power of 2
- Nyquist frequency: fs/2 where fs = (L-1)/t_max
- Frequency resolution: ~0.01 THz

## References

1. **Energy Parameters:** Marcus-like studies (MLS) for HOMO; literature compilation for LUMO
2. **Tight-binding models:** Standard solid-state physics approach adapted to DNA
3. **Disorder models:** Inspired by Anderson localization studies
4. **Participation ratio:** Definition from quantum physics of disordered systems

## Assumptions & Approximations

1. **Tight-binding approximation:** Valid for weak overlap between sites
2. **Nearest-neighbor only:** Long-range hopping neglected
3. **Time-independent Hamiltonian:** No dynamics of DNA structure itself
4. **Single-particle picture:** No electron-electron interactions
5. **Zero temperature:** Thermal effects ignored
6. **Coherent transport:** No decoherence or dissipation

## Future Extensions

- Include electron-phonon coupling (vibrations)
- Add decoherence and relaxation
- Implement sequence-dependent structure (bending, twisting)
- Multi-particle calculations (Coulomb interactions)
- Temperature-dependent parameters
