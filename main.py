from handlers.gui import MainWindow
from handlers.data import JSON, ParseDate


def main() -> None:
    data_handler = JSON(path='data/test_words.json')
    date_parser = ParseDate()
    root_window = MainWindow(data_handler=data_handler, date_parser=date_parser)
    root_window.mainloop()


if __name__ == '__main__':
    main()
