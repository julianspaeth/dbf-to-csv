import os

folder_path = "."  # Specify the folder path


def remove_csv_files(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"File '{file}' removed successfully!")


remove_csv_files(folder_path)

