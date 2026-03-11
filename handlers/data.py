import json
import re
import logging
from collections import namedtuple
from random import sample
from datetime import datetime


Date = namedtuple('Date', ['day', 'month', 'year'])


class DateParsingError(Exception):
    pass


class FileReadingWritingError(Exception):
    pass


class WordIsEmptyError(FileReadingWritingError):
    pass


class InvalidDateError(DateParsingError):
    pass


class DateNotFoundError(DateParsingError):
    pass


class ParseDate:
    def __init__(self) -> None:
        self._REGEXPR_DATE = r"(\d{1,2})[\./-](\d{1,2})[\./-](\d{3,4})"

    def parse(self, date: str) -> Date:
        date = date.strip()
        found_date = re.search(self._REGEXPR_DATE, date)

        if found_date is None:
            raise InvalidDateError(f'Date "{date}" is invalid.')

        day = found_date.group(1)  # type: ignore
        month = found_date.group(2)  # type: ignore
        year = found_date.group(3)  # type: ignore

        result = self.format_date(Date(day, month, year))
        return result

    def format_date(self, old_date: Date) -> Date:
        # Забиваем нулями, чтоб довести до "дд.мм.гггг".
        new_day = old_date.day.zfill(2)
        new_month = old_date.month.zfill(2)
        new_year = old_date.year.zfill(4)
        return Date(new_day, new_month, new_year)

    def date_to_str(self, date: Date) -> str:
        return f'{date.day}.{date.month}.{date.year}'


class JSON:
    def __init__(self, path: str, date_parser: ParseDate, logger: logging.Logger) -> None:
        self._logger = logger
        self._path = path
        self._date_parser = date_parser

    def get_words(self, date: Date) -> dict[str, str]:
        json = self.__load_json()
        all_words = self.__raw_dict_to_dict_with_namedtuple(json)
        try:
            words = all_words[date]
        except KeyError:
            raise DateNotFoundError(
                f'Не найдено ни одного слова за дату "{self._date_parser.date_to_str(date)}".')

        return words

    def get_all_words(self) -> dict[str, str]:
        # NOTE: Кстати, при объединении словарей несколько одинаковых ключей превращаются в один.
        json: dict = self.__load_json()
        all_words = self.__raw_dict_to_dict_with_namedtuple(json)
        words = {}

        for date in all_words.keys():  # Делаем один общий словарь со всеми словами.
            words |= self.get_words(date)  # Объединяем словари.

        return words

    def add_word(self, date: Date, word: str, translating: str) -> None:
        word = word.strip().lower()
        translating = translating.strip().lower()
        if not word or not translating:
            self._logger.warning("Пользователь попытался добавить пустое слово.")
            raise WordIsEmptyError

        json = self.__load_json()
        words = self.__raw_dict_to_dict_with_namedtuple(json)
        try:
            words[date][word] = translating
        except KeyError:  # Если даты ещё нет,
            words[date] = {}  # то мы её добавляем.
            words[date][word] = translating

        # Пишем в json.
        self.__write_to_json(
            data=self.__dict_with_namedtuple_to_raw_dict(words))
        self._logger.info(f"В {self._path} добавлено новое слово.")

    def __load_json(self) -> dict[str, dict[str, str]]:
        with open(self._path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def __write_to_json(self, data: dict[str, dict[str, str]]) -> None:
        with open(self._path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=True)

    def __raw_dict_to_dict_with_namedtuple(self, raw_dict: dict[str, dict]) -> dict[Date, dict]:
        words: dict[Date, dict[str, str]] = {}
        for date, content in raw_dict.items():
            parsed_date = self._date_parser.parse(date)
            words[parsed_date] = content
        return words

    def __dict_with_namedtuple_to_raw_dict(self, dict_with_namedtuple: dict[Date, dict]) -> dict[str, dict]:
        words: dict[str, dict[str, str]] = {}
        for date, content in dict_with_namedtuple.items():
            str_date = self._date_parser.date_to_str(date)
            words[str_date] = content
        return words


def get_today(date_parser: ParseDate) -> Date:
    return date_parser.parse(datetime.now().strftime("%d.%m.%Y"))


def gen_random_dict_key(dictionary: dict):
    for rand_key in sample(list(dictionary), len(dictionary)):
        yield rand_key
