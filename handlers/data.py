import json
import re
import logging
from typing import NamedTuple
from random import sample
from datetime import datetime

from . import exceptions


class Date(NamedTuple):
    day: str
    month: str
    year: str

    def __str__(self) -> str:
        return f'{self.day}.{self.month}.{self.year}'

    @staticmethod
    def parse(date: str) -> 'Date':
        _REGEXPR_DATE = r"(\d{1,2})[\./-](\d{1,2})[\./-](\d{3,4})"
        date = date.strip()
        found_date = re.search(_REGEXPR_DATE, date)

        if found_date is None:
            raise exceptions.InvalidDateError(f'Date "{date}" is invalid.')

        day = found_date.group(1)  # type: ignore
        month = found_date.group(2)  # type: ignore
        year = found_date.group(3)  # type: ignore

        result = Date._format(Date(day, month, year))
        return result

    @staticmethod
    def _format(old_date: 'Date') -> 'Date':
        # Забиваем нулями, чтоб довести до "дд.мм.гггг".
        new_day = old_date.day.zfill(2)
        new_month = old_date.month.zfill(2)
        new_year = old_date.year.zfill(4)
        return Date(new_day, new_month, new_year)


class JSON:
    def __init__(self, path) -> None:
        self._path = path

    def load_json(self) -> dict[str, dict[str, str]]:
        with open(self._path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def write_to_json(self, data: dict[str, dict[str, str]]) -> None:
        with open(self._path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=True)

    @staticmethod
    def raw_dict_to_dict_with_namedtuple(raw_dict: dict[str, dict]) -> dict[Date, dict]:
        words: dict[Date, dict[str, str]] = {}
        for date, content in raw_dict.items():
            parsed_date = Date.parse(date)
            words[parsed_date] = content
        return words

    @staticmethod
    def dict_with_namedtuple_to_raw_dict(dict_with_namedtuple: dict[Date, dict]) -> dict[str, dict]:
        words: dict[str, dict[str, str]] = {}
        for date, content in dict_with_namedtuple.items():
            str_date = str(date)
            words[str_date] = content
        return words

    # FIXME: Сделать отдельной ф-цией, т.к. это не имеет отношения к классу.
    @staticmethod
    def gen_random_dict_key(dictionary: dict):
        for rand_key in sample(list(dictionary), len(dictionary)):
            yield rand_key


class WordsStore:
    # UNTESTED
    def __init__(self, data_handler: JSON, logger: logging.Logger) -> None:
        self._data_handler = data_handler
        self._logger = logger

    def get_words(self, date: Date) -> dict[str, str]:
        raw_json = self._data_handler.load_json()
        all_words = self._data_handler.raw_dict_to_dict_with_namedtuple(
            raw_json)
        try:
            words = all_words[date]
        except KeyError:
            raise exceptions.DateNotFoundError(
                f'Не найдено ни одного слова за дату "{str(date)}".')

        return words

    def get_all_words(self) -> dict[str, str]:
        # NOTE: Кстати, при объединении словарей несколько одинаковых ключей превращаются в один.
        raw_json: dict = self._data_handler.load_json()
        words = {}

        for date in raw_json.keys():  # Делаем один общий словарь со всеми словами.
            words |= raw_json[date]  # Объединяем словари.

        return words

    def add_word(self, date: Date, word: str, translating: str) -> None:
        word = word.strip().lower()
        translating = translating.strip().lower()
        if not word or not translating:
            self._logger.warning(
                "Пользователь попытался добавить пустое слово.")
            raise exceptions.WordIsEmptyError

        json = self._data_handler.load_json()
        words = self._data_handler.raw_dict_to_dict_with_namedtuple(json)
        try:
            words[date][word] = translating
        except KeyError:  # Если даты ещё нет,
            words[date] = {}  # то мы её добавляем.
            words[date][word] = translating

        # Пишем в json.
        self._data_handler.write_to_json(
            data=self._data_handler.dict_with_namedtuple_to_raw_dict(words))
        self._logger.info("Добавлено новое слово.")

    def search_word(self, word: str, is_search_in_main_lang: bool) -> str:
        # UNTESTED
        word = word.strip().lower()
        words = self.get_all_words()
        if not is_search_in_main_lang:
            words = {value: key for key, value in words.items()}
        if not word:
            self._logger.warning(
                "Пользователь попытался найти пустое слово.")
            raise exceptions.WordIsEmptyError
        try:
            return words[word]
        except KeyError:
            self._logger.warning(f"Слово {word} не найдено.")
            raise exceptions.WordNotFoundError(f"Слово {word} не найдено.")


def get_today() -> Date:
    return Date.parse(datetime.now().strftime("%d.%m.%Y"))
