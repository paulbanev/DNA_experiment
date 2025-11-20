"""Test script to verify randomness is independent between runs"""
import random
import numpy as np

# Test 1: Does setting seed make disorder reproducible?
print("=== Test 1: Reproducibility with same seed ===")
random.seed(0)
values_run1 = [random.gauss(0, 1) for _ in range(5)]
print(f"Run 1 (seed=0): {values_run1}")

random.seed(0)
values_run2 = [random.gauss(0, 1) for _ in range(5)]
print(f"Run 2 (seed=0): {values_run2}")
print(f"Are they identical? {values_run1 == values_run2}")

# Test 2: Does different seed give different values?
print("\n=== Test 2: Independence with different seeds ===")
random.seed(0)
values_seed0 = [random.gauss(0, 1) for _ in range(5)]
print(f"Seed 0: {values_seed0}")

random.seed(1)
values_seed1 = [random.gauss(0, 1) for _ in range(5)]
print(f"Seed 1: {values_seed1}")
print(f"Are they different? {values_seed0 != values_seed1}")

# Test 3: Simulate disorder application
print("\n=== Test 3: Simulating disorder on energies ===")
base_energy = 8.3
disorder_strength = 0.05

energies_run0 = []
energies_run1 = []

for run_id in [0, 1]:
    random.seed(run_id)
    energies = []
    for _ in range(5):  # 5 bases
        E_disordered = base_energy * (1 + disorder_strength * random.gauss(0, 1))
        energies.append(E_disordered)
    
    if run_id == 0:
        energies_run0 = energies
    else:
        energies_run1 = energies

print(f"Run 0 energies: {energies_run0}")
print(f"Run 1 energies: {energies_run1}")
print(f"Are they different? {energies_run0 != energies_run1}")
print(f"Mean difference: {np.mean(np.abs(np.array(energies_run0) - np.array(energies_run1))):.6f} eV")
