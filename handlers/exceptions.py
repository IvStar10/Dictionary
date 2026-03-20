class DateParsingError(Exception):
    pass


class FileReadingWritingError(Exception):
    pass


class WordIsEmptyError(FileReadingWritingError):
    pass


class WordNotFoundError(FileReadingWritingError):
    pass


class InvalidDateError(DateParsingError):
    pass


class DateNotFoundError(DateParsingError):
    pass
