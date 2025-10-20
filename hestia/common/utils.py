from .exceptions import InvalidArgumentsError
from .types import Identifier


def ensure_args(identifier: Identifier, args: list[str], expected_length: int):
    """
    Проверяет, соответствует ли количество аргументов ожидаемому.

    :param identifier: идентификатор вызванной функции
    :param args: переданные аргументы
    :param expected_length: ожидаемое (требуемое) количество аргументов
    :raises InvalidArgumentsError: если ожидаемое количество аргументов не соответствует действительности.
    """
    if len(args) != expected_length:
        raise InvalidArgumentsError(identifier, expected_length, len(args))
