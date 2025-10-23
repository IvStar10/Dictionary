import tkinter as tk
from tkinter import ttk
import logging


logging.basicConfig(level=logging.DEBUG)


class MainWindow(tk.Tk):
    def __init__(self, *, data_handler):
        self.data_handler = data_handler

        super().__init__()

        self.title('')

        self.__define_internal_vars()
        self.__define_tabs()
        self.__define_frames()
        self.__define_widgets()
        self.__pack_widgets()

    def __define_internal_vars(self):
        self.radiobtn_tests_time_var = tk.StringVar()
        self.radiobtn_tests_lang_var = tk.IntVar()

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
            master=self.frame_tests_time, text='всё время',
            variable=self.radiobtn_tests_time_var, value='all')
        self.radiobtn_fixed_time = ttk.Radiobutton(
            master=self.frame_tests_time, text='определённое время',
            variable=self.radiobtn_tests_time_var, value='fixed')

        # На рамке "lang"
        self.radiobtn_test_lang1 = ttk.Radiobutton(
            master=self.frame_tests_lang, text="англ.-рус.",
            variable=self.radiobtn_tests_lang_var, value=1)
        self.radiobtn_test_lang2 = ttk.Radiobutton(
            master=self.frame_tests_lang, text="рус.-англ.",
            variable=self.radiobtn_tests_lang_var, value=2)

        self.btn_start_test = ttk.Button(
            master=self.tab_tests, text='Начать тест',
            command=self.__btn_start_test_click)

    def __pack_widgets(self):
        self.label_test_time.pack()
        self.radiobtn_all_time.pack()
        self.radiobtn_fixed_time.pack()

        self.radiobtn_test_lang1.pack()
        self.radiobtn_test_lang2.pack()

        self.btn_start_test.pack(anchor='e')

    # Обработчики нажатий кнопок
    def __btn_start_test_click(self) -> None:
        self.test_window = TestWindow(data_handler=self.data_handler,
                                      tests_time=self.radiobtn_tests_time_var.get(),
                                      tests_lang=self.radiobtn_tests_lang_var.get())


class AddWordWindow(tk.Tk):
    ...


class SelectDateWindow(tk.Tk):
    ...


class TestWindow(tk.Tk):
    def __init__(self, *, data_handler, tests_time, tests_lang):
        self.data_handler = data_handler
        self.tests_time = tests_time
        self.tests_lang = tests_lang

        super().__init__()

        self.__define_internal_vars()
        self.__define_widgets()
        self.__pack_widgets()

    def __define_internal_vars(self):
        self._user_translating = tk.StringVar()

    def __define_widgets(self):
        self.label_greeting = ttk.Label(master=self, text='Переведите слово:')
        self.label_word = ttk.Label(master=self, text='')

        self.entry_translating = ttk.Entry(
            master=self, textvariable=self._user_translating)
        self.button_check = ttk.Button(
            master=self, text='Проверить', command=self.__button_check_click)

        self.label_result = ttk.Label(master=self, text='')
        self.label_true_translating = ttk.Label(master=self, text='')

        self.button_next = ttk.Button(
            master=self, text='Далее', command=self.__button_next_click)

    def __pack_widgets(self):
        self.label_greeting.pack()
        self.label_word.pack()

        self.entry_translating.pack()
        self.button_check.pack(anchor='e')

        self.label_result.pack()
        self.label_true_translating.pack()

        self.button_next.pack(anchor='e')

    def __button_check_click(self):
        logging.debug(f"{self.tests_time=}")
        logging.debug(f"{self.tests_lang=}")

        word: str = self._user_translating.get()

        match self.tests_time:
            # Здесь мы формируем словарь со словами, которые будем проверять
            # в зависимости от времени.
            case 'all':
                ...
            case 'fixed':
                ...

        match self.tests_lang:
            case 1:
                ...
            case 2:
                ...

    def __button_next_click(self):
        ...
