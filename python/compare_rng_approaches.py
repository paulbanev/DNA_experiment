"""
Comparison: Seeded vs Unseeded Random Number Generation
"""
import random
import numpy as np
import time

print("="*70)
print("COMPARISON: Different Random Number Generation Approaches")
print("="*70)

# Simulate applying disorder to a base energy
base_energy = 8.3  # eV
disorder_strength = 0.05

print("\n" + "="*70)
print("APPROACH 1: Python random with SEED (current approach)")
print("="*70)

def apply_disorder_with_seed(seed):
    random.seed(seed)
    noise = random.gauss(0, 1)
    return base_energy * (1 + disorder_strength * noise)

# Run twice with same seed
energy1a = apply_disorder_with_seed(42)
energy1b = apply_disorder_with_seed(42)
print(f"\nRun 1 (seed=42): {energy1a:.10f} eV")
print(f"Run 2 (seed=42): {energy1b:.10f} eV")
print(f"Reproducible? {energy1a == energy1b} <- Can reproduce results for debugging")

print("\n" + "="*70)
print("APPROACH 2: Python random WITHOUT seed (truly random)")
print("="*70)

def apply_disorder_no_seed():
    # No seed - uses system entropy (time, OS state, etc.)
    noise = random.gauss(0, 1)
    return base_energy * (1 + disorder_strength * noise)

# Run twice
energy2a = apply_disorder_no_seed()
time.sleep(0.001)  # Small delay to ensure different state
energy2b = apply_disorder_no_seed()
print(f"\nRun 1: {energy2a:.10f} eV")
print(f"Run 2: {energy2b:.10f} eV")
print(f"Reproducible? {energy2a == energy2b} <- Cannot reproduce!")

print("\n" + "="*70)
print("APPROACH 3: NumPy random (modern approach)")
print("="*70)

def apply_disorder_numpy_seeded(seed):
    rng = np.random.default_rng(seed)
    noise = rng.normal(0, 1)
    return base_energy * (1 + disorder_strength * noise)

def apply_disorder_numpy_unseeded():
    rng = np.random.default_rng()  # Seed from OS entropy
    noise = rng.normal(0, 1)
    return base_energy * (1 + disorder_strength * noise)

# With seed
energy3a = apply_disorder_numpy_seeded(42)
energy3b = apply_disorder_numpy_seeded(42)
print(f"\nWith seed=42:")
print(f"  Run 1: {energy3a:.10f} eV")
print(f"  Run 2: {energy3b:.10f} eV")
print(f"  Reproducible? {energy3a == energy3b}")

# Without seed
energy4a = apply_disorder_numpy_unseeded()
energy4b = apply_disorder_numpy_unseeded()
print(f"\nWithout seed:")
print(f"  Run 1: {energy4a:.10f} eV")
print(f"  Run 2: {energy4b:.10f} eV")
print(f"  Reproducible? {energy4a == energy4b}")

print("\n" + "="*70)
print("STATISTICAL EQUIVALENCE TEST")
print("="*70)
print("Testing: Do all approaches give same distribution over many samples?")

n_samples = 10000

# Approach 1: Seeded
random.seed(0)
samples_seeded = [base_energy * (1 + disorder_strength * random.gauss(0, 1)) 
                  for _ in range(n_samples)]

# Approach 2: Unseeded (well, we'll use different seeds to simulate)
samples_unseeded = []
for i in range(n_samples):
    random.seed(None)  # Re-seed from OS entropy each time
    samples_unseeded.append(base_energy * (1 + disorder_strength * random.gauss(0, 1)))

# Approach 3: NumPy seeded
rng_seeded = np.random.default_rng(0)
samples_numpy_seeded = base_energy * (1 + disorder_strength * rng_seeded.normal(0, 1, n_samples))

# Approach 3: NumPy unseeded
rng_unseeded = np.random.default_rng()
samples_numpy_unseeded = base_energy * (1 + disorder_strength * rng_unseeded.normal(0, 1, n_samples))

print(f"\nStatistics over {n_samples} samples:")
print(f"{'Approach':<20} {'Mean (eV)':<15} {'Std Dev (eV)':<15}")
print("-" * 50)
print(f"{'Seeded (Python)':<20} {np.mean(samples_seeded):<15.6f} {np.std(samples_seeded):<15.6f}")
print(f"{'Unseeded (Python)':<20} {np.mean(samples_unseeded):<15.6f} {np.std(samples_unseeded):<15.6f}")
print(f"{'Seeded (NumPy)':<20} {np.mean(samples_numpy_seeded):<15.6f} {np.std(samples_numpy_seeded):<15.6f}")
print(f"{'Unseeded (NumPy)':<20} {np.mean(samples_numpy_unseeded):<15.6f} {np.std(samples_numpy_unseeded):<15.6f}")
print(f"{'Expected':<20} {base_energy:<15.6f} {base_energy*disorder_strength:<15.6f}")

print("\n" + "="*70)
print("SUMMARY & RECOMMENDATIONS")
print("="*70)
print("""
STATISTICS:
  All approaches give the same distribution (Mean ~ 8.3 eV, Std ~ 0.415 eV)
  -> Statistically equivalent in the limit of many samples

REPRODUCIBILITY:
  Seeded:   Can reproduce exact results (good for debugging, publishing)
  Unseeded: Cannot reproduce (bad for science!)

RECOMMENDATIONS:

1. FOR SCIENTIFIC WORK (your case):
   Use seeded approach with time-based default seed
   - Gives different results each run (explores disorder space)
   - Can reproduce if needed (prints seed for you)
   - Best of both worlds!

2. FOR MONTE CARLO GAMES/SIMULATIONS:
   Use unseeded approach
   - You don't care about reproducing specific games
   - Want true randomness

3. FOR PRODUCTION SCIENTIFIC CODE:
   Consider NumPy's modern RNG (np.random.default_rng)
   - Better statistical properties
   - Faster
   - More flexible
   - Independent RNG per worker (better for parallel code)

CURRENT CODE: Uses Python random + time-based seed = GOOD CHOICE
""")
print("="*70)
