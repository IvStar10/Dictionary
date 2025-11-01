from handlers.gui import MainWindow
from handlers.data import JSON


def main() -> None:
    data_handler: JSON = JSON(path='data/test_words.json')
    root_window = MainWindow(data_handler=data_handler)
    root_window.mainloop()


if __name__ == '__main__':
    main()
