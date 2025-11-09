"""
Модуль рациональных чисел

Авторы:
- Арефьев Иван <arefev.ivan.2000@gmail.com>
...
"""

from common.exceptions import UnknownIdentifierError
from common.types import Identifier, Module
from common.utils import ensure_args
from typing import Any
from natural import NaturalNumber, NaturalModule
from integer import Integer, IntegerModule

class RationalNumber:
    def __init__(self, numerator: Integer, denominator: NaturalNumber):
        """
        Инициализация рационального числа
        numerator: числитель, целое число
        denominator: знаменатель, натуральное число
        """
        if denominator <= 0:
            raise ValueError("Знаменатель не может быть меньше либо равен 0")

        self.numerator = numerator
        self.denominator = denominator

    def __str__(self) -> str:
        """
        Строковое представление рационального числа
        """
        if self.numerator == 0:
            return str(self.numerator)
        return str(self.numerator) + "/" + str(self.denominator)

    @classmethod
    def from_str(cls, s: str) -> "RationalNumber":
        """
        Создание рационального числа из строки
        """
        if not s:
            raise ValueError("Пустая строка")

        s = s.split("/")
        numerator = int(s[0])
        denominator = int(s[1])

        return cls(numerator, denominator)

class RationalModule(Module):
    def __init__(self, natural_module: NaturalModule, integer_module: IntegerModule):
        """
        Инициализация модуля рациональных чисел.
        natural_module: модуль натуральных чисел для использования его функций
        integer_module: модуль целых чисел для использования его функций
        """
        self.natural_module = natural_module
        self.integer_module = integer_module

    def reduce_fraction(self, q: RationalNumber) -> RationalNumber:
        """
        Q-1. Сокращение дроби, результат - рациональное
        """
        ...

    def rational_to_integer_check(self, q: RationalNumber) -> bool:
        """
        Q-2. Проверка сокращенного дробного на целое
        Возвращает:
        True - если рац. число является целым,
        False - иначе
        """
        ...

    def integer_to_rational(self, z: Integer) -> RationalNumber:
        """
        Q-3. Преобразование целого в дробное
        """
        ...

    def rational_to_integer(self, q: RationalNumber) -> Integer:
        """
        Q-4. Преобразование сокращенного дробного в целое (если знаменатель равен 1)
        """
        ...

    def addition(self, q1: RationalNumber, q2: RationalNumber) -> RationalNumber:
        """
        Q-5. Сложение дробей
        """
        ...

    def subtraction(self, q1: RationalNumber, q2: RationalNumber) -> RationalNumber:
        """
        Q-6. Вычитание дробей
        """
        ...

    def multiplication(self, q1: RationalNumber, q2: RationalNumber) -> RationalNumber:
        """
        Q-7. Умножение дробей
        """
        ...

    def division(self, q1: RationalNumber, q2: RationalNumber) -> RationalNumber:
        """
        Q-8. Деление дробей (делитель отличен от нуля)
        """
        ...

    def call(self, identifier: Identifier, args: list[str]) -> Any:
        """
        Вызывает метод модуля по идентификатору.
        identifier - идентификатор вызываемого метода
        args - аргументы метода в виде строк
        """
        match identifier:
            case Identifier.RED_Q_Q:
                ensure_args(identifier, args, 1)
                q = RationalNumber.from_str(args[0])
                return self.reduce_fraction(q)

            case Identifier.INT_Q_B:
                ensure_args(identifier, args, 1)
                q = RationalNumber.from_str(args[0])
                return self.rational_to_integer_check(q)

            case Identifier.TRANS_Z_Q:
                ensure_args(identifier, args, 1)
                z = Integer.from_str(args[0])
                return self.integer_to_rational(z)

            case Identifier.TRANS_Q_Z:
                ensure_args(identifier, args, 1)
                q = RationalNumber.from_str(args[0])
                return self.rational_to_integer(q)

            case Identifier.ADD_QQ_Q:
                ensure_args(identifier, args, 2)
                q1 = RationalNumber.from_str(args[0])
                q2 = RationalNumber.from_str(args[1])
                return self.addition(q1, q2)

            case Identifier.SUB_QQ_Q:
                ensure_args(identifier, args, 2)
                q1 = RationalNumber.from_str(args[0])
                q2 = RationalNumber.from_str(args[1])
                return self.subtraction(q1, q2)

            case Identifier.MUL_QQ_Q:
                ensure_args(identifier, args, 2)
                q1 = RationalNumber.from_str(args[0])
                q2 = RationalNumber.from_str(args[1])
                return self.multiplication(q1, q2)

            case Identifier.DIV_QQ_Q:
                ensure_args(identifier, args, 2)
                q1 = RationalNumber.from_str(args[0])
                q2 = RationalNumber.from_str(args[1])
                return self.division(q1, q2)

            case _:
                raise UnknownIdentifierError(identifier)


    def methods(self) -> set[Identifier]:
        """
        Возвращает множество идентификаторов методов, поддерживаемых модулем.
        """
        return {
            Identifier.RED_Q_Q,
            Identifier.INT_Q_B,
            Identifier.TRANS_Z_Q,
            Identifier.TRANS_Q_Z,
            Identifier.ADD_QQ_Q,
            Identifier.SUB_QQ_Q,
            Identifier.MUL_QQ_Q,
            Identifier.DIV_QQ_Q
        }
