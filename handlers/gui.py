import tkinter as tk
from tkinter import ttk


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('')

        self.__define_internal_vars()
        self.__define_tabs()
        self.__define_frames()
        self.__define_widgets()
        self.__pack_widgets()

    def __define_internal_vars(self):
        self.radiobtn_time_var = tk.IntVar()

    def __define_tabs(self):
        self.notebook = ttk.Notebook(master=self)
        self.notebook.pack()

        self.tab_dictionary = ttk.Frame(master=self.notebook)
        self.tab_dictionary.pack()
        self.notebook.add(self.tab_dictionary, text="Словарь")

        self.tab_tests = ttk.Frame(master=self.notebook)
        self.tab_tests.pack()
        self.notebook.add(self.tab_tests, text="Тесты")

        self.notebook.pack()

    def __define_frames(self):
        # На вкладке "Тесты"
        self.frame_tests_time = ttk.Frame(master=self.tab_tests)
        self.frame_tests_lang = ttk.Frame(master=self.tab_tests)
        self.frame_tests_time.pack()
        self.frame_tests_lang.pack()

    def __define_widgets(self):
        # На вкладке "Тесты"

        # На рамке "time"
        self.label_test_time = ttk.Label(
            master=self.frame_tests_time, text="Тестировать за:")
        self.radiobtn_all_time = ttk.Radiobutton(
            master=self.frame_tests_time, text='всё время', variable=self.radiobtn_time_var, value=1)
        self.radiobtn_fixed_time = ttk.Radiobutton(
            master=self.frame_tests_time, text='определённое время', variable=self.radiobtn_time_var, value=2)

    def __pack_widgets(self):
        self.label_test_time.pack()
        self.radiobtn_all_time.pack()
        self.radiobtn_fixed_time.pack()


class AddWordWindow(tk.Tk):
    ...


class SelectDateWindow(tk.Tk):
    ...


class TestWindow(tk.Tk):
    ...


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()
