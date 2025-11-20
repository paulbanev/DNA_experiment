"""DNA Transport Simulation - Main Entry Point

This module provides the command-line interface for running quantum transport
simulations on DNA sequences. It orchestrates the workflow: sequence validation,
matrix construction, quantum analysis, visualization, and optional data export.

Usage:
    python main.py --sequence ATGCAT --mode HOMO --model FISHBONE --disorder 0

For detailed documentation, see README.md
"""

import argparse
import os
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from matrixes import matrixes
from disorder import get_disorder_model
from analysis import computations
from sequence import sequence_properties, validate_sequence
from visualization import save_plots

L = 64 * 16385
t = np.linspace(0, 100000, L)
NN = 10

h = 4.135667517  # eV·fs
hbar = h / (2 * np.pi)
eVperhbar = (2 * np.pi) / h

def run_simulation_once(NN, A, MD, eVperhbar, t, L, h, dos_flag=True, 
                        analytical_flag=True, fft_flag=True, 
                        dipole_fft_flag=True, fourier_flag=True):
    """Execute a single simulation run with the given parameters.
    
    This is a thin wrapper around the computations function that performs
    the quantum mechanical analysis.
    
    Args:
        NN (int): Number of DOS (Density of States) bins
        A (ndarray): Hamiltonian matrix (MD × MD)
        MD (int): Matrix dimension (number of sites)
        eVperhbar (float): Conversion factor (2π/h) in fs⁻¹
        t (ndarray): Time array for evolution
        L (int): Length of time array
        h (float): Planck constant in eV·fs
        dos_flag (bool): Enable DOS calculation (default: True)
        analytical_flag (bool): Enable analytical calculations (default: True)
        fft_flag (bool): Enable FFT analysis (default: True)
        dipole_fft_flag (bool): Enable dipole FFT (default: True)
        fourier_flag (bool): Enable Fourier analysis (default: True)
    
    Returns:
        dict: Dictionary containing all computed metrics (eigenvalues,
              participation ratio, transfer rates, DOS, etc.)
    """
    return computations(NN, A, MD, eVperhbar, t, L, h, dos_flag,
                       analytical_flag, fft_flag, dipole_fft_flag, fourier_flag)

def run_single_simulation(params):
    """Worker function for parallel execution of a single simulation run.
    
    This function is designed to be called by ProcessPoolExecutor. It takes
    all necessary parameters, builds the Hamiltonian matrix, and runs the
    quantum transport simulation.
    
    Args:
        params (tuple): (run_index, args_dict, global_params) where:
            - run_index (int): Index of this run (0 to num_runs-1)
            - args_dict (dict): Parsed command-line arguments
            - global_params (dict): Global parameters (NN, t, L, h, eVperhbar)
    
    Returns:
        dict: Metrics dictionary from computations()
    """
    run_index, args_dict, global_params = params
    
    # Calculate seed for this run
    seed = args_dict['seed'] + run_index if args_dict['seed'] is not None else run_index
    
    # Get disorder model
    disorder_params = get_disorder_model(args_dict['disorder'], seed=seed)
    
    # Validate sequence and get properties
    validated_seq = validate_sequence(args_dict['sequence'])
    Ebp, tbb = sequence_properties(validated_seq, args_dict['mode'], args_dict['model'])
    
    # Build Hamiltonian matrix
    A, MD = matrixes(Ebp, tbb, disorder_params, validated_seq, 
                     mode=args_dict['mode'], model=args_dict['model'], 
                     seed=seed, symmetry=args_dict['symmetry'])
    
    
    # Run quantum simulation
    metrics = run_simulation_once(global_params['NN'], A, MD, 
                                   global_params['eVperhbar'], 
                                   global_params['t'], 
                                   global_params['L'], 
                                   global_params['h'],
                                   global_params['dos_flag'],
                                   global_params['analytical_flag'],
                                   global_params['fft_flag'],
                                   global_params['dipole_fft_flag'],
                                   global_params['fourier_flag'])
    
    return metrics

