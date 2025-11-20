import pandas as pd

print("=== EXCEL FILE CONTENTS ===")
sheets = ['pithanotites', 'mean transfer rate', 'participation ratio']

for sheet in sheets:
    df = pd.read_excel(r'c:\Users\Pavlos Banev\Develop\DNA_experiment - Copy\results\results.xlsx', 
                       sheet_name=sheet)
    print(f'\n{sheet}:')
    print(df[['Run 0']].head(10).to_string(index=False))
