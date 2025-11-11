# TODO: Навести порядок в логах (ненужные убрать, нужные добавить), а то сейчас бардак творится!
import tkinter as tk
from tkinter import ttk
from random import choice
import logging
from .data import JSON


logging.basicConfig(level=logging.INFO)


def get_random_dict_key(dictionary: dict):
    # TODO: Пожалуй, стоит генерировать последовательность через random.sample.
    return choice(list(dictionary))


class MainWindow(tk.Tk):
    def __init__(self, *, data_handler: JSON):
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
        # На вкладке "Словарь"
        self.button_select_date = ttk.Button(
            master=self.tab_dictionary, text='Выбрать дату', command=self.__button_select_date_click)

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
        self.button_select_date.pack()

        self.label_test_time.pack()
        self.radiobtn_all_time.pack()
        self.radiobtn_fixed_time.pack()

        self.radiobtn_test_lang1.pack()
        self.radiobtn_test_lang2.pack()

        self.btn_start_test.pack(anchor='e')

    # Обработчики нажатий кнопок
    def __button_select_date_click(self) -> None:
        self.select_date_window = SelectDateWindow()

    def __btn_start_test_click(self) -> None:
        self.test_window = TestWindow(data_handler=self.data_handler,
                                      tests_time=self.radiobtn_tests_time_var.get(),
                                      tests_lang=self.radiobtn_tests_lang_var.get())


class AddWordWindow(tk.Tk):
    ...


class SelectDateWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Выбор даты')

        self.__define_internal_vars()
        self.__define_widgets()
        self.__pack_widgets()

    def __define_internal_vars(self):
        ...

    def __define_widgets(self):
        self.label_instruction = ttk.Label(
            self, text='Введите дату в формате "дд.мм.гггг"')
        self.entry_date = ttk.Entry(self)
        self.button_ok = ttk.Button(
            self, text='Выбрать', command=self.__button_ok_click)

    def __pack_widgets(self):
        self.label_instruction.pack()
        self.entry_date.pack()
        self.button_ok.pack(anchor='e')

    def __button_ok_click(self):
        ...

    def get_date(self):
        ...


class TestWindow(tk.Tk):
    def __init__(self, *, data_handler: JSON, tests_time, tests_lang):
        # Прокидываем обработчики и настройки.
        self.data_handler = data_handler
        self.tests_time = tests_time
        self.tests_lang = tests_lang

        super().__init__()

        self.__define_internal_vars()
        self.__define_widgets()
        self.__pack_widgets()

        self.__form_words_dict()

        self.current_word = get_random_dict_key(self.words)
        self.label_word.configure(text=self.current_word)

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

    def __form_words_dict(self):
        match self.tests_time:
            # Здесь мы формируем словарь со словами, которые будем проверять
            # в зависимости от времени.
            case 'all':
                words: dict = self.data_handler.get_all_words()
                logging.debug(f'{words=}')
            case 'fixed':
                # TODO: Здесь надо будет создавать окно с выбором даты.
                logging.error("Вызов нереализованной функции.")
                self.destroy()

        match self.tests_lang:
            case 1:
                self.words = words
                # Ничего не делаем, слова и так в правильном порядке.
                logging.debug("Не перевёрнутый словарь: %s", (self.words))
            case 2:
                # Переворачиваем словарь.
                self.words = {value: key for key, value in words.items()}
                logging.debug("Перевёрнутый словарь: %s", (self.words))

    def __button_check_click(self):
        logging.info('Нажата кнопка "Проверить"')
        logging.debug(self.entry_translating.get())
        user_translating: str = self.entry_translating.get().strip()

        current_translating = self.words[self.current_word]
        logging.debug(f'{current_translating=}')

        logging.debug(f'{user_translating=}')

        if user_translating == current_translating:
            self.label_result.configure(text="Правильно!", foreground='green')
        else:
            self.label_result.configure(
                text="Неправильно :(", foreground='red')

        self.label_true_translating.configure(
            text=f"Правильный перевод: {current_translating}")

    def __button_next_click(self):
        logging.info('Нажата кнопка "Далее".')

        # Сбрасываем надписи
        self.label_result.configure(text='')
        self.label_true_translating.configure(text='')

        # Сбрасываем поле ввода
        self.entry_translating.delete(0, last='end')

        # Берём случайное слово
        self.current_word = get_random_dict_key(self.words)

        # Меняем надписи
        self.label_word.configure(text=self.current_word)
