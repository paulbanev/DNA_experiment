import numpy as np
from sequence import sequence_properties, validate_sequence
from matrixes import matrixes
from disorder import get_disorder_model
from analysis import computations

# Reproduce the exact calculation
validated_seq = validate_sequence("ATGCAT")
Ebp, tbb = sequence_properties(validated_seq, "HOMO", "FISHBONE")

disorder_params = get_disorder_model(0, seed=0)
A, MD = matrixes(Ebp, tbb, disorder_params, validated_seq, 
                 mode="HOMO", model="FISHBONE", seed=0, symmetry="symmetric")

L = 64 * 16385
t = np.linspace(0, 100000, L)
h = 4.135667517
eVperhbar = (2 * np.pi) / h

metrics = computations(10, A, MD, eVperhbar, t, L, h)

print("\n=== ACTUAL COMPUTED VALUES (full precision) ===")
print(f"pithanotites[0]: {metrics['pithanotites'][0]:.15f}")
print(f"pithanotites[1]: {metrics['pithanotites'][1]:.15f}")
print(f"pithanotites[4]: {metrics['pithanotites'][4]:.15f}")

print(f"\nmean transfer rate[0]: {metrics['mean transfer rate'][0]:.15e}")
print(f"mean transfer rate[1]: {metrics['mean transfer rate'][1]:.15e}")
print(f"mean transfer rate[4]: {metrics['mean transfer rate'][4]:.15e}")

print("\n=== AS SHOWN IN TERMINAL (numpy default, 4 decimals) ===")
print(f"pithanotites: {metrics['pithanotites'][:5]}")
print(f"mean transfer rate: {metrics['mean transfer rate'][:5]}")