def print_summary_stats(results):
    """Print formatted summary statistics from simulation results.
    
    For single-run results, prints individual element values.
    For multi-run results, prints mean ± standard deviation.
    Large matrices (eigenvectors, dipole moments) are skipped.
    
    Args:
        results (dict): Dictionary where keys are metric names and values
                       are lists of results from multiple runs
    """
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
    """Main execution function - parses arguments and runs simulation workflow.
    
    Workflow:
        1. Parse command-line arguments
        2. Validate DNA sequence
        3. Determine number of runs (1 for clean, 10 for disorder)
        4. For each run:
           a. Generate disorder parameters (if applicable)
           b. Extract sequence properties (energies and hoppings)
           c. Construct Hamiltonian matrix
           d. Run quantum analysis
           e. Collect results
        5. Print summary statistics
        6. Export to Excel (if requested)
        7. Generate and save visualization plots
    
    Command-line arguments are defined using argparse. See README.md for details.
    """
    parser = argparse.ArgumentParser(description="Run Fishbone DNA Transport Simulation")
    parser.add_argument('--sequence', type=str, required=True, help='One side of your polymer sequence')
    parser.add_argument('--mode', choices=['HOMO', 'LUMO'], required=True, help='Electronic mode')
    parser.add_argument('--model', choices=['WIRE','FISHBONE','LADDER', 'EXTENDED_LADDER', 'SPECIALE'], required=True, help='transoport model to use')
    parser.add_argument('--symmetry', choices=['symmetric', 'asymmetric'], default='symmetric', help='Hopping symmetry: symmetric (tSp=tS) or asymmetric (tSp=0.16)')
    parser.add_argument('--disorder', type=int, default=0, help='Disorder type (0–10)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed for disorder')
    parser.add_argument('--export', action='store_true', help='Export results to Excel')
    parser.add_argument('--dos-bins', type=int, default=10, 
                        help='Number of energy bins for Density of States histogram (default: 10)')
    parser.add_argument('--disable-dos', action='store_true', 
                        help='Disable DOS calculation to save computation time')
    parser.add_argument('--disable-analytical', action='store_true',
                        help='Disable analytical calculations (frequencies, mean probabilities, etc.)')
    parser.add_argument('--disable-fft', action='store_true',
                        help='Disable FFT analysis of probability evolution')
    parser.add_argument('--disable-dipole-fft', action='store_true',
                        help='Disable FFT analysis of dipole moments')
    parser.add_argument('--disable-fourier', action='store_true',
                        help='Disable Fourier amplitude and frequency calculations')
    parser.add_argument('--workers', type=int, default=None, 
                        help='Number of parallel workers (default: all CPUs, 1 = sequential)')

    args = parser.parse_args()

    # Start timing
    start_time = time.time()

    # If no seed specified, use a random seed based on time
    # This ensures different disorder realizations between program runs
    if args.seed is None:
        args.seed = int(time.time() * 1000) % (2**31)  # Use milliseconds, keep within int32 range
        print(f"No seed specified. Using random seed: {args.seed}")
        print(f"To reproduce this run, use: --seed {args.seed}")

    # Determine number of workers
    if args.workers is None:
        args.workers = os.cpu_count()  # Use all available CPUs
    
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
        "weighted mean frequency":[],
        "PWMF": [],
        "count":[]    
    }

    # Package global parameters
    global_params = {
        'NN': args.dos_bins,  # Number of DOS bins
        'dos_flag': not args.disable_dos,  # Enable DOS unless --disable-dos is set
        'analytical_flag': not args.disable_analytical,  # Enable analytical calculations
        'fft_flag': not args.disable_fft,  # Enable FFT analysis
        'dipole_fft_flag': not args.disable_dipole_fft,  # Enable dipole FFT
        'fourier_flag': not args.disable_fourier,  # Enable Fourier analysis
        't': t,
        'L': L,
        'h': h,
        'eVperhbar': eVperhbar
    }
    
    # Package arguments for workers
    args_dict = {
        'sequence': args.sequence,
        'mode': args.mode,
        'model': args.model,
        'symmetry': args.symmetry,
        'disorder': args.disorder,
        'seed': args.seed
    }

    # Execute simulations (parallel or sequential)
    if args.workers == 1 or num_runs == 1:
        # Sequential execution (original behavior)
        print(f"Running {num_runs} simulation(s) sequentially...")
        for run in range(num_runs):
            params = (run, args_dict, global_params)
            metrics = run_single_simulation(params)
            
            for key in results:
                results[key].append(metrics.get(key))
    else:
        # Parallel execution
        print(f"Running {num_runs} simulations in parallel using {args.workers} workers...")
        
        # Create parameter tuples for each run
        run_params = [(i, args_dict, global_params) for i in range(num_runs)]
        
        # Execute in parallel
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            metrics_list = list(executor.map(run_single_simulation, run_params))
        
        # Aggregate results
        for metrics in metrics_list:
            for key in results:
                results[key].append(metrics.get(key))

    print_summary_stats(results)

    if args.export:
        from export_results import export_to_excel
        export_to_excel(results)
        print("Results exported to Excel.")

    save_plots(results)

    # Print total execution time
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Format time nicely
    if elapsed_time < 60:
        print(f"\nTotal execution time: {elapsed_time:.2f} seconds")
    elif elapsed_time < 3600:
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60
        print(f"\nTotal execution time: {minutes}m {seconds:.2f}s")
    else:
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = elapsed_time % 60
        print(f"\nTotal execution time: {hours}h {minutes}m {seconds:.2f}s")

if __name__ == '__main__':
    main()
