import json
import re


class JSON:
    def __init__(self, path: str) -> None:
        self._path = path

    def get_words(self, date: str) -> dict[str, str]:
        json = self.__load_json()
        words = json[date]
        return words

    def add_word(self, date: str, word: str, translating: str) -> None:
        json = self.__load_json()
        try:
            json[date][word] = translating
        except KeyError:  # Если даты ещё нет,
            json[date] = {}  # то мы её добавляем.
            json[date][word] = translating

        # Пишем в json.
        self.__write_to_json(data=json)

    def __load_json(self) -> dict[str, dict[str, str]]:
        with open(self._path, 'r') as file:
            return json.load(file)

    def __write_to_json(self, data: dict[str, dict[str, str]]) -> None:
        with open(self._path, 'w') as file:
            json.dump(data, file)

    def test(self):
        self.add_word('2.10.2025', 'another word', 'translating')
        return self.get_words('2.10.2025')


class ParseDate:
    def __init__(self) -> None:
        self._REGEXPR_DATE = ...

    # TODO: Тут бы возвращать namedtuple
    def parse(self, date: str) -> tuple[int, int, int]:
        ...


if __name__ == "__main__":
    json_handler = JSON(path='../data/test_words.json')  # Здесь путь считаем от data.py. В main'е будем считать от main.py.
    print(json_handler.test())

