"""
Demonstration: How the same seed leads to exactly the same results
"""
import random
import numpy as np

print("="*70)
print("DEMONSTRATION: Why same seed = same disorder = same results")
print("="*70)

# Simulate a simple 3-base DNA system (GGGGG truncated to GGG for clarity)
base_energies = [8.3, 8.3, 8.3]  # G, G, G (clean values)
hopping_integrals = [0.116, 0.116]  # GG, GG (clean values)

disorder_strength_energy = 0.05  # 5%
disorder_strength_hopping = 0.5  # 50%

def apply_disorder_to_system(seed, sequence_name):
    """Apply disorder using a specific seed"""
    random.seed(seed)  # THIS IS THE KEY LINE
    
    # Apply disorder to energies
    disordered_energies = []
    for E_clean in base_energies:
        random_number = random.gauss(0, 1)  # Draw from N(0,1)
        E_disordered = E_clean * (1 + disorder_strength_energy * random_number)
        disordered_energies.append(E_disordered)
    
    # Apply disorder to hopping integrals
    disordered_hoppings = []
    for t_clean in hopping_integrals:
        random_number = random.gauss(0, 1)  # Draw from N(0,1)
        t_disordered = t_clean * (1 + disorder_strength_hopping * random_number)
        disordered_hoppings.append(t_disordered)
    
    # Compute a simple "result" (e.g., total energy of the system)
    total_energy = sum(disordered_energies) + sum(disordered_hoppings)
    
    print(f"\n{sequence_name} (seed={seed}):")
    print(f"  Disordered energies:  {[f'{E:.6f}' for E in disordered_energies]}")
    print(f"  Disordered hoppings:  {[f'{t:.6f}' for t in disordered_hoppings]}")
    print(f"  Total energy:         {total_energy:.10f} eV")
    
    return total_energy

print("\n" + "="*70)
print("EXPERIMENT 1: Running simulation twice with NO seed specified")
print("              (Old behavior: always used seeds 0, 1, 2, ...)")
print("="*70)

# First program run (no --seed flag)
print("\n--- FIRST PROGRAM RUN ---")
result1_run0 = apply_disorder_to_system(0, "Run 0")
result1_run1 = apply_disorder_to_system(1, "Run 1")
result1_run2 = apply_disorder_to_system(2, "Run 2")

# Second program run (no --seed flag, again!)
print("\n--- SECOND PROGRAM RUN (different day) ---")
result2_run0 = apply_disorder_to_system(0, "Run 0")  # Same seed = 0!
result2_run1 = apply_disorder_to_system(1, "Run 1")  # Same seed = 1!
result2_run2 = apply_disorder_to_system(2, "Run 2")  # Same seed = 2!

print("\n--- COMPARISON ---")
print(f"Are Run 0 results identical? {result1_run0 == result2_run0} (YES)")
print(f"Are Run 1 results identical? {result1_run1 == result2_run1} (YES)")
print(f"Are Run 2 results identical? {result1_run2 == result2_run2} (YES)")

print("\n" + "="*70)
print("EXPERIMENT 2: Using different base seeds (with time-based seed)")
print("              (New behavior: each program run uses different seed)")
print("="*70)

# First program run with time-based seed
base_seed_1 = 1732082426123  # Simulated time-based seed
print(f"\n--- FIRST PROGRAM RUN (base seed = {base_seed_1}) ---")
result3_run0 = apply_disorder_to_system(base_seed_1 + 0, "Run 0")
result3_run1 = apply_disorder_to_system(base_seed_1 + 1, "Run 1")
result3_run2 = apply_disorder_to_system(base_seed_1 + 2, "Run 2")

# Second program run with different time-based seed
base_seed_2 = 1732082999456  # Different time = different seed
print(f"\n--- SECOND PROGRAM RUN (base seed = {base_seed_2}) ---")
result4_run0 = apply_disorder_to_system(base_seed_2 + 0, "Run 0")
result4_run1 = apply_disorder_to_system(base_seed_2 + 1, "Run 1")
result4_run2 = apply_disorder_to_system(base_seed_2 + 2, "Run 2")

print("\n--- COMPARISON ---")
print(f"Are Run 0 results identical? {result3_run0 == result4_run0}")
print(f"Are Run 1 results identical? {result3_run1 == result4_run1}")
print(f"Are Run 2 results identical? {result3_run2 == result4_run2}")
print(f"  -> Different disorder realizations! (GOOD)")

print("="*70)
print("KEY INSIGHT:")
print("="*70)
print("• Same seed -> Same sequence of random numbers -> Same Hamiltonian")
print("• Same Hamiltonian -> Same eigenvalues -> Same quantum dynamics")
print("• Same dynamics -> Same TWMF, transfer rates, etc.")
print("\nThis is why your two sets of 10 runs gave IDENTICAL values!")
print("="*70)
