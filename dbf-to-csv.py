import os
from tkinter import messagebox

import customtkinter
import pandas as pd

from helper import get_dbf_files, convert_to_df, write_csv

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")


global directory_path

global button_choose_dir, button_convert


class CustomApplication(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.geometry("800x400")
        self.title("DBF-to-CSV Converter 1.0")

        global button_choose_dir, button_convert

        label_1 = customtkinter.CTkLabel(master=self, justify=customtkinter.LEFT)
        label_1.pack(pady=10, padx=10)
        label_1.configure(text="DBF-to-CSV Converter 1.0")

        button_choose_dir = customtkinter.CTkButton(master=self, command=choose_directory)
        button_choose_dir.pack(pady=10, padx=10)
        button_choose_dir.configure(text="Choose directory")

        button_convert = customtkinter.CTkButton(master=self, command=convert_to_csv)
        button_convert.pack(pady=10, padx=10)
        button_convert.configure(state="disabled")
        button_convert.configure(text="Convert to CSV")

        button_exit = customtkinter.CTkButton(master=self, command=end)
        button_exit.pack(pady=10, padx=10)
        button_exit.configure(text="Exit")


def end():
    global app
    app.destroy()


def choose_directory():
    global directory_path
    directory_path = customtkinter.filedialog.askdirectory()
    button_choose_dir.configure(state='disabled')
    button_convert.configure(state='normal')


def convert_to_csv():
    global directory_path
    files = get_dbf_files(directory_path)
    directory_path = os.path.dirname(files[0])
    parsing_errors = {}
    parsing_successes = []
    writing_errors = {}
    writing_successes = []
    for file in files:
        filename = os.path.basename(file)
        try:
            df = convert_to_df(file)
            parsing_successes.append(filename)
            try:
                write_csv(df, file)
                writing_successes.append(filename)
            except Exception as e:
                writing_errors[filename] = e
        except Exception as e:
            parsing_errors[filename] = e

    if len(parsing_errors.keys()) > 0:
        pd.DataFrame.from_dict(parsing_errors, orient='index').to_csv(f'{directory_path}/parsing_errors.csv',
                                                                      index=False, header=False)
    if len(writing_errors.keys()) > 0:
        pd.DataFrame.from_dict(writing_errors, orient='index').to_csv(f'{directory_path}/writing_errors.csv',
                                                                      index=False, header=False)
    if len(parsing_successes) > 0:
        pd.DataFrame(parsing_successes).to_csv(f'{directory_path}/parsing_successes.csv', index=False, header=False)
    if len(writing_successes) > 0:
        pd.DataFrame(writing_successes).to_csv(f'{directory_path}/writing_successes.csv', index=False, header=False)

    button_convert.configure(state='disabled')

    messagebox.showinfo(title="Finished", message=f'Finished. Please check the logs.')


if __name__ == '__main__':
    app = CustomApplication()
    app.mainloop()
