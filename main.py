# TODO: Добавить поиск по словарю (что-то вроде гугл-переводчика).
# TODO: Разобраться с tkinter.Treeview наконец-то!
# TODO: Написать тесты, хотя бы для data.py
import logging
from handlers.gui import MainWindow
from handlers.data import JSON, WordsStore


def main() -> None:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    data_handler = JSON(path='data/words.json')
    words_store = WordsStore(data_handler=data_handler,
                             logger=logger)
    root_window = MainWindow(words_store=words_store,
                             logger=logger)
    root_window.mainloop()


if __name__ == '__main__':
    main()
