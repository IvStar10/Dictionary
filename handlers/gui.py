# TODO: Навести порядок в логах (ненужные убрать, нужные добавить), а то сейчас бардак творится!
import logging

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo

from .data import (
    JSON,
    Date,
    gen_random_dict_key,
    get_today
)
from .exceptions import (
    InvalidDateError,
    DateNotFoundError,
    WordIsEmptyError,
    WordNotFoundError
)


# Знаю, использовать глобальную переменную для этих целей не есть хорошо...
user_selected_date: Date = get_today()


class MainWindow(tk.Tk):
    def __init__(self, *, data_handler: JSON, logger: logging.Logger):
        self._logger = logger
        self.data_handler = data_handler

        super().__init__()

        self.title('Словарь')

        self._define_internal_vars()
        self._define_tabs()
        self._define_frames()
        self._define_widgets()
        self._pack_widgets()

        # Привязываем событие для обновления даты.
        self.bind('<<OnDateUpdate>>',
                  lambda _: self.label_date.configure(text=f'Выбраная дата: {str(user_selected_date)}'))

    def _define_internal_vars(self):
        self.show_as = tk.IntVar()
        self.radiobtn_tests_time_var = tk.StringVar()
        self.radiobtn_tests_lang_var = tk.IntVar()

    def _define_tabs(self):
        self.notebook = ttk.Notebook(master=self)
        self.notebook.pack()

        self.tab_dictionary = ttk.Frame(master=self.notebook)
        self.tab_dictionary.pack()
        self.notebook.add(self.tab_dictionary, text="Словарь")

        self.tab_tests = ttk.Frame(master=self.notebook)
        self.tab_tests.pack()
        self.notebook.add(self.tab_tests, text="Тесты")

        self.notebook.pack()

    def _define_frames(self):
        # На вкладке "Словарь"
        self.tools_frame = ttk.Frame(master=self.tab_dictionary)
        self.frame_dictionary_show_as = ttk.Frame(master=self.tab_dictionary)
        # На вкладке "Тесты"
        self.frame_tests_time = ttk.Frame(master=self.tab_tests)
        self.frame_tests_lang = ttk.Frame(master=self.tab_tests)

    def _define_widgets(self):
        # На вкладке "Словарь"
        # На рамке "tools"
        # TODO: Добавить иконки.
        self.label_date = ttk.Label(
            master=self.tools_frame, text=f'Выбраная дата: {str(user_selected_date)}')
        self.add_word_button = ttk.Button(
            master=self.tools_frame, text='Добавить слово',
            command=self._add_word_button_click)
        self.search_word_button = ttk.Button(
            master=self.tools_frame, text="Search", command=self._search_word_button_click)
        self.button_select_date = ttk.Button(
            master=self.tools_frame, text='Выбрать дату', command=self._button_select_date_click)
        # На рамке "show_as"
        self.label_show_as = ttk.Label(
            master=self.frame_dictionary_show_as, text="Показывать")
        self.radiobutton_as_abc = ttk.Radiobutton(master=self.frame_dictionary_show_as, text="В алфавитном порядке",
                                                  variable=self.show_as, value=1)
        self.radiobutton_as_time = ttk.Radiobutton(master=self.frame_dictionary_show_as, text="В хронологическом порядке",
                                                   variable=self.show_as, value=2)
        self.radiobutton_by_fixed_time = ttk.Radiobutton(master=self.frame_dictionary_show_as, text="За определённое время",
                                                         variable=self.show_as, value=3)
        self.treeview_words = ttk.Treeview(master=self.tab_dictionary)

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
            command=self._btn_start_test_click)

    def _pack_frames(self):
        self.tools_frame.pack(anchor='w')
        self.frame_dictionary_show_as.pack(anchor='w')
        self.frame_tests_time.pack()
        self.frame_tests_lang.pack()

    def _pack_widgets(self):
        self._pack_frames()  # Все рамки.

        # На вкладке "Словарь"
        self.label_date.grid(row=0, column=0)
        self.add_word_button.grid(row=0, column=1)
        self.search_word_button.grid(row=0, column=2)
        self.button_select_date.grid(row=0, column=3)
        self.label_show_as.pack(anchor='w')
        self.radiobutton_as_abc.pack(anchor='w')
        self.radiobutton_as_time.pack(anchor='w')
        self.radiobutton_by_fixed_time.pack(anchor='w')
        self.treeview_words.pack()

        # На вкладке "Тесты"
        self.label_test_time.pack()
        self.radiobtn_all_time.pack()
        self.radiobtn_fixed_time.pack()

        self.radiobtn_test_lang1.pack()
        self.radiobtn_test_lang2.pack()

        self.btn_start_test.pack(anchor='e')

    # Обработчики нажатий кнопок
    def _button_select_date_click(self) -> None:
        SelectDateWindow(data_handler=self.data_handler,
                         parent_window=self,
                         logger=self._logger)

    def _add_word_button_click(self) -> None:
        AddWordWindow(data_handler=self.data_handler,
                      logger=self._logger)

    def _search_word_button_click(self) -> None:
        SearchWordWindow(data_handler=self.data_handler,
                         logger=self._logger)

    def _btn_start_test_click(self) -> None:
        tests_time = self.radiobtn_tests_time_var.get()
        tests_lang = self.radiobtn_tests_lang_var.get()

        # Здесь мы формируем словарь со словами, которые будем проверять
        # в зависимости от времени.
        match tests_time:
            case 'all':
                words: dict = self.data_handler.get_all_words()
                self._logger.debug(f'{words=}')
            case 'fixed':
                select_date_window = SelectDateWindow(
                    data_handler=self.data_handler,
                    parent_window=self,
                    logger=self._logger)
                select_date_window.wait_window()
                # Создаём локальную переменную, чтоб случайно не изменить глобальную.
                date = user_selected_date
                try:
                    words: dict = self.data_handler.get_words(
                        date)  # type: ignore
                except DateNotFoundError as e:
                    showerror("Дата не найдена", str(e))
                    self._logger.warning(e)
                    return

        match tests_lang:
            case 1:
                # Ничего не делаем, слова и так в правильном порядке.
                self._logger.debug("Не перевёрнутый словарь: %s", (words))
            case 2:
                # Переворачиваем словарь.
                words = {value: key for key, value in words.items()}
                self._logger.debug("Перевёрнутый словарь: %s", (words))

        TestWindow(data_handler=self.data_handler,
                   words=words,
                   logger=self._logger)


