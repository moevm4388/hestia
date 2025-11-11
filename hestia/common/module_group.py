from functools import reduce
from typing import Any

from .exceptions import UnknownIdentifierError
from .types import Module, Identifier


class ModuleGroup(Module):
    """
    Композитный тип для модулей.
    """

    def __init__(self, *modules: Module) -> None:
        self.__modules = modules

    def call(self, identifier: Identifier, args: list[str]) -> Any:
        """
        Вызывает метод, если он реализуется хотя бы одним модулем из группы.

        Если несколько модулей реализуют метод, вызывается метод того модуля,
        который был указан первым в конструкторе.

        :param identifier: Идентификатор метода
        :param args: Аргументы метода
        :returns: Результат вызова метода
        :raises UnknownIdentifierError: если метод не реализован ни одним модулем
        """
        for module in self.__modules:
            if identifier in module.methods():
                return module.call(identifier, args)
        raise UnknownIdentifierError(identifier)

    def methods(self) -> set[Identifier]:
        """
        Возвращает множество всех методов, поддерживаемых всеми модулями из
        группы.
        """
        return reduce(lambda acc, cur: acc | cur.methods(), self.__modules, set())
