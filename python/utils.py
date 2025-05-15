import numpy as np

def print_summary_stats(results_dict):
    print("=== AVERAGE RESULTS ===")
    for key, values in results_dict.items():
        arr = np.array(values)  # shape: (num_runs, array_length)
        mean = np.mean(arr, axis=0)  # element-wise mean
        std_err = np.std(arr, axis=0) / np.sqrt(arr.shape[0])  # element-wise standard error
        
        print(f"{key.upper()}:")
        for i, (m, e) in enumerate(zip(mean, std_err)):
            print(f"  Element {i}: {m:.4f} ± {e:.4f}")
