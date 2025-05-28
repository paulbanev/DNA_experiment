import pandas as pd
import os
import numpy as np

def export_to_excel(results):
    os.makedirs("results", exist_ok=True)
    writer = pd.ExcelWriter("results/results.xlsx", engine='openpyxl')

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
            std = data_array.std()
            sem = std / np.sqrt(n)

            combined = data_array.T
            combined.columns = [f"Run {i}" for i in range(data_array.shape[0])]
            combined["Mean"] = mean.values
            combined["Average error"] = sem.values

            combined.index.name = "Element"
            combined.to_excel(writer, sheet_name=metric_name[:31])

    writer.close()
