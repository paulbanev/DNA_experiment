"""Excel Export Functionality

This module handles exporting simulation results to Excel format with
multiple sheets for different metrics, including statistical summaries.

Output Structure:
    - Each metric gets its own sheet
    - Columns: Run 0, Run 1, ..., Run N, Mean, Average Error
    - Eigenvector matrix gets special handling (too large for normal format)
"""

import pandas as pd
import os
import numpy as np
from pathlib import Path

def export_to_excel(results):
    """Export simulation results to Excel file with statistical summary.
    
    Creates a multi-sheet Excel workbook where each metric has its own sheet
    containing all runs plus mean and standard error.
    
    Args:
        results (dict): Dictionary of simulation results where keys are metric
                       names and values are lists of results from multiple runs
    
    Output File:
        results/results.xlsx with sheets:
            - One sheet per metric (truncated to 31 chars for Excel limit)
            - Each sheet has columns: Run 0, Run 1, ..., Mean, Average error
            - Rows correspond to elements (sites, eigenstates, etc.)
    
    Excluded Metrics:
        - 'eigenvector matrix' (too large, would be unreadable)
        - 'x axis dipole moment' (time series, too large)
        - 'y axis dipole moment' (time series, too large)
    
    Statistical Calculations:
        - Mean: Average across all runs for each element
        - Average error: Standard error = std / sqrt(n_runs)
    
    Notes:
        - Creates 'results/' directory if it doesn't exist
        - Uses openpyxl engine for .xlsx format
        - Sheet names are limited to 31 characters by Excel
    """
    # Get the project root directory (parent of python folder)
    project_root = Path(__file__).parent.parent
    results_dir = project_root / "results"
    
    os.makedirs(results_dir, exist_ok=True)
    writer = pd.ExcelWriter(results_dir / "results.xlsx", engine='openpyxl')

    exclude_keys = {"eigenvector matrix", "x axis dipole moment", "y axis dipole moment"}

    for metric_name, data in results.items():
        if metric_name in exclude_keys:
            continue  # Skip large or unwanted metrics

        if metric_name == "eigenvector matrix":
            all_Vs = []
            for i, V in enumerate(data):
                df = pd.DataFrame(V)
                df.insert(0, "Row", range(1, V.shape[0] + 1))
                df.insert(0, "Run", f"Run {i}")
                all_Vs.append(df)
                all_Vs.append(pd.DataFrame([[""] * df.shape[1]]))  # blank row
            all_V_df = pd.concat(all_Vs, ignore_index=True)
            all_V_df.to_excel(writer, sheet_name="eigenvectors", index=False)
        else:
            data_array = pd.DataFrame(data)
            mean = data_array.mean()
            n = data_array.shape[0]
            
            # Handle single run case (n=1) to avoid NaN in standard error
            if n == 1:
                std = pd.Series(0, index=mean.index)
                sem = pd.Series(0, index=mean.index)
            else:
                std = data_array.std()
                sem = std / np.sqrt(n)

            combined = data_array.T
            combined.columns = [f"Run {i}" for i in range(data_array.shape[0])]
            combined["Mean"] = mean.values
            combined["Average error"] = sem.values

            combined.index.name = "Element"
            combined.to_excel(writer, sheet_name=metric_name[:31])

    writer.close()
