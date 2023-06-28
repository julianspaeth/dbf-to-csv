import os
import threading
from time import sleep

import customtkinter
import dbfread
import pandas as pd
from dbfread import MissingMemoFile

from helper import get_dbf_files, write_csv

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")


class CustomApplication(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.geometry("800x400")
        self.title("DBF-to-CSV Converter 1.0")

        self.directory_path = None

        label_1 = customtkinter.CTkLabel(master=self, justify=customtkinter.LEFT)
        label_1.pack(pady=10, padx=10)
        label_1.configure(text="DBF-to-CSV Converter 1.0")

        self.button_choose_dir = customtkinter.CTkButton(master=self, command=self.choose_directory)
        self.button_choose_dir.pack(pady=10, padx=10)
        self.button_choose_dir.configure(text="Choose directory")

        self.button_convert = customtkinter.CTkButton(master=self,
                                                      command=threading.Thread(target=self.convert_to_csv).start)
        self.button_convert.pack(pady=10, padx=10)
        self.button_convert.configure(state="disabled")
        self.button_convert.configure(text="Convert to CSV")

        self.label_2 = customtkinter.CTkLabel(master=self, justify=customtkinter.LEFT)
        self.label_2.pack(pady=10, padx=10)
        self.label_2.configure(text="")

        button_exit = customtkinter.CTkButton(master=self, command=self.end)
        button_exit.pack(pady=10, padx=10)
        button_exit.configure(text="Exit")

    def end(self):
        self.destroy()

    def choose_directory(self):
        self.directory_path = customtkinter.filedialog.askdirectory()
        self.button_choose_dir.configure(state='disabled')
        self.button_convert.configure(state='normal')

    def convert_to_csv(self):
        files = get_dbf_files(self.directory_path)
        directory_path = os.path.dirname(files[0])
        parsing_errors = {}
        parsing_successes = {}
        writing_errors = {}
        writing_successes = {}
        for file in files:
            self.label_2.configure(text="Convert to CSV: " + file)
            filename = os.path.basename(file)
            try:
                print(file, filename)
                try:
                    dbf = dbfread.DBF(f'{file}', char_decode_errors='ignore')
                except MissingMemoFile as e:
                    parsing_successes[f'{filename} [WARNING]'] = e
                    print("Missing Memo File")
                    dbf = dbfread.DBF(f'{file}', char_decode_errors='ignore', ignore_missing_memofile=True)
                df = pd.DataFrame(iter(dbf))
                parsing_successes[filename] = 'OK'
                try:
                    write_csv(df, file)
                    writing_successes[filename] = 'OK'
                except Exception as e:
                    writing_errors[filename] = e
            except Exception as e:
                parsing_errors[filename] = e
            sleep(1)

        if len(parsing_errors.keys()) > 0:
            pd.DataFrame.from_dict(parsing_errors, orient='index').to_csv(f'{directory_path}/parsing_errors.csv',
                                                                          index=True, header=False)
        if len(writing_errors.keys()) > 0:
            pd.DataFrame.from_dict(writing_errors, orient='index').to_csv(f'{directory_path}/writing_errors.csv',
                                                                          index=True, header=False)
        if len(parsing_successes) > 0:
            pd.DataFrame.from_dict(parsing_successes, orient='index').to_csv(f'{directory_path}/parsing_successes.csv',
                                                                             index=True, header=False)
        if len(writing_successes) > 0:
            pd.DataFrame.from_dict(writing_successes, orient='index').to_csv(f'{directory_path}/writing_successes.csv',
                                                                             index=True, header=False)

        self.button_convert.configure(state='disabled')
        self.label_2.configure(text="Finished. Please check the logs.")
        print('finished.')


if __name__ == '__main__':
    app = CustomApplication()
    app.mainloop()
