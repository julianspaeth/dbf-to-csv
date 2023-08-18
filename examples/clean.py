import os

folder_path = "."  # Specify the folder path


def remove_csv_files(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".csv") or file.endswith(".tsv") or file.endswith(".ssv") or file.endswith(".xlsx") or file.endswith(".parquet.gzip"):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"File '{file}' removed successfully!")


remove_csv_files(folder_path)

