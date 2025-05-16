import pandas as pd
import os

def export_to_excel(results):
    os.makedirs("results", exist_ok=True)
    writer = pd.ExcelWriter("results/results.xlsx", engine='openpyxl')

    for metric_name, data in results.items():
        data_array = pd.DataFrame(data)
        mean = data_array.mean()
        std = data_array.std()

        # Combine into one DataFrame
        combined = data_array.T
        combined.columns = [f"Run {i}" for i in range(data_array.shape[0])]
        combined["Mean"] = mean.values
        combined["Std"] = std.values

        combined.index.name = "Element"
        combined.to_excel(writer, sheet_name=metric_name[:31])  # Excel sheet names have max 31 chars

    writer.close()
