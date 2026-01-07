# TODO: Добавить поиск по словарю (что-то вроде гугл-переводчика).
# TODO: На окно с тестами добавить отображение правильно/неправильно введённых слов на закрытие окна.
# TODO: Разобраться с tkinter.Treeview наконец-то!
from handlers.gui import MainWindow
from handlers.data import JSON, ParseDate


def main() -> None:
    date_parser = ParseDate()
    data_handler = JSON(path='data/words.json', date_parser=date_parser)
    root_window = MainWindow(data_handler=data_handler,
                             date_parser=date_parser)
    root_window.mainloop()


if __name__ == '__main__':
    main()