class AddWordWindow(tk.Tk):
    def __init__(self, *, data_handler: JSON, logger: logging.Logger):
        super().__init__()

        self._logger = logger
        self.data_handler = data_handler

        self.title('Добавление слова')

        self._define_widgets()
        self._pack_widgets()

    def _define_widgets(self):
        self.label_word = ttk.Label(self, text='Слово:')
        self.entry_word = ttk.Entry(self)
        self.label_translating = ttk.Label(self, text='Перевод:')
        self.entry_translating = ttk.Entry(self)
        self.button_add_a_word = ttk.Button(
            self, text='Добавить', command=self._add_word)

    def _pack_widgets(self):
        self.label_word.pack(anchor='w')
        self.entry_word.pack()
        self.label_translating.pack(anchor='w')
        self.entry_translating.pack()
        self.button_add_a_word.pack(anchor='e')

    def _add_word(self):
        today: Date = get_today()
        self._logger.debug(f'{today=}')
        try:
            self.data_handler.add_word(today, self.entry_word.get(),
                                       self.entry_translating.get())
        except WordIsEmptyError:
            showerror("Ошибка", "Введено пустое слово.")
            self._logger.warning("Пользователь ввёл пустое слово.")
        self._logger.debug(self.data_handler.get_all_words())


class SearchWordWindow(tk.Tk):
    def __init__(self, *, data_handler: JSON, logger: logging.Logger):
        super().__init__()
        self._logger = logger
        self.data_handler = data_handler
        self.languages = ("английское", "русское")

        self._define_widgets()
        self._pack_widgets()
        self.combobox_lang.current(0)

        self.title("Поиск слов.")

    def _define_widgets(self):
        self.label1 = ttk.Label(self, text="Найти")
        self.combobox_lang = ttk.Combobox(self, values=self.languages)
        self.label2 = ttk.Label(self, text="слово")
        self.entry_word = ttk.Entry(self)
        self.button_search = ttk.Button(
            self, text="Поиск", command=self._search)
        self.answer_label = ttk.Label(self, text="")

    def _pack_widgets(self):
        self.label1.grid(row=0, column=0)
        self.combobox_lang.grid(row=0, column=1)
        self.label2.grid(row=0, column=2)
        self.entry_word.grid(row=1, column=0, columnspan=2)
        self.button_search.grid(row=1, column=2)
        self.answer_label.grid(row=2, column=0, columnspan=3)

    def _search(self):
        # UNTESTED
        if self.combobox_lang.get() == self.languages[0]:
            is_eng = True
        elif self.combobox_lang.get() == self.languages[1]:
            is_eng = False
        else:
            # Мало ли, что пользователь введёт
            self._logger.warning("Получен неизвесный язык.")
            showerror("Ошибка", "Введён неизвесный язык.")
        try:
            answer = self.data_handler.search_word(
                self.entry_word.get(), is_eng)
        except WordIsEmptyError:
            showerror("Ошибка", "Введено пустое слово.")
            self._logger.warning("Пользователь ввёл пустое слово.")
            return
        except WordNotFoundError as e:
            showerror("Ошибка", str(e))
            return
        self.answer_label.configure(text=answer)


