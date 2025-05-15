# main.py
import argparse
import numpy as np
from matrixes import matrixes
from disorder import get_disorder_model
from analysis import computations


def run_simulation_once(A, MD, eVperhbar, t):
    return computations(A, MD, eVperhbar, t)

def print_summary_stats(results):
    print("\nSummary Statistics:")
    for key, values in results.items():
        values = np.array(values)

        # Take only real parts if complex
        values = np.real(values)

        if values.ndim == 1 or values.shape[0] == 1:
            # Single run or 1D results, print elements directly
            arr = values if values.ndim == 1 else values[0]
            print(f"{key}:")
            for i, v in enumerate(arr):
                print(f"  Element {i}: {v:.4f}")
        else:
            # Multiple runs, element-wise average and std dev
            mean_vals = np.mean(values, axis=0)
            std_vals = np.std(values, axis=0)
            print(f"{key}:")
            for i, (m, s) in enumerate(zip(mean_vals, std_vals)):
                print(f"  Element {i}: {m:.4f} ± {s:.4f}")

def main():
    parser = argparse.ArgumentParser(description="Run Fishbone DNA Transport Simulation")
    parser.add_argument('--length', type=int, required=True, help='Number of base-pairs')
    parser.add_argument('--mode', choices=['HOMO', 'LUMO'], required=True, help='Electronic mode')
    parser.add_argument('--disorder', type=int, default=0, help='Disorder type (0–10)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed for disorder')
    args = parser.parse_args()

    t = np.linspace(0, 100000, 64 * 16385)

    num_runs = 10 if args.disorder != 0 else 1
    results = {"idiotimes": [], "mesox": [], "participation ratio": [], "mean transfer rate": []}

    for run in range(num_runs):
        if args.seed is None:
            seed = run
        else:
            seed = args.seed + run  # ensure different seeds for each run
    
        disorder_params = get_disorder_model(args.disorder, args.length, seed=seed)
        A, MD, eVperhbar = matrixes(args.length, args.mode, disorder_params, seed=seed)
        metrics = run_simulation_once(A, MD, eVperhbar, t)

        results["idiotimes"].append(metrics["idiotimes"])
        results["mesox"].append(metrics["mesox"])
        results["participation ratio"].append(metrics["participation ratio"])
        results["mean transfer rate"].append(metrics["mean transfer rate"])

    print_summary_stats(results)

if __name__ == '__main__':
    main()
