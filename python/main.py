# main.py
import argparse
import numpy as np
from matrixes import matrixes
from disorder import get_disorder_model
from analysis import computations
from sequence import sequence_properties, validate_sequence
from visualization import save_plots

L=64*16385
t = np.linspace(0, 100000, L) 

h = 4.135667517  # eV·fs
hbar = h / (2 * np.pi)
eVperhbar = (2 * np.pi) / h

def run_simulation_once(A, MD, eVperhbar, t, L, h):
    return computations(A, MD, eVperhbar, t, L, h)

def print_summary_stats(results):
    print("\nSummary Statistics:")
    for key, values in results.items():
        if key in {"eigenvector matrix", "x axis dipole moment", "y axis dipole moment"}:
            continue  # Avoid printing large matrices

        values = np.array(values)

        # Take only real parts if complex
        values = np.real(values)

        print(f"{key}:")
        if values.ndim == 1 or values.shape[0] == 1:
            arr = values if values.ndim == 1 else values[0]
            for i, v in enumerate(arr):
                if np.isscalar(v):
                    print(f"  Element {i}: {v:.4f}")
                else:
                    print(f"  Element {i}: {v}")  # fallback for array values
        else:
            mean_vals = np.mean(values, axis=0)
            std_vals = np.std(values, axis=0)
            for i, (m, s) in enumerate(zip(mean_vals, std_vals)):
                if np.isscalar(m) and np.isscalar(s):
                    print(f"  Element {i}: {m:.4f} ± {s:.4f}")
                else:
                    print(f"  Element {i}: {m} ± {s}")  # fallback for array values

def main():
    #this is what is shown on the command line
    #here you give the model which will run
    parser = argparse.ArgumentParser(description="Run Fishbone DNA Transport Simulation")
    #parser.add_argument('--length', type=int, required=True, help='Number of base-pairs') # Later this will be changed to sequence input by user
    parser.add_argument('--sequence', type=str, required=True, help='Give one side of your polymer. Since we work on basepair for now no need for the second')
    parser.add_argument('--mode', choices=['HOMO', 'LUMO'], required=True, help='Electronic mode')
    parser.add_argument('--symmetry', choices=['symmetric', 'asymmetric'], default='symmetric',help='Choose hopping symmetry: symmetric (tSp=tS) or asymmetric (tSp=0.16)')
    parser.add_argument('--disorder', type=int, default=0, help='Disorder type (0–10)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed for disorder')
    parser.add_argument('--export', action='store_true', help='Export results to Excel')

    args = parser.parse_args()
    
    

#if you run for no disorder, the program is executed once
#for now you can save the results manually to have a baseline
#otherwise the program is executed 10 times and you get the average value of each element of the arrays representing the quantities studied
# aswell as their standard deviation errors. find more in utils.py
    num_runs = 10 if args.disorder != 0 else 1
    results = {
        "idiotimes": [],
        "pithanotites": [],
        "participation ratio": [],
        "mean transfer rate": [],
        "eigenvector matrix": [],
        "total weighted mean frequency": [],
        "x axis dipole moment": [], 
        "y axis dipole moment": []  
    }
    for run in range(num_runs):
        if args.seed is None:
            seed = run
        else:
            seed = args.seed + run  # ensure different seeds for each run. Meaning fresh randomness each time
    
        disorder_params = get_disorder_model(args.disorder, seed=seed)
        validated_seq = validate_sequence(args.sequence)
        Ebp, tbb = sequence_properties(validated_seq, args.mode)
        A, MD= matrixes(Ebp, tbb, disorder_params, validated_seq, mode=args.mode, seed=seed, symmetry=args.symmetry)
        metrics = run_simulation_once(A, MD, eVperhbar, t, L, h)

        results["idiotimes"].append(metrics["idiotimes"])
        results["pithanotites"].append(metrics["pithanotites"])
        results["participation ratio"].append(metrics["participation ratio"])
        results["mean transfer rate"].append(metrics["mean transfer rate"])
        results["eigenvector matrix"].append(metrics["eigenvector matrix"])
        results["total weighted mean frequency"].append(metrics["total weighted mean frequency"])
        results["x axis dipole moment"].append(metrics["x axis dipole moment"])
        results["y axis dipole moment"].append(metrics["y axis dipole moment"])

    print_summary_stats(results)
    if args.export:
        from export_results import export_to_excel
        export_to_excel(results)
        print("Results exported to Excel.")

    save_plots(results)

if __name__ == '__main__':
    main()