class SelectDateWindow(tk.Tk):
    def __init__(self, *, data_handler: JSON, parent_window: tk.Tk, logger: logging.Logger):
        super().__init__()
        self._logger = logger
        self.data_handler = data_handler
        self.parent_window = parent_window

        self.title('Выбор даты')

        self._define_widgets()
        self._pack_widgets()

    def _define_widgets(self):
        self.label_instruction = ttk.Label(
            self, text='Введите дату в формате "дд.мм.гггг"')
        self.entry_date = ttk.Entry(self)
        self.button_ok = ttk.Button(
            self, text='Выбрать', command=self._button_ok_click)
        self.button_select_todays_date = ttk.Button(
            self, text='Выбрать сегодняшнюю дату.', command=self._button_select_todays_date_click)

    def _pack_widgets(self):
        self.label_instruction.grid(row=0, column=0, columnspan=2)
        self.entry_date.grid(row=1, column=0, columnspan=2)
        self.button_select_todays_date.grid(row=2, column=0)
        self.button_ok.grid(row=2, column=1)

    def _button_ok_click(self):
        self._logger.info('Кнопка "Выбрать" (на окне с выбором даты) нажата.')
        user_date: str = self.entry_date.get()
        try:
            parsed_date: Date = Date.parse(user_date)
        except InvalidDateError:
            self._logger.warning(
                f'Пользователь ввёл неправильную дату, а именно - {user_date}')
            showerror("Неправильная дата",
                      """Введена неправильная дата!
Пожалуйста, введите дату в формате \"дд.мм.гггг\"
Например, 01.01.2025 или 08.11.2020""")
            return
        else:
            global user_selected_date
            user_selected_date = parsed_date

            # Создаём событие для обновления даты в надписи на окне.
            self.parent_window.event_generate('<<OnDateUpdate>>')

            # Чтоб пользователь сам не закрывал.
            self.destroy()

    def _button_select_todays_date_click(self):
        self._logger.info(
            'Кнопка "Выбрать сегодняшнюю дату." (на окне с выбором даты) нажата.')
        global user_selected_date
        user_selected_date = get_today()

        # Создаём событие для обновления даты в надписи на окне.
        self.parent_window.event_generate('<<OnDateUpdate>>')

        # Чтоб пользователь сам не закрывал.
        self.destroy()


class TestWindow(tk.Tk):
    def __init__(self, *, data_handler: JSON, words: dict, logger: logging.Logger):
        # Прокидываем обработчики и настройки.
        self._logger = logger
        self.data_handler = data_handler
        self.words = words

        # Счетчики кол-ва правильно и неправильно угаданных пользователем слов.
        self._correct_words_counter: int = 0
        self._incorrect_words_counter: int = 0

        super().__init__()

        self._define_internal_vars()
        self._define_widgets()
        self._pack_widgets()

        # Создаём новый генератор, чтобы была именно последовательность.
        self.get_next_random_dict_key = gen_random_dict_key(self.words)
        self.current_word = next(self.get_next_random_dict_key)
        # Выводим первое слово.
        self.label_word.configure(text=self.current_word)

        self.protocol('WM_DELETE_WINDOW', self._on_closing)

    def _define_internal_vars(self):
        self._user_translating = tk.StringVar()

    def _define_widgets(self):
        self.label_greeting = ttk.Label(master=self, text='Переведите слово:')
        self.label_word = ttk.Label(master=self, text='')

        self.entry_translating = ttk.Entry(
            master=self, textvariable=self._user_translating)
        self.button_check = ttk.Button(
            master=self, text='Проверить', command=self._button_check_click)

        self.label_result = ttk.Label(master=self, text='')
        self.label_true_translating = ttk.Label(master=self, text='')

        self.button_next = ttk.Button(
            master=self, text='Далее', command=self._button_next_click)

    def _pack_widgets(self):
        self.label_greeting.pack()
        self.label_word.pack()

        self.entry_translating.pack()
        self.button_check.pack(anchor='e')

        self.label_result.pack()
        self.label_true_translating.pack()

        self.button_next.pack(anchor='e')

    def _button_check_click(self):
        self._logger.info('Нажата кнопка "Проверить"')
        self._logger.debug(self.entry_translating.get())
        user_translating: str = self.entry_translating.get().strip().lower()

        current_translating = self.words[self.current_word]
        self._logger.debug(f'{current_translating=}')

        self._logger.debug(f'{user_translating=}')

        if user_translating == current_translating:
            self._correct_words_counter += 1
            self.label_result.configure(text="Правильно!", foreground='green')
        else:
            self._incorrect_words_counter += 1
            self.label_result.configure(
                text="Неправильно :(", foreground='red')

        self.label_true_translating.configure(
            text=f"Правильный перевод: {current_translating}")

    def _button_next_click(self):
        self._logger.info('Нажата кнопка "Далее".')

        # Сбрасываем надписи
        self.label_result.configure(text='')
        self.label_true_translating.configure(text='')

        # Сбрасываем поле ввода
        self.entry_translating.delete(0, last='end')

        try:
            # Берём случайное слово
            self.current_word = next(self.get_next_random_dict_key)
        except StopIteration:
            self.destroy()
            showinfo('Тест завершён', f"""Результаты:
{self._correct_words_counter} правильных слов, {self._incorrect_words_counter} неправильных слов.""")
            self._logger.info('Тесты завершены, окно с тестами закрыто.')
            return

        # Меняем надписи
        self.label_word.configure(text=self.current_word)

    def _on_closing(self, *args, **kwargs):
        self.destroy()
        showinfo('Тест завершён', f"""Результаты:
{self._correct_words_counter} правильных слов, {self._incorrect_words_counter} неправильных слов.""")
        self._logger.info('Окно с тестами закрыто пользователем.')
