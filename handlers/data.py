import json
import re
import logging
from collections import namedtuple
from random import sample


logging.basicConfig(level=logging.DEBUG)
Date = namedtuple('Date', ['day', 'month', 'year'])


def gen_random_dict_key(dictionary: dict):
    for rand_key in sample(list(dictionary), len(dictionary)):
        yield rand_key


class InvalidDateError(Exception):
    pass


class DateNotFoundError(Exception):
    pass


class JSON:
    def __init__(self, path: str) -> None:
        self._path = path

    def get_words(self, date: str) -> dict[str, str]:  # TODO: date: Date
        """FIXME:
        Тут может быть такой баг:
        В нашем json`чике есть неформатированная дата.
        Пользователь вводит как раз-таки эту дату, мы её форматируем,
        обращаемся к json`у по ключу, НО оп - такого ключа нет!
        Я к чему - надо сделать метод, который форматировал бы даты в json`е.
        Или (а может быть, обязательно) переписать этот метод.
        """
        json = self.__load_json()
        try:
            words = json[date]
        except KeyError:
            raise DateNotFoundError(
                f'Не найдено ни одного слова за дату "{date}".')

        return words

    def get_all_words(self) -> dict[str, str]:
        # NOTE: Кстати, при объединении словарей несколько одинаковых ключей превращаются в один.
        json: dict = self.__load_json()
        words = {}

        for date in json.keys():  # Делаем один общий словарь со всеми словами.
            words |= self.get_words(date)  # Объединяем словари.

        return words

    def add_word(self, date: str, word: str, translating: str) -> None:
        word = word.strip()
        translating = translating.strip()
        json = self.__load_json()
        try:
            json[date][word] = translating
        except KeyError:  # Если даты ещё нет,
            json[date] = {}  # то мы её добавляем.
            json[date][word] = translating

        # Пишем в json.
        self.__write_to_json(data=json)
        logging.info(f"В {self._path} добавлено новое слово.")

    def __load_json(self) -> dict[str, dict[str, str]]:
        with open(self._path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def __write_to_json(self, data: dict[str, dict[str, str]]) -> None:
        with open(self._path, 'w', encoding='utf-8') as file:
            json.dump(data, file)

    def test(self):  # DEBUG
        return self.get_all_words()


class ParseDate:
    def __init__(self) -> None:
        self._REGEXPR_DATE = r"(\d{1,2})[\./-](\d{1,2})[\./-](\d{3,4})"

    def parse(self, date: str) -> Date:
        date = date.strip()
        found_date = re.search(self._REGEXPR_DATE, date)

        try:
            day = found_date.group(1)  # type: ignore
            month = found_date.group(2)  # type: ignore
            year = found_date.group(3)  # type: ignore
        # Если found_date - None, то found_date.group() вызовет ошибку AttributeError.
        except AttributeError:
            raise InvalidDateError(f'Date "{date}" is invalid.')

        result = self.format_date(Date(day, month, year))
        return result

    def format_date(self, old_date: Date) -> Date:  # UNTESTED
        # Забиваем нулями, чтоб довести до "дд.мм.гггг".
        new_day = old_date.day.zfill(2)
        new_month = old_date.month.zfill(2)
        new_year = old_date.year.zfill(4)
        return Date(new_day, new_month, new_year)

    def date_to_str(self, date: Date) -> str:  # UNTESTED
        formatted_date = self.format_date(date)
        return f'{formatted_date.day}.{formatted_date.month}.{formatted_date.year}'


if __name__ == "__main__":
    # Здесь путь считаем от data.py. В main'е будем считать от main.py.
    # json_handler = JSON(path='../data/test_words.json')
    # print(json_handler.test())

    date_parser = ParseDate()
    dates = ('01.01.2025', '12.05.2025', '02.11.2025',
             '2.11.2025', '12.5.2025', '1.1.205',
             '07.11.2025', '07-11-2025', '07/11/2025')
    for date in dates:
        print(date_parser.parse(date))
