"""Utility Functions

Helper functions for data processing and output formatting.
"""

import numpy as np

def print_summary_stats(results_dict):
    """Print formatted summary statistics from simulation results.
    
    For single-run results, prints individual element values.
    For multi-run results, prints mean ± standard deviation.
    
    Args:
        results_dict (dict): Dictionary where keys are metric names and
                            values are arrays/lists of results
    
    Output Format:
        Single run: "Element i: value"
        Multiple runs: "Element i: mean ± std"
    
    Note:
        Complex values are automatically converted to real parts.
    """
    print("=== AVERAGE RESULTS ===")
    for key, values in results_dict.items():
        arr = np.real(np.array(values))  # convert complex to real

        if arr.shape[0] == 1 or arr.ndim == 1:
            print(f"{key.upper()}:")
            for i, v in enumerate(arr[0] if arr.shape[0] == 1 else arr):
                print(f"  Element {i}: {v:.4f}")
        else:
            mean = np.mean(arr, axis=0)
            std = np.std(arr, axis=0)
            print(f"{key.upper()}:")
            for i, (m, s) in enumerate(zip(mean, std)):
                print(f"  Element {i}: {m:.4f} ± {s:.4f}")
