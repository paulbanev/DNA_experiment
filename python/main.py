import argparse
import numpy as np
from matrixes import matrixes
from disorder import get_disorder_model
from analysis import computations
from sequence import sequence_properties, validate_sequence
from visualization import save_plots

L = 64 * 16385
t = np.linspace(0, 100000, L)

h = 4.135667517  # eV·fs
hbar = h / (2 * np.pi)
eVperhbar = (2 * np.pi) / h

def run_simulation_once(NN, A, MD, eVperhbar, t, L, h):
    return computations(NN, A, MD, eVperhbar, t, L, h)

def print_summary_stats(results):
    print("\nSummary Statistics:")
    for key, values in results.items():
        if key in {"eigenvector matrix", "x axis dipole moment", "y axis dipole moment"}:
            continue  # skip large matrix prints

        values = np.array(values)
        values = np.real(values)  # take real part if complex

        print(f"{key}:")
        if values.ndim == 1 or values.shape[0] == 1:
            arr = values if values.ndim == 1 else values[0]
            for i, v in enumerate(arr):
                if np.isscalar(v):
                    print(f"  Element {i}: {v:.4f}")
                else:
                    print(f"  Element {i}: {v}")
        else:
            mean_vals = np.mean(values, axis=0)
            std_vals = np.std(values, axis=0)
            for i, (m, s) in enumerate(zip(mean_vals, std_vals)):
                if np.isscalar(m) and np.isscalar(s):
                    print(f"  Element {i}: {m:.4f} ± {s:.4f}")
                else:
                    print(f"  Element {i}: {m} ± {s}")

def main():
    parser = argparse.ArgumentParser(description="Run Fishbone DNA Transport Simulation")
    parser.add_argument('--sequence', type=str, required=True, help='One side of your polymer sequence')
    parser.add_argument('--mode', choices=['HOMO', 'LUMO'], required=True, help='Electronic mode')
    parser.add_argument('--symmetry', choices=['symmetric', 'asymmetric'], default='symmetric',
                        help='Hopping symmetry: symmetric (tSp=tS) or asymmetric (tSp=0.16)')
    parser.add_argument('--disorder', type=int, default=0, help='Disorder type (0–10)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed for disorder')
    parser.add_argument('--export', action='store_true', help='Export results to Excel')
    parser.add_argument('--number_of_DOS_points', type=int, default=10)

    args = parser.parse_args()

    num_runs = 10 if args.disorder != 0 else 1

    results = {
        "idiotimes": [],
        "pithanotites": [],
        "participation ratio": [],
        "mean transfer rate": [],
        "eigenvector matrix": [],
        "total weighted mean frequency": [],
        "x axis dipole moment": [],
        "y axis dipole moment": [],
        "mesi thesi": [],
        "count": []
    }

    for run in range(num_runs):
        seed = args.seed + run if args.seed is not None else run

        disorder_params = get_disorder_model(args.disorder, seed=seed)
        validated_seq = validate_sequence(args.sequence)
        Ebp, tbb = sequence_properties(validated_seq, args.mode)
        A, MD = matrixes(Ebp, tbb, disorder_params, validated_seq, mode=args.mode, seed=seed, symmetry=args.symmetry)

        metrics = run_simulation_once(args.number_of_DOS_points, A, MD, eVperhbar, t, L, h)

        for key in results:
            results[key].append(metrics.get(key))

    print_summary_stats(results)

    if args.export:
        from export_results import export_to_excel
        export_to_excel(results)
        print("Results exported to Excel.")

    save_plots(results)

if __name__ == '__main__':
    main()
