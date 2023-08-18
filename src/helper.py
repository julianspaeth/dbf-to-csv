import os
import pandas as pd
import dbfread


def get_dbf_files(path):
    dbf_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".dbf"):
                dbf_files.append(os.path.join(root, file))
    return dbf_files



def write_csv(df: pd.DataFrame, filepath: str):
    filepath = os.path.splitext(filepath)[0]
    df.to_csv(f'{filepath}.tsv', index=False, sep='\t', na_rep='NULL', errors='replace')
    df.to_csv(f'{filepath}.csv', index=False, sep=',', na_rep='NULL', errors='replace')
    df.to_csv(f'{filepath}.ssv', index=False, sep=';', na_rep='NULL', errors='replace')
    df.to_parquet(f'{filepath}.parquet.gzip', index=False, compression='gzip')
    df.to_excel(f'{filepath}.xlsx', index=False, na_rep='NULL', engine='xlsxwriter')
