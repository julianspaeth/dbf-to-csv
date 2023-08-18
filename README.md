# dbf-to-csv

## GUI application
The GUI application is a simple tool to convert DBF files to CSV files. It is written in Python 3 and uses the Tkinter library for the GUI.

### Usage
The GUI application can be started by running the `dbf-to-csv.py` file. 

1. The `Choose directory` button will open a dialog to select the directory with the DBF files.
2. Afterward, the `Convert to CSV` button will be enabled and converts all dbf files in the directory and all subdirectories to CSV. Therefore, it also considers the corresponding .dbt files, if available with the same filename.
3. You can check the log csv files for more information.