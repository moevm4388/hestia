from .types import Identifier


class InvalidArgumentsError(Exception):
    """
    Вызывается, если метод `.call` модуля был вызван с неверным количеством
    аргументов.
    """

    def __init__(self, identifier: Identifier, expected: int, actual: int) -> None:
        super().__init__(
            f"{identifier.name}: expected {expected} parameter(s), got {actual}"
        )
        self.expected = expected
        self.actual = actual


class UnknownIdentifierError(Exception):
    """
    Вызывается, если метод `.call` модуля был вызван с неизвестным
    идентификатором.
    """

    def __init__(self, identifier: Identifier) -> None:
        super().__init__(f"unknown identifier: {identifier.name}")
        self.identifier = identifier
