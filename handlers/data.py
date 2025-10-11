import json
import re


class JSON:
    def __init__(self, path: str) -> None:
        self._path = path

    def get_word(self, date: str) -> dict[str, str]:
        ...

    def add_word(self, date: str, word: str) -> None:
        ...

    def __load_json(self) -> dict[str, dict[str, str]]:
        ...

    def __add_date(self, date: str) -> None:
        ...

    def __is_date_exists(self, date: str) -> bool:
        ...


class ParseDate:
    def __init__(self) -> None:
        self._REGEXPR_DATE = ...

    # TODO: Тут бы возвращать namedtuple
    def parse(self, date: str) -> tuple[int, int, int]:
        ...
