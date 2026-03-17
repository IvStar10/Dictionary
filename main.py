# TODO: Добавить поиск по словарю (что-то вроде гугл-переводчика).
# TODO: Разобраться с tkinter.Treeview наконец-то!
import logging
from handlers.gui import MainWindow
from handlers.data import JSON


def main() -> None:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    data_handler = JSON(path='data/words.json',
                        logger=logger)
    root_window = MainWindow(data_handler=data_handler,
                             logger=logger)
    root_window.mainloop()


if __name__ == '__main__':
    main()
