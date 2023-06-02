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


def convert_to_df(filepath: str):
    dbf = dbfread.DBF(f'{filepath}', char_decode_errors='ignore')
    dbf_df = pd.DataFrame(iter(dbf))

    return dbf_df


def write_csv(df: pd.DataFrame, filepath: str):
    filepath = os.path.splitext(filepath)[0]
    df.to_csv(f'{filepath}.csv', index=False)
