"""
Модуль рациональных чисел

Авторы:
- Арефьев Иван <arefev.ivan.2000@gmail.com>
- Денисенко Варвара <dvs2202@mail.ru>
- Шарапов Даниил <sharapowdanya@gmail.com>
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
        s = s.split("/")
        if (len(s)) != 2:
            raise ValueError("Невозможно создать рациональное число из поданной строки")

        numerator = Integer.from_str(s[0])
        denominator = NaturalNumber.from_str(s[1])

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

        """
        Ищем НОД знаменателя и делителя.
        Делим числитель и знаменатель на НОД.
        Возвращаем результат деления - сокращённую дробь.
        """

        gcd = self.natural_module.gcd(
            self.integer_module.absolute_value(q.numerator),
            q.denominator
        )

        """
        НОД = 1 -> сокращение не требуется (взаимно простые)
        """
        if self.natural_module.comparison(gcd, NaturalNumber(1)) == 0:
            return q

        numerator = self.integer_module.quotient(
            q.numerator,
            self.integer_module.natural_to_integer(gcd)
        )

        denominator = self.natural_module.division(
            q.denominator,
            gcd
        )

        return RationalNumber(numerator, denominator)

    def rational_to_integer_check(self, q: RationalNumber) -> bool:
        """
        Q-2. Проверка сокращенного дробного на целое
        Возвращает:
        True - если рациональное число является целым,
        False - иначе
        """

        q = self.reduce_fraction(q)

        return self.natural_module.comparison(
                    q.denominator,
                    NaturalNumber(1)
                    ) == 0

    def integer_to_rational(self, z: Integer) -> RationalNumber:
        """
        Q-3. Преобразование целого в дробное
        """

        """
        Примитивное преобразование:
        z (Integer) -> z/1 (RationalNumber)
        """

        return RationalNumber(z, NaturalNumber(1))

    def rational_to_integer(self, q: RationalNumber) -> Integer:
        """
        Q-4. Преобразование сокращенного дробного в целое (если знаменатель равен 1)
        """

        q = self.reduce_fraction(q)

        if self.natural_module.comparison(q.denominator, NaturalNumber(1)) == 0:
            return q.numerator
        raise ValueError("Дробное число не может быть представлено в виде целого!")

    def addition(self, q1: RationalNumber, q2: RationalNumber) -> RationalNumber:
        """
        Q-5. Сложение дробей
        """

        """
        Складываем числители с коэффициентами.
        Умножаем знаменатели.
        Возвращаем результат функции сокращения дроби.
        """

        """
        q1.n      q2.n
        ____   +  ____
        q1.d      q2.d
        
        left_num  = q1.n * to_int(q2.d)
        right_num = q2.n * to_int(q1.d)
        
        num = left_num + right_num
        den = q1.d * q2.d
        """
        left_numerator  = self.integer_module.multiplication(
            q1.numerator,
            self.integer_module.natural_to_integer(
                q2.denominator
            )
        )

        right_numerator = self.integer_module.multiplication(
            q2.numerator,
            self.integer_module.natural_to_integer(
                q1.denominator
            )
        )

        numerator = self.integer_module.addition(
            left_numerator,
            right_numerator
        )

        denominator = self.natural_module.multiplication(
            q1.denominator,
            q2.denominator
        )

        return self.reduce_fraction(RationalNumber(numerator, denominator))


    def subtraction(self, q1: RationalNumber, q2: RationalNumber) -> RationalNumber:
        """
        Q-6. Вычитание дробей
        """

        """
        Вычитаем числители с коэффициентами.
        Умножаем знаменатели.
        Возвращаем результат функции сокращения дроби.
        """

        """
        q1.n    q2.n
        ____  - ____
        q1.d    q2.d

        left_num  = q1.n * to_int(q2.d)
        right_num = q2.n * to_int(q1.d)

        num = left_num - right_num
        den = q1.d * q2.d
        """
        left_numerator = self.integer_module.multiplication(
            q1.numerator,
            self.integer_module.natural_to_integer(
                q2.denominator
            )
        )

        right_numerator = self.integer_module.multiplication(
            q2.numerator,
            self.integer_module.natural_to_integer(
                q1.denominator
            )
        )

        numerator = self.integer_module.subtraction(
            left_numerator,
            right_numerator
        )

        denominator = self.natural_module.multiplication(
            q1.denominator,
            q2.denominator
        )

        return self.reduce_fraction(RationalNumber(numerator, denominator))

    def multiplication(self, q1: RationalNumber, q2: RationalNumber) -> RationalNumber:
        """
        Q-7. Умножение дробей
        """

        """
        Попарно умножаем числители и знаменатели.
        Возвращаем результат функции сокращения дроби.
        """

        numerator = self.integer_module.multiplication(
                        q1.numerator, q2.numerator
                    )

        denominator = self.natural_module.multiplication(
                        q1.denominator, q2.denominator
                    )

        return self.reduce_fraction(RationalNumber(numerator, denominator))

    def division(self, q1: RationalNumber, q2: RationalNumber) -> RationalNumber:
        """
        Q-8. Деление дробей (делитель отличен от нуля)
        """

        """
        Проверка q2 на ноль.
        """

        natural_numerator = self.natural_module.integer_to_natural(
            q2.numerator
        ) #NaturalNumber

        if self.natural_module.is_zero(natural_numerator):
            raise ZeroDivisionError("Деление на ноль недопустимо!")

        """
        Деление рациональных дробей - умножение на обратную.
        Умножаем числитель q1 на знаменатель q2.
        Умножаем знаменатель q1 на числитель q2.
        Возвращаем результат функции сокращение дроби.
        """

        numerator = self.integer_module.multiplication(
            q1.numerator,
            self.integer_module.natural_to_integer(q2.denominator)
        )

        """
        q2.n - целое число -> может дать отрицательность -> проверяем знак
        """

        sign = -1 if self.integer_module.sign_determination(q2.numerator) == 1 else 1
        numerator = self.integer_module.multiplication(numerator, Integer(sign))

        denominator = self.natural_module.multiplication(
            q1.denominator,
            self.integer_module.integer_to_natural(q2.numerator)
        )

        return self.reduce_fraction(RationalNumber(numerator, denominator))

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
