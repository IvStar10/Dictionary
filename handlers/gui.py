import tkinter as tk
from tkinter import ttk


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()


class AddWordWindow(tk.Tk):
    ...


class SelectDateWindow(tk.Tk):
    ...


class TestWindow(tk.Tk):
    ...


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()

